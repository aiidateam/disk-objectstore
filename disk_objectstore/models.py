"""Models for the container index file (SQLite DB)."""
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()  # pylint: disable=invalid-name,useless-suppression


class Obj(Base):  # pylint: disable=too-few-public-methods
    """The main (and only) table to store object metadata (hashkey, offset, length, ...)."""
    __tablename__ = 'db_object'

    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name

    # Important: there are parts of the code that rely on the fact that this field is unique.
    # If you really do not want a uniqueness field, you will need to adapt the code.
    hashkey = Column(String, nullable=False, unique=True, index=True)
    compressed = Column(Boolean, nullable=False)
    size = Column(Integer, nullable=False)  # uncompressed size; if uncompressed, size == length
    offset = Column(Integer, nullable=False)
    length = Column(Integer, nullable=False)
    pack_id = Column(Integer, nullable=False)  # integer ID of the pack in which this entry is stored
