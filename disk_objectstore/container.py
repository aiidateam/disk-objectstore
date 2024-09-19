"""
The main implementation of the ``Container`` class of the object store.
"""

from __future__ import annotations

# pylint: disable=too-many-lines
import dataclasses
import io
import json
import os
import shutil
import uuid
from collections import defaultdict, namedtuple
from contextlib import contextmanager
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, overload

from sqlalchemy.orm.session import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import delete, select, text, update

from .database import Obj, get_session
from .dataclasses import ObjectCount, ObjectMeta, TotalSize, ValidationIssues
from .exceptions import InconsistentContent, NotExistent, NotInitialised
from .utils import (
    CallbackStreamWrapper,
    CompressMode,
    LazyLooseStream,
    LazyOpener,
    Location,
    ObjectWriter,
    PackedObjectReader,
    StreamReadBytesType,
    StreamSeekBytesType,
    StreamWriteBytesType,
    ZlibStreamDecompresser,
    chunk_iterator,
    compute_hash_and_size,
    detect_where_sorted,
    get_compressobj_instance,
    get_hash_cls,
    get_stream_decompresser,
    is_known_hash,
    merge_sorted,
    nullcontext,
    rename_callback,
    safe_flush_to_disk,
    should_compress,
    yield_first_element,
)

if TYPE_CHECKING:
    from typing import (
        Any,
        Callable,
        Dict,
        Iterator,
        List,
        Literal,
        Optional,
        Sequence,
        Set,
        Tuple,
        Type,
        Union,
    )

    from mypy_extensions import Arg

ObjQueryResults = namedtuple(
    "ObjQueryResults", ["hashkey", "offset", "length", "compressed", "size"]
)


class ObjectType(Enum):
    """Enum that describes the various types of an objec (as returned in ``meta['type']``)."""

    LOOSE = "loose"
    PACKED = "packed"
    MISSING = "missing"


class Container:  # pylint: disable=too-many-public-methods
    """A class representing a container of objects (which is stored on a disk folder)"""

    _PACK_INDEX_SUFFIX = ".idx"
    # Size in bytes of each of the chunks used when (internally) reading or writing in chunks, e.g.
    # when packing.
    _CHUNKSIZE = 65536

    # The pack ID that is used for repacking as a temporary location.
    # NOTE: It MUST be an integer and it MUST be < 0 to avoid collisions with 'actual' packs
    _REPACK_PACK_ID = -1

    # When performing an `in_` query in SQLite, this is converted to something like
    # 'SELECT * FROM db_object WHERE db_object.hashkey IN (?, ?)' with parameters = ('hash1', 'hash2')
    # Now, the maximum number of parameters is limited in SQLite, see variable SQLITE_MAX_VARIABLE_NUMBER
    # as described in https://www.sqlite.org/limits.html
    # Now, until recently (at the moment of writing) this defaults to 999 for SQLite versions
    # prior to 3.32.0 (2020-05-22) or 32766 for SQLite versions after 3.32.0.
    # So we need to assume that we cannot put more than 999 elements in the `.in_` parameter.
    # Note that on some OSs, the value is increased at compile time. E.g. on my Mac OS X with python 3.6
    # compiled with HomeBrew, the limit (I tested it) is 250000.
    # See also e.g. this comment https://bugzilla.redhat.com/show_bug.cgi?id=1798134
    _IN_SQL_MAX_LENGTH = 950

    # If the length of required elements is larger than this, instead of iterating an IN statement over chunks of size
    # _IN_SQL_MAX_LENGTH, it just quickly lists all elements (ordered by hashkey, requires a VACUUMed DB for
    # performance) and returns only the intersection.
    # This length might need some benchmarking, but seems OK on very large DBs of 6M nodes
    # (after VACUUMing, as mentioned above).
    _MAX_CHUNK_ITERATE_LENGTH = 9500

    def __init__(self, folder: str | Path) -> None:
        """Create the class that represents the container.

        :param folder: the path to a folder that will host this object-store container.
        """
        self._folder = Path(folder).resolve()
        # Will be populated by the _get_session function
        self._session: Session | None = None

        # These act as caches and will be populated by the corresponding properties
        # IMPORANT! IF YOU ADD MORE, REMEMBER TO CLEAR THEM IN `init_container()`!
        self._current_pack_id: int | None = None
        self._config: dict | None = None

    def get_folder(self) -> Path:
        """Return the path to the folder that will host the object-store container."""
        return self._folder

    def close(self) -> None:
        """Close open files (in particular, the connection to the SQLite DB)."""
        if self._session is not None:
            self._session.close()
            self._session = None

    def __enter__(self) -> Container:
        """Return a context manager that will close the session when exiting the context."""
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        """Close the session when exiting the context."""
        self.close()

    def _get_sandbox_folder(self) -> Path:
        """Return the path to the sandbox folder that is used during a new object creation.

        It is a subfolder of the container folder.
        """
        return self._folder / "sandbox"

    def _get_loose_folder(self) -> Path:
        """Return the path to the folder that will host the loose objects.

        It is a subfolder of the container folder.
        """
        return self._folder / "loose"

    def _get_pack_folder(self) -> Path:
        """Return the path to the folder that will host the packed objects.

        It is a subfolder of the container folder.
        """
        return self._folder / "packs"

    def _get_duplicates_folder(self) -> Path:
        """Return the path to the folder that will host the duplicate loose objects that couldn't be written.

        This should happen only in race conditions on Windows. See `utils.ObjectWriter.__exit__` for its usage, and
        `utils._store_duplicate_copy`.

        It is a subfolder of the container folder.
        """
        return self._folder / "duplicates"

    def _get_config_file(self) -> Path:
        """Return the path to the container config file."""
        return self._folder / "config.json"

    @overload
    def _get_session(
        self, create: bool = False, raise_if_missing: Literal[True] = True
    ) -> Session:
        ...

    @overload
    def _get_session(
        self, create: bool = False, raise_if_missing: Literal[False] = False
    ) -> Session | None:
        ...

    def _get_session(
        self, create: bool = False, raise_if_missing: bool = False
    ) -> Session | None:
        """Return a new session to connect to the pack-index SQLite DB.

        :param create: if True, creates the sqlite file and schema.
        :param raise_if_missing: ignored if create==True. If create==False, and the index file
           is missing, either raise an exception (FileNotFoundError) if this flag is True, or return None
        """
        return get_session(
            self._get_pack_index_path(),
            create=create,
            raise_if_missing=raise_if_missing,
        )

    def _get_cached_session(self) -> Session:
        """Return the SQLAlchemy session to access the SQLite file,
        reusing the same one."""
        # We want to catch both if it's missing, and if it's None
        # the latter means that in the previous run the pack file was missing
        # but maybe by now it has been created!
        if self._session is None:
            self._session = self._get_session(create=False, raise_if_missing=True)
        return self._session

    def _get_loose_path_from_hashkey(self, hashkey: str) -> Path:
        """Return the path of a loose object on disk containing the data of a given hash key.

        :param hashkey: the hashkey of the object to get.
        """
        if self.loose_prefix_len:
            return (
                self._get_loose_folder()
                / hashkey[: self.loose_prefix_len]
                / hashkey[self.loose_prefix_len :]
            )
        # if loose_prefix_len is zero, there is no subfolder
        return self._get_loose_folder() / hashkey

    def _get_pack_path_from_pack_id(
        self, pack_id: str | int, allow_repack_pack: bool = False
    ) -> Path:
        """Return the path of the pack file on disk for the given pack ID.

        :param pack_id: the pack ID.
        :param pack_id: Whether to allow the repack pack id
        """
        pack_id = str(pack_id)
        assert self._is_valid_pack_id(
            pack_id, allow_repack_pack=allow_repack_pack
        ), f"Invalid pack ID {pack_id}"
        return self._get_pack_folder() / pack_id

    def _get_pack_index_path(self) -> Path:
        """Return the path to the SQLite file containing the index of packed objects."""
        return self._folder / f"packs{self._PACK_INDEX_SUFFIX}"

    def _get_pack_id_to_write_to(self) -> int:
        """Return the pack ID to write the next object.

        This function checks that there is a pack file with the current pack ID.
        If it does not exist, that it returns that ID (the file is new and must be created).
        If it exists, it returns the ID only if the size is smaller than the container's pack_size_target,
        otherwise it increases by one until it finds a valid "non-full" pack ID.

        :return: an integer pack ID.
        """
        # Default to zero if not set (e.g. if it's None)
        pack_id = self._current_pack_id or 0
        while True:
            pack_path = self._get_pack_path_from_pack_id(pack_id)
            if not pack_path.exists():
                # Use this ID - the pack file does not exist yet
                break
            if pack_path.stat().st_size < self.pack_size_target:
                # Use this ID - the pack file is not "full" yet
                break
            # Try the next pack
            pack_id += 1

        # Cache the value
        self._current_pack_id = pack_id
        return pack_id

    @property
    def is_initialised(self) -> bool:
        """Return True if the container is already initialised."""
        # If the config file does not exist, the container is not initialised
        try:
            with open(self._get_config_file(), encoding="utf8") as fhandle:
                json.load(fhandle)
        except (ValueError, OSError):
            return False
        # I also check that the four sub-folders exist
        subfolders = [
            self._get_pack_folder(),
            self._get_loose_folder(),
            self._get_duplicates_folder(),
            self._get_sandbox_folder(),
        ]
        for folder in subfolders:
            if not folder.exists():
                return False
        return True

    def init_container(
        self,
        clear: bool = False,
        pack_size_target: int = 4 * 1024 * 1024 * 1024,
        loose_prefix_len: int = 2,
        hash_type: str = "sha256",
        compression_algorithm: str = "zlib+1",
    ) -> None:
        """Initialise the container folder, if not already done.

        If this is called multiple times, it does not corrupt the data,
        unless you add the ``clear=True`` option.

        :param clear: if True, delete everything in the container and
          initialise a new, empty one.
        :param pack_size_target: The minimum size (in bytes) of a pack file before
          a new pack file is created. Pack files will be typically larger than this.
        :param loose_prefix_len: The length of the prefix of the loose objects.
          The longer the length, the more folders will be used to store loose
          objects. Suggested values: 0 (for not using subfolders) or 2.
        :param hash_type: a string defining the hash type to use.
        :param compression_algorithm: a string defining the compression algorithm to use for compressed objects.
        """
        if loose_prefix_len < 0:
            raise ValueError(
                "The loose prefix length can only be zero or a positive integer"
            )
        if pack_size_target <= 0:
            raise ValueError(
                "The pack size target can only be a non-zero positive integer"
            )
        if not is_known_hash(hash_type):
            raise ValueError(f'Unknown hash type "{hash_type}"')

        if clear:
            if self._folder.exists():
                shutil.rmtree(self._folder)

            # Reinitialize the configuration cache, since this will change
            # (at least the container_id, possibly the rest), and the other caches
            self._config = None
            self._current_pack_id = None

        if self.is_initialised:
            raise FileExistsError(
                "The container already exists, so you cannot initialise it - "
                "use the clear option if you want to overwrite with a clean one"
            )

        # If we are here, either the folder is empty, or just cleared.
        # It could also be that one of the folders does not exist. This is considered an invalid situation.
        # But this will be catched later, where I check that the folder is empty before overwriting the
        # configuration file.
        # In this case, I have to generate a new UUID to be used as the container_id
        container_id = uuid.uuid4().hex

        try:
            os.makedirs(self._folder)
        except FileExistsError:
            # The directory already exists: it's ok
            pass

        if os.listdir(self._folder):
            raise FileExistsError(
                "There is already some file or folder in the Container folder, I cannot initialise it!"
            )

        # validate the compression algorithm: check if I'm able to load the classes to compress and decompress
        # with the given specified string
        get_compressobj_instance(compression_algorithm)
        get_stream_decompresser(compression_algorithm)

        # Create config file
        with open(self._get_config_file(), "w", encoding="utf8") as fhandle:
            json.dump(
                {
                    "container_version": 1,  # For future compatibility, this is the version of the format
                    "loose_prefix_len": loose_prefix_len,
                    "pack_size_target": pack_size_target,
                    "hash_type": hash_type,
                    "container_id": container_id,
                    "compression_algorithm": compression_algorithm,
                },
                fhandle,
            )

        for folder in [
            self._get_pack_folder(),
            self._get_loose_folder(),
            self._get_duplicates_folder(),
            self._get_sandbox_folder(),
        ]:
            os.makedirs(folder)

        self._get_session(create=True)

    def _get_repository_config(self) -> dict[str, int | str]:
        """Return the repository config."""
        if self._config is None:
            if not self.is_initialised:
                raise NotInitialised(
                    "The container is not initialised yet - use .init_container() first"
                )
            with open(self._get_config_file(), encoding="utf8") as fhandle:
                self._config = json.load(fhandle)
        return self._config

    @property
    def loose_prefix_len(self) -> int:
        """Return the length of the prefix of loose objects, when sharding.

        This is read from the (cached) repository configuration.
        """
        return self._get_repository_config()["loose_prefix_len"]  # type: ignore[return-value]

    @property
    def pack_size_target(self) -> int:
        """Return the length of the pack name, when sharding.

        This is read from the (cached) repository configuration.
        """
        return self._get_repository_config()["pack_size_target"]  # type: ignore[return-value]

    @property
    def hash_type(self) -> str:
        """Return the length of the prefix of loose objects, when sharding.

        This is read from the (cached) repository configuration.
        """
        return self._get_repository_config()["hash_type"]  # type: ignore[return-value]

    @property
    def container_id(self) -> str:
        """Return the repository unique ID.

        This is read from the (cached) repository configuration, and is a UUID uniquely identifying
        this specific container. This is generated at the container initialization (call `init_container`) and will
        never change for this container.

        Clones of the container should have a different ID even if they have the same content.
        """
        return self._get_repository_config()["container_id"]  # type: ignore[return-value]

    @property
    def compression_algorithm(self) -> str:
        """Return the compression algorithm defined for this container.

        This is read from the repository configuration."""
        return self._get_repository_config()["compression_algorithm"]  # type: ignore[return-value]

    def _get_compressobj_instance(self):
        """Return the correct `compressobj` class for the compression algorithm defined for this container."""
        return get_compressobj_instance(self.compression_algorithm)

    def _get_stream_decompresser(self) -> type[ZlibStreamDecompresser]:
        """Return a new instance of the correct StreamDecompresser class for the compression algorithm
        defined for this container.
        """
        return get_stream_decompresser(self.compression_algorithm)

    def get_object_content(self, hashkey: str) -> bytes:
        """Get the content of an object with a given hash key.

        :param hashkey: The hash key of the object to retrieve.
        :return: a byte stream with the object content.
        """
        with self.get_object_stream(hashkey) as handle:
            return handle.read()

    @contextmanager
    def get_object_stream(self, hashkey: str) -> Iterator[StreamReadBytesType]:
        """Return a context manager yielding a stream to get the content of an object.

        To be used as a context manager::

          with container.get_object_stream(hashkey) as fhandle:
              data = fhandle.read()

        The returned object supports *at least* the read() method that
        accepts an optional parameter to read the file in chunks, and might
        not be seekable.
        :param hashkey: the hashkey of the object to stream.
        """
        with self.get_object_stream_and_meta(hashkey=hashkey) as (fhandle, _):
            yield fhandle

    @contextmanager
    def get_object_stream_and_meta(
        self, hashkey: str
    ) -> Iterator[tuple[StreamReadBytesType, ObjectMeta],]:
        """Return a context manager yielding a stream to get the content of an object, and a metadata dictionary.

        To be used as a context manager::

          with container.get_object_stream(hashkey) as (fhandle, meta):
              data = fhandle.read()
              assert len(data) == meta['size']

        The returned file-handle object supports *at least* the read() method that
        accepts an optional parameter to read the file in chunks, and might
        not be seekable.
        The returned metadata is an ObjectMeta dataclass.

        :param hashkey: the hashkey of the object to stream.
        """
        with self.get_objects_stream_and_meta(
            hashkeys=[hashkey], skip_if_missing=False
        ) as triplets:
            counter = 0
            for (
                obj_hashkey,
                stream,
                meta,
            ) in triplets:  # pylint: disable=not-an-iterable
                counter += 1
                assert (
                    counter == 1
                ), "There is more than one item returned by get_objects_stream_and_meta"
                assert obj_hashkey == hashkey

                if stream is None:
                    raise NotExistent(f"No object with hash key {hashkey}")

                yield stream, meta

    @overload
    def _get_objects_stream_meta_generator(
        self,
        hashkeys: Sequence[str],
        skip_if_missing: bool,
        with_streams: Literal[False],
    ) -> Iterator[tuple[str, ObjectMeta]]:
        ...

    @overload
    def _get_objects_stream_meta_generator(
        self,
        hashkeys: Sequence[str],
        skip_if_missing: bool,
        with_streams: Literal[True],
    ) -> Iterator[tuple[str, StreamSeekBytesType | None, ObjectMeta]]:
        ...

    def _get_objects_stream_meta_generator(  # pylint: disable=too-many-branches,too-many-statements,too-many-locals
        self,
        hashkeys: Sequence[str],
        skip_if_missing: bool,
        with_streams: bool,
    ) -> Iterator[
        (tuple[str, ObjectMeta] | tuple[str, StreamSeekBytesType | None, ObjectMeta])
    ]:
        """Return a generator yielding triplets of (hashkey, open stream, size).

        :note: The stream is already open and at the right position, and can
            just be read.

        :note: size is the length of the object (uncompressed) when doing a
            ``read()`` on the returned stream

        :note: do not use directly! Call always the proper public methods. This is only
            for internal use

        :param hashkeys: a list of hash keys for which we want to get a stream reader
        :param skip_if_missing: if True, just skip hash keys that are not in the container
            (i.e., neither packed nor loose). If False, return ``None`` instead of the
            stream.
        :param with_streams: if True, yield triplets (hashkey, stream, meta).
            If False, yield pairs (hashkey, meta) and avoid to open any file.
        """
        # pylint: disable=too-many-nested-blocks

        # During the run, this variable is updated with the currently open file.
        # This file is closed before opening a new one - so we ensure only one is
        # open at a given time.
        # The try/finally block makes sure we close it at the end, if any was open.
        last_open_file = None
        lazy_loose_stream: LazyLooseStream | None = None

        # Operate on a set - only return once per required hashkey, even if required more than once
        hashkeys_set = set(hashkeys)

        hashkeys_in_packs: set[str] = set()

        packs = defaultdict(list)
        # Currently ordering in the DB (it's ordered across all packs, but this should not be
        # a problem as we then split them by pack). To be checked, performance-wise, if it's better
        # to order in python instead
        session = self._get_cached_session()

        obj_reader: StreamReadBytesType

        if len(hashkeys_set) <= self._MAX_CHUNK_ITERATE_LENGTH:
            # Operate in chunks, due to the SQLite limits
            # (see comment above the definition of self._IN_SQL_MAX_LENGTH)
            for chunk in chunk_iterator(hashkeys_set, size=self._IN_SQL_MAX_LENGTH):
                stmt = select(
                    Obj.pack_id,
                    Obj.hashkey,
                    Obj.offset,
                    Obj.length,
                    Obj.compressed,
                    Obj.size,
                ).where(Obj.hashkey.in_(chunk))
                for res in session.execute(stmt):
                    packs[res[0]].append(
                        ObjQueryResults(res[1], res[2], res[3], res[4], res[5])
                    )
        else:
            sorted_hashkeys = sorted(hashkeys_set)
            pack_iterator = session.execute(
                text(
                    "SELECT pack_id, hashkey, offset, length, compressed, size FROM db_object ORDER BY hashkey"
                )
            )
            # The left_key returns the second element of the tuple, i.e. the hashkey (that is the value to compare
            # with the right iterator)
            for res, where in detect_where_sorted(
                pack_iterator, sorted_hashkeys, left_key=lambda x: x[1]
            ):
                if where == Location.BOTH:
                    # If it's in both, it returns the left one, i.e. the full data from the DB
                    packs[res[0]].append(
                        ObjQueryResults(res[1], res[2], res[3], res[4], res[5])
                    )

        for pack_int_id, pack_metadata in packs.items():
            pack_metadata.sort(key=lambda metadata: metadata.offset)
            hashkeys_in_packs.update(obj.hashkey for obj in pack_metadata)
            pack_path = self._get_pack_path_from_pack_id(str(pack_int_id))
            try:
                # Open only once per file (if in `with_streams` mode)
                if with_streams:
                    last_open_file = open(  # pylint: disable=consider-using-with
                        pack_path, mode="rb"
                    )
                for metadata in pack_metadata:
                    meta = {
                        "type": ObjectType.PACKED,
                        "size": metadata.size,
                        "pack_id": pack_int_id,
                        "pack_compressed": metadata.compressed,
                        "pack_offset": metadata.offset,
                        "pack_length": metadata.length,
                    }

                    if with_streams:
                        assert last_open_file is not None
                        obj_reader = PackedObjectReader(
                            fhandle=last_open_file,
                            offset=metadata.offset,
                            length=metadata.length,
                        )
                        lazy_loose_stream = None
                        if metadata.compressed:
                            # I create a LazyLooseStream. It is the
                            # responsibility of the stream decompresser to open
                            # the stream if it feels it needs it.
                            lazy_loose_stream = self.get_lazy_loose_stream(
                                hashkey=metadata.hashkey
                            )
                            obj_reader = self._get_stream_decompresser()(
                                obj_reader, lazy_uncompressed_stream=lazy_loose_stream
                            )
                        yield metadata.hashkey, obj_reader, ObjectMeta(**meta)
                        # Here I check if the LazyLooseStream that I passed has
                        # been openeed - if so, I close it so I don't leave
                        # open file streams around
                        if (
                            lazy_loose_stream is not None
                            and not lazy_loose_stream.closed
                        ):
                            lazy_loose_stream.close_stream()
                    else:
                        yield metadata.hashkey, ObjectMeta(**meta)
            finally:
                if last_open_file is not None:
                    if not last_open_file.closed:
                        last_open_file.close()

        # Collect loose hash keys that are not found
        # Reason: a concurrent process might have packed them,
        # in the meantime.
        loose_not_found = set()
        for loose_hashkey in hashkeys_set.difference(hashkeys_in_packs):
            obj_path = self._get_loose_path_from_hashkey(hashkey=loose_hashkey)
            try:
                if with_streams:
                    last_open_file = open(  # pylint: disable=consider-using-with
                        obj_path, mode="rb"
                    )
                    # I do not use Pathlib to get the size, in case the file has just
                    # been deleted by a concurrent writer, but I use the lower-level os.fstat
                    # on the fileno() of the open file
                    meta = {
                        "type": ObjectType.LOOSE,
                        "size": os.fstat(last_open_file.fileno()).st_size,
                        "pack_id": None,
                        "pack_compressed": None,
                        "pack_offset": None,
                        "pack_length": None,
                    }

                    yield loose_hashkey, last_open_file, ObjectMeta(**meta)
                else:
                    # This will also raise a FileNotFoundError if the file does not exist
                    size = obj_path.stat().st_size
                    meta = {
                        "type": ObjectType.LOOSE,
                        "size": size,
                        "pack_id": None,
                        "pack_compressed": None,
                        "pack_offset": None,
                        "pack_length": None,
                    }

                    yield loose_hashkey, ObjectMeta(**meta)
            except FileNotFoundError:
                loose_not_found.add(loose_hashkey)
                continue
            finally:
                # Close each loose file, if open
                if last_open_file is not None:
                    if not last_open_file.closed:
                        last_open_file.close()

        # There were some loose objects that were not found
        # Give a final try - if they have been deleted in the meantime
        # while being packed, I should have the guarantee that they
        # are by now in the pack.
        # If they are not, the object does not exist.
        if loose_not_found:
            # IMPORTANT. I need to close the session (and flush the
            # self._session cache) to refresh the DB, otherwise since I am
            # reading in WAL mode, I will be keeping to read from the "old"
            # state of the DB.
            # Note that this is an expensive operation!
            # This means that asking for non-existing objects will be
            # slow.
            if self._session is not None:
                self._session.close()
                self._session = None

            packs = defaultdict(list)
            session = self._get_cached_session()
            if len(loose_not_found) <= self._MAX_CHUNK_ITERATE_LENGTH:
                for chunk in chunk_iterator(
                    loose_not_found, size=self._IN_SQL_MAX_LENGTH
                ):
                    stmt = select(
                        Obj.pack_id,
                        Obj.hashkey,
                        Obj.offset,
                        Obj.length,
                        Obj.compressed,
                        Obj.size,
                    ).where(Obj.hashkey.in_(chunk))
                    for res in session.execute(stmt):
                        packs[res[0]].append(
                            ObjQueryResults(res[1], res[2], res[3], res[4], res[5])
                        )
            else:
                sorted_hashkeys = sorted(loose_not_found)
                pack_iterator = session.execute(
                    text(
                        "SELECT pack_id, hashkey, offset, length, compressed, size FROM db_object ORDER BY hashkey"
                    )
                )
                # The left_key returns the second element of the tuple, i.e. the hashkey (that is the value to compare
                # with the right iterator)
                for res, where in detect_where_sorted(
                    pack_iterator, sorted_hashkeys, left_key=lambda x: x[1]
                ):
                    if where == Location.BOTH:
                        # If it's in both, it returns the left one, i.e. the full data from the DB
                        packs[res[0]].append(
                            ObjQueryResults(res[1], res[2], res[3], res[4], res[5])
                        )

            # I will construct here the really missing objects.
            # I make a copy of the set.
            really_not_found = loose_not_found.copy()

            for pack_int_id, pack_metadata in packs.items():
                pack_metadata.sort(key=lambda metadata: metadata.offset)
                # I remove those that I found
                really_not_found.difference_update(obj.hashkey for obj in pack_metadata)

                pack_path = self._get_pack_path_from_pack_id(str(pack_int_id))
                try:
                    if with_streams:
                        last_open_file = open(  # pylint: disable=consider-using-with
                            pack_path, mode="rb"
                        )

                    for metadata in pack_metadata:
                        meta = {
                            "type": ObjectType.PACKED,
                            "size": metadata.size,
                            "pack_id": pack_int_id,
                            "pack_compressed": metadata.compressed,
                            "pack_offset": metadata.offset,
                            "pack_length": metadata.length,
                        }
                        if with_streams:
                            assert last_open_file is not None
                            obj_reader = PackedObjectReader(
                                fhandle=last_open_file,
                                offset=metadata.offset,
                                length=metadata.length,
                            )

                            lazy_loose_stream = None
                            if metadata.compressed:
                                # I create a LazyLooseStream.
                                # It is the responsibility of the stream decompresser to open the stream if it feels it
                                # needs it.
                                lazy_loose_stream = self.get_lazy_loose_stream(
                                    hashkey=metadata.hashkey
                                )
                                obj_reader = self._get_stream_decompresser()(
                                    obj_reader,
                                    lazy_uncompressed_stream=lazy_loose_stream,
                                )
                            yield metadata.hashkey, obj_reader, ObjectMeta(**meta)
                            # Here I check if the LazyLooseStream that I passed has
                            # been openeed - if so, I close it so I don't leave
                            # open file streams around
                            if (
                                lazy_loose_stream is not None
                                and not lazy_loose_stream.closed
                            ):
                                lazy_loose_stream.close_stream()
                        else:
                            yield metadata.hashkey, ObjectMeta(**meta)
                finally:
                    if last_open_file is not None:
                        if not last_open_file.closed:
                            last_open_file.close()

            # If there are really missing objects, and skip_if_missing is False, yield them
            if really_not_found and not skip_if_missing:
                for missing_hashkey in really_not_found:
                    meta = {
                        "type": ObjectType.MISSING,
                        "size": None,
                        "pack_id": None,
                        "pack_compressed": None,
                        "pack_offset": None,
                        "pack_length": None,
                    }
                    if with_streams:
                        yield missing_hashkey, None, ObjectMeta(**meta)
                    else:
                        yield missing_hashkey, ObjectMeta(**meta)

    @contextmanager
    def get_objects_stream_and_meta(
        self, hashkeys: Sequence[str], skip_if_missing: bool = True
    ) -> Iterator[Iterator[tuple[str, StreamSeekBytesType | None, ObjectMeta]]]:
        """A context manager returning a generator yielding triplets of (hashkey, open stream, metadata).

        :note: the hash keys yielded are often in a *different* order than the original
            ``hashkeys`` list. This is done for efficiency reasons, to reduce to a minimum
            file opening and to try to read file chunks (for packs) in sequential
            order rather than in random order.

        To use it, you should do something like the following::

            with container.get_objects_stream_and_meta(hashkeys=hashkeys) as triplets:
                for obj_hashkey, stream, meta in triplets:
                    if stream is None:
                        # This should happen only if you pass skip_if_missing=False
                        retrieved[obj_hashkey] = None
                    else:
                        # len(stream.read() will be equal to size
                        retrieved[obj_hashkey] = stream.read()

        The returned metadata is an ObjectMeta dataclass.

        :param hashkeys: a list of hash keys for which we want to get a stream reader
        :param skip_if_missing: if True, just skip hash keys that are not in the container
            (i.e., neither packed nor loose). If False, return ``None`` instead of the
            stream. In this latter case, the length of the generator returned by this context
            manager has always the same length as the input ``hashkeys`` list.
        """
        yield self._get_objects_stream_meta_generator(
            hashkeys=hashkeys, skip_if_missing=skip_if_missing, with_streams=True
        )

    def get_lazy_loose_stream(self, hashkey: str) -> LazyLooseStream:
        """Return a LazyLooseStream pointing to the given hashkey.

        As explained in the docsring of LazyLooseStream, the goal is to return a stream that needs to be explicitly
        opened and points to a "cached copy" of an already existing packed object, that is made loose again
        in order to have an uncompressed version of it.
        """
        return LazyLooseStream(container=self, hashkey=hashkey)

    def get_objects_meta(
        self, hashkeys: Sequence[str], skip_if_missing: bool = True
    ) -> Iterator[tuple[str, ObjectMeta]]:
        """A generator yielding pairs of (hashkey, metadata).

        :note: the hash keys yielded are often in a *different* order than the original
            ``hashkeys`` list. This is to have the same behavior of ``get_objects_stream_and_meta``,
            and for efficiency (even if efficiency is less of an issue for this method).

        To use it, you should do something like the following::

            for obj_hashkey, meta in container.get_objects_meta(hashkeys=hashkeys):
                sizes[obj_hashkey] = meta['size']

        Note that if you can afford putting everything in memory and do not want to bother with the
        different ordering, you can just do::

            metas = dict(container.get_objects_meta(hashkeys=hashkeys))

        and then you can access the meta of an object via ``metas[hashkey]``.

        The returned metadata is an ObjectMeta dataclass.

        :param hashkeys: a list of hash keys for which we want to get a stream reader
        :param skip_if_missing: if True, just skip hash keys that are not in the container
            (i.e., neither packed nor loose). If False, return them (``meta['type']`` will have value
            ObjectType.MISSING in this case).
            In this latter case, the length of the generator returned by this context
            manager has always the same length as the input ``hashkeys`` list.
        """
        return self._get_objects_stream_meta_generator(
            hashkeys=hashkeys, skip_if_missing=skip_if_missing, with_streams=False
        )

    def get_object_meta(self, hashkey: str) -> ObjectMeta:
        """Return the metadata dictionary for the given hash key.

        To be used as follows:

          meta = container.get_object_meta(hashkey)
          print(meta['size'])

        The returned metadata is an ObjectMeta dataclass.

        :param hashkey: the hashkey of the object to stream.
        """
        counter = 0
        for (
            obj_hashkey,
            meta,
        ) in self.get_objects_meta(  # pylint: disable=not-an-iterable
            hashkeys=[hashkey], skip_if_missing=False
        ):
            counter += 1
            assert (
                counter == 1
            ), "There is more than one item returned by get_objects_stream_and_meta"
            assert obj_hashkey == hashkey

            if meta["type"] != ObjectType.MISSING:
                return meta

        assert (
            counter == 1
        ), "No object found, this should never happen since I pass skip_if_missing=False!"
        raise NotExistent(f"No object with hash key {hashkey}")

    def has_objects(self, hashkeys: list[str] | tuple[str, ...]) -> list[bool]:
        """Return whether the container contains objects with the given hash keys.

        :param hashkeys: a list of hash keys to check.
        :return: a list of booleans, where the i-th value is True if the i-th object of the ``hashkeys``
            list exists, False otherwise.
        """
        existing_hashkeys = set()

        # Note: This iterates in a 'random' order, different than the `hashkeys` list
        for obj_hashkey, _ in self.get_objects_meta(  # pylint: disable=not-an-iterable
            hashkeys=hashkeys, skip_if_missing=True
        ):
            # Since I use skip_if_missing=True, I should only iterate on those that exist
            existing_hashkeys.add(obj_hashkey)

        # Return a list of booleans
        return [hashkey in existing_hashkeys for hashkey in hashkeys]

    def has_object(self, hashkey: str) -> bool:
        """Return whether the container contains an object with the given hashkey.

        :param hashkey: the hashkey of the object.
        :return: True if the object exists, False otherwise.
        """
        return self.has_objects([hashkey])[0]

    def get_objects_content(
        self, hashkeys: list[str], skip_if_missing: bool = True
    ) -> dict[str, bytes | None]:
        """Get the content of a number of objects with given hash keys.

        :note: use this method only if you know objects fit in memory.
            Otherwise, use the ``get_objects_stream_and_meta`` context manager and
            process the objects one by one.

        :param hashkeys: A list of hash kyes of the objects to retrieve.
        :return: a dictionary of byte streams where the keys are the hash keys and the values
            are the object contents.
        """
        retrieved: dict[str, bytes | None] = {}
        with self.get_objects_stream_and_meta(
            hashkeys=hashkeys, skip_if_missing=skip_if_missing
        ) as triplets:
            for obj_hashkey, stream, _ in triplets:  # pylint: disable=not-an-iterable
                if stream is None:
                    # This should happen only if skip_if_missing is False
                    retrieved[obj_hashkey] = None
                else:
                    retrieved[obj_hashkey] = stream.read()
        return retrieved

    def _new_object_writer(self) -> ObjectWriter:
        """Return a context manager that can be used to create a new object.

        To use it, do the following::

          new_object_writer = repo._new_object_writer()
          with new_object_writer as fhandle:
              fhandle.write(b'something')
          new_hashkey = new_object_writer.get_hashkey()
        """
        return ObjectWriter(
            sandbox_folder=self._get_sandbox_folder(),
            loose_folder=self._get_loose_folder(),
            loose_prefix_len=self.loose_prefix_len,
            duplicates_folder=self._get_duplicates_folder(),
            hash_type=self.hash_type,
        )

    def add_object(self, content: bytes) -> str:
        """Add a loose object from its content.

        :param content: a binary stream with the file content.
        :return: the hash key of the newly created object.
        """
        stream = io.BytesIO(content)
        return self.add_streamed_object(stream)

    def add_streamed_object(self, stream: StreamReadBytesType) -> str:
        """Add a loose object getting the content from a stream and limiting memory usage even for large objects.

        :param stream: an (open) stream. The stream will be read from the current position, so make sure that
           the seek() position on the stream is at zero. The stream will be read until the end, and the content
           will be then stored as an object.
        :return: the hash key of the newly created loose object.
        """
        _read_chunk_size = 524288
        writer = self._new_object_writer()

        with writer as fhandle:
            while True:
                chunk = stream.read(_read_chunk_size)
                if not chunk:
                    break
                fhandle.write(chunk)

        hashkey = writer.get_hashkey()
        assert hashkey is not None
        return hashkey

    def count_objects(self) -> ObjectCount:
        """Return an ObjectCount object with the count of objects.

        In particular, it returns the number of loose objects,
        of packed objects, and the number of pack files."""

        number_packed = self._get_cached_session().scalar(
            select(func.count()).select_from(Obj)
        )
        return ObjectCount(
            packed=number_packed,
            loose=sum(1 for _ in self._list_loose()),
            pack_files=sum(1 for _ in self._list_packs()),
        )

    @classmethod
    def _is_valid_pack_id(cls, pack_id: str, allow_repack_pack: bool = False) -> bool:
        """Return True if the name is a valid pack ID.

        If allow_repack_pack is True, also the pack id used for repacking is considered as valid.
        """
        if not pack_id:
            # Must be a non-empty string
            return False
        if pack_id != "0" and pack_id[0] == "0":
            # The ID must be a valid integer: either zero, or it should not start by zero
            return False
        if allow_repack_pack and pack_id == str(cls._REPACK_PACK_ID):
            return True
        if not all(char in "0123456789" for char in pack_id):
            return False
        return True

    def _is_valid_loose_prefix(self, prefix: str) -> bool:
        """Return True if the name is a valid prefix."""
        if len(prefix) != self.loose_prefix_len:
            return False
        if not all(char in "0123456789abcdef" for char in prefix):
            return False
        return True

    @staticmethod
    def _is_valid_hashkey(hashkey: str) -> bool:
        """Return True is the name is a valid hashkey.

        Note that it currently does not check the length but only that the key is composed only
        by hexadecimal characters.
        """
        if not all(char in "0123456789abcdef" for char in hashkey):
            return False
        return True

    def get_total_size(self) -> TotalSize:
        """Return a dictionary with the total size of objects in the container.

        The information returned is a TotalSize dataclass.
        """
        retval = {}

        session = self._get_cached_session()
        # COALESCE is used to return 0 if there are no results, rather than None
        # SQL's COALESCE returns the first non-null result
        retval["total_size_packed"] = session.scalar(
            select(func.coalesce(func.sum(Obj.size), 0).label("total_size_packed"))
        )
        retval["total_size_packed_on_disk"] = session.scalar(
            select(func.coalesce(func.sum(Obj.length), 0).label("total_length_packed"))
        )

        total_size_packfiles_on_disk = 0
        for pack_id in list(self._list_packs()):
            total_size_packfiles_on_disk += (
                self._get_pack_path_from_pack_id(pack_id).stat().st_size
            )
        retval["total_size_packfiles_on_disk"] = total_size_packfiles_on_disk

        retval["total_size_packindexes_on_disk"] = (
            self._get_pack_index_path().stat().st_size
        )

        total_size_loose = 0
        for loose_hashkey in self._list_loose():
            loose_path = self._get_loose_path_from_hashkey(loose_hashkey)
            total_size_loose += loose_path.stat().st_size
        retval["total_size_loose"] = total_size_loose

        return TotalSize(**retval)

    @contextmanager
    def lock_pack(
        self, pack_id: str, allow_repack_pack: bool = False
    ) -> Iterator[StreamWriteBytesType]:
        """Lock the given pack id. Use as a context manager.

        Raise if the pack is already locked. If you enter the context manager,
        it means you successfully locked the pack.

        Important to use for avoiding concurrent access/append to the same file.
        :param pack_id: a string with a valid pack name.
        :param allow_pack_repack: if True, allow to open the pack file used for repacking
        """
        assert self._is_valid_pack_id(pack_id, allow_repack_pack=allow_repack_pack)

        # Open file in exclusive mode
        lock_file = self._get_pack_folder() / f"{pack_id}.lock"
        pack_file = self._get_pack_path_from_pack_id(
            pack_id, allow_repack_pack=allow_repack_pack
        )
        try:
            with open(lock_file, "x"):
                with open(pack_file, "ab") as pack_handle:
                    yield pack_handle
        finally:
            # Release resource (I check if it exists in case there was an exception)
            if lock_file.exists():
                os.remove(lock_file)

    def _list_loose(self) -> Iterator[str]:
        """Iterate over loose objects.

        This returns all loose objects, even if a packed version of the same object exists.

        .. note:: this returns a generator of hash keys.
        """
        for first_level in os.listdir(self._get_loose_folder()):
            if self.loose_prefix_len:
                if not self._is_valid_loose_prefix(first_level):
                    continue
                for second_level in os.listdir(self._get_loose_folder() / first_level):
                    hashkey = f"{first_level}{second_level}"
                    if not self._is_valid_hashkey(hashkey):
                        continue
                    yield hashkey
            else:
                # It's flat (loose_prefix_len == 0)
                if not self._is_valid_hashkey(first_level):
                    continue
                yield first_level

    def _list_packs(self) -> Iterator[str]:
        """Iterate over packs.

        .. note:: this returns a generator of the pack IDs.
        """
        for fname in os.listdir(self._get_pack_folder()):
            ## I actually check for pack index files
            # if not fname.endswith(self._PACK_INDEX_SUFFIX):
            #    continue
            # pack_id = fname[:-len(self._PACK_INDEX_SUFFIX)]
            if self._is_valid_pack_id(fname):
                yield fname

    def list_all_objects(self) -> Iterator[str]:
        """Iterate of all object hashkeys.

        This function might be slow if there are many loose objects!
        Use only if needed.
        """
        yield_per_size = 1000

        # We get all objects that are loose, create a set
        loose_objects = set(self._list_loose())

        # Let us initialise a session
        session = self._get_cached_session()

        # This variable stored the last PK that we saw. We are assuming that PKs are always positive integers.
        # NOTE: We don't use limit+offset, but a filter on the last PK being > than the last PK seen.
        # In this way, we don't risk to miss objects if an object is deleted while we are iterating.
        # We could still miss objects if an object is recreated after deletion and it re-uses an old, unused PK.
        # In any case, we are working in WAL mode, and I think it's ok not to report an object that was created
        # after this call was called. It would be bad instead to miss an object that has always existed
        last_pk = -1
        while True:
            stmt = (
                select(Obj.id, Obj.hashkey)
                .where(Obj.id > last_pk)
                .order_by(Obj.id)
                .limit(yield_per_size)
            )
            results_chunk = session.execute(stmt).all()

            for _, hashkey in results_chunk:
                # I need to use a comma because I want to create a tuple
                loose_objects.difference_update((hashkey,))
                yield hashkey

            if not results_chunk:
                break
            last_pk = results_chunk[-1][0]

        # What is left are the loose objects that are not in the packs
        for hashkey in loose_objects:
            yield hashkey

    def _write_data_to_packfile(
        self,
        pack_handle: StreamWriteBytesType,
        read_handle: StreamReadBytesType,
        compress: bool,
        hash_type: str | None = None,
    ) -> tuple[int, None] | tuple[int, str]:
        """Append data, read from read_handle until it ends, to the correct packfile.

        Return the number of bytes READ (note that this will be different
        than the number of bytes written to pack_handle, if compress==True).
        If you need to know how many bytes were written, call pack_handle.tell() before
        and after calling this function.

        :note: this function just writes to disk, but is not concerned with locking the file,
          nor with updating the index. THEREFORE, call it ONLY within a locking block and make
          sure you update the index as well.

        :param pack_handle: an open pack handle to write to (must be open in write and append mode).
           Also, should be seekable (in particular, .tell() should work).
        :param read_handle: a file-like object to read from (must be a binary stream, needs to
           support at least the .read() method with a size parameter).
        :param compress: if True, compress the stream when writing to disk
        :param hash_type: if None, no hash is computed (more efficient). If it is a string, use that hash type.
        :return: a tuple with ``(number_of_bytes, hashkey)`` where ``number_of_bytes`` is the (uncompressed)
            size and ``hash_key`` is ``None`` is ``hash_type`` is ``None``, otherwise it contains the hash
            computed with the given ``hash_type`` algorithm.
        """
        assert "b" in pack_handle.mode
        assert "a" in pack_handle.mode

        if hash_type:
            hasher = get_hash_cls(hash_type=hash_type)()

        if compress:
            compressobj = self._get_compressobj_instance()

        count_read_bytes = 0
        while True:
            chunk = read_handle.read(self._CHUNKSIZE)
            if chunk == b"":
                # Returns an empty bytes object on EOF.
                # Returns None if the underlying raw stream was open in non-blocking
                # mode and no data is available at the moment.
                break
            count_read_bytes += len(chunk)
            if hash_type:
                hasher.update(chunk)
            if compress:
                pack_handle.write(compressobj.compress(chunk))
            else:
                pack_handle.write(chunk)

        if compress:
            # Write the remaining of the file, if any leftovers are still present in the
            # compressobj
            pack_handle.write(compressobj.flush())

        return (count_read_bytes, hasher.hexdigest() if hash_type else None)

    def pack_all_loose(  # pylint: disable=too-many-locals,too-many-branches,too-many-statements
        self,
        compress: bool | CompressMode = CompressMode.NO,
        validate_objects: bool = True,
        do_fsync: bool = True,
        callback: None
        | (Callable[[Arg(str, "action"), Arg(Any, "value")], None]) = None,
    ) -> None:
        """Pack all loose objects.

        This is an operation that can be run at any time even when the container is being read
        and written (ony to loose files, though), **BUT it needs to be done only by one
        process at any given time**.

        :param compress: either a boolean or a `CompressMode` objects.
           If True (or `CompressMode.YES`), compress objects before storing them.
           If False (or `CompressMode.NO`), do not compress objects (the default).
           Also other `CompressMode`s are allowed, such as `CompressMode.AUTO` to use fast heuristics
           to decide whether to compress or not.
           Note that since loose objects are always uncompressed, `CompressMode.KEEP` is equivalent to
           `CompressMode.NO` in this function.
        :param validate_objects: if True, recompute the hash while packing, and raises if there is a problem.
        :param do_fsync: if True, calls a flush to disk of the pack files before closing it.
            Needed to guarantee that data will be there even in the case of a power loss.
            Set to False if you don't need such a guarantee (anyway the loose version will be kept,
            so often this guarantee is not strictly needed).
        :param callback: a callback function that can be used to report progress.
            The callback function should accept two arguments: a string with the action being performed
            and the value of the action. The action can be "init" (initialization),
            "update" (update of the progress), or "close" (finalization).
            In case of "init", the value is a dictionary with the key "total" as the total size of the operation
            and key "description" as the label of the operation.
            In case of "update", the value is amount of the operation that has been completed.
            In case of "close", the value is None.
            return value of the callback function is ignored.
        """
        hash_type = self.hash_type if validate_objects else None

        compress_mode: CompressMode
        # For backwards-compatibility, convert boolean to CompressMode
        if isinstance(compress, bool):
            if compress:
                compress_mode = CompressMode.YES
            else:
                compress_mode = CompressMode.NO
        else:
            compress_mode = compress

        loose_objects = set(self._list_loose())
        pack_int_id = self._get_pack_id_to_write_to()
        session = self._get_cached_session()

        # I first skip all loose hashkeys that already exist in the pack.
        # Packing should be performed by a single process at a given time as a
        # maintenance operation, so I don't have to worry about concurrency:
        # If I don't find it here, is should not appear midway during the rest of the process

        existing_packed_hashkeys = []

        if len(loose_objects) <= self._MAX_CHUNK_ITERATE_LENGTH:
            for chunk in chunk_iterator(loose_objects, size=self._IN_SQL_MAX_LENGTH):
                # I check the hash keys that are already in the pack
                stmt = select(Obj.hashkey).where(Obj.hashkey.in_(chunk))
                for res in session.execute(stmt):
                    existing_packed_hashkeys.append(res[0])
        else:
            sorted_hashkeys = sorted(loose_objects)
            pack_iterator = session.execute(
                text("SELECT hashkey FROM db_object ORDER BY hashkey")
            )

            # The query returns a tuple of length 1, so I still need a left_key
            for res, where in detect_where_sorted(
                pack_iterator, sorted_hashkeys, left_key=lambda x: x[0]
            ):
                if where == Location.BOTH:
                    existing_packed_hashkeys.append(res[0])

        # I remove them from the loose_objects list
        loose_objects.difference_update(existing_packed_hashkeys)
        # Now, I should be left only with objects with hash keys that are not yet known.
        # I can then continue

        # Here, I could do some clean up of loose objects that are already in the packs,
        # by removing all loose objects with hash key `existing_packed_hashkeys`, that are
        # already packed.
        # HOWEVER, while this would work fine on Linux, there are concurrency issues both
        # on Mac and on Windows (see issues #37 and #43). Therefore, I do NOT delete them,
        # and deletion is deferred to a manual clean-up operation.

        if callback:
            callback(
                action="init",
                value={
                    "total": self.get_total_size()["total_size_loose"],
                    "description": "Packing loose objects",
                },
            )
            # I wish this would show as MB, GB. In tqdm it's easy:
            # just pass unit='B' and unit_scale=1024.
            # But to do this here, some changes is in callback function is needed.
            # see this feature request for more details: https://github.com/aiidateam/aiida-core/issues/6564

        # Outer loop: this is used to continue when a new pack file needs to be created
        while loose_objects:
            # Store the last pack integer ID, needed to know later if I need to open a new pack
            last_pack_int_id = pack_int_id
            # Avoid concurrent writes on the pack file
            with self.lock_pack(str(pack_int_id)) as pack_handle:
                # Inner loop: continue until when there is a file, or
                # if we need to change pack (in this case `break` is called)

                # We will store here the dictionaries with the data to be pushed in the DB
                # By collecting the data and committing as a bulk operation at the end,
                # we highly improve performance
                obj_dicts = []

                while loose_objects:
                    # Check in which pack I need to write to the next object
                    pack_int_id = self._get_pack_id_to_write_to()
                    if pack_int_id != last_pack_int_id:
                        # new pack file needed!
                        # Break from the inner while loop. This will:
                        # 1. go down after the while loop, performing commits and
                        #    final closing operations for this pack file
                        # 2. close the pack file, that was opened in the with statement
                        # 3. Iterate again with the outer loop, opening a new file
                        #    with the new pack_int_id that was just generated
                        break

                    # Get next hash key to process
                    loose_hashkey = loose_objects.pop()

                    obj_dict: dict[str, Any] = {}
                    obj_dict["hashkey"] = loose_hashkey
                    obj_dict["pack_id"] = pack_int_id
                    obj_dict["offset"] = pack_handle.tell()
                    try:
                        with open(
                            self._get_loose_path_from_hashkey(loose_hashkey), "rb"
                        ) as loose_handle:
                            # It's always a standard file, I get its size
                            loose_size = os.fstat(loose_handle.fileno()).st_size
                            # Determine if I should compress this object or not.
                            # Note: source_compressed is always False because loose objects are always uncompressed
                            # Therefore, it is also true that source_length == source_size
                            obj_dict["compressed"] = should_compress(
                                source_stream=loose_handle,
                                compress_mode=compress_mode,
                                source_compressed=False,
                                source_length=loose_size,
                                source_size=loose_size,
                            )

                            # The second parameter is `None` since we are not computing the hash
                            # We can instead pass the hash algorithm and assert that it is correct
                            (
                                obj_dict["size"],
                                new_hashkey,
                            ) = self._write_data_to_packfile(
                                pack_handle=pack_handle,
                                read_handle=loose_handle,
                                compress=obj_dict["compressed"],
                                hash_type=hash_type,
                            )
                    except PermissionError:
                        # This might happen if the file is being written and is locked.
                        # In this case, don't pack this file. We will pack it in a future call.
                        continue
                    if hash_type and new_hashkey != loose_hashkey:
                        raise InconsistentContent(
                            f"Error when packing object '{loose_hashkey}': "
                            f"re-computed hash is different! '{new_hashkey}'"
                        )
                    obj_dict["length"] = pack_handle.tell() - obj_dict["offset"]

                    # Appending for later bulk commit - see comments in add_streamed_objects_to_pack
                    obj_dicts.append(obj_dict)

                    if callback:
                        callback(
                            action="update",
                            value=obj_dict["size"],
                        )
                # It's now time to write to the DB, in a single bulk operation (per pack)
                if obj_dicts:
                    # Here I shouldn't need to do `OR IGNORE` as in `add_streamed_objects_to_pack`
                    # Because I'm already checking the hash keys and avoiding to add twice the same
                    session.execute(
                        Obj.__table__.insert(), obj_dicts  # pylint: disable=no-member
                    )
                    # Clean up the list - this will be cleaned up also later,
                    # but it's better to make sure that we do it here, to avoid trying to rewrite
                    # the same objects again
                    obj_dicts = []
                # I don't commit here; I commit after making sure the file is flushed and closed

                # flush and sync to disk before closing
                if do_fsync:
                    safe_flush_to_disk(
                        pack_handle,
                        Path(pack_handle.name).resolve(),
                        use_fullsync=True,
                    )

            # OK, if we are here, file was flushed, synced to disk and closed.
            # Let's commit then the information to the DB, so it's officially a
            # packed object. Note: committing as soon as we are done with one pack,
            # so if there's a problem with one pack we don't start operating on the next one
            # Note: because of the logic above, in theory this should not raise an IntegrityError!
            session.commit()

            # If we are here, things should be guaranteed by SQLite to be written to disk.
            # Then, it would be safe to already do some clean up of loose objects that are now packed,
            # and by doing it here we would do it after each pack.
            # This would mean keeping track of the loose objects added to packs, and removing them.
            # HOWEVER, while this would work fine on Linux, there are concurrency issues both
            # on Mac and on Windows (see issues #37 and #43). Therefore, I do NOT delete them,
            # and deletion is deferred to a manual clean-up operation.
        if callback:
            callback(action="close", value=None)

    def add_streamed_object_to_pack(  # pylint: disable=too-many-arguments
        self,
        stream: StreamSeekBytesType,
        compress: bool = False,
        open_streams: bool = False,
        no_holes: bool = False,
        no_holes_read_twice: bool = True,
        callback: Callable | None = None,
        callback_size_hint: int = 0,
        do_fsync: bool = True,
        do_commit: bool = True,
    ) -> str:
        """Add a single object in streamed form to a pack.

        For the description of the parameters, see the docstring of ``add_streamed_objects_to_pack``.

        The only difference is that here the callback will provide feedback on the progress of this specific object.
        :param callback_size_hint: the expected size of the stream - if provided, it is used send back the total
            length in the callbacks
        :return: a single object hash key
        """
        streams: list[StreamSeekBytesType] = [
            CallbackStreamWrapper(
                stream, callback=callback, total_length=callback_size_hint
            )
        ]

        # I specifically set the callback to None
        retval = self.add_streamed_objects_to_pack(
            streams,
            compress=compress,
            open_streams=open_streams,
            no_holes=no_holes,
            no_holes_read_twice=no_holes_read_twice,
            callback=None,
            do_fsync=do_fsync,
            do_commit=do_commit,
        )

        # Close the callback so the bar doesn't remain open
        streams[0].close_callback()  # type: ignore[union-attr]

        return retval[0]

    def add_streamed_objects_to_pack(  # pylint: disable=too-many-locals, too-many-branches, too-many-statements, too-many-arguments
        self,
        stream_list: list[StreamSeekBytesType] | list[LazyOpener],
        compress: bool = False,
        open_streams: bool = False,
        no_holes: bool = False,
        no_holes_read_twice: bool = True,
        callback: Callable | None = None,
        do_fsync: bool = True,
        do_commit: bool = True,
    ) -> list[str]:
        """Add objects directly to a pack, reading from a list of streams.

        This is a maintenance operation, available mostly for efficiency reasons
        e.g. if you are creating a container from scratch.
        As such, it needs to be done only by one process.

        :param stream_list: a list of BytesIO bytestreams to add.
        :param compress: if True, compress objects before storing them. Note that at variance with
            other methods such as `pack_all_loose` or `repack`, where various `CompressMode`s are possible,
            this is not (yet) implemented here.
        :param open_streams: if True, then open the streams using a ``with`` context
            manager. Otherwise, just read from them (assuming the responsibility of opening
            them is on the caller). Setting to True is useful when reading from many files,
            and passing here a number of ``LazyOpener`` objects.
        :param no_holes: if True, goes back and truncate the pack if the object that was just
            added already exists on the container. It is False by default because if you add millions of times
            objects that already exist, you risk to keep writing on the same bits and damaging the hard drive.
            If ``no_holes`` is False, you will need a full repack to claim back disk space. (Note that repacking
            is always needed after deleting an object).
        :param no_holes_read_twice: Read the objects and streams twice (and recompute the hash twice but avoid
            to write on disk and then overwrite with another object).
            This of course gives a performance hit as data has to be read twice, and rehashed twice; but avoids
            risking to damage the hard drive if e.g. re-importing the exact same data).
            This variable is ignored if `no_holes` is False.
        :param do_fsync: if True (default), call an fsync for every pack file, to ensure flushing to
            disk. Important to guarantee that data is not lost even in the case of a power loss.
            For performance (especially if you don't need such a guarantee, e.g. if you are creating
            from scratch a new repository with copy of objects), set it to False.
        :param do_commit: if True (default), commit data to the DB after every pack is written.
            In this way, even if there is an issue, partial objects end up in the repository.
            Set to False for efficiency if you need to call this function multiple times. In this case,
            however, remember to call a `commit()` call on the `session` manually at the end of the
            operations! (See e.g. the `import_files()` method).
        :return: a list of object hash keys
        """
        assert isinstance(
            compress, bool
        ), "Only True of False are valid `compress` modes when adding direclty to a pack"
        yield_per_size = 1000
        hashkeys: list[str] = []

        # Make a copy of the list and revert its order, so we can pop from the list
        # without affecting the original list, and it's from the end so it's fast
        working_stream_list = list(stream_list[::-1])
        pack_int_id = self._get_pack_id_to_write_to()
        session = self._get_cached_session()

        if no_holes:
            if callback:
                total = session.scalar(select(func.count()).select_from(Obj))
                if total:
                    # If we have a callback, compute the total count of objects in this pack
                    callback(
                        action="init",
                        value={"total": total, "description": "List existing"},
                    )
                    # Update at most 400 times, avoiding to increase CPU usage; if the list is small: every object.
                    update_every = max(int(total / 400), 1)
                    # Counter of how many objects have been since since the last update.
                    # A new callback will be performed when this value is > update_every.
                    since_last_update = 0

            known_packed_hashkeys = set()
            # I need to get the full list of PKs to know if the object exists
            # As this is expensive, I will do it only if it is needed, i.e. when no_holes is True
            last_pk = -1
            while True:
                stmt = (
                    select(Obj.id, Obj.hashkey)
                    .where(Obj.id > last_pk)
                    .order_by(Obj.id)
                    .limit(yield_per_size)
                )
                results_chunk = session.execute(stmt).all()

                if not results_chunk:
                    # No more packed objects
                    break

                for _, hashkey in results_chunk:
                    known_packed_hashkeys.add(hashkey)

                last_pk = results_chunk[-1][0]
                if callback:
                    since_last_update += len(results_chunk)
                    if since_last_update >= update_every:
                        callback(action="update", value=since_last_update)
                        since_last_update = 0

            if callback and total:
                # Final call to complete the bar
                if since_last_update:
                    callback(action="update", value=since_last_update)
                # Perform any wrap-up, if needed
                callback(action="close", value=None)

        if callback:
            total = len(working_stream_list)
            # If we have a callback, compute the total count of objects in this pack
            callback(
                action="init", value={"total": total, "description": "Bulk storing"}
            )
            # Update at most 400 times, avoiding to increase CPU usage; if the list is small: every object.
            update_every = max(int(total / 400), 1)
            # Counter of how many objects have been since since the last update.
            # A new callback will be performed when this value is > update_every.
            since_last_update = 0

        # Outer loop: this is used to continue when a new pack file needs to be created
        while working_stream_list:
            # Store the last pack integer ID, needed to know later if I need to open a new pack
            last_pack_int_id = pack_int_id

            # Avoid concurrent writes on the pack file
            with self.lock_pack(str(pack_int_id)) as pack_handle:
                # Inner loop: continue until when there is a file, or
                # if we need to change pack (in this case `break` is called)

                # We will store here the dictionaries with the data to be pushed in the DB
                # By collecting the data and committing as a bulk operation at the end,
                # we highly improve performance
                obj_dicts = []

                while working_stream_list:
                    # Check in which pack I need to write to the next object
                    pack_int_id = self._get_pack_id_to_write_to()
                    if pack_int_id != last_pack_int_id:
                        # Break from the inner while loop. This will:
                        # 1. go down after the while loop, performing commits and
                        #    final closing operations for this pack file
                        # 2. close the pack file, that was opened in the with statement
                        # 3. Iterate again with the outer loop, opening a new file
                        #    with the new pack_int_id that was just generated
                        break

                    # Get next stream, possibly preparing it to be open, or wrapping it
                    # if it is already open so it does not get open again
                    next_stream = working_stream_list.pop()
                    if open_streams:
                        stream_context_manager = next_stream
                    else:
                        stream_context_manager = nullcontext(next_stream)  # type: ignore[assignment]

                    if callback:
                        since_last_update += 1
                        if since_last_update >= update_every:
                            callback(action="update", value=since_last_update)
                            since_last_update = 0

                    # Get the position before writing the object - I need it if `no_holes` is True and the object
                    # is already there
                    position_before = pack_handle.tell()

                    obj_dict: dict[str, Any] = {}
                    obj_dict["pack_id"] = pack_int_id
                    obj_dict["compressed"] = compress
                    obj_dict["offset"] = pack_handle.tell()
                    with stream_context_manager as stream:
                        if no_holes and no_holes_read_twice:
                            # Compute the hash key before writing (I just read once)
                            (
                                obj_dict["hashkey"],
                                obj_dict["size"],
                            ) = compute_hash_and_size(stream, hash_type=self.hash_type)
                            if obj_dict["hashkey"] in known_packed_hashkeys:
                                # I recomputed the hashkey and this was already there: I don't try to write on disk,
                                # but I just continue.
                                # Note, however, that I first need to append the hash key to the list of
                                # hash keys to return at the end
                                hashkeys.append(obj_dict["hashkey"])
                                continue
                            # I didn't continue. Then, I need to store on disk, as it is a new unknown object.
                            # I therefore need to seek back to zero, because the next line will read it again
                            # in _write_data_to_packfile.
                            stream.seek(0)

                        (
                            obj_dict["size"],
                            obj_dict["hashkey"],
                        ) = self._write_data_to_packfile(
                            pack_handle=pack_handle,
                            read_handle=stream,
                            compress=compress,
                            hash_type=self.hash_type,
                        )
                    obj_dict["length"] = pack_handle.tell() - obj_dict["offset"]
                    # Here, we have appended the object to the pack file.
                    # And now that we are done, we know the hash key.
                    # However, we have to cope with the fact that an object with the same hash key
                    # could be already inside the object.
                    # We cannot do a query for each object, it would be too expensive and inefficient.
                    # We need instead to rely of the unique constraint on the DB.
                    # However, the IntegrityError is raised not during the `add` call, but at the final
                    # `commit`.

                    # In this case, I have in memory a set of hash keys already in packs.
                    # Note that known_packed_hashkeys is defined only if no_holes is True.
                    if no_holes and obj_dict["hashkey"] in known_packed_hashkeys:
                        # The object is there!
                        # I seek back; I don't truncate, it's not needed.
                        # I will truncate only at the very end, if needed.
                        pack_handle.seek(position_before)
                    else:
                        # I use this, instead of a session.add()
                        # Either no_holes is False: then I don't know if the object exists, so I just try to insert
                        # it and in case do nothing; the space on disk might remain allocated (but unreferenced).
                        # Or `no_holes` is True and I don't have the object: this will insert the entry
                        obj_dicts.append(obj_dict)

                        # In the future, if there are memory issues with millions of objects,
                        # We can flush here to DB if there are too many objects in the cache.
                        # Also, there are other optimisations that can be done, like deleting
                        # the pack_metadata when not needed anymore etc.

                        # I also add the hash key in the known_packed_hashkeys (if no_holes, when this is defined)
                        if no_holes:
                            known_packed_hashkeys.add(obj_dict["hashkey"])

                    # Now, I have two options.
                    # 1. I just leave in the unused bits, and we do a re-packing later.
                    #    This is ok for efficiency, but might be problematic if you put a lot of
                    #    very similar objects, and get close to the hard-drive disk limit.
                    #    In this case, it becomes very hard to create a new 'vacuumed' pack.
                    # 2. We do a check (but this must be done object by object), performing another query,
                    #    and checking if we get the same object or a different one. If it's a different one,
                    #    we go back in the file and truncate it (or simply start writing again from there).
                    #    This might be slow as you have to do a query per object, and also risks that if you
                    #    are writing a lot of times objects that already exist, you 'burn' your hard-drive
                    #    by writing in the very same spot.
                    # 3. We do a very first query at the beginning to get *all hashes*, and we use it to drop
                    #    immediately. However, it's risky as one might run out of memory.
                    #    3a. An option could be not to store the *whole* hash key, but just the first part of the
                    #    hash. This should reduce the memory requirements, and we can do the query only if there
                    #    are potential conflicts.
                    # For now, I just go with option 1 - it's simpler to code, and still safe unless you
                    # end out of space. I would try next 3a, in case.

                    # Append the new hash key to the list of hash keys to return
                    hashkeys.append(obj_dict["hashkey"])

                if no_holes:
                    # If I don't want holes, I might be left in a case where at the end of the pack
                    # I have written some bytes and then I have seeked back. I truncate then the file at the current
                    # position.
                    pack_handle.truncate()

                # It's now time to write to the DB, in a single bulk operation (per pack)
                if obj_dicts:
                    session.execute(
                        Obj.__table__.insert().prefix_with(  # pylint: disable=no-member
                            "OR IGNORE"
                        ),
                        obj_dicts,
                    )
                    # Clean up the list - this will be cleaned up also later,
                    # but it's better to make sure that we do it here, to avoid trying to rewrite
                    # the same objects again
                    obj_dicts = []
                # I don't commit here; I commit after making sure the file is flushed and closed

                if do_fsync:
                    safe_flush_to_disk(
                        pack_handle,
                        Path(pack_handle.name).resolve(),
                        use_fullsync=True,
                    )

            # OK, if we are here, file was flushed, synced to disk and closed.
            # Let's commit then the information to the DB, so it's officially a
            # packed object. Note: committing as soon as we are done with one pack,
            # so if there's a problem with one pack we don't start operating on the next one
            # Note: because of the logic above, in theory this should not raise an IntegrityError!
            # For efficiency, you might want to set do_commit = False in the call, and then
            # call a `session.commit()` in the caller, as it is done for instance in `import_files()`.
            if do_commit:
                session.commit()

        if callback:
            # Final call to complete the bar
            if since_last_update:
                callback(action="update", value=since_last_update)
            # Perform any wrap-up, if needed
            callback(action="close", value=None)

        return hashkeys

    def add_objects_to_pack(  # pylint: disable=too-many-arguments
        self,
        content_list: list[bytes] | tuple[bytes, ...],
        compress: bool = False,
        no_holes: bool = False,
        no_holes_read_twice: bool = True,
        callback: Callable | None = None,
        do_fsync: bool = True,
        do_commit: bool = True,
    ) -> list[str]:
        """Add objects directly to a pack, reading from a list of content byte arrays.

        This is a maintenance operation, available mostly for efficiency reasons
        e.g. if you are creating a container from scratch.
        As such, it needs to be done only by one process.

        :note: use this only if you know the full list of contents fits in memory.
          Otherwise, call the add_streamed_objects_to_pack instead.

        :param content_list: a list of content bytestreams to add.
        :param compress: if True, compress objects before storing them.
        :param no_holes: if True, goes back and truncate the pack if the object that was just
            added already exists on the container. See comments in the docstring of ``add_streamed_objects_to_pack``.
        :param no_holes_read_twice: Read the objects and streams twice (and recompute the hash twice but avoid
            to write on disk and then overwrite with another object).
            See comments in the docstring of ``add_streamed_objects_to_pack``.
            This variable is ignored if `no_holes` is False.
        :param callback: a callback to monitor the progress, see docstring of `_validate_hashkeys_pack()`
        :param do_fsync: if True (default), call an fsync for every pack file, to ensure flushing to
            disk. See docstring of `add_streamed_objects_to_pack()` for further comments on the use of this flag.
        :param do_commit: if True (default), commit data to the DB after every pack is written.
            See docstring of `add_streamed_objects_to_pack()` for further comments on the use of this flag.

        :return: a list of object hash keys
        """
        stream_list: list[StreamSeekBytesType] = [
            io.BytesIO(content) for content in content_list
        ]
        return self.add_streamed_objects_to_pack(
            stream_list=stream_list,
            compress=compress,
            no_holes=no_holes,
            no_holes_read_twice=no_holes_read_twice,
            callback=callback,
            do_fsync=do_fsync,
            do_commit=do_commit,
        )

    def loosen_object(self, hashkey):
        """
        Takes a specific object and makes it also available in the loose directory.

        Return the path to the loose file.

        **Important note**: this function cannot guarantee that later code
        will find the loose object. If a concurrent packing/clean_storage
        operation is running, the loose object might be deleted.
        So it's the responsibility of the caller to check the file
        and possibly re-call this method to re-loosen it.

        This is used when reading a packed file that was compressed and is accessed with seek
        (especially when whence=1 or 2). Then, we just uncompress it fully in the loose folder.
        This will allow very efficient random access to the file, without the need to re-decompress
        the file at every seek (at a previous position than the current one).

        See also https://github.com/aiidateam/disk-objectstore/issues/136#issuecomment-1599337449
        for a discussion of why this is better than trying to keep a cache in memory of the
        decompresser at specific positions in the file, to reduce the amount of bytes to decompress.
        """
        # If the object already exists, I just return the path and
        # avoid to re-create it. As mentioned in the docstring, this is
        # OK as I'm not giving a guarantee that the file will be there later
        # (I cannot do it - even if I put more complex logic here, once the
        # function returns another concurrent clean_storage call could
        # remove the file.
        loose_path = self._get_loose_path_from_hashkey(hashkey)
        if loose_path.exists():
            return loose_path

        with self.get_object_stream(hashkey) as stream:
            # This always rewrites it as loose
            written_hashkey = self.add_streamed_object(stream)

        assert (
            written_hashkey == hashkey
        ), "Mismatch in the hashkey when rewriting an existing object as loose! {written_hashkey} vs {hashkey}"
        return self._get_loose_path_from_hashkey(hashkey)

    def _vacuum(self) -> None:
        """Perform a `VACUUM` operation on the SQLite operation.

        This is critical for two aspects:

        1. reclaiming unused space after many deletions
        2. reordering data on disk to make data access *much* more efficient

        (See also description in issue #94).
        """
        # VACUUM cannot be performed from within a transaction
        # see: https://github.com/sqlalchemy/sqlalchemy/discussions/6959
        session = self._get_cached_session()
        session.execute(text("COMMIT"))
        session.execute(text("VACUUM"))
        # ensure sqlalchemy knows to open a new transaction for the next execution
        session.commit()

    def clean_storage(  # pylint: disable=too-many-branches,too-many-locals
        self, vacuum: bool = False
    ) -> None:
        """Perform some clean-up of the container.

        .. note:: this is an operation that should be run only by one process at a given time! Don't call it twice.

        In particular:
        - if `vacuum` is True, it first VACUUMs the DB, reclaiming unused space and
          making access much faster
        - it removes duplicates if any, with some validation
        - it cleans up loose objects that are already in packs
        """
        # I start by VACUUMing the DB - this is something useful to do
        if vacuum:
            self._vacuum()

        all_duplicates = os.listdir(self._get_duplicates_folder())
        duplicates_mapping = defaultdict(list)

        for duplicate in all_duplicates:
            # I check only duplicates, but I don't delete files that start with a dot
            # (these might have been added by some process scanning the folders or something similar, like
            # .DS_Store on macOS)
            if "." in duplicate and not duplicate.startswith("."):
                reference_obj_hashkey = duplicate.partition(".")[0]
                duplicates_mapping[reference_obj_hashkey].append(duplicate)

        for reference_obj_hashkey in duplicates_mapping:
            try:
                with self.get_object_stream(reference_obj_hashkey) as stream:
                    computed_hash, _ = compute_hash_and_size(stream, self.hash_type)
            except NotExistent:
                # pylint: disable=raise-missing-from
                # The object is not in the repository. It has probably been deleted and for some
                # reason the duplicates have not been cleaned. I raise: this might have appened for instance
                # because two processes tried to write, the first locked, the second gave up and created a
                # duplicate, but then the first failed.
                # We don't implement it, but what should be done is to pick one of the duplicates, check that
                # the hash is correct, and put it in the right place as a loose object.
                raise InconsistentContent(
                    f"There is at least a duplicate for object '{reference_obj_hashkey}' "
                    "that however does not exist anymore. "
                    "If you don't need it, use `delete_objects()` passing this hash key to clean up the repository, "
                    "or attempt a manual recovery of the duplicate"
                )

            if computed_hash == reference_obj_hashkey:
                # The object is in the repo and has the correct hashkey: we just remove all duplicates
                for duplicate in duplicates_mapping[reference_obj_hashkey]:
                    os.remove(self._get_duplicates_folder() / duplicate)
            else:
                good_duplicate = None
                for duplicate in duplicates_mapping[reference_obj_hashkey]:
                    with open(
                        self._get_duplicates_folder() / duplicate, "rb"
                    ) as fhandle:
                        computed_hash, _ = compute_hash_and_size(
                            fhandle, self.hash_type
                        )
                    if computed_hash == reference_obj_hashkey:
                        # We found a duplicate that has the correct hash key: let's put it in place
                        good_duplicate = duplicate
                        break
                else:
                    # No valid duplicates found! I raise
                    raise InconsistentContent(
                        f"There are duplicates of '{reference_obj_hashkey}' but they are all corrupt"
                    )
                # If we are here, we found the "good duplicate"; let's put it in place
                # It should not be None, I should have raised!
                assert good_duplicate is not None
                os.replace(
                    self._get_duplicates_folder() / good_duplicate,
                    self._get_loose_path_from_hashkey(reference_obj_hashkey),
                )
                # Let's remove all other duplicates
                for duplicate in duplicates_mapping[reference_obj_hashkey]:
                    if duplicate == good_duplicate:
                        # Let's skip the one I already moved
                        continue
                    os.remove(self._get_duplicates_folder() / duplicate)

        loose_objects = set(self._list_loose())
        # Force reload of the session to get the most up-to-date packed objects
        self.close()

        session = self._get_cached_session()
        # I search now for all loose hash keys that exist also in the packs
        existing_packed_hashkeys = []
        if len(loose_objects) <= self._MAX_CHUNK_ITERATE_LENGTH:
            for chunk in chunk_iterator(loose_objects, size=self._IN_SQL_MAX_LENGTH):
                # I check the hash keys that are already in the pack
                stmt = select(Obj.hashkey).where(Obj.hashkey.in_(chunk))
                for row in session.execute(stmt):
                    existing_packed_hashkeys.append(row[0])
        else:
            sorted_hashkeys = sorted(loose_objects)
            pack_iterator = session.execute(
                text("SELECT hashkey FROM db_object ORDER BY hashkey")
            )

            # The query returns a tuple of length 1, so I still need a left_key
            for res, where in detect_where_sorted(
                pack_iterator, sorted_hashkeys, left_key=lambda x: x[0]
            ):
                if where == Location.BOTH:
                    existing_packed_hashkeys.append(res[0])

        # I now clean up loose objects that are already in the packs.
        # Here, we assume that if it's already packed, it's safe to assume it's uncorrupted.
        # If we want to do checks, they should be done here before deleting
        for obj_hashkey in existing_packed_hashkeys:
            try:
                os.remove(self._get_loose_path_from_hashkey(obj_hashkey))
            except PermissionError:
                # This can happen on Windows if one of the loose objects is still open.
                # I just ignore, I will remove it in a future call of this method.
                pass

    def import_objects(  # pylint: disable=too-many-locals,too-many-statements,too-many-branches,too-many-arguments
        self,
        hashkeys: Sequence[str],
        source_container: Container,
        compress: bool = False,
        target_memory_bytes: int = 104857600,
        callback: Callable | None = None,
        do_fsync: bool = True,
    ) -> dict[str, str]:
        """Imports the objects with the specified hashkeys into the container.

        :param hashkeys: an iterable of hash keys.
        :param source_container: another Container class containing the objects with the given hash keys.
        :param compress: specifies if content should be stored in compressed form.
        :param target_memory_bytes: how much data to store in RAM before actually storing in the container.
            Larger values allow to read and write in bulk that is more efficient, but of course require more memory.
            Note that actual memory usage will be larger (SQLite DB, storage of the hashkeys are not included - this
            only counts the RAM needed for the object content). Default: 100MB.
        :param callback: a callback to monitor the importing process. See docstring of `_validate_hashkeys_pack()`.
        :param do_fsync: whether to do a fsync on every pack object when it's written. True by default; set it
            to False for efficiency if this guarantee is not needed, e.g. if you are creating a new
            Container from scratch as a part of a larger import/export operation.

        :return: a mapping from the old hash keys (in the ``source_container``) to the new hash keys
            (in this container).
        """
        old_obj_hashkeys = []
        new_obj_hashkeys = []

        # We load data in this cache as long as the memory usage is < target_memory_bytes
        # We then flush in 'bulk' to the `other_container`, thus speeding up the process
        content_cache: dict[str, bytes] = {}
        cache_size = 0

        if source_container.hash_type == self.hash_type:
            # In this case, I can use some optimisation, because I can just work on the intersection
            # of the hash keys, since I can know in advnace which objects are already present.
            sorted_hashkeys = sorted(set(hashkeys))

            if callback:
                # If we have a callback, compute the total count of objects in this pack
                total = len(sorted_hashkeys)
                callback(
                    action="init",
                    value={"total": total, "description": "Listing objects"},
                )
                # Update at most 400 times, avoiding to increase CPU usage; if the list is small: every object.
                update_every = max(int(total / 1000), 1)
                # Counter of how many objects have been since since the last update.
                # A new callback will be performed when this value is > update_every.
                since_last_update = 0

            sorted_loose = sorted(self._list_loose())
            # This is a very efficient way to get a sorted iterator without preloading everything in memory
            # NOTE: this might be slow in the combination of these two cases:
            # 1. the pack index (SQLite DB) of this repository is not VACUUMed
            # AND
            # 2. the pack index (SQLite DB) is not in the OS disk cache
            # In this case, also the index on the hash key is scattered on disk and reading will be very slow,
            # see issue #94.
            # NOTE: I need to wrap in the `yield_first_element` iterator since it returns a list of lists
            sorted_packed = yield_first_element(
                self._get_cached_session().execute(
                    text("SELECT hashkey FROM db_object ORDER BY hashkey")
                )
            )
            sorted_existing = merge_sorted(sorted_loose, sorted_packed)

            # Hashkeys will be replaced with only those that are not yet in this repository (i.e., LEFTONLY)
            hashkeys = []
            for item, where in detect_where_sorted(sorted_hashkeys, sorted_existing):
                if callback and where in [Location.BOTH, Location.LEFTONLY]:
                    # It is in the sorted hash keys. Since this is the one for which I know the length efficiently,
                    # I use it for the progress bar. This will be relatively accurate for large lists of hash keys,
                    # but will not show a continuous bar if the list of hash keys to import is much shorter than
                    # the list of hash keys in this (destination) container. This is probably OK, though.
                    since_last_update += 1
                    if since_last_update >= update_every:
                        callback(action="update", value=since_last_update)
                        since_last_update = 0

                if where == Location.LEFTONLY:
                    hashkeys.append(item)

            if callback:
                # Final call to complete the bar
                if since_last_update:
                    callback(action="update", value=since_last_update)
                # Perform any wrap-up, if needed
                callback(action="close", value=None)

            # I just insert the new objects without first checking that I am not leaving holes in the pack files,
            # as I already checked here.
            no_holes = False
            no_holes_read_twice = False
        else:
            # hash types are different: I have to add all objects that were provided as I have no way to check
            # if they already exist
            no_holes = True
            no_holes_read_twice = True

        if callback:
            # If we have a callback, compute the total count of objects in this pack
            total = len(hashkeys)
            callback(
                action="init", value={"total": total, "description": "Copy objects"}
            )
            # Update at most 400 times, avoiding to increase CPU usage; if the list is small: every object.
            update_every = max(int(total / 1000), 1)
            # Counter of how many objects have been since since the last update.
            # A new callback will be performed when this value is > update_every.
            since_last_update = 0

        with source_container.get_objects_stream_and_meta(hashkeys) as triplets:
            for old_obj_hashkey, stream, meta in triplets:
                # If we are here, these are not None - I check, this is also
                # useful to help mypy check the types
                assert stream is not None
                assert meta.size is not None
                if meta.size > target_memory_bytes:
                    # If the object itself is too big, just write it directly
                    # via streams, bypassing completely the cache. I don't touch the cache in this case,
                    # maybe it's still almost empty.
                    old_obj_hashkeys.append(old_obj_hashkey)
                    # I put this object to the pack, in streamed form, and I store the hash key
                    # I accept the performance hit of reading twice (possibly uncompressing from the source)
                    # but I avoid to write a huge object to disk when it's not needed because already available
                    # on the destination
                    new_obj_hashkeys.append(
                        self.add_streamed_object_to_pack(
                            stream,
                            compress=compress,
                            no_holes=no_holes,
                            no_holes_read_twice=no_holes_read_twice,
                            do_fsync=do_fsync,
                            do_commit=False,  # I will do a final commit
                        )
                    )
                elif cache_size + meta.size > target_memory_bytes:
                    # I were to read the content, I would be filling too much memory - I flush the cache first,
                    # and transfer the data, before acting on this object.

                    # I just flush the cache if it's not empty (zip would fail in this case)
                    # This should always be True if we are here, but I do it just in case
                    if content_cache:
                        # I create a list of hash keys and the corresponding content
                        temp_old_hashkeys, data = zip(*content_cache.items())

                        # I put all of them in bulk
                        # I accept the performance hit of reading twice if the hash type is different
                        # (especially since it's already on memory)
                        temp_new_hashkeys = self.add_objects_to_pack(
                            data,
                            compress=compress,
                            no_holes=no_holes,
                            no_holes_read_twice=no_holes_read_twice,
                            do_fsync=do_fsync,
                            do_commit=False,
                        )

                        # I update the list of known old (this container) and new (other_container) hash keys
                        old_obj_hashkeys += temp_old_hashkeys
                        new_obj_hashkeys += temp_new_hashkeys

                        # Flush the content of the cache
                        content_cache = {}
                        cache_size = 0

                    # I add this to the cache for the next round (I know it's going to fit in the memory,
                    # otherwise I would have processed it directly, bypassing the cache).
                    content_cache[old_obj_hashkey] = stream.read()
                    # I update the cache size
                    cache_size += meta.size
                else:
                    # I can add this object to the memory cache, it is not too big.
                    # I store it as a BytesIO so it still provides the stream methods like `.read`.
                    # Key old hash key (in this repo); value: the stream
                    content_cache[old_obj_hashkey] = stream.read()
                    # I update the cache size
                    cache_size += meta.size

                if callback:
                    since_last_update += 1
                    if since_last_update >= update_every:
                        callback(action="update", value=since_last_update)
                        since_last_update = 0

        if callback:
            # Final call to complete the bar
            if since_last_update:
                callback(action="update", value=since_last_update)
            # Perform any wrap-up, if needed
            callback(action="close", value=None)

        # The for loop is finished. I can also go out of the `with` context manager because whatever is in the
        # cache is in memory. Most probably I still have content in the cache, just flush it,
        # with the same logic as above.

        # I just flush the cache if it's not empty (zip would fail in this case)
        if content_cache:
            # I create a list of hash keys and the corresponding content
            temp_old_hashkeys, data = zip(*content_cache.items())
            # I put all of them in bulk

            temp_new_hashkeys = self.add_objects_to_pack(
                data,
                compress=compress,
                no_holes=no_holes,
                no_holes_read_twice=no_holes_read_twice,
                callback=rename_callback(callback, new_description="Final flush"),
                do_fsync=do_fsync,
                # I will commit at the end
                do_commit=False,
            )

            # I update the list of known old (this container) and new (other_container) hash keys
            old_obj_hashkeys += temp_old_hashkeys
            new_obj_hashkeys += temp_new_hashkeys

        # Create a mapping from the old to the new hash keys: old_new_obj_hashkey_mapping[old_hashkey] = new_hashkey
        old_new_obj_hashkey_mapping = dict(zip(old_obj_hashkeys, new_obj_hashkeys))

        # Since I called the `add_objects_to_pack` without committing (gives a boost for performance),
        # I need now to commit to save what I've been doing.
        self._get_cached_session().commit()

        return old_new_obj_hashkey_mapping

    # Let us also compute the hash
    def _validate_hashkeys_pack(  # pylint: disable=too-many-locals
        self, pack_id: int, callback: Callable | None = None
    ) -> dict[str, list[str | Any] | list[Any]]:
        """Validate all hashkeys and returns a dictionary of problematic entries.

        The keys are the problem type, the values are a list of hashkeys of problematic objects.
        Currently implemented problems:

        - ``invalid_hashes_packed``: the (re)computed hash does not match the hash key
        - ``invalid_sizes_packed``: the (re)computed size does not match the object size (this can happen for
          compressed objects)
        - ``overlapping_packed``: packed object have some
          overlap

        Note that the same hash key can appear in multiple lists.

        The correct, future-proof way to check if there is any error is:

          retdict = _validate_hashkeys_pack(...)
          has_error = any(retdict.values())

        Note however that, as an user, you should *not* do this.
        This is an internal function that returns
        a dictionary. But when called internally from `validate()`, then
        `validate()` will convert the results (enriched with the results)
        from loose objects into a `ValidationIssues` dataclass.
        In that case, you can just call the `is_valid()` method of the `ValidationIssues` dataclass.

        :param pack_id: the pack ID to check
        :param callback: a callback to be called at every iteration of an object. This is useful to show e.g. a
            progress bar.
            This callback shold have the following signature: ``def callback(action, value)``.
            The call back is called:
            - at the very beginning, with ``action=='init'`` and value being a dictionary with the following keys:
              ``total``, with the total number of objects that the function will loop on, and ``description`` with a
              human-readable description with the current pack number.
            - after every object has been processed, with ``action=='update'`` and value equal to the number of
              newly processed entries since the last call.
            - at the end, with ``action=='close'`` and value equal to ``None``.

        Here is a minimal example of progress bar using the ``tqdm`` library:

            class CallbackTqdm:
                def __init__(self):
                    self.progress_bar = None

                def callback(self, action, value):
                    import tqdm

                    if action == 'init':
                        if self.progress_bar is not None:
                            self.progress_bar.close()
                        self.progress_bar = tqdm.tqdm(total=value['total'], desc=value['description'])
                    elif action == 'update':
                        if value is None:
                            value = 1
                        self.progress_bar.update(n=value)
                    elif action == 'close':
                        self.progress_bar.close()
                        self.progress_bar = None

            callback_tqdm = CallbackTqdm()
            container.validate(callback=callback_tqdm.callback)
        """
        # pylint: disable=too-many-locals
        # Will contain hashkeys of invalid objects
        invalid_hashes = []
        invalid_sizes = []
        overlapping = []

        session = self._get_cached_session()

        if callback:
            # If we have a callback, compute the total count of objects in this pack
            total = session.scalar(
                select(func.count()).select_from(Obj).where(Obj.pack_id == pack_id)
            )
            callback(
                action="init",
                value={"total": total, "description": f"Pack {pack_id}"},
            )
            # Update at most 400 times, avoiding to increase CPU usage; if the list is small: every object.
            update_every = max(int(total / 400), 1)
            # Counter of how many objects have been since since the last update.
            # A new callback will be performed when this value is > update_every.
            since_last_update = 0

        # Open the pack only once, read it in order
        pack_path = self._get_pack_path_from_pack_id(str(pack_id))
        current_pos = 0
        with open(pack_path, mode="rb") as pack_handle:
            stmt = (
                select(Obj.hashkey, Obj.size, Obj.offset, Obj.length, Obj.compressed)
                .where(Obj.pack_id == pack_id)
                .order_by(Obj.offset)
            )
            for hashkey, size, offset, length, compressed in session.execute(stmt):
                obj_reader: StreamSeekBytesType = PackedObjectReader(
                    fhandle=pack_handle, offset=offset, length=length
                )
                if compressed:
                    # I don't pass a LazyLooseStream: in the validate
                    # I should only ever read linearly, so it should not be needed
                    # to have the possibility to get a loose uncompressed version
                    # of the object.
                    obj_reader = self._get_stream_decompresser()(obj_reader)

                computed_hash, computed_size = compute_hash_and_size(
                    obj_reader, self.hash_type
                )

                # Check object correctness
                if computed_hash != hashkey:
                    invalid_hashes.append(hashkey)
                if computed_size != size:
                    invalid_sizes.append(hashkey)

                # Check that there are no overlapping objects
                if offset < current_pos:
                    overlapping.append(hashkey)
                current_pos = offset + length

                if callback:
                    since_last_update += 1
                    if since_last_update >= update_every:
                        callback(action="update", value=since_last_update)
                        since_last_update = 0

        if callback:
            # Final call to complete the bar
            if since_last_update:
                callback(action="update", value=since_last_update)
            # Perform any wrap-up, if needed
            callback(action="close", value=None)

        return {
            "invalid_hashes_packed": invalid_hashes,
            "invalid_sizes_packed": invalid_sizes,
            "overlapping_packed": overlapping,
        }

    def validate(self, callback: Callable | None = None) -> ValidationIssues:
        """Perform a number of validations on the container content, to make sure it is not corrupt.

        The callback can be used to show a progress bar (see e.g. its use in the `validate` command of
        the `dostore` command-line interface).

        Return a `ValidationIssues` dataclass.
        You can call the `is_valid()` method of the returned `ValidationIssues`
        dataclass to check if there are errors, or check all fields if you
        prefer and see if all fields are empty lists (which means no error).
        """
        all_errors: dict[str, list[str]] = {
            field.name: [] for field in dataclasses.fields(ValidationIssues)
        }

        all_loose = set(self._list_loose())

        if callback:
            callback(
                action="init",
                value={"total": len(all_loose), "description": "Loose objects"},
            )

        for hashkey in all_loose:
            with open(self._get_loose_path_from_hashkey(hashkey), "rb") as fhandle:
                computed_hash, _ = compute_hash_and_size(fhandle, self.hash_type)
                if computed_hash != hashkey:
                    all_errors["invalid_hashes_loose"].append(hashkey)
                if callback:
                    # Update for each object
                    callback(action="update", value=1)
        if callback:
            callback(action="close", value=None)

        session = self._get_cached_session()

        all_pack_ids = sorted(
            {res[0] for res in session.execute(select(Obj.pack_id).distinct())}
        )

        for pack_id in all_pack_ids:
            pack_errors = self._validate_hashkeys_pack(
                pack_id=pack_id, callback=callback
            )
            for error_type, problematic_objects in pack_errors.items():
                all_errors[error_type] += problematic_objects

        return ValidationIssues(**dict(all_errors))

    def delete_objects(self, hashkeys: list[str]) -> list[str | Any]:
        """Delete the selected objects.

        .. note:: In the current version, this has to be considered a maintenance operation, and as such it should
           be executed when *no process is accessing the repository*.

           If processes are accessing in parallel, a few race conditions might happen:

           - The delete might fail because the loose object is open or reading the object might fail with
             a PermissionError because the object is being deleted (on Windows)
           - On MacOS, there is an unexpected race condition for which when reading the object during concurrent delete,
             one gets an empty handle instead of either FileNotFoundError or the actual content (even if this seems
             not to be the case anymore with recent, post-2021 Apple filesystems)
           - Routines might get the list of files before performing operations, and the objects might disappear in the
             meantime
           - Write access to packs is not possible as the DB will be locked (e.g. writing directly to packs, or
             packing loose objects).

          For this reason, we stop at the first error (a subset of the objects requested might have been deleted), i.e.
          the delete operation is not atomic or transacted.

        .. note:: If an object is both loose and packed, this is a valid condition. For this reason, when deleting,
           we first remove it from loose objects - if the object is also packed, this is a no-op from the point of
           view of the container. Only then we delete the packed versions. If we did the opposite, we would have
           situations, e.g. in failures, where objects go back from packed to loose.
           In addition, however, especially on Windows we might have created some duplicates in the duplicates folder.
           I will delete those, if they exist, as the first thing.

        .. note:: Deletion of loose objects is done by directly removing the objects.
           Deletion of packed objects is a 'soft' delete, meaning that the entry is just removed from the SQLite DB,
           but the data will still occupy data on disk.
           One needs to do a full repack to recover disk space.

        :param hashkeys: hashkeys to be deleted
        :return: a list of hashkeys that were actually deleted (might be shorted if non-existing hashkeys were asked)
        """
        deleted_loose = set()
        deleted_packed = set()

        all_duplicates = os.listdir(self._get_duplicates_folder())

        for hashkey in hashkeys:
            # Filter only duplicates of this object and delete them
            duplicates_this_object = [
                duplicate_fname
                for duplicate_fname in all_duplicates
                if duplicate_fname.startswith(f"{hashkey}.")
            ]
            for duplicate_fname in duplicates_this_object:
                # For now I don't put checks - I should be the only one accessing the container, so I should not
                # get PermissionError or similar exceptionss
                os.remove(self._get_duplicates_folder() / duplicate_fname)
            try:
                os.remove(self._get_loose_path_from_hashkey(hashkey))
                deleted_loose.add(hashkey)
            except FileNotFoundError:
                # No loose object: it's OK
                pass

        session = self._get_cached_session()

        # Operate in chunks, due to the SQLite limits
        # (see comment above the definition of self._IN_SQL_MAX_LENGTH)
        for chunk in chunk_iterator(hashkeys, size=self._IN_SQL_MAX_LENGTH):
            results = session.execute(select(Obj.hashkey).where(Obj.hashkey.in_(chunk)))
            deleted_this_chunk = [res[0] for res in results]
            # I need to specify either `False` or `'fetch'`
            # otherwise one gets 'sqlalchemy.exc.InvalidRequestError: Could not evaluate current criteria in Python'
            # `'fetch'` will run the query twice so it's less efficient
            # False is beter but one needs to either `expire_all` at the end, or commit.
            # I will commit at the end.
            stmt = (
                delete(Obj)
                .where(Obj.hashkey.in_(chunk))
                .execution_options(synchronize_session=False)
            )
            session.execute(stmt)
            deleted_packed.update(deleted_this_chunk)

        session.commit()

        # If no error occurred, then the union is the list of all objects deleted.
        # Note: in the future, if we allow partial deletion, if an object was deleted from loose but there was
        # an error while deleting the packed version of an object (even if the loose version of the same object
        # was deleted) should be considered as if the object has *not* been deleted
        return list(deleted_loose.union(deleted_packed))

    def repack(
        self,
        compress_mode: CompressMode = CompressMode.KEEP,
        callback: None
        | (Callable[[Arg(str, "action"), Arg(Any, "value")], None]) = None,
    ) -> None:
        """Perform a repack of all packed objects.

        At the end, it also VACUUMs the DB to reclaim unused space and make
        access more efficient.

        This is a maintenance operation.

        :param compress_mode: see docstring of ``repack_pack``.
        :param callback: a callback function that can be used to report progress.
            The callback function should accept two arguments: a string with the action being performed
            and the value of the action. The action can be "init" (initialization),
            "update" (update of the progress), or "close" (finalization).
            In case of "init", the value is a dictionary with the key "total" as the total size of the operation
            and key "description" as the label of the operation.
            In case of "update", the value is amount of the operation that has been completed.
            In case of "close", the value is None.
            return value of the callback function is ignored.
        """
        for pack_id in self._list_packs():
            self.repack_pack(pack_id, compress_mode=compress_mode, callback=callback)
        self._vacuum()

    def repack_pack(  # pylint: disable=too-many-branches,too-many-statements,too-many-locals
        self,
        pack_id: str,
        compress_mode: CompressMode = CompressMode.KEEP,
        callback: None
        | (Callable[[Arg(str, "action"), Arg(Any, "value")], None]) = None,
    ) -> None:
        """Perform a repack of a given pack object.

        This is a maintenance operation.

        :param compress_mode: must be a valid CompressMode enum type.
            Currently, the only implemented mode is KEEP, meaning that it
            preserves the same compression (this means that repacking is *much* faster
            as it can simply transfer the bytes without decompressing everything first,
            and recompressing it back again).
        :param callback: a callback function that can be used to report progress.
            The callback function should accept two arguments: a string with the action being performed
            and the value of the action. The action can be "init" (initialization),
            "update" (update of the progress), or "close" (finalization).
            In case of "init", the value is a dictionary with the key "total" as the total size of the operation
            and key "description" as the label of the operation.
            In case of "update", the value is amount of the operation that has been completed.
            In case of "close", the value is None.
            return value of the callback function is ignored.
        """
        assert (
            pack_id != self._REPACK_PACK_ID
        ), f"The specified pack_id '{pack_id}' is invalid, it is the one used for repacking"

        # Check that it does not exist
        assert not self._get_pack_path_from_pack_id(
            self._REPACK_PACK_ID, allow_repack_pack=True
        ).exists(), f"The repack pack '{self._REPACK_PACK_ID}' already exists, probably a previous repacking aborted?"

        session = self._get_cached_session()

        one_object_in_pack = session.execute(
            select(Obj.id).where(Obj.pack_id == pack_id).limit(1)
        ).all()
        if not one_object_in_pack:
            # No objects. Clean up the pack file, if it exists.
            if self._get_pack_path_from_pack_id(pack_id).exists():
                os.remove(self._get_pack_path_from_pack_id(pack_id))
            return

        obj_dicts = []
        # At least one object. Let's repack. We have checked before that the
        # REPACK_PACK_ID did not exist.
        if callback:
            callback(
                action="init",
                value={
                    "total": self.get_total_size()["total_size_packed"],
                    "description": f"Repack {pack_id}",
                },
            )
        with self.lock_pack(
            str(self._REPACK_PACK_ID), allow_repack_pack=True
        ) as write_pack_handle:
            with open(self._get_pack_path_from_pack_id(pack_id), "rb") as read_pack:
                stmt = (
                    select(
                        Obj.id,
                        Obj.hashkey,
                        Obj.size,
                        Obj.offset,
                        Obj.length,
                        Obj.compressed,
                    )
                    .where(Obj.pack_id == pack_id)
                    .order_by(Obj.offset)
                )
                for (
                    rowid,
                    hashkey,
                    size,
                    offset,
                    length,
                    source_compressed,
                ) in session.execute(stmt):
                    # This is the read handle of the bytes in the pack - it might be
                    read_handle: (
                        PackedObjectReader | ZlibStreamDecompresser
                    ) = PackedObjectReader(read_pack, offset, length)

                    # Determine if I should compress or not the destination - this function will
                    # try to do it in a cheap way (e.g. if the source is already compressed, will just
                    # use the information to decide; only if the source is uncompressed and
                    # the compress_mode is AUTO, it will need to read (part of) the stream to decide if
                    # it's worth compressing or not.
                    dest_compressed = should_compress(
                        source_stream=read_handle,
                        compress_mode=compress_mode,
                        source_compressed=source_compressed,
                        source_length=length,
                        source_size=size,
                    )

                    # Prepare the object for the new entry in the repack-pack
                    obj_dict = {}
                    obj_dict["id"] = rowid
                    # no need to rehash, it's the same object, and we are in the same container, so we are
                    # using the same hashing algorithm
                    obj_dict["hashkey"] = hashkey
                    obj_dict["pack_id"] = self._REPACK_PACK_ID
                    # The uncompressed size is the same
                    obj_dict["size"] = size
                    obj_dict["compressed"] = dest_compressed
                    obj_dict["offset"] = write_pack_handle.tell()

                    if source_compressed == dest_compressed:
                        # In this branch, we can just transfer the bytes, as we are using the *same* compression
                        # method in the source and destionation

                        # Transfer data in chunks.
                        # No need to rehash - it's the same container so the same hash.
                        # Not checking the compression on source or destination - we are assuming
                        # for now that the mode is KEEP.
                        while True:
                            chunk = read_handle.read(self._CHUNKSIZE)
                            if chunk == b"":
                                # Returns an empty bytes object on EOF.
                                break
                            write_pack_handle.write(chunk)
                    else:
                        # The compression mode is different: then, I have to properly take into account compression
                        # in the source and in the destination.
                        if source_compressed:
                            read_handle = self._get_stream_decompresser()(read_handle)
                        if dest_compressed:
                            compressobj = self._get_compressobj_instance()
                            while True:
                                chunk = read_handle.read(self._CHUNKSIZE)
                                if chunk == b"":
                                    # Returns an empty bytes object on EOF.
                                    break
                                write_pack_handle.write(compressobj.compress(chunk))
                            # Write the remaining of the file, if any leftovers are still present in the
                            # compressobj
                            write_pack_handle.write(compressobj.flush())
                        else:
                            while True:
                                chunk = read_handle.read(self._CHUNKSIZE)
                                if chunk == b"":
                                    # Returns an empty bytes object on EOF.
                                    break
                                write_pack_handle.write(chunk)

                    # Set correctly the length on disk
                    obj_dict["length"] = write_pack_handle.tell() - obj_dict["offset"]
                    # Appending for later bulk commit
                    # I will assume that all objects of a single pack fit in memory
                    obj_dicts.append(obj_dict)
                    if callback:
                        callback(action="update", value=obj_dict["size"])
            # safe flush to disk seems to be a time consuming operation, but no easy way to include in the progress bar
            safe_flush_to_disk(
                write_pack_handle,
                self._get_pack_path_from_pack_id(
                    self._REPACK_PACK_ID, allow_repack_pack=True
                ),
            )
        if callback:
            callback(action="close", value=None)
        # We are done with data transfer.
        # At this stage we just have a new pack -1 (_REPACK_PACK_ID) but it is never referenced.
        # Let us store the information in the DB.
        # We had already checked earlier that this at least one exists.
        session.bulk_update_mappings(Obj, obj_dicts)
        # I also commit.
        session.commit()
        # Clean up the cache
        obj_dicts = []

        # Now we can safely delete the old object. I just check that there is no object still
        # refencing the old pack, to be sure.
        one_object_in_pack = session.execute(
            select(Obj.id).where(Obj.pack_id == pack_id).limit(1)
        ).all()
        assert not one_object_in_pack, (
            f"I moved the objects of pack '{pack_id}' to pack '{self._REPACK_PACK_ID}' "
            f"but there are still references to pack '{pack_id}'!"
        )
        os.remove(self._get_pack_path_from_pack_id(pack_id))

        # I need now to move the file back. I need to be careful, to avoid conditions in which
        # I remain with inconsistent data.
        # Since hard links seem to be supported on all three platforms, I do a hard link
        # of -1 back to the correct pack ID.
        os.link(
            self._get_pack_path_from_pack_id(
                self._REPACK_PACK_ID, allow_repack_pack=True
            ),
            self._get_pack_path_from_pack_id(pack_id),
        )

        # Before deleting the source (pack -1) I need now to update again all
        # entries to point to the correct pack id
        session.execute(
            update(Obj)
            .where(Obj.pack_id == self._REPACK_PACK_ID)
            .values(pack_id=pack_id)
        )
        session.commit()

        # Technically, to be crash safe, before deleting I should also fsync the folder
        # I am not doing this for now
        # I now can unlink/delete the original source
        os.unlink(
            self._get_pack_path_from_pack_id(
                self._REPACK_PACK_ID, allow_repack_pack=True
            )
        )

        # We are now done. The temporary pack is gone, and the old `pack_id`
        # has now been replaced with an udpated, repacked pack.
