"""Test basic I/O functionality.

This is also a way to verify the behavior of the underlying OS/filesystem.
"""
import os
import subprocess
import sys

import pytest

# pylint: disable=invalid-name


def test_concurrent_append_read(temp_dir):
    """Check what happens when reading a file that is being written in append mode in the meantime."""
    fname = os.path.join(temp_dir, 'test_file')

    first_part = b'v92jgwkf'
    intermediate = b'fbd9pjv2klmwg'
    second_part = b'2flemawlefm'

    with open(fname, 'ab') as write_handle:
        write_handle.write(first_part)
        # Flush to make sure everything is out of the buffer and visible to other processes
        write_handle.flush()

        # Verify that I can open in read mode and that I already find the content,
        # even if the write_handle is not closed
        with open(fname, 'rb') as read_handle:
            # Read the first part, check it's correct
            read_chunk = read_handle.read(len(first_part))
            assert read_chunk == first_part

            # Write the intermediate and the second part, and flush out buffers
            write_handle.write(intermediate)
            write_handle.write(second_part)
            write_handle.flush()

            # Check that the file size on disk is the expected one
            assert os.path.getsize(fname) == len(first_part) + len(intermediate) + len(second_part)

            # Now, jump to the beginning of the second part for reading (skipping 'intermediate')
            read_handle.seek(len(first_part) + len(intermediate))
            read_chunk = read_handle.read(len(second_part))
            assert read_chunk == second_part


def test_concurrent_append_read_multiprocess(temp_dir):
    """Check what happens when reading a file that is being written in append mode in the meantime."""
    fname = os.path.join(temp_dir, 'test_file')

    first_part = b'v92jgwkf'
    intermediate = b'fbd9pjv2klmwg'
    second_part = b'2flemawlefm'

    with open(fname, 'ab') as write_handle:
        write_handle.write(first_part)
        # Flush to make sure everything is out of the buffer and visible to other processes
        write_handle.flush()

        # Verify that I can open in read mode from a different process and that I already find the content,
        # even if the write_handle is not closed
        read_chunk = subprocess.check_output([
            sys.executable, '-c',
            'fhandle=open(r"{}"); print(fhandle.read(), end=""); fhandle.close()'.format(os.path.realpath(fname))
        ])
        assert read_chunk == first_part

        # Write the intermediate and the second part, and flush out buffers
        write_handle.write(intermediate)
        write_handle.write(second_part)
        write_handle.flush()

        # Check that the file size on disk is the expected one
        filesize_str = subprocess.check_output([
            sys.executable, '-c', 'import os; print(os.path.getsize(r"{}"), end="")'.format(os.path.realpath(fname))
        ])

        assert filesize_str == str(len(first_part) + len(intermediate) + len(second_part)).encode('ascii')

        # Now, jump to the beginning of the second part for reading (skipping 'intermediate')
        read_chunk = subprocess.check_output([
            sys.executable, '-c',
            'fhandle=open(r"{}"); fhandle.seek({}); print(fhandle.read(), end=""); fhandle.close()'.format(
                os.path.realpath(fname),
                len(first_part) + len(intermediate)
            )
        ])
        assert read_chunk == second_part


def test_concurrent_append_write_buffer_size(temp_dir):
    """While I keep the file open, I let another process write (in append mode) to the file.

    I also check that I have no issues with buffered read. To check this, I read a single byte (out of two written),
    and then I append more and continue reading.

    I check both when reading a fixed number of bytes (less than the total), and when exhausting the read
    (with read()) before re-appending.

    If the file is read as a buffer, I would expect that it might not notice immediately that content has been appended.
    """
    fname = os.path.join(temp_dir, 'test_file')

    first_part = b'v92'
    intermediate = b'efwefdf'
    second_part = b'2flemawlefm'

    # Let's write 2 bytes in the file
    with open(fname, 'wb') as write_handle:
        write_handle.write(first_part)

    with open(fname, 'rb') as read_handle:
        # Read only 1 byte
        beginning = read_handle.read(1)
        assert beginning == first_part[:1]

        # Let's append some content from a second process, in append (bytes) mode
        subprocess.check_output([
            sys.executable, '-c', 'fhandle=open(r"{}", "ab"); fhandle.write(b"{}"); fhandle.close()'.format(
                os.path.realpath(fname), intermediate.decode('ascii')
            )
        ])

        # Let's read three more bytes
        beginning += read_handle.read(3)
        assert beginning == (first_part + intermediate)[:1 + 3]

        # Read the rest until the end with no parameters to read()
        beginning += read_handle.read()
        assert beginning == first_part + intermediate

        # Append the second part
        subprocess.check_output([
            sys.executable, '-c', 'fhandle=open(r"{}", "ab"); fhandle.write(b"{}"); fhandle.close()'.format(
                os.path.realpath(fname), second_part.decode('ascii')
            )
        ])

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
    fname = os.path.join(temp_dir, 'test_file')

    content = b'rfr23ewv3wg4w'
    assert len(content) >= bytes_read_pre

    # Write something to the file
    with open(fname, 'wb') as fhandle:
        fhandle.write(content)

    # Now open again the file
    with open(fname, 'rb') as fhandle:
        if bytes_read_pre:
            read_content_pre = fhandle.read(bytes_read_pre)
        else:
            read_content_pre = b''

        # I (try to) delete the file in a different subprocess
        try:
            # I assume here that the fname does not contain double quotes
            subprocess.check_output([
                sys.executable, '-c', 'import os; os.remove(r"{}")'.format(os.path.realpath(fname))
            ],
                                    stderr=subprocess.STDOUT)
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
            assert os.path.isfile(fname), 'The file was actually deleted on Windows, unexpected!'
        else:
            assert os.name == 'posix', "I should be able to delete a file while it's still open only on POSIX!"
            assert not os.path.isfile(fname), "The file wasn't really deleted in POSIX, unexpected!"

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
        os.remove(fname)

    # The file should not be there on any platform, now
    assert not os.path.isfile(fname)


def test_rename_when_existing(temp_dir):
    """Check the different behavior of os.rename.

    On POSIX: I can delete silently rename even if open.
    On Windows: I cannot rename a file to a location where a file already exists.
    """
    fname = os.path.join(temp_dir, 'test_file')
    fname_replacement = os.path.join(temp_dir, 'test_file_repl')

    content = b'rfr23ewv3wg4w'
    first_part_len = 4

    new_content = b'NEWFILECONTENT'

    # Write something to the file
    with open(fname, 'wb') as fhandle:
        fhandle.write(content)

    # Write something to the file
    with open(fname_replacement, 'wb') as fhandle:
        fhandle.write(new_content)

    # Now open again the file
    with open(fname, 'rb') as fhandle:
        read_content_pre = fhandle.read(first_part_len)

        # I (try to) rename the file where the dest is the file that is open
        try:
            os.rename(fname_replacement, fname)
        except FileExistsError:
            # This should happen only on Windows
            assert os.name == 'nt', 'I should get a FileExistsError only on Windows!'

            # The source should still be there
            assert os.path.exists(fname_replacement)
            # I continue
        else:
            assert os.name == 'posix', 'I should be able to rername a file to an open destination on POSIX!'

            # The source should still not be there anymore
            assert not os.path.exists(fname_replacement)

        # Read the rest. On Windows, it should still be the original,
        # unreplaced file. On POSIX, it should be replaced, but I should
        # still be reading the original file.
        read_content = read_content_pre + fhandle.read()
        assert read_content == content

    # I reopen the file
    with open(fname, 'rb') as fhandle:
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
        os.remove(fname)
        os.rename(fname_replacement, fname)

    # Old file should not be there on any platform
    assert not os.path.exists(fname_replacement)

    # Now I should have the new file on any platform
    with open(fname, 'rb') as fhandle:
        read_content = fhandle.read()
        assert read_content == new_content


# Run only on Windows where we want to check the locking behavior
@pytest.mark.skipif(os.name != 'nt', reason='This test only makes sense on Windows')
def test_exclusive_mode_windows(temp_dir, lock_file_on_windows):
    """Test that indeed I can open a file with exclusive lock on Windows.

    This means someone else cannot even open the file in read mode.
    """
    fname = os.path.join(temp_dir, 'test_file')
    content = b'sfsfdkl;2fd'

    # Write something to the file
    with open(fname, 'wb') as fhandle:
        fhandle.write(content)

    # Now open the file with exclusive locking
    # we need to use os.open
    fd = os.open(fname, os.O_RDONLY)
    lock_file_on_windows(fd)

    # I (try to) read the file in a different subprocess
    try:
        # I assume here that the fname does not contain double quotes
        output = subprocess.check_output([
            sys.executable, '-c', 'f=open(r"{}", "rb"); print(f.read()); f.close()'.format(os.path.realpath(fname))
        ],
                                         stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        # I should get a PermissionError
        output = exc.output or b''  # It could be none
        assert b'PermissionError' in output
        read_content = os.fdopen(fd, 'rb', closefd=False).read()
        assert read_content == content, 'Unexpeced content: {}'.format(read_content)
        del read_content
    else:
        raise AssertionError('Subprocess should have raised! OUTPUT:\n{}'.format(output))
    finally:
        # Close the file at the end, important!
        # If I close, I shouldn't need to unlock
        #win32file.UnlockFileEx(winfd, 0, -0x10000, overlapped)
        os.close(fd)
