from sqlalchemy import create_engine

from ..objectstore.container import Container
from .models import Base, Folder, File

class ObjectExists(Exception):
    pass

class FileTracker:

    def __init__(self, db_user, db_name, db_password, folder, db_port=5432, db_host="localhost"): # pylint: disable=too-many-arguments
        self._container = Container(folder=folder)
        if not self._container.is_initialised:
            self._container.init_container(pack_prefix_len=2, loose_prefix_len=2)
        self._db_user = db_user
        self._db_name = db_name
        self._db_password = db_password
        self._db_host = db_host
        self._db_port = db_port
        self._session = None
        self._initialize_db()

    def _initialize_db(self):
        self._get_session(create=True)

    def drop_db(self):
        session = self._get_cached_session()
        session.query(File).delete()
        session.query(Folder).delete()
        session.commit()

    def _get_session(self, create=False):
        """Return a new session to connect to the pack-index SQLite DB."""
        from sqlalchemy.orm import sessionmaker

        engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
            self._db_user, self._db_password, self._db_host, self._db_port, self._db_name
        ))

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

    def _get_file_from_path(self, relpath):
        pieces = relpath.split('/')
        if len(pieces) == 1:
            folders = []
            filename = pieces[0]
        else:
            folders = pieces[:-1]
            filename = pieces[-1]
        
        parent = None
        for folder in folders:
            parent = self._get_folder(parent=parent, name=folder)
        file = self._get_file(parent=parent, name=filename)
        return file

    def _get_folder_from_path(self, relpath):
        pieces = relpath.split('/')
        
        parent = None
        for folder in pieces:
            parent = self._get_folder(parent=parent, name=folder)
        return parent

    def _get_folder(self, parent, name):
        session = self._get_cached_session()
        return session.query(Folder).filter(Folder.parent==parent, Folder.name==name).one()
    
    def _get_file(self, parent, name):
        session = self._get_cached_session()
        return session.query(File).filter(File.parent==parent, File.name==name).one()
    
    def _get_file_content(self, file):
        return self._container.get_object_content(file.object_id)
    
    def get_file_content_from_path(self, relpath):
        return self._get_file_content(self._get_file_from_path(relpath))

    def _add_folder(self, name, parent, existing_ok=False):
        session = self._get_cached_session()
        folder = session.query(Folder).filter(Folder.name==name, Folder.parent==parent).one_or_none()
        if folder is not None:
            if existing_ok:
                return folder
            else:
                raise ObjectExists("Folder '{}' exists!".format(folder.get_relpath()))
        folder = Folder(name=name, parent=parent)
        session.add(folder)
        return folder
    
    def _add_file(self, name, parent, content):
        session = self._get_cached_session()
        file = session.query(File).filter(File.name==name, File.parent==parent).one_or_none()
        if file is not None:
            raise ObjectExists("File '{}' exists!".format(file.get_relpath()))

        object_id = self._container.add_object(content)
        file = File(name=name, parent=parent, object_id=object_id)
        session.add(file)
        return file

    def add_file_from_path(self, relpath, content):
        session = self._get_cached_session()

        pieces = relpath.split('/')
        if len(pieces) == 1:
            folders = []
            filename = pieces[0]
        else:
            folders = pieces[:-1]
            filename = pieces[-1]

        parent = None
        for folder in folders:
            parent = self._add_folder(name=folder, parent=parent, existing_ok=True)
        self._add_file(name=filename, parent=parent, content=content)

        session.commit()

    def mkdir(self, relpath, recursive=False, existing_ok=False):
        session = self._get_cached_session()

        pieces = relpath.split('/')
        
        if recursive:
            parent = None
            for folder in pieces[:-1]:
                parent = self._add_folder(parent=parent, name=folder, existing_ok=True)
        else:
            parent = self._get_folder_from_path('/'.join(pieces[:-1]))
    
        folder = self._add_folder(parent=parent, name=pieces[-1], existing_ok=existing_ok)
        session.commit()

    def _get_subitems(self, folder):
        if folder is not None:
            subfolders = folder.subfolders
            files = folder.files
        else:
            session = self._get_cached_session()
            subfolders = session.query(Folder).filter(Folder.parent==None).all()
            files = session.query(File).filter(File.parent==None).all()
        return subfolders, files

    def _internal_ls(self, folder, recursive, indent=0):
        subfolders, files = self._get_subitems(folder)
        for subfolder in subfolders:
            print('{}{}/'.format(" "*indent, subfolder.name))
            if recursive:
                self._internal_ls(subfolder, recursive=True, indent=indent+2)
        for file in files:
            print('{}{}'.format(" "*indent, file.name))

    def ls(self, relpath, recursive=False):
        if relpath == '' or relpath == '/':
                folder = None
        else:
            folder = self._get_folder_from_path(relpath)
        self._internal_ls(folder, recursive=recursive)

    def mkdirs(self, relpaths, recursive=False, existing_ok=False):
        session = self._get_cached_session()

        for relpath in relpaths:
            pieces = relpath.split('/')
            
            if recursive:
                parent = None
                for folder in pieces[:-1]:
                    parent = self._add_folder(parent=parent, name=folder, existing_ok=True)
            else:
                parent = self._get_folder_from_path('/'.join(pieces[:-1]))
        
            folder = self._add_folder(parent=parent, name=pieces[-1], existing_ok=existing_ok)

        session.commit()

    def mkdirs_root_nocheck(self, names):
        session = self._get_cached_session()

        for name in names:        
            folder = Folder(name=name, parent=None)
            session.add(folder)

        session.commit()