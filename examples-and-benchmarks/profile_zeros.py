#!/usr/bin/env python
"""A simple profiling test to write a single large file (only containing zeros).

This checks the performance (can be run with profiling as well) and can be used to check
that in streaming mode, even when dealing with very large data, the memory usage is always
limited."""
import click
import psutil
import numpy as np

from disk_objectstore.container import Container


def get_memory():
    """Get memory info on the current process."""
    full_info = psutil.Process().as_dict(attrs=['memory_full_info'])['memory_full_info']
    return {
        'rss': full_info.rss,
        'vms': full_info.vms,
        'uss': full_info.uss,
    }


class LimitLengthWrapper:
    """A class to read from an open file handle, but stop after a given length.

    This ensures that the .read() method works and does not go beyond the
    length of the given object."""

    @property
    def seekable(self):
        """Return whether object supports random access."""
        return False

    def seek(self, target, whence=0):  # pylint: disable=unused-argument,no-self-use
        """Change stream position."""
        raise OSError('Object not seekable')

    def tell(self):  # pylint: disable=no-self-use
        """Return current stream position."""
        raise OSError('Object not seekable')

    def __init__(self, fhandle, length):
        """
        Initialises the reader to a pack file.

        :param fhandle: an open handle to the pack file, must be opened in read and binary mode.
        :param length: the integer length of the byte stream.
          The read() method will ensure that you never go beyond the given length.
        """
        assert 'b' in fhandle.mode
        assert 'r' in fhandle.mode

        self._fhandle = fhandle
        self._length = length
        self._pos = 0

    def read(self, size=-1):
        """
        Read and return up to n bytes.

        If the argument is omitted, None, or negative, reads and
        returns all data until EOF (that corresponds to the length specified
        in the __init__ method).

        Returns an empty bytes object on EOF.
        """
        # Check how many bytes are left on this portion of the pack
        # (avoid to go beyond)
        remaining_bytes = self._length - self._pos

        if size is None or size < 0:
            stream = self._fhandle.read(remaining_bytes)
            self._pos += remaining_bytes
            return stream

        # Get the requested bytes, but at most the remaining_bytes
        bytes_to_fetch = min(remaining_bytes, size)
        stream = self._fhandle.read(bytes_to_fetch)
        self._pos += bytes_to_fetch
        return stream


@click.command()
@click.option('-s', '--size-gb', default=1, help='File size in GB.')
@click.option(
    '-p',
    '--path',
    default='/tmp/test-container',
    help='The path to a test folder in which the container will be created.'
)
@click.option('-c', '--clear', is_flag=True, help='Clear the repository path folder before starting.')
@click.option(
    '-m', '--check-memory-measurement', is_flag=True, help='Clear the repository path folder before starting.'
)
@click.option('-z', '--compress-packs', is_flag=True, help='Compress objects while packing.')
@click.help_option('-h', '--help')
def main(size_gb, path, clear, check_memory_measurement, compress_packs):
    """Testing performance and size on disk when storing a single big file containing only zeros."""
    # pylint: disable=too-many-locals,too-many-statements
    import time

    start_mem = get_memory()

    if check_memory_measurement:  # To test that the measurement of the memory is reliable
        # Test of memory allocation
        size_factor = 100  # 1 means 8MB (size of float64) -> this will allocate a 800MB array in mem
        size = size_factor * 1024 * 1024
        temp_array = np.zeros(size, dtype=np.float64)  #  noqa: F841

        print('*' * 74)
        print('AFTER CREATING AN ARRAY of {} MBs:'.format(size_factor * 8))
        end_mem = get_memory()
        for key in end_mem:
            print(
                '{}: {} -> {} (DELTA = {} = {:.2f} MB)'.format(
                    key, start_mem[key], end_mem[key], end_mem[key] - start_mem[key],
                    (end_mem[key] - start_mem[key]) / 1024. / 1024.
                )
            )
        del temp_array

        print('*' * 74)
        print('AFTER DELETING THE ARRAY:')
        end_mem = get_memory()
        for key in end_mem:
            print(
                '{}: {} -> {} (DELTA = {} = {:.2f} MB)'.format(
                    key, start_mem[key], end_mem[key], end_mem[key] - start_mem[key],
                    (end_mem[key] - start_mem[key]) / 1024. / 1024.
                )
            )
        print('*' * 74)

    container = Container(path)
    if clear:
        print('Clearing the container...')
        container.init_container(clear=clear)
    if not container.is_initialised:
        print('Initialising the container...')
        container.init_container()

    size_bytes = size_gb * 1024 * 1024 * 1024

    start_counts = container.count_objects()
    print('Currently known objects: {} packed, {} loose'.format(start_counts['packed'], start_counts['loose']))
    print('Pack objects on disk:', start_counts['pack_files'])

    with open('/dev/zero', 'rb') as zero_handle:
        zero_stream = LimitLengthWrapper(zero_handle, length=size_bytes)
        start = time.time()
        # Store objects (directly to pack)
        obj_uuid = container.add_streamed_objects_to_pack(stream_list=[zero_stream], compress=compress_packs)[0]
        tot_time = time.time() - start
        print('Time to store one file of zeros of size {} GB: {:.4} s'.format(size_gb, tot_time))

    # Check that no loose files were created
    counts = container.count_objects()
    assert counts['loose'] == start_counts['loose'], 'Mismatch (loose in packed case): {} != {}'.format(
        start_counts['loose'], counts['loose']
    )
    assert counts['packed'] == start_counts['packed'] + 1, 'Mismatch (packed in packed case): {} + 1 != {}'.format(
        start_counts['packed'], counts['packed']
    )

    # print container size info
    size_info = container.get_total_size()
    print('Object store size info:')
    for key in sorted(size_info.keys()):
        print('- {:30s}: {}'.format(key, size_info[key]))

    # Retrieve the object (if it's too small (a few KB) it's slow)
    chunk_size = 16 * 1024 * 1024
    num_bytes_retrieved = 0

    start = time.time()
    with container.get_object_stream(obj_uuid) as retrieved_stream:
        while True:
            data = retrieved_stream.read(chunk_size)
            # Note that this takes ~50% of the time (1s out of 3s)
            assert data == bytes(len(data))  # string of zeros
            num_bytes_retrieved += len(data)
            if not data:
                break

    tot_time = time.time() - start
    print('Time to retrieve 1 packed object of size {} GB: {} s'.format(size_gb, tot_time))

    assert size_bytes == num_bytes_retrieved
    #assert md5_beginning == md5_retrieved

    print('All tests passed')

    end_mem = get_memory()
    for key in end_mem:
        print(
            '{}: {} -> {} (DELTA = {} = {:.2f} MB)'.format(
                key, start_mem[key], end_mem[key], end_mem[key] - start_mem[key],
                (end_mem[key] - start_mem[key]) / 1024. / 1024.
            )
        )


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
