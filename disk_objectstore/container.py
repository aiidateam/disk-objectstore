"""
The main implementation of the ``Container`` class of the object store.
"""
# pylint: disable=too-many-lines
import io
import json
import os
import shutil
import zlib

from collections import defaultdict, namedtuple
from contextlib import contextmanager
from sqlalchemy import create_engine, event

from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker

from .models import Base, Obj
from .utils import (
    ObjectWriter, PackedObjectReader, StreamDecompresser, chunk_iterator, is_known_hash, nullcontext,
    safe_flush_to_disk, get_hash
)
from .exceptions import NotExistent, NotInitialised, InconsistentContent

ObjQueryResults = namedtuple('ObjQueryResults', ['hashkey', 'offset', 'length', 'compressed', 'size'])


class Container:  # pylint: disable=too-many-public-methods
    """A class representing a container of objects (which is stored on a disk folder)"""

    _PACK_INDEX_SUFFIX = '.idx'
    # Default compression level (when compression is requested)
    # This is the lowest one, to get some reasonable compression without too much CPU time required
    _COMPRESSLEVEL = 1
    # Size in bytes of each of the chunks used when (internally) reading or writing in chunks, e.g.
    # when packing.
    _CHUNKSIZE = 65536

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

    def __init__(self, folder):
        """Create the class that represents the container.

        :param folder: the path to a folder that will host this object-store container.
        """
        self._folder = os.path.realpath(folder)
        self._session = None  # Will be populated by the _get_session function
        # These act as caches and will be populated by the corresponding properties
        self._loose_prefix_len = None
        self._pack_size_target = None
        self._current_pack_id = None
        self._hash_type = None

    def get_folder(self):
        """Return the path to the folder that will host the object-store container."""
        return self._folder

    def close(self):
        """Close open files (in particular, the connection to the SQLite DB)."""
        if self._session is not None:
            self._session.close()
            self._session = None

    def _get_sandbox_folder(self):
        """Return the path to the sandbox folder that is used during a new object creation.

        It is a subfolder of the container folder.
        """
        return os.path.join(self._folder, 'sandbox')

    def _get_loose_folder(self):
        """Return the path to the folder that will host the loose objects.

        It is a subfolder of the container folder.
        """
        return os.path.join(self._folder, 'loose')

    def _get_pack_folder(self):
        """Return the path to the folder that will host the packed objects.

        It is a subfolder of the container folder.
        """
        return os.path.join(self._folder, 'packs')

    def _get_duplicates_folder(self):
        """Return the path to the folder that will host the duplicate loose objects that couldn't be written.

        This should happen only in race conditions on Windows. See `utils.ObjectWriter.__exit__` for its usage, and
        `utils._store_duplicate_copy`.

        It is a subfolder of the container folder.
        """
        return os.path.join(self._folder, 'duplicates')

    def _get_config_file(self):
        """Return the path to the container config file."""
        return os.path.join(self._folder, 'config.json')

    def _get_session(self, create=False, raise_if_missing=False):
        """Return a new session to connect to the pack-index SQLite DB.

        :param create: if True, creates the sqlite file and schema.
        :param raise_if_missing: ignored if create==True. If create==False, and the index file
           is missing, either raise an exception (FileNotFoundError) if this flag is True, or return None
        """
        if not create and not os.path.exists(self._get_pack_index_path()):
            if raise_if_missing:
                raise FileNotFoundError('Pack index does not exist')
            return None

        engine = create_engine('sqlite:///{}'.format(self._get_pack_index_path()))

        # For the next two bindings, see background on
        # https://docs.sqlalchemy.org/en/13/dialects/sqlite.html#serializable-isolation-savepoints-transactional-ddl
        @event.listens_for(engine, 'connect')
        def do_connect(dbapi_connection, connection_record):  # pylint: disable=unused-argument,unused-variable
            """Hook function that is called upon connection.

            It modifies the default behavior of SQLite to use WAL and to
            go back to the 'default' isolation level mode.
            """
            # disable pysqlite's emitting of the BEGIN statement entirely.
            # also stops it from emitting COMMIT before any DDL.
            dbapi_connection.isolation_level = None
            # Open the file in WAL mode (see e.g. https://stackoverflow.com/questions/9671490)
            # This allows to have as many readers as one wants, and a concurrent writer (up to one)
            # Note that this writes on a journal, on a different packs.idx-wal,
            # and also creates a packs.idx-shm file.
            # Note also that when the session is created, you will keep reading from the same version,
            # so you need to close and reload the session to see the newly written data.
            # Docs on WAL: https://www.sqlite.org/wal.html
            cursor = dbapi_connection.cursor()
            cursor.execute('PRAGMA journal_mode=wal;')
            cursor.close()

        # For this binding, see background on
        # https://docs.sqlalchemy.org/en/13/dialects/sqlite.html#serializable-isolation-savepoints-transactional-ddl
        @event.listens_for(engine, 'begin')
        def do_begin(conn):  # pylint: disable=unused-variable
            # emit our own BEGIN
            conn.execute('BEGIN')

        if create:
            # Create all tables in the engine. This is equivalent to "Create Table"
            # statements in raw SQL.
            Base.metadata.create_all(engine)

        # Bind the engine to the metadata of the Base class so that the
        # declaratives can be accessed through a DBSession instance
        Base.metadata.bind = engine

        # We set autoflush = False to avoid to lock the DB if just doing queries/reads
        DBSession = sessionmaker(  # pylint: disable=invalid-name
            bind=engine, autoflush=False, autocommit=False
        )
        session = DBSession()

        return session

    def _get_cached_session(self):
        """Return the SQLAlchemy session to access the SQLite file,
        reusing the same one."""
        # We want to catch both if it's missing, and if it's None
        # the latter means that in the previous run the pack file was missing
        # but maybe by now it has been created!
        if self._session is None:
            self._session = self._get_session(create=False, raise_if_missing=True)
        return self._session

    def _get_loose_path_from_hashkey(self, hashkey):
        """Return the path of a loose object on disk containing the data of a given hash key.

        :param hashkey: the hashkey of the object to get.
        """
        if self.loose_prefix_len:
            return os.path.join(
                self._get_loose_folder(),
                hashkey[:self.loose_prefix_len],
                hashkey[self.loose_prefix_len:],
            )
        # if loose_prefix_len is zero, there is no subfolder
        return os.path.join(self._get_loose_folder(), hashkey)

    def _get_pack_path_from_pack_id(self, pack_id):
        """Return the path of the pack file on disk for the given pack ID.

        :param pack_id: the pack ID.
        """
        pack_id = str(pack_id)
        assert self._is_valid_pack_id(pack_id), 'Invalid pack ID {}'.format(pack_id)
        return os.path.join(self._get_pack_folder(), pack_id)

    def _get_pack_index_path(self):
        """Return the path to the SQLite file containing the index of packed objects.
        """
        return os.path.join(self._folder, 'packs{}'.format(self._PACK_INDEX_SUFFIX))

    def _get_pack_id_to_write_to(self):
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
            if not os.path.exists(pack_path):
                # Use this ID - the pack file does not exist yet
                break
            if os.path.getsize(pack_path) < self.pack_size_target:
                # Use this ID - the pack file is not "full" yet
                break
            # Try the next pack
            pack_id += 1

        # Cache the value
        self._current_pack_id = pack_id
        return pack_id

    @property
    def is_initialised(self):
        """Return True if the container is already initialised."""
        # If the config file does not exist, the container is not initialised
        try:
            with open(self._get_config_file()) as fhandle:
                json.load(fhandle)
        except (ValueError, OSError, IOError):
            return False
        # I also check that the four sub-folders exist
        subfolders = [
            self._get_pack_folder(),
            self._get_loose_folder(),
            self._get_duplicates_folder(),
            self._get_sandbox_folder()
        ]
        for folder in subfolders:
            if not os.path.exists(folder):
                return False
        return True

    def init_container(  # pylint: disable=bad-continuation
        self, clear=False, pack_size_target=4 * 1024 * 1024 * 1024, loose_prefix_len=2, hash_type='sha256'
    ):
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
        """
        if loose_prefix_len < 0:
            raise ValueError('The loose prefix length can only be zero or a positive integer')
        if pack_size_target <= 0:
            raise ValueError('The pack size target can only be a non-zero positive integer')
        if not is_known_hash(hash_type):
            raise ValueError('Unknown hash type "{}"'.format(hash_type))

        if clear:
            if os.path.exists(self._folder):
                shutil.rmtree(self._folder)

        if self.is_initialised:
            raise FileExistsError(
                'The container already exists, so you cannot initialise it - '
                'use the clear option if you want to overwrite with a clean one'
            )

        try:
            os.makedirs(self._folder)
        except FileExistsError:
            # The directory already exists: it's ok
            pass

        if os.listdir(self._folder):
            raise FileExistsError(
                'There is already some file or folder in the Container folder, I cannot initialise it!'
            )

        # Create config file
        with open(self._get_config_file(), 'w') as fhandle:
            json.dump(
                {
                    'container_version': 1,  # For future compatibility, this is the version of the format
                    'loose_prefix_len': loose_prefix_len,
                    'pack_size_target': pack_size_target,
                    'hash_type': hash_type
                },
                fhandle
            )

        for folder in [
            self._get_pack_folder(),
            self._get_loose_folder(),
            self._get_duplicates_folder(),
            self._get_sandbox_folder()
        ]:
            os.makedirs(folder)

        self._get_session(create=True)

    def _get_repository_config(self):
        """Return the repository config."""
        if not self.is_initialised:
            raise NotInitialised('The container is not initialised yet - use .init_container() first')
        with open(self._get_config_file()) as fhandle:
            config = json.load(fhandle)
        return config

    @property
    def loose_prefix_len(self):
        """Return the length of the prefix of loose objects, when sharding.

        This is read from the repository configuration.
        """
        if self._loose_prefix_len is None:
            self._loose_prefix_len = self._get_repository_config()['loose_prefix_len']
        return self._loose_prefix_len

    @property
    def pack_size_target(self):
        """Return the length of the pack name, when sharding.

        This is read from the repository configuration.
        """
        if self._pack_size_target is None:
            self._pack_size_target = self._get_repository_config()['pack_size_target']
        return self._pack_size_target

    @property
    def hash_type(self):
        """Return the length of the prefix of loose objects, when sharding.

        This is read from the repository configuration.
        """
        if self._hash_type is None:
            self._hash_type = self._get_repository_config()['hash_type']
        return self._hash_type

    def get_object_content(self, hashkey):
        """Get the content of an object with a given hash key.

        :param hashkey: The hash key of the object to retrieve.
        :return: a byte stream with the object content.
        """
        with self.get_object_stream(hashkey) as handle:
            return handle.read()

    @contextmanager
    def get_object_stream(self, hashkey):
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
    def get_object_stream_and_meta(self, hashkey):
        """Return a context manager yielding a stream to get the content of an object, and a metadata dictionary.

        To be used as a context manager::

          with container.get_object_stream(hashkey) as (fhandle, meta):
              data = fhandle.read()
              assert len(data) == meta['size']

        The returned file-handle object supports *at least* the read() method that
        accepts an optional parameter to read the file in chunks, and might
        not be seekable.
        The schema of the returned metadata `meta` dict is documented in the docstring
        of `get_objects_stream_and_meta`).

        :param hashkey: the hashkey of the object to stream.
        """
        with self.get_objects_stream_and_meta(hashkeys=[hashkey], skip_if_missing=False) as triplets:
            counter = 0
            for obj_hashkey, stream, meta in triplets:
                counter += 1
                assert counter == 1, 'There is more than one item returned by get_objects_stream_and_meta'
                assert obj_hashkey == hashkey

                if stream is None:
                    raise NotExistent('No object with hash key {}'.format(hashkey))

                yield stream, meta

    def _get_objects_stream_meta_generator(  # pylint: disable=too-many-branches,too-many-statements,too-many-locals
            self, hashkeys, skip_if_missing, with_streams
        ):
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
        :param with_streams: if False, yield pairs (hashkey, meta) and avoid to open any file.
        """
        # pylint: disable=too-many-nested-blocks

        # During the run, this variable is updated with the currently open file.
        # This file is closed before opening a new one - so we ensure only one is
        # open at a given time.
        # The try/finally block makes sure we close it at the end, if any was open.
        last_open_file = None

        # Operate on a set - only return once per required hashkey, even if required more than once
        hashkeys_set = set(hashkeys)

        hashkeys_in_packs = set()

        packs = defaultdict(list)
        # Currently ordering in the DB (it's ordered across all packs, but this should not be
        # a problem as we then split them by pack). To be checked, performance-wise, if it's better
        # to order in python instead
        session = self._get_cached_session()

        # Operate in chunks, due to the SQLite limits
        # (see comment above the definition of self._IN_SQL_MAX_LENGTH)
        for chunk in chunk_iterator(hashkeys_set, size=self._IN_SQL_MAX_LENGTH):
            query = session.query(Obj).filter(
                Obj.hashkey.in_(chunk)
            ).with_entities(Obj.pack_id, Obj.hashkey, Obj.offset, Obj.length, Obj.compressed,
                            Obj.size).order_by(Obj.offset)
            for res in query:
                packs[res[0]].append(ObjQueryResults(res[1], res[2], res[3], res[4], res[5]))

        for pack_int_id, pack_metadata in packs.items():
            hashkeys_in_packs.update(obj.hashkey for obj in pack_metadata)
            pack_path = self._get_pack_path_from_pack_id(str(pack_int_id))
            try:
                # Open only once per file (if in `with_streams` mode)
                if with_streams:
                    last_open_file = open(pack_path, mode='rb')
                for metadata in pack_metadata:
                    meta = {
                        'type': 'packed',
                        'size': metadata.size,
                        'pack_id': pack_int_id,
                        'pack_compressed': metadata.compressed,
                        'pack_offset': metadata.offset,
                        'pack_length': metadata.length,
                    }

                    if with_streams:
                        obj_reader = PackedObjectReader(
                            fhandle=last_open_file, offset=metadata.offset, length=metadata.length
                        )
                        if metadata.compressed:
                            obj_reader = StreamDecompresser(obj_reader)
                        yield metadata.hashkey, obj_reader, meta
                    else:
                        yield metadata.hashkey, meta
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
                    last_open_file = open(obj_path, mode='rb')
                    # I do not use os.path.getsize in case the file has just
                    # been deleted by a concurrent writer
                    meta = {
                        'type': 'loose',
                        'size': os.fstat(last_open_file.fileno()).st_size,
                        'pack_id': None,
                        'pack_compressed': None,
                        'pack_offset': None,
                        'pack_length': None,
                    }

                    yield loose_hashkey, last_open_file, meta
                else:
                    # This will also raise a FileNotFoundError if the file does not exist
                    size = os.path.getsize(obj_path)
                    meta = {
                        'type': 'loose',
                        'size': size,
                        'pack_id': None,
                        'pack_compressed': None,
                        'pack_offset': None,
                        'pack_length': None,
                    }

                    yield loose_hashkey, meta
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
            for chunk in chunk_iterator(loose_not_found, size=self._IN_SQL_MAX_LENGTH):
                query = session.query(Obj).filter(
                    Obj.hashkey.in_(chunk)
                ).with_entities(Obj.pack_id, Obj.hashkey, Obj.offset, Obj.length, Obj.compressed,
                                Obj.size).order_by(Obj.offset)
                for res in query:
                    packs[res[0]].append(ObjQueryResults(res[1], res[2], res[3], res[4], res[5]))

            # I will construct here the really missing objects.
            # I make a copy of the set.
            really_not_found = loose_not_found.copy()

            for pack_int_id, pack_metadata in packs.items():
                # I remove those that I found
                really_not_found.difference_update(obj.hashkey for obj in pack_metadata)

                pack_path = self._get_pack_path_from_pack_id(str(pack_int_id))
                try:
                    if with_streams:
                        last_open_file = open(pack_path, mode='rb')

                    for metadata in pack_metadata:
                        meta = {
                            'type': 'packed',
                            'size': metadata.size,
                            'pack_id': pack_int_id,
                            'pack_compressed': metadata.compressed,
                            'pack_offset': metadata.offset,
                            'pack_length': metadata.length,
                        }
                        if with_streams:
                            obj_reader = PackedObjectReader(
                                fhandle=last_open_file, offset=metadata.offset, length=metadata.length
                            )
                            if metadata.compressed:
                                obj_reader = StreamDecompresser(obj_reader)
                            yield metadata.hashkey, obj_reader, meta
                        else:
                            yield metadata.hashkey, meta
                finally:
                    if last_open_file is not None:
                        if not last_open_file.closed:
                            last_open_file.close()

            # If there are really missing objects, and skip_if_missing is False, yield them
            if really_not_found and not skip_if_missing:
                for missing_hashkey in really_not_found:
                    meta = {
                        'type': 'missing',
                        'size': None,
                        'pack_id': None,
                        'pack_compressed': None,
                        'pack_offset': None,
                        'pack_length': None,
                    }
                    if with_streams:
                        yield missing_hashkey, None, meta
                    else:
                        yield missing_hashkey, meta

    @contextmanager
    def get_objects_stream_and_meta(self, hashkeys, skip_if_missing=True):
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

        `meta` is a dictionary containing a number of keys. These include:

        - `type`: always present. It can be one of the following strings: `loose`, `packed`, `missing`, where
          `missing` is returned for missing objects if `skip_if_missing` is False.
        - `size`: the size of the object in bytes (i.e., `len(stream.read())`). Always present, set to None if
          `type` is `missing`.
        - `pack_id`: the ID of the pack in which this object is stored. Set to `None` if `type` is not `packed`.
        - `pack_compressed`: a boolean indicating if the object has been stored as compressed on disk or not
        - `pack_offset`: the offset in the pack file. Set to `None` if `type` is not `packed`.
        - `pack_length`: the size *on disk* of the object within the pack, in bytes.
           It is equal to `size` if `pack_compressed` is False, otherwise it can be different (in general smaller,
           but for small or uncompressible objects, even larger). Set to `None` if `type` is not `packed`.

        :param hashkeys: a list of hash keys for which we want to get a stream reader
        :param skip_if_missing: if True, just skip hash keys that are not in the container
            (i.e., neither packed nor loose). If False, return ``None`` instead of the
            stream. In this latter case, the length of the generator returned by this context
            manager has always the same length as the input ``hashkeys`` list.
        """
        yield self._get_objects_stream_meta_generator(
            hashkeys=hashkeys, skip_if_missing=skip_if_missing, with_streams=True
        )

    def get_objects_meta(self, hashkeys, skip_if_missing=True):
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

        ``meta`` is a dictionary containing a number of keys, for the documentation check the
        ``get_objects_stream_and_meta`` documentation.

        :param hashkeys: a list of hash keys for which we want to get a stream reader
        :param skip_if_missing: if True, just skip hash keys that are not in the container
            (i.e., neither packed nor loose). If False, return them (``meta['type']`` will be the
            string ``none`` in this case).
            In this latter case, the length of the generator returned by this context
            manager has always the same length as the input ``hashkeys`` list.
        """
        return self._get_objects_stream_meta_generator(
            hashkeys=hashkeys, skip_if_missing=skip_if_missing, with_streams=False
        )

    def get_object_meta(self, hashkey):
        """Return the metadata dictionary for the given hash key.

        To be used as follows:

          meta = container.get_object_meta(hashkey)
          print(meta['size'])

        The schema of the returned metadata `meta` dict is documented in the docstring
        of `get_objects_stream_and_meta`).

        :param hashkey: the hashkey of the object to stream.
        """
        counter = 0
        for obj_hashkey, meta in self.get_objects_meta(hashkeys=[hashkey], skip_if_missing=False):
            counter += 1
            assert counter == 1, 'There is more than one item returned by get_objects_stream_and_meta'
            assert obj_hashkey == hashkey

            if meta['type'] == 'missing':
                raise NotExistent('No object with hash key {}'.format(hashkey))

            return meta

    def has_objects(self, hashkeys):
        """Return whether the container contains objects with the given hash keys.

        :param hashkeys: a list of hash keys to check.
        :return: a list of booleans, where the i-th value is True if the i-th object of the ``hashkeys``
            list exists, False otherwise.
        """
        existing_hashkeys = set()

        # Note: This iterates in a 'random' order, different than the `hashkeys` list
        for obj_hashkey, _ in self.get_objects_meta(hashkeys=hashkeys, skip_if_missing=True):
            # Since I use skip_if_missing=True, I should only iterate on those that exist
            existing_hashkeys.add(obj_hashkey)

        # Return a list of booleans
        return [hashkey in existing_hashkeys for hashkey in hashkeys]

    def has_object(self, hashkey):
        """Return whether the container contains an object with the given hashkey.

        :param hashkey: the hashkey of the object.
        :return: True if the object exists, False otherwise.
        """
        return self.has_objects([hashkey])[0]

    def get_objects_content(self, hashkeys, skip_if_missing=True):
        """Get the content of a number of objects with given hash keys.

        :note: use this method only if you know objects fit in memory.
            Otherwise, use the ``get_objects_stream_and_meta`` context manager and
            process the objects one by one.

        :param hashkeys: A list of hash kyes of the objects to retrieve.
        :return: a dictionary of byte streams where the keys are the hash keys and the values
            are the object contents.
        """
        retrieved = {}
        with self.get_objects_stream_and_meta(hashkeys=hashkeys, skip_if_missing=skip_if_missing) as triplets:
            for obj_hashkey, stream, _ in triplets:
                if stream is None:
                    # This should happen only if skip_if_missing is False
                    retrieved[obj_hashkey] = None
                else:
                    retrieved[obj_hashkey] = stream.read()
        return retrieved

    def _new_object_writer(self):
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
            hash_type=self.hash_type
        )

    def add_object(self, content):
        """Add a loose object.

        :param content: a binary stream with the file content.
        :return: the hash key of the newly created object.
        """
        writer = self._new_object_writer()
        with writer as fhandle:
            fhandle.write(content)

        return writer.get_hashkey()

    def count_objects(self):
        """Return a dictionary with the count of objects, keys are 'loose' and 'packed'.

        Also return a number of packs under 'pack_files'."""
        retval = {}

        number_packed = self._get_cached_session().query(Obj).count()
        retval['packed'] = number_packed

        retval['loose'] = 0
        for loose_hashkey in self._list_loose():  # pylint: disable=unused-variable
            retval['loose'] += 1

        retval['pack_files'] = len(list(self._list_packs()))

        return retval

    @staticmethod
    def _is_valid_pack_id(pack_id):
        """Return True if the name is a valid pack ID."""
        if not pack_id:
            # Must be a non-empty string
            return False
        if pack_id != '0' and pack_id[0] == '0':
            # The ID must be a valid integer: either zero, or it should not start by zero
            return False
        if not all(char in '0123456789' for char in pack_id):
            return False
        return True

    def _is_valid_loose_prefix(self, prefix):
        """Return True if the name is a valid prefix."""
        if len(prefix) != self.loose_prefix_len:
            return False
        if not all(char in '0123456789abcdef' for char in prefix):
            return False
        return True

    @staticmethod
    def _is_valid_hashkey(hashkey):
        """Return True is the name is a valid hashkey.

        Note that it currently does not check the length but only that the key is composed only
        by hexadecimal characters.
        """
        if not all(char in '0123456789abcdef' for char in hashkey):
            return False
        return True

    def get_total_size(self):
        """Return a dictionary with the total size of objects in the container.

        - total_size_packed: size of the objects (before compressing) in the packs.
        - total_size_packed_on_disk: size actually occupied on disk by the objects (including optional compression).
        - total_size_packfiles_on_disk: size of the packs on disk (can be larger if objects are still
          in the packs but are not referenced anymore).
        - total_size_packindexes_on_disk: size of the pack indexes on disk.
        - total_size_loose: size of the loose objects in the packs (always uncompressed).
        """
        retval = {}

        session = self._get_cached_session()
        # COALESCE is used to return 0 if there are no results, rather than None
        # SQL's COALESCE returns the first non-null result
        retval['total_size_packed'] = session.query(func.coalesce(func.sum(Obj.size),
                                                                  0).label('total_size_packed')).all()[0][0]
        retval['total_size_packed_on_disk'] = session.query(
            func.coalesce(func.sum(Obj.length), 0).label('total_length_packed')
        ).all()[0][0]

        total_size_packfiles_on_disk = 0
        for pack_id in list(self._list_packs()):
            total_size_packfiles_on_disk += os.path.getsize(self._get_pack_path_from_pack_id(pack_id))
        retval['total_size_packfiles_on_disk'] = total_size_packfiles_on_disk

        retval['total_size_packindexes_on_disk'] = os.path.getsize(self._get_pack_index_path())

        total_size_loose = 0
        for loose_hashkey in self._list_loose():
            loose_path = self._get_loose_path_from_hashkey(loose_hashkey)
            total_size_loose += os.path.getsize(loose_path)
        retval['total_size_loose'] = total_size_loose

        return retval

    @contextmanager
    def lock_pack(self, pack_id):
        """Lock the given pack id. Use as a context manager.

        Raise if the pack is already locked. If you enter the context manager,
        it means you successfully locked the pack.

        Important to use for avoiding concurrent access/append to the same file.
        :param pack_id: a string with a valid pack name.
        """
        assert self._is_valid_pack_id(pack_id)

        # Open file in exclusive mode
        lock_file = os.path.join(self._get_pack_folder(), '{}.lock'.format(pack_id))
        try:
            with open(lock_file, 'x'):
                with open(self._get_pack_path_from_pack_id(pack_id), 'ab') as pack_handle:
                    yield pack_handle
        finally:
            # Release resource (I check if it exists in case there was an exception)
            if os.path.exists(lock_file):
                os.remove(lock_file)

    def _list_loose(self):
        """Iterate over loose objects.

        This returns all loose objects, even if a packed version of the same object exists.

        .. note:: this returns a generator of hash keys.
        """
        for first_level in os.listdir(self._get_loose_folder()):
            if self.loose_prefix_len:
                if not self._is_valid_loose_prefix(first_level):
                    continue
                for second_level in os.listdir(os.path.join(self._get_loose_folder(), first_level)):
                    hashkey = '{}{}'.format(first_level, second_level)
                    if not self._is_valid_hashkey(hashkey):
                        continue
                    yield hashkey
            else:
                # It's flat (loose_prefix_len == 0)
                if not self._is_valid_hashkey(first_level):
                    continue
                yield first_level

    def _list_packs(self):
        """Iterate over packs.

        .. note:: this returns a generator of the pack IDs.
        """
        for fname in os.listdir(self._get_pack_folder()):
            ## I actually check for pack index files
            #if not fname.endswith(self._PACK_INDEX_SUFFIX):
            #    continue
            #pack_id = fname[:-len(self._PACK_INDEX_SUFFIX)]
            if self._is_valid_pack_id(fname):
                yield fname

    def list_all_objects(self):
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
            results_chunk = session.query(Obj).filter(Obj.id > last_pk).order_by(
                Obj.id
            ).limit(yield_per_size).with_entities(Obj.id, Obj.hashkey).all()

            for _, hashkey in results_chunk:
                # I need to use a comma because I want to create a tuple
                loose_objects.difference_update((hashkey,))
                yield hashkey

            if results_chunk:
                last_pk = results_chunk[-1][0]
            else:
                # No more packed objects
                break

        # What is left are the loose objects that are not in the packs
        for hashkey in loose_objects:
            yield hashkey

    def _write_data_to_packfile(self, pack_handle, read_handle, compress, hash_type=None):
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
        assert 'b' in pack_handle.mode
        assert 'a' in pack_handle.mode

        if hash_type:
            hasher = get_hash(hash_type=hash_type)()

        if compress:
            compressobj = zlib.compressobj(level=self._COMPRESSLEVEL)

        count_read_bytes = 0
        while True:
            chunk = read_handle.read(self._CHUNKSIZE)
            if chunk == b'':
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

    def pack_all_loose(self, compress=False, validate_objects=True):
        """Pack all loose objects.

        This is a maintenance operation, needs to be done only by one process.
        :param compress: if True, compress objects before storing them.
        :param validate_objects: if True, recompute the hash while packing, and raises if there is a problem.
        """
        hash_type = self.hash_type if validate_objects else None

        loose_objects = set(self._list_loose())
        pack_int_id = self._get_pack_id_to_write_to()
        session = self._get_cached_session()

        # I first skip all loose hashkeys that already exist in the pack.
        # Packing should be performed by a single process at a given time as a
        # maintenance operation, so I don't have to worry about concurrency:
        # If I don't find it here, is should not appear midway during the rest of the process

        existing_packed_hashkeys = []

        for chunk in chunk_iterator(loose_objects, size=self._IN_SQL_MAX_LENGTH):
            # I check the hash keys that are already in the pack
            for res in session.query(Obj).filter(Obj.hashkey.in_(chunk)).with_entities(Obj.hashkey).all():
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

        # Outer loop: this is used to continue when a new pack file needs to be created
        while loose_objects:
            # Store the last pack integer ID, needed to know later if I need to open a new pack
            last_pack_int_id = pack_int_id
            # Avoid concurrent writes on the pack file
            with self.lock_pack(str(pack_int_id)) as pack_handle:
                loose_objects_this_pack = []
                # Inner loop: continue until when there is a file, or
                # if we need to change pack (in this case `break` is called)
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
                    # Keep track of it for later deletion
                    loose_objects_this_pack.append(loose_hashkey)

                    obj = Obj(hashkey=loose_hashkey)
                    obj.pack_id = pack_int_id
                    obj.compressed = compress
                    obj.offset = pack_handle.tell()
                    with open(self._get_loose_path_from_hashkey(loose_hashkey), 'rb') as loose_handle:
                        # The second parameter is `None` since we are not computing the hash
                        # We can instead pass the hash algorithm and assert that it is correct
                        obj.size, new_hashkey = self._write_data_to_packfile(
                            pack_handle=pack_handle, read_handle=loose_handle, compress=compress, hash_type=hash_type
                        )
                        if hash_type and new_hashkey != loose_hashkey:
                            raise InconsistentContent(
                                "Error when packing object '{}': re-computed hash is different! '{}'".format(
                                    loose_hashkey, new_hashkey
                                )
                            )
                    obj.length = pack_handle.tell() - obj.offset
                    session.add(obj)

                # flush and sync to disk before closing
                safe_flush_to_disk(pack_handle, os.path.realpath(pack_handle.name), use_fullsync=True)

            # OK, if we are here, file was flushed, synced to disk and closed.
            # Let's commit then the information to the DB, so it's officially a
            # packed object. Note: committing as soon as we are done with one pack,
            # so if there's a problem with one pack we don't start operating on the next one
            # Note: because of the logic above, in theory this should not raise an IntegrityError!
            session.commit()

            # If we are here, things should be guaranteed by SQLite to be written to disk.
            # Then, it would be safe to already do some clean up of loose objects that are now packed,
            # and by doing it here we would do it after each pack.
            # This would mean removing objects that are in `loose_objects_this_pack`.
            # HOWEVER, while this would work fine on Linux, there are concurrency issues both
            # on Mac and on Windows (see issues #37 and #43). Therefore, I do NOT delete them,
            # and deletion is deferred to a manual clean-up operation.

    def add_streamed_objects_to_pack(self, stream_list, compress=False, open_streams=False):
        """Add objects directly to a pack, reading from a list of streams.

        This is a maintenance operation, available mostly for efficiency reasons
        e.g. if you are creating a container from scratch.
        As such, it needs to be done only by one process.

        :param stream_list: a list of BytesIO bytestreams to add.
        :param compress: if True, compress objects before storing them.
        :param open_streams: if True, then open the streams using a ``with`` context
            manager. Otherwise, just read from them (assuming the responsibility of opening
            them is on the caller). Setting to True is useful when reading from many files,
            and passing here a number of ``LazyOpener`` objects.
        :return: a list of object hash keys
        """
        hashkeys = []

        # Make a copy of the list and revert its order, so we can pop from the list
        # without affecting the original list, and it's from the end so it's fast
        working_stream_list = list(stream_list[::-1])
        pack_int_id = self._get_pack_id_to_write_to()
        session = self._get_cached_session()

        # Outer loop: this is used to continue when a new pack file needs to be created
        while working_stream_list:
            # Store the last pack integer ID, needed to know later if I need to open a new pack
            last_pack_int_id = pack_int_id
            # Avoid concurrent writes on the pack file
            with self.lock_pack(str(pack_int_id)) as pack_handle:
                # Inner loop: continue until when there is a file, or
                # if we need to change pack (in this case `break` is called)
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
                        stream_context_manager = nullcontext(next_stream)

                    #obj = Obj()
                    obj_dict = {}
                    obj_dict['pack_id'] = pack_int_id
                    obj_dict['compressed'] = compress
                    obj_dict['offset'] = pack_handle.tell()
                    with stream_context_manager as stream:
                        obj_dict['size'], obj_dict['hashkey'] = self._write_data_to_packfile(
                            pack_handle=pack_handle, read_handle=stream, compress=compress, hash_type=self.hash_type
                        )
                    obj_dict['length'] = pack_handle.tell() - obj_dict['offset']
                    # Here, we have appended the object to the pack file.
                    # And now that we are done, we know the hash key.
                    # However, we have to cope with the fact that an object with the same hash key
                    # could be already inside the object.
                    # We cannot do a query for each object, it would be too expensive and inefficient.
                    # We need instead to rely of the unique constraint on the DB.
                    # However, the IntegrityError is raised not during the `add` call, but at the final
                    # `commit`.
                    # One option is to use this, instead of a session.add()
                    insert_command = Obj.__table__.insert().prefix_with('OR IGNORE').values(obj_dict)
                    session.execute(insert_command)
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
                    hashkeys.append(obj_dict['hashkey'])

                # flush and sync to disk before closing
                safe_flush_to_disk(pack_handle, os.path.realpath(pack_handle.name), use_fullsync=True)

            # OK, if we are here, file was flushed, synced to disk and closed.
            # Let's commit then the information to the DB, so it's officially a
            # packed object. Note: committing as soon as we are done with one pack,
            # so if there's a problem with one pack we don't start operating on the next one
            # Note: because of the logic above, in theory this should not raise an IntegrityError!
            session.commit()

        return hashkeys

    def add_objects_to_pack(self, content_list, compress=False):
        """Add objects directly to a pack, reading from a list of content byte arrays.

        This is a maintenance operation, available mostly for efficiency reasons
        e.g. if you are creating a container from scratch.
        As such, it needs to be done only by one process.

        :note: use this only if you know the full list of contents fits in memory.
          Otherwise, call the add_streamed_objects_to_pack instead.

        :param content_list: a list of content bytestreams to add.
        :param compress: if True, compress objects before storing them.
        :return: a list of object hash keys
        """
        stream_list = [io.BytesIO(content) for content in content_list]
        return self.add_streamed_objects_to_pack(stream_list=stream_list, compress=compress)

    def clean_storage(self):
        """Perform some maintenance clean-up of the container.

        .. note:: this is a maintenance operation, must be performed when nobody is using the container!

        In particular:
        - it cleans up loose objects that are already in packs
        """
        loose_objects = set(self._list_loose())
        # Force reload of the session to get the most up-to-date packed objects
        self.close()

        session = self._get_cached_session()
        # I search now for all loose hash keys that exist also in the packs
        existing_packed_hashkeys = []
        for chunk in chunk_iterator(loose_objects, size=self._IN_SQL_MAX_LENGTH):
            # I check the hash keys that are already in the pack
            for res in session.query(Obj).filter(Obj.hashkey.in_(chunk)).with_entities(Obj.hashkey).all():
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

        # TODO: implement logic to check, remove duplicates if the corresponding existing
        # (loose or packed) file exists and is correct, otherwise replace, or show an error.
