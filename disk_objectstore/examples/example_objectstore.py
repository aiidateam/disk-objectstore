#!/usr/bin/env python
"""A simple implementation with some testing to showcase the functionality and to run some benchmarks."""
import os
import uuid

import click
from profilehooks import profile

from disk_objectstore import Container


@click.command()
@click.option('-n', '--num-files', default=100, help='Number of files to create.')
@click.option('-m', '--min-size', default=0, help='Minimum file size (bytes).')
@click.option('-M', '--max-size', default=1000, help='Maximum file size (bytes).')
@click.option(
    '-d', '--directly-to-pack', is_flag=True, help='Add directly files to the packs rather than as loose objects.'
)
@click.option(
    '-p',
    '--path',
    default='/tmp/test-container',
    help='The path to a test folder in which the container will be created.'
)
@click.option('-c', '--clear', is_flag=True, help='Clear the repository path folder before starting.')
@click.option('-B', '--num-bulk-calls', default=10, help='Number of bulk calls to get the files.')
@click.option('-z', '--compress-packs', is_flag=True, help='Compress objects while packing.')
@click.option(
    '-P',
    '--profile-file',
    default=None,
    help='Perform the bulk read with profiling and output results onto this file name.'
)
@click.help_option('-h', '--help')
def main(num_files, min_size, max_size, directly_to_pack, path, clear, num_bulk_calls, compress_packs, profile_file):
    """Testing some basic functionality of the object-store, with timing."""
    # pylint: disable=too-many-arguments,too-many-locals,too-many-statements,too-many-branches
    import random
    import time

    container = Container(path)
    if clear:
        print('Clearing the container...')
        container.init_container(clear=clear)
    if not container.is_initialised:
        print('Initialising the container...')
        container.init_container()

    files = {}

    start_counts = container.count_objects()
    print('Currently known objects: {} packed, {} loose'.format(start_counts['packed'], start_counts['loose']))
    print('Pack objects on disk:', start_counts['pack_files'])

    print('Generating {} files in memory...'.format(num_files))
    for _ in range(num_files):
        filename = 'filename-{}'.format(str(uuid.uuid4()))
        size = random.randint(min_size, max_size)
        content = bytearray(random.getrandbits(8) for _ in range(size))
        files[filename] = content
    total_size = sum(len(content) for content in files.values())
    print('Done. Total size: {} bytes (~{:.3f} MB).'.format(total_size, (total_size // 1024) / 1024))

    if directly_to_pack:
        # Store objects (directly to pack)
        start = time.time()
        filenames = list(files.keys())
        files_content = [files[key] for key in filenames]
        uuids = container.add_objects_to_pack(files_content, compress=compress_packs)
        uuid_mapping = dict(zip(filenames, uuids))
        tot_time = time.time() - start
        print('Time to store {} objects DIRECTLY TO THE PACKS: {:.4} s'.format(num_files, tot_time))

        # Check that no loose files were created
        counts = container.count_objects()
        assert counts['loose'] == start_counts['loose'], 'Mismatch (loose in packed case): {} != {}'.format(
            start_counts['loose'], counts['loose']
        )
        assert counts['packed'
                     ] == start_counts['packed'] + num_files, 'Mismatch (packed in packed case): {} + {} != {}'.format(
                         start_counts['packed'], num_files, counts['packed']
                     )
    else:
        # Store objects (loose)
        start = time.time()
        uuid_mapping = {}
        for filename, content in files.items():
            obj_uuid = container.add_object(content)
            uuid_mapping[filename] = obj_uuid
        tot_time = time.time() - start
        print('Time to store {} loose objects: {:.4} s'.format(num_files, tot_time))

        # Retrieve objects (loose)
        retrieved = {}
        random_keys = list(files.keys())
        random.shuffle(random_keys)
        start = time.time()
        for filename in random_keys:
            obj_uuid = uuid_mapping[filename]
            retrieved_content = container.get_object_content(obj_uuid)
            retrieved[filename] = retrieved_content
        tot_time = time.time() - start
        print('Time to retrieve {} loose objects: {:.4} s'.format(num_files, tot_time))

        # Check that the content is correct
        for filename in retrieved:
            assert retrieved[filename] == files[filename], 'Mismatch (content) for {}'.format(filename)

        # Check that num_files new loose files are present now
        counts = container.count_objects()
        assert counts['loose'
                     ] == start_counts['loose'] + num_files, 'Mismatch (loose in unpacked case): {} + {} != {}'.format(
                         start_counts['loose'], num_files, counts['loose']
                     )

        # Print container size info (before packing)
        size_info = container.get_total_size()
        print('Object store size info:')
        for key in sorted(size_info.keys()):
            print('- {:30s}: {}'.format(key, size_info[key]))

        # Pack all loose objects
        start = time.time()
        container.pack_all_loose(compress=compress_packs)
        tot_time = time.time() - start
        print('Time to pack all loose objects: {:.4} s'.format(tot_time))

        # Check that all loose files are gone
        counts = container.count_objects()
        assert not counts['loose'], 'loose objects left: {}'.format(os.listdir(container._get_loose_folder()))  # pylint: disable=protected-access
        assert counts['packed'] == start_counts['packed'] + start_counts[
            'loose'] + num_files, 'Mismatch (post-pack): {} + {} + {} != {}'.format(
                start_counts['packed'], start_counts['loose'], num_files, counts['packed']
            )

    # print container size info
    size_info = container.get_total_size()
    print('Object store size info:')
    for key in sorted(size_info.keys()):
        print('- {:30s}: {}'.format(key, size_info[key]))

    # In all cases, retrieve all objects (in shuffled order)
    retrieved = {}
    random_keys = list(files.keys())
    random.shuffle(random_keys)

    # Will be needed later
    reverse_uuid_mapping = {v: k for k, v in uuid_mapping.items()}

    ########################################
    # FIRST: single bulk read
    def bulk_read_data(container, uuid_list):
        """A function to read the data in bulk.

        It's defined as a functon so it can be profiled."""
        return container.get_object_contents(uuid_list, skip_if_missing=False)

    all_uuids = [uuid_mapping[filename] for filename in random_keys]
    start = time.time()

    if profile_file is not None:
        func = profile(sort='cumtime', filename=profile_file, stdout=False)(bulk_read_data)
    else:
        func = bulk_read_data
    raw_retrieved = func(container=container, uuid_list=all_uuids)
    if profile_file is not None:
        print("You can check the profiling results running 'snakeviz {}'".format(profile_file))

    tot_time = time.time() - start
    print('Time to retrieve {} packed objects in random order WITH ONE BULK CALL: {} s'.format(num_files, tot_time))
    retrieved = {reverse_uuid_mapping[key]: val for key, val in raw_retrieved.items()}
    for filename in retrieved:
        assert retrieved[filename] == files[filename], 'Mismatch for {}'.format(filename)

    ########################################
    # SECOND: num_bulk_calls bulk reads
    random.shuffle(random_keys)
    all_uuids = [uuid_mapping[filename] for filename in random_keys]
    start = time.time()
    raw_retrieved = {}

    # Split the list into num_bulk_call even chunks
    chunk_len = len(all_uuids) // num_bulk_calls
    if len(all_uuids) % num_bulk_calls != 0:
        chunk_len += 1
    split_iterator = (all_uuids[start:start + chunk_len] for start in range(0, len(all_uuids), chunk_len))

    # Retrieve in num_bulk_call chunks
    for chunk_of_uuids in split_iterator:
        raw_retrieved.update(container.get_object_contents(chunk_of_uuids, skip_if_missing=False))

    tot_time = time.time() - start
    print(
        'Time to retrieve {} packed objects in random order WITH {} BULK CALLS: {} s'.format(
            num_files, num_bulk_calls, tot_time
        )
    )
    retrieved = {reverse_uuid_mapping[key]: val for key, val in raw_retrieved.items()}
    for filename in retrieved:
        assert retrieved[filename] == files[filename], 'Mismatch for {}'.format(filename)

    ########################################
    # THIRD: a lot of independent reads, one per object
    random.shuffle(random_keys)
    start = time.time()
    for filename in random_keys:
        obj_uuid = uuid_mapping[filename]
        retrieved_content = container.get_object_content(obj_uuid)
        retrieved[filename] = retrieved_content
    tot_time = time.time() - start
    print('Time to retrieve {} packed objects in random order: {} s'.format(num_files, tot_time))

    for filename in retrieved:
        assert retrieved[filename] == files[filename], 'Mismatch for {}'.format(filename)

    print('All tests passed')


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
