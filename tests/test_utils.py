"""Test of the utils wrappers."""
import io
import os
import random
import tempfile
import zlib

import psutil
import pytest

import disk_objectstore.utils as utils
import disk_objectstore.exceptions as exc


def _assert_is_uuid(possible_uuid):
    """Check that a string is a valid UUID.

    In particular, it should be 32 hex characters, without dashes."""
    assert len(possible_uuid) == 32
    assert all(char in '0123456789abcdef' for char in possible_uuid)


def test_get_new_uuid():
    """Check that the get_new_uuid function returns a UUID composed of 32 hex characters, without dashes."""
    new_uuid = utils.get_new_uuid()
    _assert_is_uuid(new_uuid)


def test_lazy_opener_read():
    """Test the LazyOpener."""
    content = b'sfdssdfd 34fwfd'
    with tempfile.NamedTemporaryFile(mode='bw', delete=False) as fhandle:
        fhandle.write(content)

    try:
        current_process = psutil.Process()
        start_open_files = len(current_process.open_files())
        lazy = utils.LazyOpener(fhandle.name, mode='rb')

        assert lazy.path == fhandle.name
        assert lazy.mode == 'rb'

        assert len(current_process.open_files()
                  ) == start_open_files, ('The LazyOpener is not lazy, but axtually opened the file instead!')
        with lazy as fhandle:
            read_content = fhandle.read()
            assert len(current_process.open_files()) == start_open_files + 1, 'The count of open files is wrong!'
            assert read_content == content, 'Unexpected content read from file'

        assert len(current_process.open_files()) == start_open_files, 'The LazyOpener did not close the file on exit!'
    finally:
        os.remove(fhandle.name)


def test_lazy_opener_not_twice():
    """Test that the LazyOpener cannot be opened twice."""
    content = b'sfdfsdj2322d'
    with tempfile.NamedTemporaryFile(mode='bw', delete=False) as fhandle:
        fhandle.write(content)

    try:
        lazy = utils.LazyOpener(fhandle.name, mode='rb')

        # The first open should go through
        with lazy as fhandle:
            # The second open should fail
            with pytest.raises(IOError) as excinfo:
                with lazy:
                    pass
            assert 'already open' in str(excinfo.value)
            # The exception should not have corrupted the first stream
            assert fhandle.read() == content
    finally:
        os.remove(fhandle.name)


def test_nullcontext():
    """Test the nullcontext."""
    result = 'something'
    with utils.nullcontext(enter_result=result) as manager:
        assert manager == result


@pytest.mark.parametrize('loose_prefix_len', [0, 2, 3])
def test_object_writer(temp_dir, loose_prefix_len):
    """Test the ObjectWriter, directly writing objects (loose, via a sandbox)."""
    sandbox_folder = os.path.join(temp_dir, 'sandbox')
    loose_folder = os.path.join(temp_dir, 'loose')

    content = b'fsddfq232v'

    # Create the two folders, make sure they
    # are empty
    os.mkdir(sandbox_folder)
    os.mkdir(loose_folder)
    assert not os.listdir(sandbox_folder)
    assert not os.listdir(loose_folder)

    object_writer = utils.ObjectWriter(
        sandbox_folder=sandbox_folder, loose_folder=loose_folder, loose_prefix_len=loose_prefix_len
    )

    # Just creating the object should not create files
    assert not os.listdir(sandbox_folder)
    assert not os.listdir(loose_folder)

    with object_writer as fhandle:
        # Check the file is being written in the sandbox
        assert len(os.listdir(sandbox_folder)) == 1
        assert not os.listdir(loose_folder)
        fhandle.write(content)

    # Check the file has been removed from the sandbox
    # and moved to the loose-objects folder
    assert not os.listdir(sandbox_folder)
    assert len(os.listdir(loose_folder)) == 1

    obj_uuid = object_writer.get_uuid()
    _assert_is_uuid(obj_uuid)
    # Open manually the file, implicitly checking
    # that the prefix length is the expected one,
    # and that the content is correct
    if loose_prefix_len:
        loose_filename = os.path.join(loose_folder, obj_uuid[:loose_prefix_len], obj_uuid[loose_prefix_len:])
    else:
        loose_filename = os.path.join(loose_folder, obj_uuid)
    with open(loose_filename, 'rb') as fhandle:
        assert fhandle.read() == content


def test_object_writer_with_exc(temp_dir):
    """Test that the ObjectWRite does not write anything if there is an exception."""
    sandbox_folder = os.path.join(temp_dir, 'sandbox')
    loose_folder = os.path.join(temp_dir, 'loose')
    loose_prefix_len = 2
    os.mkdir(sandbox_folder)
    os.mkdir(loose_folder)

    content = b'523453dfvsd'

    object_writer = utils.ObjectWriter(
        sandbox_folder=sandbox_folder, loose_folder=loose_folder, loose_prefix_len=loose_prefix_len
    )

    assert not os.listdir(sandbox_folder)
    assert not os.listdir(loose_folder)

    # The first open should go through
    with pytest.raises(ValueError) as excinfo:
        with object_writer as fhandle:
            # Write some content first
            fhandle.write(content)

            assert len(os.listdir(sandbox_folder)) == 1
            assert not os.listdir(loose_folder)

            raise ValueError('My Error')
    assert str(excinfo.value) == 'My Error'

    # Since the exception was raised, both
    # the sandbox folder and the loose folder should
    # still be empty
    assert not os.listdir(sandbox_folder)
    assert not os.listdir(loose_folder)


def test_object_writer_not_twice(temp_dir):
    """Test that the ObjectWRite cannot be opened twice."""
    sandbox_folder = os.path.join(temp_dir, 'sandbox')
    loose_folder = os.path.join(temp_dir, 'loose')
    loose_prefix_len = 2
    os.mkdir(sandbox_folder)
    os.mkdir(loose_folder)

    content = b'523453dfvsd'

    object_writer = utils.ObjectWriter(
        sandbox_folder=sandbox_folder, loose_folder=loose_folder, loose_prefix_len=loose_prefix_len
    )

    # The first open should go through
    with object_writer as fhandle:
        # Write some content first
        fhandle.write(content)
        # The second open should fail
        with pytest.raises(IOError) as excinfo:
            with object_writer:
                pass
        assert 'already opened' in str(excinfo.value)
        # The exception should not have corrupted the first stream. I write again something
        fhandle.write(content)

    obj_uuid = object_writer.get_uuid()
    loose_filename = os.path.join(loose_folder, obj_uuid[:loose_prefix_len], obj_uuid[loose_prefix_len:])
    with open(loose_filename, 'rb') as fhandle:
        # I have written the content twice
        assert fhandle.read() == content + content

    with pytest.raises(exc.ModificationNotAllowed) as excinfo:
        # Should not allow to reuse the same object_writer after storing
        with object_writer:
            pass
    assert 'already stored' in str(excinfo.value)


def test_object_writer_existing_obj(temp_dir):
    """Assert that if a loose object is found with the same UUID, the object_writer crashes."""
    sandbox_folder = os.path.join(temp_dir, 'sandbox')
    loose_folder = os.path.join(temp_dir, 'loose')
    loose_prefix_len = 2
    os.mkdir(sandbox_folder)
    os.mkdir(loose_folder)

    object_writer = utils.ObjectWriter(
        sandbox_folder=sandbox_folder, loose_folder=loose_folder, loose_prefix_len=loose_prefix_len
    )

    # Check that this crashes as I am creating
    # the loose object before exiting the context manager
    with pytest.raises(exc.ModificationNotAllowed) as excinfo:
        with object_writer:
            # Create manually a loose object where the object writer would write it
            obj_uuid = object_writer.get_uuid()
            loose_filename = os.path.join(loose_folder, obj_uuid[:loose_prefix_len], obj_uuid[loose_prefix_len:])
            os.mkdir(os.path.dirname(loose_filename))
            with open(loose_filename, 'wb'):
                # Just write an empty file
                pass
    assert 'already exists' in str(excinfo.value)


def test_packed_object_reader():
    """Test the functionality of the PackedObjectReader."""
    bytestream = b'0123456789abcdef'
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as tempfhandle:
        tempfhandle.write(bytestream)

    offset = 3
    length = 5
    expected_bytestream = bytestream[offset:offset + length]

    with open(tempfhandle.name, 'rb') as fhandle:
        packed_reader = utils.PackedObjectReader(fhandle, offset=offset, length=length)

        # Check the functionality is disabled
        assert not packed_reader.seekable
        with pytest.raises(OSError):
            packed_reader.seek(0)
        with pytest.raises(OSError):
            packed_reader.tell()

        # Read in one shot
        assert packed_reader.read() == expected_bytestream

    # Read 1 byte at a time
    with open(tempfhandle.name, 'rb') as fhandle:
        packed_reader = utils.PackedObjectReader(fhandle, offset=offset, length=length)

        data = []
        while True:
            piece = packed_reader.read(1)
            if not piece:
                break
            data.append(piece)
        assert b''.join(data) == expected_bytestream

    # Read 2 bytes at a time (note that the length is odd, so it's not a multiple)
    with open(tempfhandle.name, 'rb') as fhandle:
        packed_reader = utils.PackedObjectReader(fhandle, offset=offset, length=length)

        data = []
        while True:
            piece = packed_reader.read(2)
            if not piece:
                break
            data.append(piece)
        assert b''.join(data) == expected_bytestream

    # Offset beyond the file limit
    with open(tempfhandle.name, 'rb') as fhandle:
        packed_reader = utils.PackedObjectReader(fhandle, offset=len(bytestream) + 10, length=length)
        assert packed_reader.read() == b''

    # Offset before the file limit, but longer length
    with open(tempfhandle.name, 'rb') as fhandle:
        packed_reader = utils.PackedObjectReader(fhandle, offset=offset, length=1000000)
        assert packed_reader.read() == bytestream[offset:]


def test_stream_decompresser():
    """Test the stream decompresser."""
    # A short binary string (1025 bytes, an odd number to avoid possible alignments with the chunk size)
    original_data_short = b'0123456789abcdef' * 64 + b'E'
    # A longish binary string (2097153 bytes ~ 2MB
    # an odd number to avoid possible alignments with the chunk size), compressible
    original_data_long = b'0123456789abcdef' * 1024 * 128 + b'E'
    # A longish binary string (~4MB) with random data
    # so typically uncompressible (compressed size is typically larger)
    original_data_long_random = bytearray(random.getrandbits(8) for _ in range(4000000))

    original_data = [original_data_short, original_data_long, original_data_long_random]

    compressed_streams = [io.BytesIO(zlib.compress(data)) for data in original_data]
    for original, compressed_stream in zip(original_data, compressed_streams):
        decompresser = utils.StreamDecompresser(compressed_stream)
        # Read in one chunk
        assert original == decompresser.read(), 'Uncompressed data is wrong (single read)'

    # Redo the same, but do a read of zero bytes first, checking that
    # it returns a zero-length bytes, and that it does not move the offset
    compressed_streams = [io.BytesIO(zlib.compress(data)) for data in original_data]
    for original, compressed_stream in zip(original_data, compressed_streams):
        decompresser = utils.StreamDecompresser(compressed_stream)
        # Read in one chunk
        tmp = decompresser.read(size=0)
        assert not tmp
        assert original == decompresser.read(), 'Uncompressed data is wrong (single read)'

    compressed_streams = [io.BytesIO(zlib.compress(data)) for data in original_data]
    chunk_size = 1024
    for original, compressed_stream in zip(original_data, compressed_streams):
        data_chunks = []
        decompresser = utils.StreamDecompresser(compressed_stream)
        # Read in multiple chunk
        while True:
            chunk = decompresser.read(size=chunk_size)
            data_chunks.append(chunk)
            if not chunk:
                break
        data = b''.join(data_chunks)

        assert original == data, 'Uncompressed data is wrong (chunked read)'


def test_decompresser_corrupt():
    """Test that the stream decompresser raises on a corrupt input."""

    # Check that we get an error for an invalid stream of bytes
    decompresser = utils.StreamDecompresser(io.BytesIO(b'1234543'))
    with pytest.raises(ValueError) as excinfo:
        print(decompresser.read())
    assert 'Error while uncompressing data' in str(excinfo.value)

    # Check that we get an error for a truncated stream of bytes
    original_data = b'someDATAotherTHINGS'
    compressed_data = zlib.compress(original_data)
    # I remove the last byte, so it's corrupted
    corrupted_stream = io.BytesIO(compressed_data[:-1])

    decompresser = utils.StreamDecompresser(corrupted_stream)
    with pytest.raises(ValueError) as excinfo:
        print(decompresser.read())
    assert 'problem in the incoming buffer' in str(excinfo.value)


def test_zero_stream_single_read():
    """Test the ZeroStream class with a single .read() call."""
    length = 23523
    zero_stream = utils.ZeroStream(length=length)
    data = zero_stream.read()
    assert len(data) == length, 'The zero stream produced data of the wrong length'
    assert data == b'\x00' * length, 'The zero stream produced non-zero data'


def test_zero_stream_multi_read():
    """Test the ZeroStream class with multiple smaller .read() calls."""
    length = 23523
    chunk_size = 2342

    zero_stream = utils.ZeroStream(length=length)
    data_chunks = []
    while True:
        chunk = zero_stream.read(size=chunk_size)
        data_chunks.append(chunk)
        if not chunk:
            break
    data = b''.join(data_chunks)
    assert len(data) == length, 'The zero stream produced data of the wrong length'
    assert data == b'\x00' * length, 'The zero stream produced non-zero data'
