from sqlalchemy import (
    Column, Integer, String, Boolean) #, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import relationship

Base = declarative_base()
 
class Obj(Base):
    __tablename__ = 'db_object'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), nullable=False, index=True)
    compressed = Column(Boolean, default=False)
    size = Column(Integer) # uncompressed size; if uncompressed, size == length
    offset = Column(Integer, nullable=True)
    length = Column(Integer, nullable=True)
