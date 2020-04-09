"""
The main implementation of the ``Container`` class of the object store.
"""
import io
import json
import os
import shutil
import zlib

from collections import defaultdict
from contextlib import contextmanager
from sqlalchemy import create_engine, event

from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker

from .models import Base, Obj
from .utils import nullcontext, ObjectWriter, PackedObjectReader, StreamDecompresser, get_new_uuid
from .exceptions import NotExistent, NotInitialised


class Container:
    """A class representing a container of objects (which is stored on a disk folder)"""

    _PACK_INDEX_SUFFIX = '.idx'
    # Default compression level (when compression is requested)
    # This is the lowest one, to get some reasonable compression without too much CPU time required
    _COMPRESSLEVEL = 1
    # Size in bytes of each of the chunks used when (internally) reading or writing in chunks, e.g.
    # when packing.
    _CHUNKSIZE = 65536

    def __init__(self, folder):
        """Create the class that represents the container.

        :param folder: the path to a folder that will host this object-store continer.
        """
        self._folder = folder
        self._session = None  # Will be populated by the _get_session function
        # These act as caches and will be populated by the corresponding properties
        self._loose_prefix_len = None
        self._pack_prefix_len = None

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

    def _get_config_file(self):
        """Return the path to the container config file."""
        return os.path.join(self._folder, 'config.json')

    def _get_session(self, create=False, raise_if_missing=False):
        """Return a new session to connect to the pack-index SQLite DB.

        :param create: if True, creates the sqlite file and schema.
        :param raise_if_missing: ignored if create==True. If create==False, and the index file
           is missing, either raise an exception (FileExistsError) if this flag is True, or return None
        """
        if not create and not os.path.exists(self._get_pack_index_path()):
            if raise_if_missing:
                raise FileExistsError('Pack index does not exist')
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

    def _get_loose_path_from_uuid(self, uuid):
        """Return the path of a loose object on disk containing the data of a given UUID.

        :param uuid: the UUID of the object to get.
        """
        if self.loose_prefix_len:
            return os.path.join(
                self._get_loose_folder(),
                uuid[:self.loose_prefix_len],
                uuid[self.loose_prefix_len:],
            )
        # if loose_prefix_len is zero, there is no subfolder
        return os.path.join(self._get_loose_folder(), uuid)

    def _get_pack_path_from_pack_id(self, pack_id):
        """Return the path of the pack file on disk for the given pack ID.

        :param pack_id: the pack ID.
        """
        assert self._is_valid_pack_id(pack_id), 'Invalid pack ID {}'.format(pack_id)
        return os.path.join(self._get_pack_folder(), pack_id)

    def _get_pack_index_path(self):
        """Return the path to the SQLite file containing the index of packed objects.
        """
        return os.path.join(self._folder, 'packs{}'.format(self._PACK_INDEX_SUFFIX))

    @property
    def is_initialised(self):
        """Return True if the container is already initialised."""
        if not os.path.exists(self._folder):
            return False
        try:
            with open(self._get_config_file()) as fhandle:
                json.load(fhandle)
        except (ValueError, OSError, IOError):
            return False
        for folder in [self._get_pack_folder(), self._get_loose_folder(), self._get_sandbox_folder()]:
            if not os.path.exists(folder):
                return False
        return True

    def init_container(self, clear=False, pack_prefix_len=2, loose_prefix_len=2):
        """Initialise the container folder, if not already done.

        If this is called multiple times, it does not corrupt the data,
        unless you add the ``clear=True`` option.

        :param clear: if True, delete everything in the container and
          initialise a new, empty one.
        :param pack_prefix_len: The length of the prefix of the packed objects.
          The longer the length, the more packs will be created. Suggested
          values: 2 or 3.
        :param loose_prefix_len: The length of the prefix of the loose objects.
          The longer the length, the more folders will be used to store loose
          objects. Suggested values: 0 (for not using subfolders) or 2.
        """
        if clear:
            if os.path.exists(self._folder):
                shutil.rmtree(self._folder)

        if os.path.exists(self._folder):
            raise FileExistsError(
                'The container already exists, so you cannot initialise it - '
                'use the clear option if you want to overwrite with a clean one'
            )

        os.makedirs(self._folder)

        # Create config file
        with open(self._get_config_file(), 'w') as fhandle:
            json.dump(
                {
                    'container_version': 1,  # For future compatibility, this is the version of the format
                    'loose_prefix_len': loose_prefix_len,
                    'pack_prefix_len': pack_prefix_len
                },
                fhandle
            )

        for folder in [self._get_pack_folder(), self._get_loose_folder(), self._get_sandbox_folder()]:
            if not os.path.exists(folder):
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
    def pack_prefix_len(self):
        """Return the length of the pack name, when sharding.

        This is read from the repository configuration.
        """
        if self._pack_prefix_len is None:
            self._pack_prefix_len = self._get_repository_config()['pack_prefix_len']
        return self._pack_prefix_len

    def _split_uuid_for_pack(self, uuid):
        """Return the pack_id and the remainder of the UUID from a given UUID"""
        return uuid[:self.pack_prefix_len], uuid[self.pack_prefix_len:]

    def get_object_content(self, uuid):
        """Get the content of an object with a given UUID.

        :param uuid: The UUID of the object to retrieve.
        :return: a byte stream with the object content.
        """
        with self.get_object_stream(uuid) as handle:
            return handle.read()

    @contextmanager
    def get_object_stream(self, uuid):
        """Return a context manager yielding a stream to get the content of an object.

        To be used as a context manager::

          with container.get_object_stream(uuid) as fhandle:
              data = fhandle.read()

        The returned object supports *at least* the read() method that
        accepts an optional parameter to read the file in chunks, and might
        not be seekable.
        :param uuid: the UUID of the object to stream.
        """
        with self.get_object_streams_and_size(uuids=[uuid], skip_if_missing=False) as triplets:
            obj_uuid, stream, _ = next(triplets)  # pylint: disable=stop-iteration-return
            assert obj_uuid == uuid

            if stream is None:
                raise NotExistent('No object with UUID {}'.format(uuid))

            yield stream

            try:
                next(triplets)
                raise AssertionError('There is more than one item returned by get_object_streams_and_size')
            except StopIteration:
                # There should be only one entry
                pass

    @contextmanager
    def get_object_streams_and_size(self, uuids, skip_if_missing=True):  # pylint: disable=too-many-statements
        """A context manager returning a generator yielding triplets of (uuid, open stream, size).

        :note: the UUIDs yielded are often in a *different* order than the original
            ``uuids`` list. This is done for efficiency reasons, to reduce to a minimum
            file opening and to try to read file chunks (for packs) in sequential
            order rather than in random order.

        To use it, you should do something like the following::

            with container.get_object_streams_and_size(uuids=uuids) as triplets:
                for obj_uuid, stream, size in triplets:
                    if stream is None:
                        # This should happen only if you pass skip_if_missing=False
                        retrieved[obj_uuid] = None
                    else:
                        # len(stream.read() will be equal to size
                        retrieved[obj_uuid] = stream.read()

        :param uuids: a list of UUIDs for which we want to get a stream reader
        :param skip_if_missing: if True, just skip UUIDs that are not in the container
            (i.e., neither packed nor loose). If False, return ``None`` instead of the
            stream. In this latter case, the length of the generator returned by this context
            manager has always the same length as the input ``uuids`` list.
        """

        def get_object_stream_generator(uuids, last_open_file, skip_if_missing):  # pylint: disable=too-many-branches,too-many-statements
            """Return a generator yielding tripltes of (uuid, open stream, size).

            :note: The stream is already open and at the right position, and can
                just be read.

            :note: size is the length of the object (uncompressed) when doing a
               ``read()`` on the returned stream

            :param uuids: a list of UUIDs for which we want to get a stream reader
            :param last_open_file: must be a list of length one, initialised with None.
                During the run, the first (and only) element of the list is updated
                with the currently open file.
                When the generator is exhausted, the file is closed (but the outer
                context manager will still close the file, if it's open - this is needed
                if the caller of ``get_object_streams_and_size`` exits the ``with`` context manager
                without exhausting this generator).
            :param skip_if_missing: if True, just skip UUIDs that are not in the container
                (i.e., neither packed nor loose). If False, return ``None`` instead of the
                stream.
            """
            try:
                uuids_in_packs = set()

                packs = defaultdict(list)
                for obj_uuid in uuids:
                    pack_id = self._split_uuid_for_pack(obj_uuid)[0]
                    packs[pack_id].append(obj_uuid)

                for pack_id, obj_uuids in packs.items():
                    session = self._get_cached_session()
                    pack_metadata = {
                        res[0]: (res[1], res[2], res[3], res[4])
                        for res in session.query(Obj).filter(Obj.uuid.in_(obj_uuids)).
                        with_entities(Obj.uuid, Obj.offset, Obj.length, Obj.compressed, Obj.size).order_by(Obj.offset)
                    }
                    if pack_metadata:
                        uuids_in_packs.update(pack_metadata.keys())
                        pack_path = self._get_pack_path_from_pack_id(pack_id)
                        if last_open_file[0] is not None:
                            if not last_open_file[0].closed:
                                last_open_file[0].close()
                        # Open only once per file
                        last_open_file[0] = open(pack_path, mode='rb')
                        for obj_uuid, metadata in pack_metadata.items():
                            obj_reader = PackedObjectReader(
                                fhandle=last_open_file[0], offset=metadata[0], length=metadata[1]
                            )
                            if metadata[2]:
                                obj_reader = StreamDecompresser(obj_reader)
                            yield obj_uuid, obj_reader, metadata[3]

                # Collect loose UUIDS that are not found
                # Reason: a concurrent process might have packed them,
                # in the meantime.
                loose_not_found = []
                for loose_uuid in set(uuids).difference(uuids_in_packs):
                    obj_path = self._get_loose_path_from_uuid(uuid=loose_uuid)
                    try:
                        last_open_file[0] = open(obj_path, mode='rb')
                        yield loose_uuid, last_open_file[0], os.path.getsize(obj_path)
                    except FileNotFoundError:
                        loose_not_found.append(loose_uuid)
                        continue
                    if last_open_file[0] is not None:
                        if not last_open_file[0].closed:
                            last_open_file[0].close()

                # There were some loose objects that were not found
                # Give a final try - if they have been deleted in the meantime
                # while being packed, I should have the guarantee that they
                # are by now in the pack.
                # If they are not, the object does not exist.
                if loose_not_found:
                    # In this case, I do *not* sort them - I expect
                    # this situation to happen quite rarely, only while
                    # packing, and it's ok to lose a bit of performance
                    # in this rare case, but keep the code simpler.

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
                    session = self._get_cached_session()
                    pack_metadata = {
                        res[0]: (res[1], res[2], res[3], res[4])
                        for res in session.query(Obj).filter(Obj.uuid.in_(loose_not_found)).
                        with_entities(Obj.uuid, Obj.offset, Obj.length, Obj.compressed, Obj.size).order_by(Obj.offset)
                    }
                    # These are really missing objects
                    really_not_found = set(loose_not_found).difference(pack_metadata)

                    for obj_uuid, metadata in pack_metadata.items():
                        pack_id = self._split_uuid_for_pack(obj_uuid)[0]
                        pack_path = self._get_pack_path_from_pack_id(pack_id)

                        # Close possibly open file - might not be optimised if all
                        # are in the same pack, but as discussed above we should reach
                        # here only if someone packed exactly while we were listing the objects,
                        # and this should be rare
                        if last_open_file[0] is not None:
                            if not last_open_file[0].closed:
                                last_open_file[0].close()
                        last_open_file[0] = open(pack_path, mode='rb')
                        obj_reader = PackedObjectReader(
                            fhandle=last_open_file[0], offset=metadata[0], length=metadata[1]
                        )
                        if metadata[2]:
                            obj_reader = StreamDecompresser(obj_reader)
                        yield obj_uuid, obj_reader, metadata[3]

                    # If there are really missing objects, and skip_if_missing is False, yield them
                    if really_not_found and not skip_if_missing:
                        for missing_uuid in really_not_found:
                            yield missing_uuid, None, 0

            finally:
                if last_open_file[0] is not None:
                    last_open_file[0].close()

        # I want it to be a list of length 1 to make sure I actually have a reference to it
        last_open_file = [None]

        yield get_object_stream_generator(uuids=uuids, last_open_file=last_open_file, skip_if_missing=skip_if_missing)

        if last_open_file[0] is not None:
            if not last_open_file[0].closed:
                last_open_file[0].close()

    def get_object_contents(self, uuids, skip_if_missing=True):
        """Get the content of a number of objects with given UUIDs.

        :note: use this method only if you know objects fit in memory.
            Otherwise, use the ``get_object_streams_and_size`` context manager and
            process the objects one by one.

        :param uuids: A list of UUIDs of the objects to retrieve.
        :return: a dictionary of byte streams where the keys are the UUIDs and the values
            are the object contents.
        """
        retrieved = {}
        with self.get_object_streams_and_size(uuids=uuids, skip_if_missing=skip_if_missing) as triplets:
            for obj_uuid, stream, _ in triplets:
                if stream is None:
                    # This should happen only if skip_if_missing is False
                    retrieved[obj_uuid] = None
                else:
                    retrieved[obj_uuid] = stream.read()
        return retrieved

    def _new_object_writer(self):
        """Return a context manager that can be used to create a new object.

        To use it, do the following::

          new_object_writer = repo._new_object_writer()
          with new_object_writer as fhandle:
              fhandle.write(b'something')
          new_uuid = new_object_writer.uuid()
        """
        return ObjectWriter(
            sandbox_folder=self._get_sandbox_folder(),
            loose_folder=self._get_loose_folder(),
            loose_prefix_len=self.loose_prefix_len
        )

    def add_object(self, content):
        """Add a loose object.

        :param content: a binary stream with the file content.
        :return: the UUID of the newly created object.
        """
        writer = self._new_object_writer()
        with writer as fhandle:
            fhandle.write(content)

        return writer.get_uuid()

    def count_objects(self):
        """Return a dictionary with the count of objects, keys are 'loose' and 'packed'.

        Also return a number of packs under 'pack_files'."""
        retval = {}

        number_packed = self._get_cached_session().query(Obj).count()
        retval['packed'] = number_packed

        retval['loose'] = 0
        for loose_uuid in self._list_loose():  # pylint: disable=unused-variable
            retval['loose'] += 1

        retval['pack_files'] = len(list(self._list_packs()))

        return retval

    def _is_valid_pack_id(self, pack_id):
        """Return True if the name is a valid pack ID."""
        if len(pack_id) != self.pack_prefix_len:
            return False
        if not all(char in '0123456789abcdef' for char in pack_id):
            return False
        return True

    def _is_valid_loose_prefix(self, prefix):
        """Return True if the name is a valid prefix."""
        if len(prefix) != self.loose_prefix_len:
            return False
        if not all(char in '0123456789abcdef' for char in prefix):
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
        for loose_uuid in self._list_loose():
            loose_path = self._get_loose_path_from_uuid(loose_uuid)
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

        #import psutil
        #proc = psutil.Process()
        #print(proc.open_files())

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
        """Iterate over loose objects

        It does the right thing depending on the value of loose_prefix_len.

        Note that this returns a generator.

        TODO add a prefix filter?
        """
        for first_level in os.listdir(self._get_loose_folder()):
            if self.loose_prefix_len:
                if not self._is_valid_loose_prefix(first_level):
                    continue
                for second_level in os.listdir(os.path.join(self._get_loose_folder(), first_level)):
                    yield '{}{}'.format(first_level, second_level)
            else:
                # It's flat (loose_prefix_len == 0)
                yield first_level

    def _list_packs(self):
        """Iterate over packs.

        Note that this returns a generator of the pack IDs.

        TODO add a prefix filter?
        """
        for fname in os.listdir(self._get_pack_folder()):
            ## I actually check for pack index files
            #if not fname.endswith(self._PACK_INDEX_SUFFIX):
            #    continue
            #pack_id = fname[:-len(self._PACK_INDEX_SUFFIX)]
            if self._is_valid_pack_id(fname):
                yield fname

    def _write_data_to_packfile(self, pack_handle, read_handle, compress):
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
        :return: the number of bytes
        """
        assert 'b' in pack_handle.mode
        assert 'a' in pack_handle.mode

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
            if compress:
                pack_handle.write(compressobj.compress(chunk))
            else:
                pack_handle.write(chunk)

        if compress:
            # Write the remaining of the file, if any leftovers are still present in the
            # compressobj
            pack_handle.write(compressobj.flush())

        return count_read_bytes

    def pack_all_loose(self, compress=False):
        """Pack all loose objects.

        This is a maintenance operation, needs to be done only by one process.
        :param compress: if True, compress objects before storing them.
        """
        packs = defaultdict(list)
        for loose_uuid in self._list_loose():
            pack_id = self._split_uuid_for_pack(loose_uuid)[0]
            packs[pack_id].append(loose_uuid)
        for pack_id, loose_objects in packs.items():
            if loose_objects:
                session = self._get_cached_session()
                # Avoid concurrent writes
                with self.lock_pack(pack_id) as pack_handle:
                    for obj_uuid in loose_objects:
                        obj = Obj(uuid=obj_uuid)
                        obj.compressed = compress
                        obj.offset = pack_handle.tell()
                        with open(self._get_loose_path_from_uuid(obj_uuid), 'rb') as loose_handle:
                            obj.size = self._write_data_to_packfile(
                                pack_handle=pack_handle, read_handle=loose_handle, compress=compress
                            )
                        obj.length = pack_handle.tell() - obj.offset
                        session.add(obj)
                    # Committing as soon as we are done with one pack
                    session.commit()
                # Clean up loose objects, for each pack
                for obj_uuid in loose_objects:
                    os.remove(self._get_loose_path_from_uuid(obj_uuid))

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
        :return: a list of object UUIDs
        """
        packs = defaultdict(list)
        uuids = []

        for pos in range(len(stream_list)):
            obj_uuid = get_new_uuid()
            uuids.append(obj_uuid)
            pack_id = self._split_uuid_for_pack(obj_uuid)[0]
            packs[pack_id].append((pos, obj_uuid))
        for pack_id, obj_ids in packs.items():
            if obj_ids:
                session = self._get_cached_session()
                # Avoid concurrent writes
                with self.lock_pack(pack_id) as pack_handle:
                    for pos, obj_uuid in obj_ids:
                        obj = Obj(uuid=obj_uuid)
                        obj.compressed = compress
                        obj.offset = pack_handle.tell()
                        if open_streams:
                            stream_context_manager = stream_list[pos]
                        else:
                            stream_context_manager = nullcontext(stream_list[pos])
                        with stream_context_manager as stream:
                            obj.size = self._write_data_to_packfile(
                                pack_handle=pack_handle, read_handle=stream, compress=compress
                            )
                        obj.length = pack_handle.tell() - obj.offset
                        session.add(obj)
                    # Commit as soon as we are done with one pack
                    session.commit()
        return uuids

    def add_objects_to_pack(self, content_list, compress=False):
        """Add objects directly to a pack, reading from a list of content byte arrays.

        This is a maintenance operation, available mostly for efficiency reasons
        e.g. if you are creating a container from scratch.
        As such, it needs to be done only by one process.

        :note: use this only if you know the full list of contents fits in memory.
          Otherwise, call the add_streamed_objects_to_pack instead.

        :param content_list: a list of content bytestreams to add.
        :param compress: if True, compress objects before storing them.
        :return: a list of object UUIDs
        """
        stream_list = [io.BytesIO(content) for content in content_list]
        return self.add_streamed_objects_to_pack(stream_list=stream_list, compress=compress)
