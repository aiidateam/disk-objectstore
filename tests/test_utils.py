"""Test of the utils wrappers."""
import functools
import hashlib
import io
import os
import tempfile
import zlib

import psutil
import pytest

from disk_objectstore import utils

import disk_objectstore.exceptions as exc

# I need these definitions later for the mocked function
os._actual_replace_function = os.replace  # pylint: disable=protected-access
utils._actual_compute_hash_for_filename = utils._compute_hash_for_filename  # pylint: disable=protected-access


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
    duplicates_folder = os.path.join(temp_dir, 'duplicates')

    hash_type = 'sha256'
    expected_hash = '9975d00a6e715d830aeaa035347b3e601a0c0bb457a7f87816300e7c01c0c39b'
    content = b'some-content-to-hash'

    # Create the two folders, make sure they
    # are empty
    os.mkdir(sandbox_folder)
    os.mkdir(loose_folder)
    os.mkdir(duplicates_folder)
    assert not os.listdir(sandbox_folder)
    assert not os.listdir(loose_folder)
    assert not os.listdir(duplicates_folder)

    object_writer = utils.ObjectWriter(
        sandbox_folder=sandbox_folder,
        loose_folder=loose_folder,
        loose_prefix_len=loose_prefix_len,
        duplicates_folder=duplicates_folder,
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


def test_object_writer_duplicates_function(temp_dir):  # pylint: disable=invalid-name
    """Test that the _store_duplicate_copy function works."""
    sandbox_folder = os.path.join(temp_dir, 'sandbox')
    loose_folder = os.path.join(temp_dir, 'loose')
    duplicates_folder = os.path.join(temp_dir, 'duplicates')
    os.mkdir(sandbox_folder)
    os.mkdir(loose_folder)
    os.mkdir(duplicates_folder)

    # The duplicates folder should be empty at the beginning
    assert not os.listdir(duplicates_folder)

    content = b'24tq34waSDV'
    hash_type = 'sha256'

    object_writer = utils.ObjectWriter(
        sandbox_folder=sandbox_folder,
        loose_folder=loose_folder,
        loose_prefix_len=2,
        duplicates_folder=duplicates_folder,
        hash_type=hash_type
    )

    temp_path = os.path.join(sandbox_folder, 'tmp-file-name')
    with open(temp_path, 'wb') as fhandle:
        fhandle.write(content)
    hashkey = getattr(hashlib, hash_type)(content).hexdigest

    object_writer._store_duplicate_copy(source_file=temp_path, hashkey=hashkey)  # pylint: disable=protected-access
    # The duplicates folder should be empty at the beginning
    duplicates_files = os.listdir(duplicates_folder)
    assert len(duplicates_files) == 1, 'There is more than one file in the duplicates! {}'.format(duplicates_files)
    duplicates_file = duplicates_files[0]
    # The duplicate should start with the hashkey followed by a dot
    assert duplicates_file.startswith('{}.'.format(hashkey))


def test_object_writer_with_exc(temp_dir):
    """Test that the ObjectWriter does not write anything if there is an exception."""
    sandbox_folder = os.path.join(temp_dir, 'sandbox')
    loose_folder = os.path.join(temp_dir, 'loose')
    duplicates_folder = os.path.join(temp_dir, 'duplicates')
    loose_prefix_len = 2
    os.mkdir(sandbox_folder)
    os.mkdir(loose_folder)
    os.mkdir(duplicates_folder)

    content = b'523453dfvsd'

    object_writer = utils.ObjectWriter(
        sandbox_folder=sandbox_folder,
        loose_folder=loose_folder,
        loose_prefix_len=loose_prefix_len,
        duplicates_folder=duplicates_folder,
        hash_type='sha256'
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
    duplicates_folder = os.path.join(temp_dir, 'duplicates')
    loose_prefix_len = 2
    os.mkdir(sandbox_folder)
    os.mkdir(loose_folder)
    os.mkdir(duplicates_folder)

    content = b'523453dfvsd'

    object_writer = utils.ObjectWriter(
        sandbox_folder=sandbox_folder,
        loose_folder=loose_folder,
        loose_prefix_len=loose_prefix_len,
        duplicates_folder=duplicates_folder,
        hash_type='sha256'
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
    duplicates_folder = os.path.join(temp_dir, 'duplicates')
    loose_prefix_len = 2
    os.mkdir(sandbox_folder)
    os.mkdir(loose_folder)
    os.mkdir(duplicates_folder)

    content = b'523453dfvsd'

    object_writer = utils.ObjectWriter(
        sandbox_folder=sandbox_folder,
        loose_folder=loose_folder,
        loose_prefix_len=loose_prefix_len,
        duplicates_folder=duplicates_folder,
        hash_type='sha256'
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
    assert 'already tried to store' in str(excinfo.value)


@pytest.mark.parametrize('reappears_corrupted', [True, False])
@pytest.mark.parametrize('trust_existing', [True, False])
def test_object_writer_existing_corrupted_reappears(  # pylint: disable=invalid-name, too-many-locals
        temp_dir, trust_existing, reappears_corrupted, monkeypatch
    ):
    """Test that the ObjectWriter replaces an existing corrupted (wrong hash) loose object.

    Moreover, if reappears_corrupted is True, I patch `os.replace` to overwrite the destination with corrupted content
    are re-open it in read mode before calling the replace function, to check if I get any exception (especially on
    Windows).
    """
    sandbox_folder = os.path.join(temp_dir, 'sandbox')
    loose_folder = os.path.join(temp_dir, 'loose')
    duplicates_folder = os.path.join(temp_dir, 'duplicates')
    loose_prefix_len = 2
    hash_type = 'sha256'
    os.mkdir(sandbox_folder)
    os.mkdir(loose_folder)
    os.mkdir(duplicates_folder)

    content = b'523453dfvsd'
    hasher = utils.get_hash(hash_type=hash_type)()
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
        duplicates_folder=duplicates_folder,
        hash_type=hash_type,
        trust_existing=trust_existing
    )

    def mockreplace(src, dest, mocked_dest, new_bytes_content):
        """Replace a file, but if the dest is the mocked destination, before replacing, opens the existing file.

        It also rewrites the file with the new_bytes_content beforehand.
        """
        if os.path.realpath(dest) == os.path.realpath(mocked_dest):
            # Write back the file, with possibly a different content
            with open(dest, 'wb') as fhandle:
                fhandle.write(new_bytes_content)

                # Call the actual replace function, but while the file is open in read mode
                with open(dest, 'rb') as fhandle:
                    os._actual_replace_function(src, dest)  # pylint: disable=protected-access
        else:
            # It's a different path: just pipe through
            # I renamed this at module load to avoid infinite recursion, see above
            os._actual_replace_function(src, dest)  # pylint: disable=protected-access

    new_bytes_content = corrupted_content if reappears_corrupted else content
    monkeypatch.setattr(
        os, 'replace', functools.partial(mockreplace, mocked_dest=loose_file, new_bytes_content=new_bytes_content)
    )

    if os.name == 'nt' and not trust_existing and reappears_corrupted:
        # On Windows, if the file reappears, is corrupted, and cannot be replaced (is open)
        # then we store a duplicate copy.
        duplicates_files = os.listdir(duplicates_folder)
        assert len(duplicates_files) == 1
        duplicates_file = duplicates_files[0]
        assert duplicates_file.startswith('{}.'.format(hashkey))
    else:
        # I would like that on any other OS (POSIX), the object_writer works without exceptions
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
            # the corrupted file is left in place (there isn't much I can do)
            assert object_content == corrupted_content
        else:
            # In all other cases, if I don't trust existing files, the content should have been replaced,
            # and and if the DynamicInconsistentContent exception wasn't raised, the content must be correct
            assert object_content == content


@pytest.mark.parametrize('object_existed', [True, False])
def test_object_writer_deleted_while_checking_content(  # pylint: disable=invalid-name
        temp_dir, object_existed, monkeypatch
    ):
    """Test that the ObjectWriter works also when the destination gets deleted while checking.

    I check both the case in which the object existed, and the one in which it didn't (in which case, the
    mocking shouldn't do anything).
    """
    sandbox_folder = os.path.join(temp_dir, 'sandbox')
    loose_folder = os.path.join(temp_dir, 'loose')
    duplicates_folder = os.path.join(temp_dir, 'duplicates')
    loose_prefix_len = 2
    hash_type = 'sha256'
    trust_existing = False  # This branch is only called in this case
    os.mkdir(sandbox_folder)
    os.mkdir(loose_folder)
    os.mkdir(duplicates_folder)

    content = b'523453dfvsd'
    hasher = utils.get_hash(hash_type=hash_type)()
    hasher.update(content)
    hashkey = hasher.hexdigest()

    # I write already the loose destination
    loose_file = os.path.join(loose_folder, hashkey[:loose_prefix_len], hashkey[loose_prefix_len:])
    os.mkdir(os.path.dirname(loose_file))

    # Create the object, if `object_existed` is True (meaning that it existed before calling the ObjectWriter)
    if object_existed:
        with open(loose_file, 'wb') as fhandle:
            fhandle.write(content)

    # Check the starting condition
    assert not os.listdir(sandbox_folder)
    assert len(os.listdir(loose_folder)) == 1
    assert len(os.listdir(os.path.dirname(loose_file))) == (1 if object_existed else 0)

    def mock_compute_hash(filename, hash_type, mocked_filename):
        """Replace lowelevel_utils._compute_hash_for_filename by first deleting the destination file.

        .. note:: this is performed only for the mocked filename.

        This should return `None` but I prefer mocking in case the behavior is changed in the future.
        """
        # Delete the filename before calling through the actual function (if it exists)
        if os.path.realpath(filename) == os.path.realpath(mocked_filename) and os.path.exists(filename):
            os.remove(filename)

        # Now, just pipe through
        # I renamed this at module load to avoid infinite recursion, see above
        utils._actual_compute_hash_for_filename(filename, hash_type)  # pylint: disable=protected-access

    monkeypatch.setattr(
        utils, '_compute_hash_for_filename', functools.partial(mock_compute_hash, mocked_filename=loose_file)
    )

    object_writer = utils.ObjectWriter(
        sandbox_folder=sandbox_folder,
        loose_folder=loose_folder,
        loose_prefix_len=loose_prefix_len,
        duplicates_folder=duplicates_folder,
        hash_type=hash_type,
        trust_existing=trust_existing
    )

    with object_writer as fhandle:
        # Write some content (this should end up in the same `loose_file` location)
        fhandle.write(content)

    # Check the end condition
    # nothing in the sandbox, and:
    # - NOTHING in the loose_folder if object_existed is True: someone deleted in the meantime, and it's
    #   the choice of the current implementation that the file is not put back in place,
    #   as discussed in the comments in the ObjectWriter class
    # - a file if the file wasn't there from the beginning
    assert not os.listdir(sandbox_folder)
    assert len(os.listdir(loose_folder)) == 1
    assert len(os.listdir(os.path.dirname(loose_file))) == (0 if object_existed else 1)


@pytest.mark.parametrize('trust_existing', [True, False])
def test_object_writer_existing_OK(temp_dir, trust_existing):  # pylint: disable=invalid-name
    """Test that the ObjectWriter works if the loose object already exists (with the correct content)."""
    sandbox_folder = os.path.join(temp_dir, 'sandbox')
    loose_folder = os.path.join(temp_dir, 'loose')
    duplicates_folder = os.path.join(temp_dir, 'duplicates')
    loose_prefix_len = 2
    hash_type = 'sha256'
    os.mkdir(sandbox_folder)
    os.mkdir(loose_folder)
    os.mkdir(duplicates_folder)

    content = b'523453dfvsd'
    hasher = utils.get_hash(hash_type=hash_type)()
    hasher.update(content)
    hashkey = hasher.hexdigest()

    # Write already the content in place
    loose_file = os.path.join(loose_folder, hashkey[:loose_prefix_len], hashkey[loose_prefix_len:])
    os.mkdir(os.path.dirname(loose_file))
    with open(loose_file, 'wb') as fhandle:
        fhandle.write(content)

    # Check the starting condition
    assert not os.listdir(sandbox_folder)
    assert len(os.listdir(loose_folder)) == 1
    assert len(os.listdir(os.path.dirname(loose_file))) == 1

    object_writer = utils.ObjectWriter(
        sandbox_folder=sandbox_folder,
        loose_folder=loose_folder,
        loose_prefix_len=loose_prefix_len,
        duplicates_folder=duplicates_folder,
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

    assert object_content == content


@pytest.mark.parametrize('trust_existing', [True, False])
def test_object_writer_existing_corrupted(temp_dir, trust_existing):  # pylint: disable=invalid-name
    """Test that the ObjectWriter replaces an existing corrupted (wrong hash) loose object."""
    sandbox_folder = os.path.join(temp_dir, 'sandbox')
    loose_folder = os.path.join(temp_dir, 'loose')
    duplicates_folder = os.path.join(temp_dir, 'duplicates')
    loose_prefix_len = 2
    hash_type = 'sha256'
    os.mkdir(sandbox_folder)
    os.mkdir(loose_folder)
    os.mkdir(duplicates_folder)

    content = b'523453dfvsd'
    hasher = utils.get_hash(hash_type=hash_type)()
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
        duplicates_folder=duplicates_folder,
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
    duplicates_folder = os.path.join(temp_dir, 'duplicates')
    loose_prefix_len = 2
    os.mkdir(sandbox_folder)
    os.mkdir(loose_folder)
    os.mkdir(duplicates_folder)

    with pytest.raises(ValueError):
        object_writer = utils.ObjectWriter(
            sandbox_folder=sandbox_folder,
            loose_folder=loose_folder,
            loose_prefix_len=loose_prefix_len,
            duplicates_folder=duplicates_folder,
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
        assert packed_reader.seekable

        # Check that whence==1 and whence==2 are not implemented
        with pytest.raises(NotImplementedError):
            packed_reader.seek(0, 1)
        with pytest.raises(NotImplementedError):
            packed_reader.seek(0, 2)

        # Check that negative values and values > length are not valid
        with pytest.raises(ValueError):
            packed_reader.seek(-3)
        with pytest.raises(ValueError):
            packed_reader.seek(length + 1)

        # Seek and read all the rest
        for start in range(length + 1):
            packed_reader.seek(start)
            assert packed_reader.tell() == start
            assert packed_reader.read() == expected_bytestream[start:]
            assert packed_reader.tell() == length

        # Seek and read up to byte #4; it make sense for start to get until 4
        last_byte = 4
        for start in range(last_byte + 1):
            packed_reader.seek(start)
            assert packed_reader.tell() == start
            assert packed_reader.read(last_byte - start) == expected_bytestream[start:last_byte]
            assert packed_reader.tell() == last_byte

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


def test_packed_object_reader_mode():
    """Test the ``PackedObjectReader.mode`` property."""
    with tempfile.TemporaryFile() as handle:
        reader = utils.PackedObjectReader(handle, 0, 0)

        assert hasattr(reader, 'mode')
        assert reader.mode == handle.mode


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


def test_stream_decompresser_seek():
    """Test the seek (and tell) functionality of the StreamDecompresser."""

    original_data = b'0123456789abcdefABCDEF'
    length = len(original_data)

    compressed_stream = io.BytesIO(zlib.compress(original_data))
    decompresser = utils.StreamDecompresser(compressed_stream)

    # Check the functionality is disabled
    assert decompresser.seekable

    # Check that whence==1 and whence==2 are not implemented
    with pytest.raises(NotImplementedError):
        decompresser.seek(0, 1)
    with pytest.raises(NotImplementedError):
        decompresser.seek(0, 2)

    # Check that negative values and values > length are not valid
    with pytest.raises(ValueError):
        decompresser.seek(-3)

    # Seek and read all the rest; test also going beyond the length - in this case, I expect to get zero bytes returned
    for start in range(length + 10):
        decompresser.seek(start)
        assert decompresser.tell() == min(start, length)  # Never goes beyond length
        assert decompresser.read() == original_data[start:]
        assert decompresser.tell() == length

    # Seek and read up to byte #4; it make sense for start to get until 6
    last_byte = 6
    for start in range(last_byte + 1):
        decompresser.seek(start)
        assert decompresser.tell() == start
        assert decompresser.read(last_byte - start) == original_data[start:last_byte]
        assert decompresser.tell() == last_byte


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
        # Check the mode
        assert wrapped.mode == 'wb'

    with open(os.path.join(temp_dir, filename), 'rb') as fhandle:
        assert fhandle.read() == content


def test_chunk_iterator():
    """Test the correct functionality of the chunk iterator."""
    # Using `iter(range())` that is an iterator and does not have a length or allows
    # getting an element by index (i.e., `iter(range(10))` does not work), to make
    # sure this works also for iterators and not only for lists or similar

    # Check for lengths exactly multiple of the size
    assert list(utils.chunk_iterator(iter(range(9)), 3)) == [(0, 1, 2), (3, 4, 5), (6, 7, 8)]

    # Check for lengths that give a remainder
    assert list(utils.chunk_iterator(iter(range(10)), 3)) == [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9,)]


def test_compute_hash_from_filename(temp_dir):
    """Check the functionality of the _compute_hash_from_filename function."""
    content = b'2345j43'
    expected_hash = hashlib.sha256(content).hexdigest()

    fname = os.path.join(temp_dir, 'testfile')

    with open(fname, 'wb') as fhandle:
        fhandle.write(content)

    assert utils._compute_hash_for_filename(fname, 'sha256') == expected_hash  # pylint: disable=protected-access
    assert utils._compute_hash_for_filename(  # pylint: disable=protected-access
        os.path.join(temp_dir, 'NOT_EXISTENT_FILE'), 'sha256') is None


def test_is_known_hash():
    """Check the functionality of the is_known_hash function."""
    # At least sha256 should be supported
    assert utils.is_known_hash('sha256')
    # A weird string should not be a valid known hash
    assert not utils.is_known_hash('SOME_UNKNOWN_HASH_TYPE')
