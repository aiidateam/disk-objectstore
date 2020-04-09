"""Models for the container index file (SQLite DB)."""
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()  # pylint: disable=invalid-name,useless-suppression


class Obj(Base):  # pylint: disable=too-few-public-methods
    """The main (and only) table to store object metadata (uuid, offset, length, ...)."""
    __tablename__ = 'db_object'

    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    # 32 is the length of the UUID *without* dashes
    uuid = Column(String(32), nullable=False, index=True)
    compressed = Column(Boolean, nullable=False)
    size = Column(Integer, nullable=False)  # uncompressed size; if uncompressed, size == length
    offset = Column(Integer, nullable=False)
    length = Column(Integer, nullable=False)
