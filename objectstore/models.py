from sqlalchemy import (
    Column, ForeignKey, Integer, String, Boolean)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
 
class Obj(Base):
    __tablename__ = 'db_object'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), nullable=False, index=True)
    packed = Column(Boolean, default=False)
    #compressed = Column(Boolean, default=False)
    offset = Column(Integer, nullable=True)
    length = Column(Integer, nullable=True)

class FileRef(Base):
    __tablename__ = 'db_fileref'

    id = Column(Integer, primary_key=True)
    obj = relationship(Obj)
    obj_id = Column(Integer, ForeignKey('db_object.id'), nullable=False)
    # sha = Column(String(250), nullable=False) # This might be useful later for deduplication
    relpath = Column(String(), nullable=False, index=True, unique=True)
