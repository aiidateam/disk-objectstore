"""Test basic I/O functionality.

This is also a way to verify the behavior of the underlying OS/filesystem.
"""
import os


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

        # Verify that I can open in read ode and that I already find the content,
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


def test_deletion_while_open(temp_dir):
    """Check the different behavior of deletion of an open file (in read mode).

    On POSIX: I can delete successfully the file and I can still read the content.
    On Windows: I cannot delete a file while it is open.
    """
    fname = os.path.join(temp_dir, 'test_file')

    content = b'rfr23ewv3wg4w'

    # Write something to the file
    with open(fname, 'wb') as fhandle:
        fhandle.write(content)

    # Now open again the file
    with open(fname, 'rb') as fhandle:
        # After opening, and before starting to read, I delete the file
        try:
            os.remove(fname)
        except PermissionError as exc:
            # On Windows, I should get:
            # PermissionError: [WinError 32] The process cannot access the file because
            # it is begin used by another process: '<filename>'
            assert os.name == 'nt', 'I should get a PermissionError only on Windows!'

            # Check the error code
            # Notes:
            # - errno.EACCES == 13
            # - os.streerror(exc.errno) == 'Permission denied'
            assert exc.errno == 13
            assert os.path.isfile(fname), 'The file was actually deleted on Windows, unexpected!'
        else:
            assert os.name == 'posix', "I should be able to delete a file while it's still open only on POSIX!"
            assert not os.path.isfile(fname), "The file wasn't really deleted in POSIX, unexpected!"

        # In either case (I got an exception on Windows, I could delete the file on POSIX)
        # I should still be able to read the correct content.
        # Notably, on POSIX I can read even if the file is not there anymore.

        # I first check that I can get its size
        assert os.fstat(fhandle.fileno()).st_size == len(content)

        # And that I can read the content
        read_content = fhandle.read()
        assert read_content == content

    # Now the file is closed. On POSIX, I know it's not there.
    # Let me try to delete it also on Windows.
    if os.name == 'nt':
        # Now that the file is closed, I should be able to remove it
        os.remove(fname)

    # The file should not be there on any platform, now
    assert not os.path.isfile(fname)
