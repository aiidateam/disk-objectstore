from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DbNodeRepo(Base):
    __tablename__ = 'db_noderepo'

    id = Column(Integer, primary_key=True)
    # Will become an Integer Foreign Key
    # Actually, we probably want to link in the other direction! A Foreign Key from Node to here
    node_uuid = Column(String(36), index=True)
    folder_meta = Column(JSONB)
