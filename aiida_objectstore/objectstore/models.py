from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
 
class Obj(Base):
    __tablename__ = 'db_object'

    id = Column(Integer, primary_key=True)
    # 32 is the length of the UUID *without* dashes
    uuid = Column(String(32), nullable=False, index=True)
    compressed = Column(Boolean, nullable=False)
    size = Column(Integer, nullable=False) # uncompressed size; if uncompressed, size == length
    offset = Column(Integer, nullable=False)
    length = Column(Integer, nullable=False)
