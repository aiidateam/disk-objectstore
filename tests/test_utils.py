"""Test of the utils wrappers."""
import functools
import io
import os
import tempfile
import zlib

import psutil
import pytest

from disk_objectstore import utils
import disk_objectstore.exceptions as exc

os._actual_remove_function = os.remove  # pylint: disable=protected-access


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
        with pytest.raises(ValueError):
            # This is not open yet
            lazy.tell()

        assert len(current_process.open_files()
                  ) == start_open_files, ('The LazyOpener is not lazy, but axtually opened the file instead!')
        with lazy as fhandle:
            # Shoul be opened at position zero at the beginnign
            assert lazy.tell() == 0
            read_content = fhandle.read()
            # The position should had moved by the right amount
            assert lazy.tell() == len(read_content)

            assert len(current_process.open_files()) == start_open_files + 1, 'The count of open files is wrong!'
            assert read_content == content, 'Unexpected content read from file'

        assert len(current_process.open_files()) == start_open_files, 'The LazyOpener did not close the file on exit!'

        with pytest.raises(ValueError):
            # Should raise again after closing
            lazy.tell()
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

    hash_type = 'sha256'
    expected_hash = '9975d00a6e715d830aeaa035347b3e601a0c0bb457a7f87816300e7c01c0c39b'
    content = b'some-content-to-hash'

    # Create the two folders, make sure they
    # are empty
    os.mkdir(sandbox_folder)
    os.mkdir(loose_folder)
    assert not os.listdir(sandbox_folder)
    assert not os.listdir(loose_folder)

    object_writer = utils.ObjectWriter(
        sandbox_folder=sandbox_folder,
        loose_folder=loose_folder,
        loose_prefix_len=loose_prefix_len,
        hash_type=hash_type
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

    obj_hashkey = object_writer.get_hashkey()

    # Check that the hash was computed correctly
    assert obj_hashkey == expected_hash

    # Open manually the file, implicitly checking
    # that the prefix length is the expected one,
    # and that the content is correct
    if loose_prefix_len:
        loose_filename = os.path.join(loose_folder, obj_hashkey[:loose_prefix_len], obj_hashkey[loose_prefix_len:])
    else:
        loose_filename = os.path.join(loose_folder, obj_hashkey)
    with open(loose_filename, 'rb') as fhandle:
        assert fhandle.read() == content


def test_object_writer_with_exc(temp_dir):
    """Test that the ObjectWriter does not write anything if there is an exception."""
    sandbox_folder = os.path.join(temp_dir, 'sandbox')
    loose_folder = os.path.join(temp_dir, 'loose')
    loose_prefix_len = 2
    os.mkdir(sandbox_folder)
    os.mkdir(loose_folder)

    content = b'523453dfvsd'

    object_writer = utils.ObjectWriter(
        sandbox_folder=sandbox_folder, loose_folder=loose_folder, loose_prefix_len=loose_prefix_len, hash_type='sha256'
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


def test_object_writer_manual_close(temp_dir):
    """Test that the ObjectWriter does not allow manually closing the stream."""
    sandbox_folder = os.path.join(temp_dir, 'sandbox')
    loose_folder = os.path.join(temp_dir, 'loose')
    loose_prefix_len = 2
    os.mkdir(sandbox_folder)
    os.mkdir(loose_folder)

    content = b'523453dfvsd'

    object_writer = utils.ObjectWriter(
        sandbox_folder=sandbox_folder, loose_folder=loose_folder, loose_prefix_len=loose_prefix_len, hash_type='sha256'
    )

    assert not os.listdir(sandbox_folder)
    assert not os.listdir(loose_folder)

    # The first open should go through
    with pytest.raises(exc.ClosingNotAllowed) as excinfo:
        with object_writer as fhandle:
            # Write some content first
            fhandle.write(content)

            assert len(os.listdir(sandbox_folder)) == 1
            assert not os.listdir(loose_folder)
            fhandle.close()

    assert 'You cannot close' in str(excinfo.value)

    # Since the exception was raised, both
    # the sandbox folder and the loose folder should
    # still be empty
    assert not os.listdir(sandbox_folder)
    assert not os.listdir(loose_folder)


def test_object_writer_not_twice(temp_dir):
    """Test that the ObjectWriter cannot be opened twice."""
    sandbox_folder = os.path.join(temp_dir, 'sandbox')
    loose_folder = os.path.join(temp_dir, 'loose')
    loose_prefix_len = 2
    os.mkdir(sandbox_folder)
    os.mkdir(loose_folder)

    content = b'523453dfvsd'

    object_writer = utils.ObjectWriter(
        sandbox_folder=sandbox_folder, loose_folder=loose_folder, loose_prefix_len=loose_prefix_len, hash_type='sha256'
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

    obj_hashkey = object_writer.get_hashkey()
    loose_filename = os.path.join(loose_folder, obj_hashkey[:loose_prefix_len], obj_hashkey[loose_prefix_len:])
    with open(loose_filename, 'rb') as fhandle:
        # I have written the content twice
        assert fhandle.read() == content + content

    with pytest.raises(exc.ModificationNotAllowed) as excinfo:
        # Should not allow to reuse the same object_writer after storing
        with object_writer:
            pass
    assert 'already stored' in str(excinfo.value)


@pytest.mark.parametrize('reappears_corrupted', [True, False])
@pytest.mark.parametrize('trust_existing', [True, False])
def test_object_writer_existing_corrupted_reappears(  # pylint: disable=invalid-name
        temp_dir, trust_existing, reappears_corrupted, monkeypatch
    ):
    """Test that the ObjectWriter replaces an existing corrupted (wrong hash) loose object.

    Moreover, if the corrupted file is deleted and it quickly reappears, make sure that the code does not crash.
    In this test, the `os.remove` call is patched for the specific loose file. If reappears_corrupted is True,
    the file that will reappear as soon as it's deleted internally is going still to be corrupted. Otherwise,
    it will be a correct content (i.e., with the correct hash key, as if another process has created it at the same
    time)."""
    sandbox_folder = os.path.join(temp_dir, 'sandbox')
    loose_folder = os.path.join(temp_dir, 'loose')
    loose_prefix_len = 2
    hash_type = 'sha256'
    os.mkdir(sandbox_folder)
    os.mkdir(loose_folder)

    content = b'523453dfvsd'
    hasher = utils._get_hash(hash_type=hash_type)()  # pylint: disable=protected-access
    hasher.update(content)
    hashkey = hasher.hexdigest()

    # Some content that does not match the hash key
    corrupted_content = b'CORRUPTED CONTENT'

    loose_file = os.path.join(loose_folder, hashkey[:loose_prefix_len], hashkey[loose_prefix_len:])
    os.mkdir(os.path.dirname(loose_file))
    with open(loose_file, 'wb') as fhandle:
        fhandle.write(corrupted_content)

    # Check the starting condition
    assert not os.listdir(sandbox_folder)
    assert len(os.listdir(loose_folder)) == 1
    assert len(os.listdir(os.path.dirname(loose_file))) == 1

    object_writer = utils.ObjectWriter(
        sandbox_folder=sandbox_folder,
        loose_folder=loose_folder,
        loose_prefix_len=loose_prefix_len,
        hash_type=hash_type,
        trust_existing=trust_existing
    )

    def mockremove(path, protected_path, new_bytes_content):
        """Remove a file, mocking the os.remove functionality."""
        # I renamed this at module load to avoid infinite recursion
        os._actual_remove_function(path)  # pylint: disable=protected-access
        if os.path.realpath(path) == os.path.realpath(protected_path):
            # Write back the file, with possibly a different content
            with open(path, 'wb') as fhandle:
                fhandle.write(new_bytes_content)

    new_bytes_content = corrupted_content if reappears_corrupted else content
    monkeypatch.setattr(
        os, 'remove', functools.partial(mockremove, protected_path=loose_file, new_bytes_content=new_bytes_content)
    )

    if os.name == 'nt' and not trust_existing and reappears_corrupted:
        # On windows, I am not sure it's possible to do an atomic overwrite.
        # Currently this library implements logic such that if the file reappears,
        # but its content is correct, no error is raised. But if the file reappears
        # and its content is corrupted, an exception is raised (this should really
        # never happen, and if it happens, it means there is something really wrong!)
        with pytest.raises(exc.DynamicInconsistentContent):
            with object_writer as fhandle:
                # Write some content (this should end up in the same `loose_file` location)
                fhandle.write(content)
    else:
        # On POSIX, the os.rename is going to silently overwrite the existing file.
        # Therefore, I expect that the file write will go through without exceptions.
        with object_writer as fhandle:
            # Write some content (this should end up in the same `loose_file` location)
            fhandle.write(content)

    # Check the end condition:
    # nothing in the sandbox, nothing new in the loose_folder
    assert not os.listdir(sandbox_folder)
    assert len(os.listdir(loose_folder)) == 1
    assert len(os.listdir(os.path.dirname(loose_file))) == 1

    # Check now the content
    with open(loose_file, 'rb') as fhandle:
        object_content = fhandle.read()

    if trust_existing:
        # If I trust existing files, the content shouldn't have been touched
        # (and the logic for reappears_corrupted is not really triggered)
        assert object_content == corrupted_content
    else:
        if os.name == 'nt' and not trust_existing and reappears_corrupted:
            # Here I am just checking the current behavior: if the exception was raised,
            # the corrupted file is left in place
            assert object_content == corrupted_content
        else:
            # In all other cases, if I don't trust existing files, the content should have been replaced,
            # and if the DynamicInconsistentContent exception wasn't raised, the content must be correct
            assert object_content == content


@pytest.mark.parametrize('trust_existing', [True, False])
def test_object_writer_existing_corrupted(temp_dir, trust_existing):  # pylint: disable=invalid-name
    """Test that the ObjectWriter replaces an existing corrupted (wrong hash) loose object."""
    sandbox_folder = os.path.join(temp_dir, 'sandbox')
    loose_folder = os.path.join(temp_dir, 'loose')
    loose_prefix_len = 2
    hash_type = 'sha256'
    os.mkdir(sandbox_folder)
    os.mkdir(loose_folder)

    content = b'523453dfvsd'
    hasher = utils._get_hash(hash_type=hash_type)()  # pylint: disable=protected-access
    hasher.update(content)
    hashkey = hasher.hexdigest()

    # Some content that does not match the hash key
    corrupted_content = b'CORRUPTED CONTENT'

    loose_file = os.path.join(loose_folder, hashkey[:loose_prefix_len], hashkey[loose_prefix_len:])
    os.mkdir(os.path.dirname(loose_file))
    with open(loose_file, 'wb') as fhandle:
        fhandle.write(corrupted_content)

    # Check the starting condition
    assert not os.listdir(sandbox_folder)
    assert len(os.listdir(loose_folder)) == 1
    assert len(os.listdir(os.path.dirname(loose_file))) == 1

    object_writer = utils.ObjectWriter(
        sandbox_folder=sandbox_folder,
        loose_folder=loose_folder,
        loose_prefix_len=loose_prefix_len,
        hash_type=hash_type,
        trust_existing=trust_existing
    )

    with object_writer as fhandle:
        # Write some content (this should end up in the same `loose_file` location)
        fhandle.write(content)

    # Check the end condition:
    # nothing in the sandbox, nothing new in the loose_folder
    assert not os.listdir(sandbox_folder)
    assert len(os.listdir(loose_folder)) == 1
    assert len(os.listdir(os.path.dirname(loose_file))) == 1

    # Check now the content
    with open(loose_file, 'rb') as fhandle:
        object_content = fhandle.read()

    if trust_existing:
        # If I trust existing files, the content shouldn't have been touched
        assert object_content == corrupted_content
    else:
        # If I don't trust existing files, the content should have been replaced
        assert object_content == content


def test_unknown_hash_type(temp_dir):
    """Test that the ObjectWriter does not write anything if there is an exception."""
    sandbox_folder = os.path.join(temp_dir, 'sandbox')
    loose_folder = os.path.join(temp_dir, 'loose')
    loose_prefix_len = 2
    os.mkdir(sandbox_folder)
    os.mkdir(loose_folder)

    with pytest.raises(ValueError):
        object_writer = utils.ObjectWriter(
            sandbox_folder=sandbox_folder,
            loose_folder=loose_folder,
            loose_prefix_len=loose_prefix_len,
            hash_type='unknown_hash_string'
        )
        # The exception is actually raised here
        with object_writer as fhandle:
            # Write some content first
            fhandle.write('something')


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
    original_data_long_random = os.urandom(4000000)

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


# Set as the second parameter the hash of the 'content' string written below
# inside the test function
@pytest.mark.parametrize(
    'hash_type,expected_hash', [['sha256', '9975d00a6e715d830aeaa035347b3e601a0c0bb457a7f87816300e7c01c0c39b']]
)
def test_hash_writer_wrapper(temp_dir, hash_type, expected_hash):
    """Test some functionality of the HashWriterWrapper class."""
    content = b'some-content-to-hash'
    filename = 'test_file'

    with open(os.path.join(temp_dir, filename), 'wb') as fhandle:
        wrapped = utils.HashWriterWrapper(fhandle, hash_type=hash_type)
        wrapped.write(content)
        # Check that the flush command does not raise
        wrapped.flush()
        assert wrapped.hexdigest() == expected_hash
        assert wrapped.hash_type == hash_type

    with open(os.path.join(temp_dir, filename), 'rb') as fhandle:
        assert fhandle.read() == content
