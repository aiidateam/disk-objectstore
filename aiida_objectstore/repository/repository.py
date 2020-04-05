import collections
import enum
import os
import time
from sqlalchemy import create_engine

from ..objectstore.container import Container
from .models import DbNodeRepo, Base
from ..utils import LazyOpener


class FileType(enum.Enum):
    
    DIRECTORY = 0
    FILE = 1


File = collections.namedtuple('File', ['name', 'type'])


class Repository:

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
        session.query(DbNodeRepo).delete()
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
    
    @property
    def container(self):
        return self._container

    def _get_cached_session(self):
        """Return the SQLAlchemy session to access the SQLite file,
        reusing the same one."""
        if self._session is None:
            self._session = self._get_session(create=False)
        return self._session

    def get_node_repository(self, node_uuid):
        return NodeRepository(
            node_uuid=node_uuid,
            container=self._container,
            folder_meta=self._get_folder_meta(node_uuid))

    def get_all_node_uuids(self):
        session = self._get_cached_session()
        all_uuids = []
        for res in session.query(DbNodeRepo).with_entities(DbNodeRepo.node_uuid):
            all_uuids.append(res[0])
        return all_uuids

    def get_node_repositories(self, node_uuids):
        folder_metas = self._get_folder_metas(node_uuids)

        return [NodeRepository(node_uuid=node_uuid,
            container=self._container,
            folder_meta=folder_metas[node_uuid]) for node_uuid in node_uuids]

    def _get_folder_metas(self, node_uuids):
        return dict(self._get_cached_session().query(DbNodeRepo).filter(
            DbNodeRepo.node_uuid.in_(node_uuids)).with_entities(DbNodeRepo.node_uuid, DbNodeRepo.folder_meta))

    def _get_folder_meta(self, node_uuid):
        return self._get_cached_session().query(DbNodeRepo).filter(DbNodeRepo.node_uuid==node_uuid).one().folder_meta

    def _prepare_for_node_addition(self, folder_path):
        folder_meta = {'dir': {}}

        # keys will be (tuple_of_dir_pieces, filename) and value will be a LazyOpener object, pointing
        # to the correct object
        files_to_write = {}

        # Create the "template" for the folder_meta JSON (using None instead of the object ID,
        # but tracking which files need to be stored as objects in `files_to_write`)
        for dirpath, dirnames, filenames in os.walk(folder_path):
            this_dir = os.path.relpath(dirpath, start=folder_path)
            element = folder_meta['dir']
            dir_pieces = []
            if this_dir:
                dir_pieces = this_dir.split(os.path.sep)
                for piece in dir_pieces:
                    if this_dir == os.curdir:
                        continue
                    element = element[piece]['dir']
            for dirname in dirnames:
                element[dirname] = {'dir': {}}
            for filename in filenames:
                original_path = os.path.join(dirpath, filename)
                element[filename] = {
                    'obj': None}
                files_to_write[(tuple(dir_pieces), filename)] = LazyOpener(original_path)

        return folder_meta, files_to_write

    def create_repo_for_nodes(self, folder_paths, compress):  # pylint: disable=too-many-locals
        folder_metas = {}
        files_to_write = {}

        start = time.time()
        for node_uuid, folder_path in folder_paths.items():
            # Write all files in `files_to_write` in a bulk operation
            folder_metas[node_uuid], files_to_write[node_uuid] = self._prepare_for_node_addition(folder_path)

        paths = []
        streams = []
        for node_uuid, node_files_to_write in files_to_write.items():
            for path, stream in node_files_to_write.items():
                paths.append((node_uuid, path))
                streams.append(stream)
        tot_time = time.time() - start
        print("Time to list all files to import ({} nodes): {:.3f} s".format(
            len(folder_metas), tot_time))

        start = time.time()
        obj_uuids = self._container.add_streamed_objects_to_pack(
            streams, compress=compress, open_streams=True)
        tot_time = time.time() - start
        print("Time to store {} files directly to packs: {:.3f} s".format(len(obj_uuids), tot_time))

        start = time.time()
        paths_for_node = collections.defaultdict(dict)

        # Regroup by node UUID
        for obj_uuid, (node_uuid, path) in zip(obj_uuids, paths):
            paths_for_node[node_uuid][path] = obj_uuid

        # Update the object UUIDs of the files in the folder_meta dictionary
        for node_uuid, paths in paths_for_node.items():
            for (dir_pieces, filename), obj_uuid in paths.items():
                folder_meta = folder_metas[node_uuid]
                element = folder_meta['dir']
                for piece in dir_pieces:
                    element = element[piece]['dir']
                element[filename]['obj'] = obj_uuid

        # Store the folder_meta to the postgres DB
        session = self._get_cached_session()
        for node_uuid, folder_meta in folder_metas.items():
            # Store the JSON in the DBNodeRepo table
            # If something breaks, the files will be in the object store,
            # but one can have a clean-up step
            db_node_repo = DbNodeRepo(
                node_uuid=node_uuid,
                folder_meta=folder_meta)
            session.add(db_node_repo)
        # Nodes with no files 
        #Single commit, at the end
        session.commit()
        tot_time = time.time() - start
        print("Time to commit folder_meta for {} nodes (note: only {} with files) to postgres: {:.3f} s".format(
            len(folder_metas), len(paths_for_node), tot_time))

class NodeRepository:
    def __init__(self, node_uuid, container, folder_meta):
        self._node_uuid = node_uuid
        self._container = container
        self._folder_meta = folder_meta

    @property
    def node_uuid(self):
        return self._node_uuid

    def _get_obj_uuids_for_meta_dir(self, meta_dir):
        obj_uuids = []
        for subelement in meta_dir.values():
            if 'obj' in subelement:
                obj_uuids.append(subelement['obj'])
            else:
                obj_uuids += self._get_obj_uuids_for_meta_dir(subelement['dir'])
        return obj_uuids

    def get_all_obj_uuids(self):
        return self._get_obj_uuids_for_meta_dir(self._folder_meta['dir'])

    def list_objects(self, key=None):
        """Return a list of the objects contained in this repository, optionally in the given sub directory.

        :param key: fully qualified identifier for the object within the repository
        :return: a list of `File` named tuples representing the objects present in directory with the given key
        """
        objects = []

        this_dir = key or ''
        this_dir = os.path.normpath(this_dir)
        element = self._folder_meta['dir']
        dir_pieces = []
        try:
            if this_dir:
                dir_pieces = this_dir.split(os.path.sep)
                for piece in dir_pieces:
                    if this_dir == os.curdir:
                        continue
                    element = element[piece]['dir']
        except KeyError:
            raise IOError("{} not found in node {}".format(this_dir, self.node_uuid))

        for name, metadata in element.items():
            if 'dir' in metadata:
                objects.append(File(name, FileType.DIRECTORY))
            elif 'obj' in metadata:
                objects.append(File(name, FileType.FILE))
            else:
                raise RuntimeError("Invalid object in the folder_meta, neither a folder nor a file: {}".format(element))
        
        return objects

    def list_object_names(self, key=None):
        """Return a list of the object names contained in this repository, optionally in the given sub directory.

        :param key: fully qualified identifier for the object within the repository
        :return: a list of `File` named tuples representing the objects present in directory with the given key
        """
        return [obj.name for obj in self.list_objects(key=key)]
        
    def open(self, key):
        """Open a file handle to an object stored under the given key.

        # TODO: reinstate the 'mode' keyword
        # NOTE THIS CHANGES THE API! THIS NOW RETURNS A CONTEXT MANAGER

        :param key: fully qualified identifier for the object within the repository
        :param mode: the mode under which to open the handle
        """
        this_dir = key or ''
        this_dir = os.path.normpath(this_dir)
        element = self._folder_meta['dir']
        lastobj_name = '/'
        lastobj_meta = element
        if this_dir:
            dir_pieces = this_dir.split(os.path.sep)
            dir_pieces, lastobj_name = dir_pieces[:-1], dir_pieces[-1]
            try:
                for piece in dir_pieces:
                    if this_dir == os.curdir:
                        continue
                    element = element[piece]['dir']
                lastobj_meta = element[lastobj_name]
            except KeyError:
                raise IOError("{} not found in node {}".format(this_dir, self.node_uuid))

        if 'obj' not in lastobj_meta:
            raise IOError("{} is not a file in node {}".format(this_dir, self.node_uuid))

        obj_uuid = lastobj_meta['obj']
        return self._container.get_object_stream(obj_uuid)


    def get_object(self, key):
        """Return the object identified by key.

        :param key: fully qualified identifier for the object within the repository
        :return: a `File` named tuple representing the object located at key
        :raises IOError: if no object with the given key exists
        """
        this_dir = key or ''
        this_dir = os.path.normpath(this_dir)
        element = self._folder_meta['dir']
        lastobj_name = '/'
        lastobj_meta = element
        if this_dir:
            dir_pieces = this_dir.split(os.path.sep)
            dir_pieces, lastobj_name = dir_pieces[:-1], dir_pieces[-1]
            try:
                for piece in dir_pieces:
                    if this_dir == os.curdir:
                        continue
                    element = element[piece]['dir']
                lastobj_meta = element[lastobj_name]
            except KeyError:
                raise IOError("{} not found in node {}".format(this_dir, self.node_uuid))

        if 'dir' in lastobj_meta:
            return File(lastobj_name, FileType.DIRECTORY)
        elif 'obj' in lastobj_meta:
            return File(lastobj_name, FileType.FILE)
        else:
            raise RuntimeError("Invalid object in the folder_meta, neither a folder nor a file: {}, {}, {}, {}".format(
                lastobj_meta, dir_pieces, lastobj_name, self._folder_meta))

    def get_object_content(self, key):
        """Return the content of a object identified by key.

        # TODO: check and re-implement the 'mode' parameter

        :param key: fully qualified identifier for the object within the repository
        :param mode: the mode under which to open the handle
        """
        with self.open(key) as fhandle:
            return fhandle.read()
