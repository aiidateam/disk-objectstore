import io
import json
import os
import shutil
import uuid
import zlib

from collections import defaultdict
from contextlib import contextmanager
from sqlalchemy import create_engine, event

from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker

from .models import Base, Obj


@contextmanager
def nullcontext(enter_result):
    """Return a context manager that returns enter_result from __enter__, but otherwise does nothing.

    This can be replaced by ``contextlib.nullcontext`` if we want to support only py>=3.7.
    """
    yield enter_result


class NotExistent(Exception):
    """Raised if the request object does not exist."""

class ModificationNotAllowed(Exception):
    """Raised if the you cannot modify the given object but you are trying to do so."""

class NotInitialised(Exception):
    """Raised if you are trying to perform an operation on a container that is not yet initialised."""


def get_new_uuid():
    """Utility function to generate a new UUID.

    In this way all parts of the code that need to do it, will do it in the same
    way. Note that this returns the UUID without dashes,
    so we reduce storage space.
    """
    return uuid.uuid4().hex


class _ObjectWriter:
    """A class to get direct write access for a new object."""
    def __init__(self, sandbox_folder, loose_folder, loose_prefix_len):
        """Initialise an object to store a new loose object.
        
        :param sandbox_folder: the folder to store objects while still giving
          access to users to write them
        :param loose_folder: the folder to store the loose objects once finished
        :param loose_prefix_len: the length of the prefix to group loose objects
          in subfolders. E.g., 2 means store in folders aa/..., ab/...
          0 means store objects flat. Note that objects are always stored flat
          in the sandbox (there shouldn't be too many sandbox objects at the
          same time).
        """
        self._sandbox_folder = sandbox_folder
        self._loose_folder = loose_folder
        self._uuid = get_new_uuid()
        self._loose_prefix_len = loose_prefix_len
        self._stored = False

    def get_uuid(self):
        """Return the object ID (it's actually a uuid)."""
        return self._uuid

    def __enter__(self):
        """Start creating a new object in a context manager.

        You will get access access to a file-like object.

        :note: Do not close the file, it will be closed automatically.        
        """
        if self._stored:
            raise ModificationNotAllowed("You have already stored this object '{}'".format(
                self.get_uuid()
        ))
        self._obj_path = os.path.join(self._sandbox_folder, self._uuid)
        self._filehandle = open(self._obj_path, 'wb')
        return self._filehandle

    def __exit__(self, exc_type, value, traceback):
        """
        Close the file object, and move it from the sandbox to the loose 
        object folder, possibly using sharding if loose_prexix_len is not 0.
        """
        if not self._filehandle.closed:
            self._filehandle.close()

        if exc_type is None:
            if self._loose_prefix_len:
                parent_folder = os.path.join(
                    self._loose_folder,
                    self._uuid[:self._loose_prefix_len])
                # Create parent folder the first time
                if not os.path.exists(parent_folder):
                    os.mkdir(parent_folder)

                dest_loose_object = os.path.join(
                    self._loose_folder,
                    self._uuid[:self._loose_prefix_len], self._uuid[self._loose_prefix_len:])
            else: # prefix_len == 0
                dest_loose_object = os.path.join(self._loose_folder, self._uuid)

            if os.path.exists(dest_loose_object):
                raise ModificationNotAllowed("Destination object '{}' already exists!".format(self._uuid))
            # Hopefully this is a fast, atomic operation on most filesystems
            shutil.move(self._obj_path, dest_loose_object)
            self._stored = True
        else:
            # TODO add test to check that this works
            if os.path.exists(self._obj_path):
                os.remove(self._obj_path)


class _PackedObjectReader:
    """A class to read from a pack file.

    This ensures that the .read() method works and does not go beyond the
    length of the given object."""
    @property
    def seekable(self):
        """Return whether object supports random access."""
        return False

    def seek(self, target, whence=0):  # pylint: disable=unused-argument
        """Change stream position."""
        raise OSError("Object not seekable")
    
    def tell(self):
        """Return current stream position."""
        raise OSError("Object not seekable")

    def __init__(self, fhandle, offset, length):
        """
        Initialises the reader to a pack file.
        
        :param fhandle: an open handle to the pack file, must be opened in read and binary mode.
        :param offset: the integer offset where in the fhandle where the object starts.
        :param length: the integer length of the byte stream. 
          The read() method will ensure that you never go beyond the given length.
        """
        assert 'b' in fhandle.mode
        assert 'r' in fhandle.mode

        self._fhandle = fhandle
        self._offset = offset
        self._length = length
        
        # Move to the offset position, and keep track of the internal position
        self._fhandle.seek(self._offset)
        self._update_pos()
    
    def _update_pos(self):
        """Update the internal position variable with the correct value.

        This function must be called (internally) after any operation that 
        moves into the file.
        """
        self._pos = self._fhandle.tell() - self._offset
        assert self._pos <= self._length, RuntimeError(
            "_PackedObjectReader didn't manage to prevent to go beyond the length!")

        assert self._pos >= 0, RuntimeError(
            "_PackedObjectReader didn't manage to prevent to go beyond the length (in the negative direction)!")

    def read(self, size=-1):
        """
        Read and return up to n bytes.

        If the argument is omitted, None, or negative, reads and
        returns all data until EOF (that corresponds to the length specified
        in the __init__ method).

        Returns an empty bytes object on EOF.
        """
        # Check how many bytes are left on this portion of the pack
        # (avoid to go beyond)
        remaining_bytes = self._length-self._pos

        if size is None or size < 0:
            stream = self._fhandle.read(remaining_bytes)
            self._update_pos()
            return stream
        
        # Get the requested bytes, but at most the remaining_bytes
        bytes_to_fetch = min(remaining_bytes, size)
        stream = self._fhandle.read(bytes_to_fetch)
        self._update_pos()
        return stream


class _StreamDecompresser:
    """A class that gets a stream of compressed zlib bytes, and returns the corresponding
    uncompressed bytes when being read via the .read() method.
    """
    
    _CHUNKSIZE = 65536

    def __init__(self, compressed_stream):
        """Create the class from a given compressed bytestream.

        :param compressed_stream: an open bytes stream that supports the .read() method,
          returning a valid compressed stream.
        """
        self._compressed_stream = compressed_stream
        self._decompressor = zlib.decompressobj()
        self._internal_buffer = b''
    
    def read(self, size=-1):
        """
        Read and return up to n bytes.

        If the argument is omitted, None, or negative, reads and
        returns all data until EOF (that corresponds to the length specified
        in the __init__ method).

        Returns an empty bytes object on EOF.
        """
        if size is None or size < 0:
            # Read all the rest: we call ourselves but with a length,
            # and return the joined result
            data = []
            while True:
                next_chunk = self.read(size=self._CHUNKSIZE)
                if not next_chunk:
                    # Empty returned value: EOF
                    break
                data.append(next_chunk)
            # Making a list and joining does many less mallocs, so should be faster
            return b"".join(data)

        if size == 0:
            return b''

        while len(self._internal_buffer) < size:
            next_chunk = self._compressed_stream.read(self._CHUNKSIZE)

            old_unconsumed = self._decompressor.unconsumed_tail

            # In the previous step, I might have some leftover data
            # since I am using the max_size parameter of .decompress()
            compressed_chunk = old_unconsumed + next_chunk
            # The second parameter is max_size. We know that in any case we do
            # not need more than `size` bytes. Leftovers will be left in 
            # .unconsumed_tail and reused a the next loop
            decompressed_chunk = self._decompressor.decompress(compressed_chunk, size)
            self._internal_buffer += decompressed_chunk

            if not next_chunk and not self._decompressor.unconsumed_tail:
                # Nothing to do: no data read, and the unconsumed tail is over.
                # We break.
                break

            if not next_chunk and len(self._decompressor.unconsumed_tail) == len(old_unconsumed):
                raise ValueError(
                    "There is no data in the reading buffer, and we are not consuming the remaining decompressed chunk: "
                    "there must be a problem in the incoming buffer"
                )

        # Note that we could be here also with len(self._internal_buffer) < size,
        # if we used 'break' because the internal buffer reached EOF.
        to_return, self._internal_buffer = self._internal_buffer[:size], self._internal_buffer[size:]

        return to_return


class Container:
    """A class representing a container of objects (which is stored on a disk folder)"""

    _PACK_INDEX_SUFFIX = ".idx"
    _COMPRESSLEVEL = 1
    # Size in bytes of each of the chunks used when (internally) reading or writing in chunks, e.g.
    # when packing.
    _CHUNKSIZE = 65536

    def __init__(self, folder):
        """Create the class that represents the container.
        
        :param folder: the path to a folder that will host this object-store continer.
        """
        self._folder = folder
        self._session = None # Will be populated by the _get_session function

    def get_folder(self):
        """Return the path to the folder that will host the object-store container."""
        return self._folder

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
           is missing, either raise an exception (NotExistent) if this flag is True, or return None
        """
        if not create and not os.path.exists(self._get_pack_index_path()):
            if raise_if_missing:
                raise NotExistent("Pack index does not exist")
            return None

        engine = create_engine('sqlite:///{}'.format(self._get_pack_index_path()))

        # For the next two bindings, see background on 
        # https://docs.sqlalchemy.org/en/13/dialects/sqlite.html#serializable-isolation-savepoints-transactional-ddl
        @event.listens_for(engine, "connect")
        def do_connect(dbapi_connection, connection_record):  # pylint: disable=unused-argument,unused-variable
            # disable pysqlite's emitting of the BEGIN statement entirely.
            # also stops it from emitting COMMIT before any DDL.
            dbapi_connection.isolation_level = None

        @event.listens_for(engine, "begin")
        def do_begin(conn):  # pylint: disable=unused-variable
            # emit our own BEGIN
            conn.execute("BEGIN")

        if create:
            # Create all tables in the engine. This is equivalent to "Create Table"
            # statements in raw SQL.
            Base.metadata.create_all(engine)

        # Bind the engine to the metadata of the Base class so that the
        # declaratives can be accessed through a DBSession instance
        Base.metadata.bind = engine
        
        ## See e.g.
        ##http://pythoncentral.io/introductory-tutorial-python-sqlalchemy/
        DBSession = sessionmaker(bind=engine)
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
        assert self._is_valid_pack_id(pack_id), "Invalid pack ID {}".format(pack_id)
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
            raise ModificationNotAllowed(
                "The container already exists, so you cannot initialise it - "
                "use the clear option if you want to overwrite with a clean one"
            )
 
        os.makedirs(self._folder)

        # Create config file
        with open(self._get_config_file(), 'w') as fhandle:
            json.dump({
                'container_version': 1, # For future compatibility, this is the version of the format
                'loose_prefix_len': loose_prefix_len,
                'pack_prefix_len': pack_prefix_len
            }, fhandle)

        for folder in [self._get_pack_folder(), self._get_loose_folder(), self._get_sandbox_folder()]:
            if not os.path.exists(folder):
                os.makedirs(folder)
        
        self._get_session(create=True)

    def _get_repository_config(self):
        """Return the repository config."""
        if not self.is_initialised:
            raise NotInitialised("The container is not initialised yet - use .init_container() first")
        with open(self._get_config_file()) as fhandle:
            config = json.load(fhandle)
        return config

    @property
    def loose_prefix_len(self):
        if not hasattr(self, '_loose_prefix_len'):
            self._loose_prefix_len = self._get_repository_config()['loose_prefix_len']
        return self._loose_prefix_len

    @property
    def pack_prefix_len(self):
        if not hasattr(self, '_pack_prefix_len'):
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
        session = self._get_cached_session()
        obj = session.query(Obj).filter(Obj.uuid==uuid).one_or_none()

        if obj is not None: # packed object
            pack_id = self._split_uuid_for_pack(uuid)[0]
            obj_path = self._get_pack_path_from_pack_id(pack_id)
            with open(obj_path, 'rb') as fhandle:
                obj_reader = _PackedObjectReader(fhandle=fhandle, offset=obj.offset, length=obj.length)
                if obj.compressed:
                    yield _StreamDecompresser(obj_reader)
                else:
                    yield obj_reader
        else:
            # It might be loose
            obj_path = self._get_loose_path_from_uuid(uuid=uuid)
            if not os.path.exists(obj_path):
                raise NotExistent("No object with UUID {}".format(uuid))
            with open(obj_path, 'rb') as fhandle:
                yield fhandle

    @contextmanager  # noqa: MC0001
    def get_object_streams(self, uuids, skip_if_missing=True):  
        """A context manager returning a generator yielding pairs of (uuid, open stream).

        :note: the UUIDs yielded are often in a *different* order than the original
            ``uuids`` list. This is done for efficiency reasons, to reduce to a minimum
            file opening and to try to read file chunks (for packs) in sequential 
            order rather than in random order.

        To use it, you should do something like the following::

            with container.get_object_streams(uuids=uuids) as uuid_stream_pairs:
                for obj_uuid, stream in uuid_stream_pairs:
                    if stream is None:
                        # This should happen only if you pass skip_if_missing=False to ``get_object_streams``
                        retrieved[obj_uuid] = None
                    else:
                        retrieved[obj_uuid] = stream.read()

        :param uuids: a list of UUIDs for which we want to get a stream reader
        :param skip_if_missing: if True, just skip UUIDs that are not in the container
            (i.e., neither packed nor loose). If False, return ``None`` instead of the
            stream. In this latter case, the length of the generator returned by this context
            manager has always the same length as the input ``uuids`` list.
        """

        def get_object_stream_generator(uuids, last_open_file, skip_if_missing):  # pylint: disable=too-many-branches
            """Return a generator yielding pairs of (uuid, open stream).

            :note: The stream is already open and at the right position, and can
                just be read.

            :param uuids: a list of UUIDs for which we want to get a stream reader
            :param last_open_file: must be a list of length one, initialised with None.
                During the run, the first (and only) element of the list is updated
                with the currently open file.
                When the generator is exhausted, the file is closed (but the outer
                context manager will still close the file, if it's open - this is needed
                if the caller of ``get_object_streams`` exits the ``with`` context manager
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
                        res[0]: (res[1], res[2], res[3])
                        for res in session.query(Obj).filter(
                        Obj.uuid.in_(obj_uuids)).with_entities(
                            Obj.uuid, Obj.offset, Obj.length, Obj.compressed).order_by(Obj.offset)
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
                            obj_reader = _PackedObjectReader(
                                fhandle=last_open_file[0],
                                offset=metadata[0],
                                length=metadata[1])
                            if metadata[2]:
                                obj_reader = _StreamDecompresser(obj_reader)
                            yield obj_uuid, obj_reader

                for loose_uuid in set(uuids).difference(uuids_in_packs):
                    obj_path = self._get_loose_path_from_uuid(uuid=loose_uuid)
                    if not os.path.exists(obj_path):
                        if skip_if_missing:
                            continue
                        yield loose_uuid, None
                        continue
                    if last_open_file[0] is not None:
                        if not last_open_file[0].closed:
                            last_open_file[0].close()
                    last_open_file[0] = open(obj_path, mode='rb')
                    yield loose_uuid, last_open_file[0]
            finally:
                if last_open_file[0] is not None:
                    last_open_file[0].close()

        # I want it to be a list of length 1 to make sure I actually have a reference to it
        last_open_file = [None]

        yield get_object_stream_generator(
            uuids=uuids, last_open_file=last_open_file, skip_if_missing=skip_if_missing)        

        if last_open_file[0] is not None:
            if not last_open_file[0].closed:
                last_open_file[0].close()

    def get_object_contents(self, uuids, skip_if_missing=True):
        """Get the content of a number of objects with given UUIDs.

        :note: use this method only if you know objects fit in memory.
            Otherwise, use the ``get_object_streams`` context manager and
            process the objects one by one.

        :param uuids: A list of UUIDs of the objects to retrieve.
        :return: a dictionary of byte streams where the keys are the UUIDs and the values
            are the object contents.
        """
        retrieved = {}
        with self.get_object_streams(uuids=uuids, skip_if_missing=skip_if_missing) as uuid_stream_pairs:
            for obj_uuid, stream in uuid_stream_pairs:
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
        return _ObjectWriter(
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

        retval['pack_files'] = len([pack_id for pack_id in self._list_packs()])

        return retval

    def _is_valid_pack_id(self, pack_id):
        """Return True if the name is a valid pack ID."""
        if len(pack_id) != self.pack_prefix_len:
            return False
        if not all(char in "0123456789abcdef" for char in pack_id):
            return False
        return True

    def _is_valid_loose_prefix(self, prefix):
        """Return True if the name is a valid prefix."""
        if len(prefix) != self.loose_prefix_len:
            return False
        if not all(char in "0123456789abcdef" for char in prefix):
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
        retval['total_size_packed'] = session.query(
            func.coalesce(func.sum(Obj.size), 0).label("total_size_packed")).all()[0][0]
        retval['total_size_packed_on_disk'] = session.query(
            func.coalesce(func.sum(Obj.length), 0).label("total_length_packed")).all()[0][0]

        total_size_packfiles_on_disk = 0
        for pack_id in list(self._list_packs()):
            total_size_packfiles_on_disk += os.path.getsize(
                self._get_pack_path_from_pack_id(pack_id))
        retval['total_size_packfiles_on_disk'] = total_size_packfiles_on_disk

        retval['total_size_packindexes_on_disk'] = os.path.getsize(
                self._get_pack_index_path())

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
                for second_level in os.listdir(os.path.join(
                        self._get_loose_folder(),
                        first_level)):
                    yield "{}{}".format(first_level, second_level)
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
                                pack_handle=pack_handle, read_handle=loose_handle, compress=compress)
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
                                pack_handle=pack_handle, read_handle=stream, compress=compress)
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
