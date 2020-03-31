import os
import sys
from sqlalchemy import (
    Column, ForeignKey, Integer, String, Float, UniqueConstraint, Boolean)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
 
class Obj(Base):
    __tablename__ = 'db_object'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), nullable=False, index=True)
    packed = Column(Boolean, default=False)
    offset = Column(Integer, nullable=True)
    length = Column(Integer, nullable=True)

class FileRef(Base):
    __tablename__ = 'db_fileref'

    id = Column(Integer, primary_key=True)
    obj = relationship(Obj)
    obj_id = Column(Integer, ForeignKey('db_object.id'), nullable=False)
    # sha = Column(String(250), nullable=False) # This might be useful later for deduplication
    relpath = Column(String(), nullable=False, index=True, unique=True)

## If you prefer, uncomment the following and remove 'unique=True' above
#    node_pk = Column(Integer)
#    __table_args__ = (
#        UniqueConstraint(
#            'node_pk', 'rel_path' 
#            name='unique_file_per_node'),
#    )

def get_session(fname, create=False, verbose=False):
    from sqlalchemy.orm import sessionmaker

    engine_name = 'sqlite:///{}'.format(fname)
    if verbose:
        print("DB: {}".format(engine_name))
    # In the local directory, or an additional slash for an absolute path
    engine = create_engine(engine_name)

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
