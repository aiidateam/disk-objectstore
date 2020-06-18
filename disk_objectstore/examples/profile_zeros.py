#!/usr/bin/env python
"""A simple profiling test to write a single large file (only containing zeros).

This checks the performance (can be run with profiling as well) and can be used to check
that in streaming mode, even when dealing with very large data, the memory usage is always
limited."""
import time

import click
import psutil

from memory_profiler import memory_usage, profile

from disk_objectstore import Container
from disk_objectstore.utils import ZeroStream


def get_memory():
    """Get memory info on the current process."""
    full_info = psutil.Process().as_dict(attrs=['memory_full_info'])['memory_full_info']
    return {
        'rss': full_info.rss,
        'vms': full_info.vms,
        'uss': full_info.uss,
    }


def main_run(container, size_gb, compress_packs):
    """Main function run, possibly to be profiled."""
    size_bytes = size_gb * 1024 * 1024 * 1024

    start_counts = container.count_objects()
    print('Currently known objects: {} packed, {} loose'.format(start_counts['packed'], start_counts['loose']))
    print('Pack objects on disk:', start_counts['pack_files'])

    zero_stream = ZeroStream(length=size_bytes)
    start = time.time()
    # Store objects (directly to pack)
    obj_hashkey = container.add_streamed_objects_to_pack(stream_list=[zero_stream], compress=compress_packs)[0]
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
    with container.get_object_stream(obj_hashkey) as retrieved_stream:
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


@click.command()
@click.option('-s', '--size-gb', default=1, help='File size in GB.')
@click.option(
    '-p',
    '--path',
    default='/tmp/test-container',
    help='The path to a test folder in which the container will be created.'
)
@click.option('-c', '--clear', is_flag=True, help='Clear the repository path folder before starting.')
@click.option('-m', '--check-memory-measurement', is_flag=True, help='Perform various additional memory measurements.')
@click.option('-l', '--with-line-profiler', is_flag=True, help='When profiling memory, also run a line profiler.')
@click.option('-z', '--compress-packs', is_flag=True, help='Compress objects while packing.')
@click.help_option('-h', '--help')
def main(size_gb, path, clear, check_memory_measurement, with_line_profiler, compress_packs):
    """Testing performance and size on disk when storing a single big file containing only zeros."""
    start_mem = get_memory()

    if check_memory_measurement:  # To test that the measurement of the memory is reliable
        # Test of memory allocation
        size_mb = 400
        size = size_mb * 1024 * 1024
        temp_array = b'\x00' * size  #  noqa: F841

        print('*' * 74)
        print('AFTER CREATING AN ARRAY of {} MBs:'.format(size_mb))
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

    function = profile(main_run) if with_line_profiler else main_run
    if check_memory_measurement:
        memory_check_interval = 0.01  # seconds
        # memory_report will be a list of memory every 'interval'
        memory_report = memory_usage(
            (function, tuple(), {
                'container': container,
                'size_gb': size_gb,
                'compress_packs': compress_packs
            }),
            interval=memory_check_interval
        )
        # Check that it's not an empty list
        assert memory_report, (
            '>> Process too fast for checking memory usage '
            'with interval {} s!!!'.format(memory_check_interval)
        )
        print(
            '>> Max memory usage (check interval {} s, {} checks performed): {:.3f} MB'.format(
                memory_check_interval, len(memory_report), max(memory_report)
            )
        )
    else:
        function(container=container, size_gb=size_gb, compress_packs=compress_packs)

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
