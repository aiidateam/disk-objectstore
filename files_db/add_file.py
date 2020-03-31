#!/usr/bin/env python
import os
import uuid
from collections import defaultdict

from .models import Obj, FileRef, get_session
from .common import LOOSE_FOLDER, PACK_FOLDER,  DB_FILE, PREFIX_LEN
from sqlalchemy.exc import IntegrityError
from contextlib import contextmanager

# TODO: Other todos: 
# - use transactions (with session.begin_nested(), and probably remove manual commits, see https://docs.sqlalchemy.org/en/13/orm/session_transaction.html)
# - Understand if using SQLite is a good idea:
#   - ok, everybody can read, but even writing loose objects currently requires the DB...
#     maybe avoid using the DB in that case? (in that case, write to sandbox and move files atomically).
#   - Or just put this module into AiiDA and use a proper DB
#   - I probably prefer the first option (we could also decide if we want to have a sqlite DB per pack)


def _get_path_from_uuid(uuid, packed):
    if packed:
        return os.path.join(PACK_FOLDER, uuid[:PREFIX_LEN])
    return os.path.join(LOOSE_FOLDER, uuid)


class FileObject:
    def __init__(self, session, filename, commit_on_exit=True):
        self._session = session
        self._uuid = str(uuid.uuid4())
        self._filename = filename
        self._commit_on_exit = commit_on_exit
        self._created = False

    def __enter__(self):
        # TODO: test this
        if self._created:
            raise RuntimeError("Cannot recreate existing file")
        self._obj_path = _get_path_from_uuid(self._uuid, packed=False)
        self._filehandle = open(self._obj_path, 'wb')
        return self._filehandle

    def __exit__(self, exc_type, value, traceback):
        if not self._filehandle.closed:
            self._filehandle.close()

        if exc_type is None:    
            obj = Obj(
                uuid=self._uuid, 
                packed=False)
            self._session.add(obj)
            fileref = FileRef(
                obj = obj,
                relpath=self._filename # one could think to have a path or other
            )
            self._session.add(fileref)

            if self._commit_on_exit:
                self._session.commit()
            self._created = True
        else:
            # TODO add test to check that this works
            if os.path.exists(self._obj_path):
                os.remove(self._obj_path)


def add_file(session, filename, content):
    """Add a loose file. Content must be binary"""
    with FileObject(session=session, filename=filename) as fhandle:
        fhandle.write(content)

def add_files(session, dict_of_files):
    """Add a loose files. dict_of_files has keys=filename, values=bytestream"""
    for filename, content in dict_of_files.items():
        with FileObject(session=session, filename=filename, commit_on_exit=False) as fhandle:
            fhandle.write(content)
    session.commit()

def add_files_to_pack(session, dict_of_files):
    """Like add_files, but add directly to pack. Must be run NON concurrently (it's locking)"""
    packs = defaultdict(list)
    for filename in dict_of_files:
        obj_uuid = str(uuid.uuid4()) # TODO: make function to generate UUID strings
        packs[obj_uuid[:PREFIX_LEN]].append((filename, obj_uuid)) 
    for pack_id, filenames in packs.items():
        # Avoid concurrent writes        
        with lock_pack(pack_id) as pack_handle:
            for filename, obj_uuid in filenames:
                obj = Obj(
                    uuid=obj_uuid,  
                    packed=True)
                obj.offset = pack_handle.tell()
                pack_handle.write(dict_of_files[filename])
                obj.length = pack_handle.tell() - obj.offset
                session.add(obj)
                fileref = FileRef(
                    obj = obj,
                    relpath=filename # one could think to have a path or other
                )
                session.add(fileref)
        session.commit()

def get_total_size(session):
    total_size_packed = session.query(FileRef).join(Obj).filter(Obj.packed==True).with_entities(Obj.length).all()
    if not total_size_packed:
        total_size_packed = 0
    else:
        total_size_packed = sum(res[0] for res in total_size_packed)

    total_size_loose = 0

    for obj in session.query(FileRef).join(Obj).filter(Obj.packed==False).with_entities(Obj).all():
        loose_path = _get_path_from_uuid(obj.uuid, packed=False)
        total_size_loose += os.path.getsize(loose_path)
    
    return total_size_packed, total_size_loose

def get_file_content(session, filename):
    obj = session.query(Obj).join(FileRef).filter(FileRef.relpath==filename).one()
    obj_path = _get_path_from_uuid(obj.uuid, packed=obj.packed)
    if obj.packed:
        with open(obj_path, 'rb') as fhandle:
            fhandle.seek(obj.offset)
            return fhandle.read(obj.length)        
    else:
        with open(obj_path, 'rb') as fhandle:
            return fhandle.read()

# TODO: test that lock works
@contextmanager
def lock_pack(pack_id):
    # validate
    assert len(pack_id) == PREFIX_LEN
    assert all(char in "0123456789abcdef" for char in pack_id)

    lock_file = os.path.join(PACK_FOLDER, '{}.lock'.format(pack_id))
    with open(lock_file, 'x'):
        try:
             # TODO: next line, duplication of logic with _get_path_from_uuid
            pack_file = os.path.join(PACK_FOLDER, pack_id)
            with open(pack_file, 'ab') as pack_handle:
                yield pack_handle
        finally:
            # Code to release resource, e.g.:
            if os.path.exists(lock_file):
                os.remove(lock_file)

def pack_all_loose(session):
    packs = defaultdict(list)
    for obj in session.query(Obj).filter(Obj.packed==False).with_entities(
            Obj.uuid, Obj.id).all():
        packs[obj[0][:PREFIX_LEN]].append(obj)
    for pack_id, loose_objects in packs.items():
        # Avoid concurrent writes        
        with lock_pack(pack_id) as pack_handle:
            for obj_uuid, obj_id in loose_objects:
                obj = session.query(Obj).get(obj_id)
                obj.offset = pack_handle.tell()
                with open(_get_path_from_uuid(obj_uuid, packed=False), 'rb') as loose_handle:
                    pack_handle.write(loose_handle.read())
                obj.length = pack_handle.tell() - obj.offset
                obj.packed = True
                session.add(obj)
        session.commit()
        # Clean up loose objects
        # Todo - clean up procedure for files left in loose_objects folder, but unknown
        for obj_uuid, obj_id in loose_objects:
            os.remove(_get_path_from_uuid(obj_uuid, packed=False))

# TODO: a full repack, recreating each pack only with the known objects (e.g. if something was deleted)
# TODO: validation of pack (e.g. for overlapping bits), and sparsity (how much space is stored in unknown bytestreams)
# TODO: add flag in DB for 'zipped' object (zip first, then store just as usual; when retrieving, remember to unzip)
# TODO: streaming

