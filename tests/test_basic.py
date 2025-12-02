"""Test basic I/O functionality.

This is also a way to verify the behavior of the underlying OS/filesystem.
"""

import os
import subprocess
import sys

import pytest

from disk_objectstore import Container

# pylint: disable=invalid-name


def test_concurrent_append_read(temp_dir):
    """Check what happens when reading a file that is being written in append mode in the meantime."""
    fpath = temp_dir / 'test_file'

    first_part = b'v92jgwkf'
    intermediate = b'fbd9pjv2klmwg'
    second_part = b'2flemawlefm'

    with open(fpath, 'ab') as write_handle:
        write_handle.write(first_part)
        # Flush to make sure everything is out of the buffer and visible to other processes
        write_handle.flush()

        # Verify that I can open in read mode and that I already find the content,
        # even if the write_handle is not closed
        with open(fpath, 'rb') as read_handle:
            # Read the first part, check it's correct
            read_chunk = read_handle.read(len(first_part))
            assert read_chunk == first_part

            # Write the intermediate and the second part, and flush out buffers
            write_handle.write(intermediate)
            write_handle.write(second_part)
            write_handle.flush()

            # Check that the file size on disk is the expected one
            assert fpath.stat().st_size == len(first_part) + len(intermediate) + len(second_part)

            # Now, jump to the beginning of the second part for reading (skipping 'intermediate')
            read_handle.seek(len(first_part) + len(intermediate))
            read_chunk = read_handle.read(len(second_part))
            assert read_chunk == second_part


def test_concurrent_append_read_multiprocess(temp_dir):
    """Check what happens when reading a file that is being written in append mode in the meantime."""
    fpath = temp_dir / 'test_file'

    first_part = b'v92jgwkf'
    intermediate = b'fbd9pjv2klmwg'
    second_part = b'2flemawlefm'

    with open(fpath, 'ab') as write_handle:
        write_handle.write(first_part)
        # Flush to make sure everything is out of the buffer and visible to other processes
        write_handle.flush()

        # Verify that I can open in read mode from a different process and that I already find the content,
        # even if the write_handle is not closed
        read_chunk = subprocess.check_output(
            [
                sys.executable,
                '-c',
                f'fhandle=open(r"{fpath.resolve()}"); print(fhandle.read(), end=""); fhandle.close()',
            ]
        )
        assert read_chunk == first_part

        # Write the intermediate and the second part, and flush out buffers
        write_handle.write(intermediate)
        write_handle.write(second_part)
        write_handle.flush()

        # Check that the file size on disk is the expected one
        filesize_str = subprocess.check_output(
            [
                sys.executable,
                '-c',
                f'import pathlib; print(pathlib.Path(r"{fpath!s}").resolve().stat().st_size, end="")',
            ]
        )

        assert filesize_str == str(len(first_part) + len(intermediate) + len(second_part)).encode('ascii')

        # Now, jump to the beginning of the second part for reading (skipping 'intermediate')
        read_chunk = subprocess.check_output(
            [
                sys.executable,
                '-c',
                f'fhandle=open(r"{fpath.resolve()}"); '
                f'fhandle.seek({len(first_part) + len(intermediate)}); '
                'print(fhandle.read(), end=""); fhandle.close()',
            ]
        )
        assert read_chunk == second_part


def test_concurrent_append_write_buffer_size(temp_dir):
    """While I keep the file open, I let another process write (in append mode) to the file.

    I also check that I have no issues with buffered read. To check this, I read a single byte (out of two written),
    and then I append more and continue reading.

    I check both when reading a fixed number of bytes (less than the total), and when exhausting the read
    (with read()) before re-appending.

    If the file is read as a buffer, I would expect that it might not notice immediately that content has been appended.
    """
    fpath = temp_dir / 'test_file'

    first_part = b'v92'
    intermediate = b'efwefdf'
    second_part = b'2flemawlefm'

    # Let's write 2 bytes in the file
    with open(fpath, 'wb') as write_handle:
        write_handle.write(first_part)

    with open(fpath, 'rb') as read_handle:
        # Read only 1 byte
        beginning = read_handle.read(1)
        assert beginning == first_part[:1]

        # Let's append some content from a second process, in append (bytes) mode
        subprocess.check_output(
            [
                sys.executable,
                '-c',
                f'fhandle=open(r"{fpath.resolve()}", "ab"); '
                f'fhandle.write(b"{intermediate.decode("ascii")}"); fhandle.close()',
            ]
        )

        # Let's read three more bytes
        beginning += read_handle.read(3)
        assert beginning == (first_part + intermediate)[: 1 + 3]

        # Read the rest until the end with no parameters to read()
        beginning += read_handle.read()
        assert beginning == first_part + intermediate

        # Append the second part
        subprocess.check_output(
            [
                sys.executable,
                '-c',
                f'fhandle=open(r"{fpath.resolve()}", "ab"); '
                f'fhandle.write(b"{second_part.decode("ascii")}"); fhandle.close()',
            ]
        )

        # Read two bytes
        end = read_handle.read(2)
        assert end == second_part[:2]
        # Read the rest
        end += read_handle.read()
        assert end == second_part


@pytest.mark.parametrize('bytes_read_pre', [0, 3])
def test_deletion_while_open(temp_dir, bytes_read_pre):
    """Check the different behavior of deletion of an open file (in read mode).

    On POSIX: I can delete successfully the file and I can still read the content.
    On Windows: I cannot delete a file while it is open.

    :param bytes_read_pre: an integer stating how many bytes to read before (trying to) delete the open file.
    """
    fpath = temp_dir / 'test_file'

    content = b'rfr23ewv3wg4w'
    assert len(content) >= bytes_read_pre

    # Write something to the file
    with open(fpath, 'wb') as fhandle:
        fhandle.write(content)

    # Now open again the file
    with open(fpath, 'rb') as fhandle:
        if bytes_read_pre:
            read_content_pre = fhandle.read(bytes_read_pre)
        else:
            read_content_pre = b''

        # I (try to) delete the file in a different subprocess
        try:
            # I assume here that the fpath does not contain double quotes
            subprocess.check_output(
                [
                    sys.executable,
                    '-c',
                    f'import os; os.remove(r"{fpath.resolve()}")',
                ],
                stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError as exc:
            # On Windows, I should get:
            # PermissionError: [WinError 32] The process cannot access the file because
            # it is begin used by another process: '<filename>'
            assert os.name == 'nt', 'I should get a PermissionError only on Windows!'

            # I cannot check the error code since it's a different subprocess. As a note, it should be:
            # - errno.EACCES == 13
            # - os.streerror(exc.errno) == 'Permission denied'
            output = exc.output or b''  # It could be none
            assert b'PermissionError' in output
            assert fpath.is_file(), 'The file was actually deleted on Windows, unexpected!'
        else:
            assert os.name == 'posix', "I should be able to delete a file while it's still open only on POSIX!"
            assert not fpath.is_file(), "The file wasn't really deleted in POSIX, unexpected!"

        # In either case (I got an exception on Windows, I could delete the file on POSIX)
        # I should still be able to read the correct content.
        # Notably, on POSIX I can read even if the file is not there anymore.

        # I first check that I can get its size
        assert os.fstat(fhandle.fileno()).st_size == len(content)

        # And that I can read the rest of the content
        read_content_post = fhandle.read()
        assert read_content_pre + read_content_post == content

    # Now the file is closed. On POSIX, I know it's not there.
    # Let me try to delete it also on Windows.
    if os.name == 'nt':
        # Now that the file is closed, I should be able to remove it
        os.remove(fpath)

    # The file should not be there on any platform, now
    assert not fpath.is_file()


def test_rename_when_existing(temp_dir):
    """Check the different behavior of os.rename.

    On POSIX: I can delete silently rename even if open.
    On Windows: I cannot rename a file to a location where a file already exists.
    """
    fpath = temp_dir / 'test_file'
    fpath_replacement = temp_dir / 'test_file_repl'

    content = b'rfr23ewv3wg4w'
    first_part_len = 4

    new_content = b'NEWFILECONTENT'

    # Write something to the file
    with open(fpath, 'wb') as fhandle:
        fhandle.write(content)

    # Write something to the file
    with open(fpath_replacement, 'wb') as fhandle:
        fhandle.write(new_content)

    # Now open again the file
    with open(fpath, 'rb') as fhandle:
        read_content_pre = fhandle.read(first_part_len)

        # I (try to) rename the file where the dest is the file that is open
        try:
            os.rename(fpath_replacement, fpath)
        except FileExistsError:
            # This should happen only on Windows
            assert os.name == 'nt', 'I should get a FileExistsError only on Windows!'

            # The source should still be there
            assert fpath_replacement.exists()
            # I continue
        else:
            assert os.name == 'posix', 'I should be able to rername a file to an open destination on POSIX!'

            # The source should still not be there anymore
            assert not fpath_replacement.exists()

        # Read the rest. On Windows, it should still be the original,
        # unreplaced file. On POSIX, it should be replaced, but I should
        # still be reading the original file.
        read_content = read_content_pre + fhandle.read()
        assert read_content == content

    # I reopen the file
    with open(fpath, 'rb') as fhandle:
        read_content = fhandle.read()
        if os.name == 'nt':
            # On Windows I should still get the old content
            assert read_content == content
        else:
            # On POSIX it should be the new content
            assert read_content == new_content

    # I remove and replace the file on Windows to check that
    # I can indeed replace it
    if os.name == 'nt':
        os.remove(fpath)
        os.rename(fpath_replacement, fpath)

    # Old file should not be there on any platform
    assert not fpath_replacement.exists()

    # Now I should have the new file on any platform
    with open(fpath, 'rb') as fhandle:
        read_content = fhandle.read()
        assert read_content == new_content


# Run only on Windows where we want to check the locking behavior
@pytest.mark.skipif(os.name != 'nt', reason='This test only makes sense on Windows')
def test_exclusive_mode_windows(temp_dir, lock_file_on_windows):
    """Test that indeed I can open a file with exclusive lock on Windows.

    This means someone else cannot even open the file in read mode.
    """
    fpath = temp_dir / 'test_file'
    content = b'sfsfdkl;2fd'

    # Write something to the file
    with open(fpath, 'wb') as fhandle:
        fhandle.write(content)

    # Now open the file with exclusive locking
    # we need to use os.open
    fd = os.open(fpath, os.O_RDONLY)
    lock_file_on_windows(fd)

    # I (try to) read the file in a different subprocess
    try:
        # I assume here that the fpath does not contain double quotes
        output = subprocess.check_output(
            [
                sys.executable,
                '-c',
                f'f=open(r"{fpath.resolve()}", "rb"); print(f.read()); f.close()',
            ],
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as exc:
        # I should get a PermissionError
        output = exc.output or b''  # It could be none
        assert b'PermissionError' in output
        read_content = os.fdopen(fd, 'rb', closefd=False).read()
        assert read_content == content, f'Unexpeced content: {read_content}'
        del read_content
    else:
        raise AssertionError(f'Subprocess should have raised! OUTPUT:\n{output}')
    finally:
        # Close the file at the end, important!
        # If I close, I shouldn't need to unlock
        # win32file.UnlockFileEx(winfd, 0, -0x10000, overlapped)
        os.close(fd)


def test_get_pack_id_to_write_to_with_known_sizes(temp_container):
    """Unit test: Verify _get_pack_id_to_write_to correctly uses known_sizes parameter.

    Tests that when known_sizes is provided, it uses those values instead of stat()
    to determine which pack file to write to next.
    """
    pack_size_target = 1000
    temp_container.init_container(clear=True, pack_size_target=pack_size_target)

    # Test 1: Without known_sizes, should return pack 0 (doesn't exist yet)
    pack_id = temp_container._get_pack_id_to_write_to(known_sizes=None)
    assert pack_id == 0, 'Should start with pack 0 when no packs exist'

    # Create a small pack file (under target)
    pack_path = temp_container._get_pack_path_from_pack_id(0)
    pack_path.parent.mkdir(parents=True, exist_ok=True)
    with open(pack_path, 'wb') as f:
        f.write(b'x' * 500)  # 500 bytes, under the target

    # Test 2: Without known_sizes, should use stat() and return pack 0 (under target)
    pack_id = temp_container._get_pack_id_to_write_to(known_sizes=None)
    assert pack_id == 0, 'Should return pack 0 when it exists and is under target'

    # Test 3: With known_sizes showing pack 0 is not full, should return pack 0
    known_sizes = {0: 500}  # Under the target
    pack_id = temp_container._get_pack_id_to_write_to(known_sizes=known_sizes)
    assert pack_id == 0, 'Should return pack 0 when known_sizes shows pack 0 is not full'

    # Test 4: With known_sizes showing pack 0 is full, should return pack 1
    known_sizes = {0: 1500}  # Over the target
    pack_id = temp_container._get_pack_id_to_write_to(known_sizes=known_sizes)
    assert pack_id == 1, 'Should return pack 1 when known_sizes shows pack 0 is full'

    # Test 5: Multiple packs tracked in known_sizes
    # Create pack 1 that's also under target
    pack_path_1 = temp_container._get_pack_path_from_pack_id(1)
    with open(pack_path_1, 'wb') as f:
        f.write(b'y' * 600)

    # Now _current_pack_id is 1 (cached from previous test)
    # With known_sizes showing pack 1 is not full, should return pack 1
    known_sizes = {1: 800}  # Pack 1 not full
    pack_id = temp_container._get_pack_id_to_write_to(known_sizes=known_sizes)
    assert pack_id == 1, 'Should return pack 1 when it is cached and not full'

    # Test 6: Multiple packs, current one full, should increment
    known_sizes = {1: 1200}  # Pack 1 full
    pack_id = temp_container._get_pack_id_to_write_to(known_sizes=known_sizes)
    assert pack_id == 2, 'Should return pack 2 when pack 1 is full'

    # Test 7: Multiple packs in known_sizes with different states
    # Create pack 2
    pack_path_2 = temp_container._get_pack_path_from_pack_id(2)
    with open(pack_path_2, 'wb') as f:
        f.write(b'z' * 300)

    # known_sizes shows pack 2 is not full
    known_sizes = {0: 1500, 1: 1200, 2: 300}
    pack_id = temp_container._get_pack_id_to_write_to(known_sizes=known_sizes)
    assert pack_id == 2, 'Should return pack 2 when it is cached and not full'

    # Test 8: instantiate a new Container instance: this should not reuse the cache.
    # Even if packs 1 and 2 exist, since pack 0 is smaller, the function should return
    # pack 0.
    temp_container_new = Container(folder=temp_container.get_folder())
    pack_id = temp_container_new._get_pack_id_to_write_to()
    assert pack_id == 0, 'Should return pack 0 even if pack 1 and 2 exist, since pack 0 is smaller'
