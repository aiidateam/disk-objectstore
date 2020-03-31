import os
import uuid

from collections import defaultdict
from contextlib import contextmanager
from sqlalchemy import create_engine

#from sqlalchemy.exc import IntegrityError

from .models import Base, Obj, FileRef

def get_new_uuid():
    """Utility function to generate a new UUID.

    In this way all parts of the code that need to do it, will do it in the same
    way.
    """
    return str(uuid.uuid4())

class _FileWriter:
    def __init__(self, container, filename, commit_on_exit=True):
        self._container = container
        self._uuid = get_new_uuid()
        self._filename = filename
        self._commit_on_exit = commit_on_exit
        self._created = False

    def __enter__(self):
        # TODO: test this
        if self._created:
            raise RuntimeError("Cannot recreate existing file")
        self._obj_path = self._container._get_path_from_uuid(self._uuid, packed=False)
        self._filehandle = open(self._obj_path, 'wb')
        return self._filehandle

    def __exit__(self, exc_type, value, traceback):
        if not self._filehandle.closed:
            self._filehandle.close()

        if exc_type is None:    
            obj = Obj(
                uuid=self._uuid, 
                packed=False)
            self._container._get_cached_session().add(obj)
            fileref = FileRef(
                obj = obj,
                relpath=self._filename # one could think to have a path or other
            )
            self._container._get_cached_session().add(fileref)

            if self._commit_on_exit:
                self._container._get_cached_session().commit()
            self._created = True
        else:
            # TODO add test to check that this works
            if os.path.exists(self._obj_path):
                os.remove(self._obj_path)

class Container:
    """A class representing a container of objects (which is stored on a disk folder)"""

    def __init__(self, folder, prefix_len=2):
        """Create the class that represents the container.
        
        :param folder: the path to a folder that will host this object-store continer.
        :param prefix_len: The length of the prefix of the packed objects.
          The longer the length, the more packs will be created. Suggested
          values: 2 or 3.
        """
        self._folder = folder
        self._prefix_len = prefix_len
        self._session = None # Will be created the first time it's needed and cached.

    def get_folder(self):
        """Return the path to the folder that will host the object-store container."""
        return self._folder
    
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
            return os.path.join(self._get_pack_folder(), uuid[:self._prefix_len])
        return os.path.join(self._get_loose_folder(), uuid)

    def init_container(self, clear=False):
        """Initialise the container folder, if not already done.

        If this is called multiple times, it does not corrupt the data,
        unless you add the ``clear=True`` option.

        :param clear: if True, delete everything in the container and
          initialise a new, empty one.
        """
        import shutil

        if clear:
            if os.path.exists(self._folder):
                shutil.rmtree(self._folder)
        if not os.path.exists(self._folder):
            os.makedirs(self._folder)

        # Use the side-effect of the _get_session function 
        # to create the SQLite DB file
        self._get_session(create=True)
        for folder in [self._get_pack_folder(), self._get_loose_folder()]:
            if not os.path.exists(folder):
                os.makedirs(folder)

    def get_file_content(self, filename):
        obj = self._get_cached_session().query(Obj).join(FileRef).filter(
            FileRef.relpath==filename).one()
        obj_path = self._get_path_from_uuid(uuid=obj.uuid, packed=obj.packed)
        if obj.packed:
            with open(obj_path, 'rb') as fhandle:
                fhandle.seek(obj.offset)
                return fhandle.read(obj.length)        
        else:
            with open(obj_path, 'rb') as fhandle:
                return fhandle.read()
    
    def _new_file_writer(self, filename, commit_on_exit=True):
        """Return a context manager that can be used to create a new object.

        To use it, do the following::

          new_file_writer = repo._new_file_writer('some_file_name.txt')
          with new_file_writer as fhandle:
              fhandle.write(b'something')
        """
        return _FileWriter(self, filename, commit_on_exit=commit_on_exit)
    
    def add_file(self, filename, content):
        """Add a loose file.
        
        :param filename: the object filename.
        :param content: a binary stream with the file content.
        """
        with self._new_file_writer(filename=filename) as fhandle:
            fhandle.write(content)

    def add_files(self, dict_of_files):
        """Add more than one loose file at the same time.
        
        :param dict_of_files: a dictionary where keys are the filenames and 
          the values are the bytestream.
        """
        for filename, content in dict_of_files.items():
            with self._new_file_writer(
                    filename=filename, commit_on_exit=False) as fhandle:
                fhandle.write(content)
        self._get_cached_session().commit()

    def count_objects(self):
        """Return a dictionary with the count of objects, keys are 'loose' and 'packed'.
        
        Also return a number of packs under 'pack_files', and a number of
        loose objects 'loose_files'."""
        retval = {}

        number_packed = self._get_cached_session().query(FileRef).join(Obj).filter(
            Obj.packed==True).count()  # noqa
        retval['packed'] = number_packed

        number_loose = self._get_cached_session().query(FileRef).join(Obj).filter(
            Obj.packed==False).count()  # noqa
        retval['loose'] = number_loose

        retval['loose_files'] = len(os.listdir(self._get_loose_folder()))
        retval['pack_files'] = len([fname for fname in os.listdir(self._get_loose_folder())
            if self._is_valid_pack_id(fname)])

        return retval

    def _is_valid_pack_id(self, pack_id):
        """Return True if the name is a valid pack ID."""
        if len(pack_id) != self._prefix_len:
            return False
        if not all(char in "0123456789abcdef" for char in pack_id):
            return False
        return True

    def get_total_size(self):
        """Return a dictionary with the total size of objects in the container."""
        retval = {}

        total_size_packed = self._get_cached_session().query(FileRef).join(Obj).filter(
            Obj.packed==True).with_entities(Obj.length).all()  # noqa
        if not total_size_packed:
            total_size_packed = 0
        else:
            total_size_packed = sum(res[0] for res in total_size_packed)
        retval['total_size_packed'] = total_size_packed

        total_size_loose = 0
        for obj in self._get_cached_session().query(FileRef).join(Obj).filter(
                Obj.packed==False).with_entities(Obj).all():  # noqa
            loose_path = self._get_path_from_uuid(obj.uuid, packed=False)
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
    
    def pack_all_loose(self):
        """Pack all loose objects.

        This is a maintenance operation, needs to be done only by one process.
        """
        packs = defaultdict(list)
        for obj in self._get_cached_session().query(Obj).filter(
            Obj.packed==False).with_entities( # noqa
                Obj.uuid, Obj.id).all():
            packs[obj[0][:self._prefix_len]].append(obj)
        for pack_id, loose_objects in packs.items():
            # Avoid concurrent writes        
            with self.lock_pack(pack_id) as pack_handle:
                for obj_uuid, obj_id in loose_objects:
                    obj = self._get_cached_session().query(Obj).get(obj_id)
                    obj.offset = pack_handle.tell()
                    with open(self._get_path_from_uuid(obj_uuid, packed=False), 'rb') as loose_handle:
                        pack_handle.write(loose_handle.read())
                    obj.length = pack_handle.tell() - obj.offset
                    obj.packed = True
                    self._get_cached_session().add(obj)
            self._get_cached_session().commit()
            
            # Clean up loose objects
            for obj_uuid, obj_id in loose_objects:
                os.remove(self._get_path_from_uuid(obj_uuid, packed=False))

    def add_files_to_pack(self, dict_of_files):
        """Add files directly to a pack.
        
        This is a maintenance operation, available mostly for efficiency reasons
        e.g. if you are creating a container from scratch.
        As such, it needs to be done only by one process.
        
        :param dict_of_files: a dictionary where keys are the filenames and 
          the values are the bytestream.
        """
        packs = defaultdict(list)
        for filename in dict_of_files:
            obj_uuid = get_new_uuid()
            packs[obj_uuid[:self._prefix_len]].append((filename, obj_uuid)) 
        for pack_id, filenames in packs.items():
            # Avoid concurrent writes        
            with self.lock_pack(pack_id) as pack_handle:
                for filename, obj_uuid in filenames:
                    obj = Obj(
                        uuid=obj_uuid,  
                        packed=True)
                    obj.offset = pack_handle.tell()
                    pack_handle.write(dict_of_files[filename])
                    obj.length = pack_handle.tell() - obj.offset
                    self._get_cached_session().add(obj)
                    fileref = FileRef(
                        obj = obj,
                        relpath=filename # one could think to have a path or other
                    )
                    self._get_cached_session().add(fileref)
            self._get_cached_session().commit()