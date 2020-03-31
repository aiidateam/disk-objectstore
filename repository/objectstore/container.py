import zlib
import os
import shutil
import uuid

from collections import defaultdict
from contextlib import contextmanager
from sqlalchemy import create_engine

from sqlalchemy.sql import func

from .models import Base, Obj

class NotExistent(Exception):
    """Raised if the request object does not exist."""

class ModificationNotAllowed(Exception):
    """Raised if the you cannot modify the given object but you are trying to do so."""

def get_new_uuid():
    """Utility function to generate a new UUID.

    In this way all parts of the code that need to do it, will do it in the same
    way.
    """
    return str(uuid.uuid4())

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

class Container:
    """A class representing a container of objects (which is stored on a disk folder)"""

    def __init__(self, folder, pack_prefix_len=2, loose_prefix_len=2):
        """Create the class that represents the container.
        
        :param folder: the path to a folder that will host this object-store continer.
        :param pack_prefix_len: The length of the prefix of the packed objects.
          The longer the length, the more packs will be created. Suggested
          values: 2 or 3.
        :param loose_prefix_len: The length of the prefix of the loose objects.
          The longer the length, the more folders will be used to store loose
          objects. Suggested values: 0 (for not using subfolders) or 2.
        """
        self._folder = folder
        self._pack_prefix_len = pack_prefix_len
        self._loose_prefix_len = loose_prefix_len
        self._session = None # Will be created the first time it's needed and cached.

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
    
    def _get_pack_index(self):
        """Return the path to the SQLite file containing the index of packed objects."""
        return os.path.join(self._folder, 'pack-index.sqlite')
    
    def _get_session(self, create=False):
        """Return a new session to connect to the pack-index SQLite DB."""
        from sqlalchemy.orm import sessionmaker

        engine = create_engine('sqlite:///{}'.format(self._get_pack_index()))

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
        # A DBSession() instance establishes all conversations with the database
        # and represents a "staging zone" for all the objects loaded into the
        # database session object. Any change made against the objects in the
        # session won't be persisted into the database until you call
        # session.commit(). If you're not happy about the changes, you can
        # revert all of them back to the last commit by calling
        # session.rollback()
        session = DBSession()

        return session
    
    def _get_cached_session(self):
        """Return the SQLAlchemy session to access the SQLite file,
        reusing the same one."""
        if self._session is None:
            self._session = self._get_session(create=False)
        return self._session

    def _get_path_from_uuid(self, uuid, packed):
        """Return the path of the file on disk containing the data of a given UUID.
        
        :param uuid: the UUID of the object to get.
        :param packed: flag to specify if we expect a packed object or not.
        """
        if packed:
            return os.path.join(self._get_pack_folder(), uuid[:self._pack_prefix_len])
        
        # loose
        if self._loose_prefix_len:
            return os.path.join(
                self._get_loose_folder(),
                uuid[:self._loose_prefix_len],
                uuid[self._loose_prefix_len:],
                )
        return os.path.join(self._get_loose_folder(), uuid)

    def init_container(self, clear=False):
        """Initialise the container folder, if not already done.

        If this is called multiple times, it does not corrupt the data,
        unless you add the ``clear=True`` option.

        :param clear: if True, delete everything in the container and
          initialise a new, empty one.
        """
        if clear:
            if os.path.exists(self._folder):
                shutil.rmtree(self._folder)
        if not os.path.exists(self._folder):
            os.makedirs(self._folder)

        # Use the side-effect of the _get_session function 
        # to create the SQLite DB file
        self._get_session(create=True)
        for folder in [self._get_pack_folder(), self._get_loose_folder(), self._get_sandbox_folder()]:
            if not os.path.exists(folder):
                os.makedirs(folder)

    def get_object_content(self, uuid):
        """Get the content of an object with a given UUID.

        :param uuid: The UUID of the object to retrieve.
        """
        obj = self._get_cached_session().query(Obj).filter(
            Obj.uuid==uuid).one_or_none()
        if obj is not None: # packed object
            obj_path = self._get_path_from_uuid(uuid=uuid, packed=True)
            with open(obj_path, 'rb') as fhandle:
                fhandle.seek(obj.offset)
                raw_content = fhandle.read(obj.length)
                if obj.compressed:
                    return zlib.decompress(raw_content)
                return raw_content
        else:
            # It might be loose
            obj_path = self._get_path_from_uuid(uuid=uuid, packed=False)
            if not os.path.exists(obj_path):
                raise NotExistent("No object with UUID {}".format(uuid))
            with open(obj_path, 'rb') as fhandle:
                return fhandle.read()
    
    def _new_object_writer(self):
        """Return a context manager that can be used to create a new object.

        To use it, do the following::

          new_object_writer = repo._new_object_writer()
          with new_object_writer as fhandle:
              fhandle.write(b'something')
          new_uuid = new_objct_writer.uuid()
        """
        return _ObjectWriter(
            sandbox_folder=self._get_sandbox_folder(),
            loose_folder=self._get_loose_folder(),
            loose_prefix_len=self._loose_prefix_len
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
        for loose_uuid in self._list_loose():
            retval['loose'] += 1

        retval['pack_files'] = len([fname for fname in os.listdir(self._get_pack_folder())
            if self._is_valid_pack_id(fname)])

        return retval

    def _is_valid_pack_id(self, pack_id):
        """Return True if the name is a valid pack ID."""
        if len(pack_id) != self._pack_prefix_len:
            return False
        if not all(char in "0123456789abcdef" for char in pack_id):
            return False
        return True

    def _is_valid_loose_prefix(self, prefix):
        """Return True if the name is a valid prefix."""
        if len(prefix) != self._loose_prefix_len:
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
        - total_size_loose: size of the loose objects in the packs (always uncompressed).
        """
        retval = {}

        retval['total_size_packed'] = self._get_cached_session().query(
            func.sum(Obj.size).label("total_size_packed")).all()[0][0]

        retval['total_size_packed_on_disk'] = self._get_cached_session().query(
            func.sum(Obj.length).label("total_size_packed")).all()[0][0]

        total_size_packfiles_on_disk = 0
        packfiles = [fname for fname in os.listdir(self._get_pack_folder())
            if self._is_valid_pack_id(fname)]
        for packfile in packfiles:
            total_size_packfiles_on_disk += os.path.getsize(
                os.path.join(self._get_pack_folder(), packfile))
        retval['total_size_packfiles_on_disk'] = total_size_packfiles_on_disk

        total_size_loose = 0
        for loose_uuid in self._list_loose():
            loose_path = self._get_path_from_uuid(loose_uuid, packed=False)
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
        with open(lock_file, 'x'):
            try:
                # TODO: next line, duplication of logic with _get_path_from_uuid
                pack_file = os.path.join(self._get_pack_folder(), pack_id)
                with open(pack_file, 'ab') as pack_handle:
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
            if self._loose_prefix_len:
                if not self._is_valid_loose_prefix(first_level):
                    continue
                for second_level in os.listdir(os.path.join(
                        self._get_loose_folder(),
                        first_level)):
                    yield "{}{}".format(first_level, second_level)
            else:
                # It's flat (loose_prefix_len == 0)
                yield first_level

    def pack_all_loose(self, compress=False):
        """Pack all loose objects.

        This is a maintenance operation, needs to be done only by one process.
        :param compress: if True, compress objects before storing them.
        """
        compresslevel = 1

        packs = defaultdict(list)
        for loose_uuid in self._list_loose():
            packs[loose_uuid[:self._pack_prefix_len]].append(loose_uuid)
        for pack_id, loose_objects in packs.items():
            # Avoid concurrent writes        
            with self.lock_pack(pack_id) as pack_handle:
                for obj_uuid in loose_objects:
                    obj = obj = Obj(uuid=obj_uuid)
                    obj.compressed = compress                    
                    obj.offset = pack_handle.tell()
                    obj.size = os.path.getsize(self._get_path_from_uuid(obj_uuid, packed=False))
                    with open(self._get_path_from_uuid(obj_uuid, packed=False), 'rb') as loose_handle:
                        if compress:
                            pack_handle.write(zlib.compress(loose_handle.read(), level=compresslevel))
                        else:
                            pack_handle.write(loose_handle.read())
                    obj.length = pack_handle.tell() - obj.offset
                    self._get_cached_session().add(obj)
            self._get_cached_session().commit()
            
            # Clean up loose objects
            for obj_uuid in loose_objects:
                os.remove(self._get_path_from_uuid(obj_uuid, packed=False))

    def add_objects_to_pack(self, content_list):
        """Add objects directly to a pack.
        
        This is a maintenance operation, available mostly for efficiency reasons
        e.g. if you are creating a container from scratch.
        As such, it needs to be done only by one process.
        
        :param content_list: a list of bytestreams to add.
        :return: a list of object UUIDs
        """
        packs = defaultdict(list)
        uuids = []

        for pos in range(len(content_list)):
            obj_uuid = get_new_uuid()
            uuids.append(obj_uuid)
            packs[obj_uuid[:self._pack_prefix_len]].append((pos, obj_uuid)) 
        for pack_id, obj_ids in packs.items():
            # Avoid concurrent writes        
            with self.lock_pack(pack_id) as pack_handle:
                for pos, obj_uuid in obj_ids:
                    obj = Obj(uuid=obj_uuid)
                    obj.offset = pack_handle.tell()
                    pack_handle.write(content_list[pos])
                    obj.length = pack_handle.tell() - obj.offset
                    self._get_cached_session().add(obj)
            self._get_cached_session().commit()

        return uuids
