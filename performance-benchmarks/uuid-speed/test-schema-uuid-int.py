import sys
import time
import uuid
import numpy as np

from itertools import islice

from sqlalchemy import create_engine, event
from sqlalchemy import Column, Integer, String, Boolean, tuple_, and_, or_, Index
from sqlalchemy.ext.declarative import declarative_base

BaseUUID = declarative_base()
BaseInt = declarative_base()


def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


def uint64_from_bytes(bytestream):
    return np.frombuffer(bytestream, dtype=np.uint64)[0]


def int_from_bytes(bytestream):
    return int(np.frombuffer(bytestream, dtype=np.uint64)[0])


def hex_from_bytes(bytes1, bytes2):
    uint64_1 = np.frombuffer(bytes1, dtype=np.uint64)[0]
    uint64_2 = np.frombuffer(bytes2, dtype=np.uint64)[0]
    return hex_from_ints(int(uint64_1), int(uint64_2))


def hex_from_ints(int1, int2):
    # remove 0x, fill with zeros
    return (hex((int1 * 2**64) + int2)[2:]).zfill(32)


def uint64_from_hex(hex_string):
    hex1, hex2 = hex_string[:16], hex_string[16:]
    return np.uint64(int(hex1, 16)), np.uint64(int(hex2, 16))


def ints_from_hex(hex_string):
    hex1, hex2 = hex_string[:16], hex_string[16:]
    return int(hex1, 16), int(hex2, 16)


class ObjUUID(BaseUUID):
    __tablename__ = 'db_object'

    id = Column(Integer, primary_key=True)
    # 32 is the length of the UUID *without* dashes
    uuid = Column(String(32), nullable=False, index=True)
    compressed = Column(Boolean, nullable=False)
    size = Column(
        Integer,
        nullable=False)  # uncompressed size; if uncompressed, size == length
    offset = Column(Integer, nullable=False)
    length = Column(Integer, nullable=False)


class ObjInt(BaseInt):
    __tablename__ = 'db_object'

    id = Column(Integer, primary_key=True)
    uuidint1 = Column(Integer, nullable=False)
    uuidint2 = Column(Integer, nullable=False)
    compressed = Column(Boolean, nullable=False)
    size = Column(
        Integer,
        nullable=False)  # uncompressed size; if uncompressed, size == length
    offset = Column(Integer, nullable=False)
    length = Column(Integer, nullable=False)
    __table_args__ = (Index('uuidintindex', 'uuidint1', 'uuidint2'), )


def get_db_session_int():
    return _get_db_session('int.sqlite', BaseInt)


def get_db_session_uuid():
    return _get_db_session('uuid.sqlite', BaseUUID)


def _get_db_session(path, Base):
    from sqlalchemy.orm import sessionmaker

    engine = create_engine('sqlite:///{}'.format(path))

    # For the next two bindings, see background on
    # https://docs.sqlalchemy.org/en/13/dialects/sqlite.html#serializable-isolation-savepoints-transactional-ddl
    @event.listens_for(engine, 'connect')
    def do_connect(dbapi_connection, connection_record):  # pylint: disable=unused-argument,unused-variable
        # disable pysqlite's emitting of the BEGIN statement entirely.
        # also stops it from emitting COMMIT before any DDL.
        dbapi_connection.isolation_level = None

    @event.listens_for(engine, 'begin')
    def do_begin(conn):  # pylint: disable=unused-variable
        # emit our own BEGIN
        conn.execute('BEGIN')

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)

    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    Base.metadata.bind = engine

    ## See e.g.
    ##http://pythoncentral.io/introductory-tutorial-python-sqlalchemy/
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    return session


if __name__ == '__main__':
    session_uuid = get_db_session_uuid()
    session_int = get_db_session_int()

    N = 10000

    # Single shot storage
    uuids = [uuid.uuid4().hex for _ in range(N)]

    # Store
    start = time.time()
    for obj_uuid in uuids:
        obj = ObjUUID(uuid=obj_uuid,
                      compressed=False,
                      size=0,
                      offset=0,
                      length=0)
        session_uuid.add(obj)
    session_uuid.commit()
    tot_time = time.time() - start
    print('UUID, time to store {} UUIDs: {:.3f}s'.format(N, tot_time))

    # Store
    start = time.time()
    for obj_uuid in uuids:
        int1, int2 = uint64_from_hex(obj_uuid)
        obj = ObjInt(uuidint1=int1,
                     uuidint2=int2,
                     compressed=False,
                     size=0,
                     offset=0,
                     length=0)
        session_int.add(obj)
    session_int.commit()
    tot_time = time.time() - start
    print('Two ints, time to store {} UUIDs: {:.3f}s'.format(N, tot_time))

    # Read
    start = time.time()
    to_compare = set(
        (obj.uuid, obj.compressed)
        for obj in session_uuid.query(ObjUUID).filter(ObjUUID.uuid.in_(uuids)))
    tot_time = time.time() - start
    print('UUID, time to read {} UUIDs: {:.3f}s'.format(N, tot_time))

    assert set((uuid, False) for uuid in uuids) == to_compare

    # Read
    start = time.time()
    uuid_uint64s = [uint64_from_hex(uuid) for uuid in uuids]

    #for uuid_, uuid_intpair_ in zip(uuids, uuid_uint64s):
    #    assert uuid_ == hex_from_bytes(uuid_intpair_[0], uuid_intpair_[1]), "{}, {}: {} vs {}".format(
    #        uuid_intpair_[0], uuid_intpair_[1],
    #        uuid_, hex_from_bytes(uuid_intpair_[0], uuid_intpair_[1]))

    results = []

    # Not too many otherwise the query string is too long!
    for sublist in chunk(uuid_uint64s, 500):
        conditions = (and_(ObjInt.uuidint1 == x, ObjInt.uuidint2 == y)
                      for (x, y) in sublist)

        #    ## This works with PostgreSQL, but breaks with SQLite
        #    #.filter(tuple_(ObjInt.uuidint1, ObjInt.uuidint2).in_(uuid_uint64s)

        to_compare = [
            (hex_from_ints(int_from_bytes(obj.uuidint1),
                           int_from_bytes(obj.uuidint2)), obj.compressed)
            for obj in session_int.query(ObjInt).filter(or_(*conditions))
        ]
        results += to_compare

    results = sorted(results)
    uuids = sorted(uuids)

    tot_time = time.time() - start
    print('Two ints, time to read {} UUIDs: {:.3f}s'.format(N, tot_time))

    assert len(results) == len(uuid_uint64s)

    for idx, (before, after) in enumerate(zip(sorted(uuids), sorted(results))):
        assert (
            before,
            False) == after, 'First mismatch at pos {}/{}: {} vs {}'.format(
                idx, len(results), (before[0], before[1], False), after)
