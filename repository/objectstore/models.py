from sqlalchemy import (
    Column, Integer, String, Boolean) #, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import relationship

Base = declarative_base()
 
class Obj(Base):
    __tablename__ = 'db_object'

    id = Column(Integer, primary_key=True)
    # 32 is the length of the UUID *without* dashes
    # We could actually use a shorter column length depending on the pack_prefix_len,
    # but for simplicity we leave 32 for now
    uuid_remainder = Column(String(32), nullable=False, index=True)
    compressed = Column(Boolean, nullable=False)
    size = Column(Integer, nullable=False) # uncompressed size; if uncompressed, size == length
    offset = Column(Integer, nullable=False)
    length = Column(Integer, nullable=False)
