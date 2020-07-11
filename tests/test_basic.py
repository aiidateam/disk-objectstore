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
            'fhandle=open("{}"); print(fhandle.read(), end=""); fhandle.close()'.format(os.path.realpath(fname))
        ])
        assert read_chunk == first_part

        # Write the intermediate and the second part, and flush out buffers
        write_handle.write(intermediate)
        write_handle.write(second_part)
        write_handle.flush()

        # Check that the file size on disk is the expected one
        filesize_str = subprocess.check_output([
            sys.executable, '-c', 'import os; print(os.path.getsize("{}"), end="")'.format(os.path.realpath(fname))
        ])

        assert filesize_str == str(len(first_part) + len(intermediate) + len(second_part)).encode('ascii')

        # Now, jump to the beginning of the second part for reading (skipping 'intermediate')
        read_chunk = subprocess.check_output([
            sys.executable, '-c',
            'fhandle=open("{}"); fhandle.seek({}); print(fhandle.read(), end=""); fhandle.close()'.format(
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
            sys.executable, '-c', 'fhandle=open("{}", "ab"); fhandle.write(b"{}"); fhandle.close()'.format(
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
            sys.executable, '-c', 'fhandle=open("{}", "ab"); fhandle.write(b"{}"); fhandle.close()'.format(
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
            subprocess.check_output([sys.executable, '-c' 'import os; os.remove("{}")'.format(os.path.realpath(fname))])
        except subprocess.CalledProcessError as exc:
            # On Windows, I should get:
            # PermissionError: [WinError 32] The process cannot access the file because
            # it is begin used by another process: '<filename>'
            assert os.name == 'nt', 'I should get a PermissionError only on Windows!'

            # I cannot check the error code since it's a different subprocess. As a note, it should be:
            # - errno.EACCES == 13
            # - os.streerror(exc.errno) == 'Permission denied'
            assert 'PermissionError' in exc.stderr
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
