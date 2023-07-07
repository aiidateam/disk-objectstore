"""Models for the container index file (SQLite DB)."""
from pathlib import Path
from typing import Optional

from sqlalchemy import Boolean, Column, Integer, String, create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import text

Base = declarative_base()  # pylint: disable=invalid-name,useless-suppression


class Obj(Base):  # pylint: disable=too-few-public-methods
    """The main (and only) table to store object metadata (hashkey, offset, length, ...)."""

    __tablename__ = "db_object"

    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name

    # Important: there are parts of the code that rely on the fact that this field is unique.
    # If you really do not want a uniqueness field, you will need to adapt the code.
    hashkey = Column(String, nullable=False, unique=True, index=True)
    compressed = Column(Boolean, nullable=False)
    size = Column(
        Integer, nullable=False
    )  # uncompressed size; if uncompressed, size == length
    offset = Column(Integer, nullable=False)
    length = Column(Integer, nullable=False)
    pack_id = Column(
        Integer, nullable=False
    )  # integer ID of the pack in which this entry is stored


def get_session(
    path: Path, create: bool = False, raise_if_missing: bool = False
) -> Optional[Session]:
    """Return a new session to connect to the pack-index SQLite DB.

    :param create: if True, creates the sqlite file and schema.
    :param raise_if_missing: ignored if create==True. If create==False, and the index file
        is missing, either raise an exception (FileNotFoundError) if this flag is True, or return None
    """
    if not create and not path.exists():
        if raise_if_missing:
            raise FileNotFoundError("Pack index does not exist")
        return None

    engine = create_engine(f"sqlite:///{path}", future=True)

    # For the next two bindings, see background on
    # https://docs.sqlalchemy.org/en/13/dialects/sqlite.html#serializable-isolation-savepoints-transactional-ddl
    @event.listens_for(engine, "connect")
    def do_connect(dbapi_connection, _):
        """Hook function that is called upon connection.

        It modifies the default behavior of SQLite to use WAL and to
        go back to the 'default' isolation level mode.
        """
        # disable pysqlite's emitting of the BEGIN statement entirely.
        # also stops it from emitting COMMIT before any DDL.
        dbapi_connection.isolation_level = None
        # Open the file in WAL mode (see e.g. https://stackoverflow.com/questions/9671490)
        # This allows to have as many readers as one wants, and a concurrent writer (up to one)
        # Note that this writes on a journal, on a different packs.idx-wal,
        # and also creates a packs.idx-shm file.
        # Note also that when the session is created, you will keep reading from the same version,
        # so you need to close and reload the session to see the newly written data.
        # Docs on WAL: https://www.sqlite.org/wal.html
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=wal;")
        cursor.close()

    # For this binding, see background on
    # https://docs.sqlalchemy.org/en/13/dialects/sqlite.html#serializable-isolation-savepoints-transactional-ddl
    @event.listens_for(engine, "begin")
    def do_begin(conn):  # pylint: disable=unused-variable
        # emit our own BEGIN
        conn.execute(text("BEGIN"))

    if create:
        # Create all tables in the engine. This is equivalent to "Create Table"
        # statements in raw SQL.
        Base.metadata.create_all(engine)

    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    Base.metadata.bind = engine

    # We set autoflush = False to avoid to lock the DB if just doing queries/reads
    session = sessionmaker(
        bind=engine, autoflush=False, autocommit=False, future=True
    )()

    return session
