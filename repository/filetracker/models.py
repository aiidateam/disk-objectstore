from sqlalchemy import (
    Column, Integer, String, ForeignKey, Index)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()
 
class File(Base):
    __tablename__ = 'db_file'

    id = Column(Integer, primary_key=True)
    object_id = Column(String(36), nullable=False) # It's the UUID from the object store
    name = Column(String(), nullable=False)
    parent_id = Column(Integer, ForeignKey('db_folder.id'), nullable=True)
    parent = relationship('Folder', backref='files')

    __table_args__ = (
        Index('unique_file_per_folder_nonroot', name, parent_id,
              unique=True,
              postgresql_where=parent_id.isnot(None)),
        Index('unique_file_per_folder_root', name,
              unique=True,
              postgresql_where=(parent_id.is_(None))),
    )

    def get_relpath(self):
        return self.parent.get_relpath() + '/' + self.name


class Folder(Base):
    __tablename__ = 'db_folder'

    id = Column(Integer, primary_key=True)
    name = Column(String(), nullable=False)
    subfolders = relationship('Folder', backref=backref('parent', remote_side=[id]))
    parent_id = Column(Integer, ForeignKey('db_folder.id'), nullable=True)

    # TODO: Note that this still allows to have a folder and a file with the same name in the same folder!!
    __table_args__ = (
        Index('unique_subfolder_per_folder_nonroot', name, parent_id,
              unique=True,
              postgresql_where=parent_id.isnot(None)),
        Index('unique_subfolder_per_folder_root', name,
              unique=True,
              postgresql_where=(parent_id.is_(None))),
    )        

    def get_relpath(self):
        if self.parent is None:
            return self.name
        return self.parent.get_relpath() + '/' + self.name
