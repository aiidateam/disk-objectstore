#!/usr/bin/env python
import os
import uuid

import click

from repository.objectstore.container import Container

@click.command()
@click.option('-n', '--num-files', default=100, help='Number of files to create.')
@click.option('-m', '--min-size', default=0, help='Minimum file size (bytes).')
@click.option('-M', '--max-size', default=1000, help='Maximum file size (bytes).')
@click.option('-d', '--add-directly-to-pack', is_flag=True, help='Add directly files to the packs rather than as loose objects.')
@click.option('-p', '--path', default='test-container', help='The path to a test folder in which the container will be created.')
@click.option('-c', '--clear', is_flag=True, help='Clear the repository path folder before starting.')
@click.option('-z', '--compress-packs', is_flag=True, help='Compress objects while packing.')
@click.help_option('-h', '--help')
def main(num_files, min_size, # pylint: disable=too-many-arguments,too-many-locals,too-many-statements
        max_size, add_directly_to_pack, path, clear, compress_packs):
    """Testing some basic functionality of the object-store, with timing."""
    import random
    import time

    container = Container(path)
    container.init_container(clear=clear)

    files = {}

    start_counts = container.count_objects()
    print("Currently known objects: {} packed, {} loose".format(
        start_counts['packed'], start_counts['loose']))
    print("Pack objects on disk:", start_counts['pack_files'])

    print("Generating {} files in memory...".format(num_files))
    for _ in range(num_files):
        filename = str(uuid.uuid4())[:8]
        size = random.randint(min_size, max_size)
        content = bytearray(random.getrandbits(8) for _ in range(size))
        #md5 = str(hashlib.md5(content).hexdigest())
        #files[filename] = md5
        files[filename] = content
    total_size = sum(len(content) for content in files.values())
    print("Done. Total size: {} bytes (~{:.3f} MB).".format(total_size, (total_size // 1024) / 1024))

    if add_directly_to_pack:
        uuid_mapping = {}
        start = time.time()
        filenames = list(files.keys())
        files_content = [files[key] for key in filenames]
        uuids = container.add_objects_to_pack(files_content)
        uuid_mapping = dict(zip(filenames, uuids))
        tot_time = time.time() - start
        print("Time to store {} objects DIRECTLY TO THE PACKS: {:.4} s".format(
            num_files, tot_time))

        # No loose files were created
        counts = container.count_objects()
        assert counts['loose'] == start_counts['loose']
    else:
        start = time.time()
        uuid_mapping = {}
        for filename, content in files.items():
            obj_uuid = container.add_object(content)
            uuid_mapping[filename] = obj_uuid
        tot_time = time.time() - start
        print("Time to store {} loose objects: {:.4} s".format(
            num_files, tot_time))

        retrieved = {}
        random_keys = list(files.keys())
        random.shuffle(random_keys)
        start = time.time()
        for filename in random_keys:
            obj_uuid = uuid_mapping[filename]
            retrieved_content = container.get_object_content(obj_uuid)
            retrieved[filename] = retrieved_content
            #retrieved = str(hashlib.md5(retrieved_content).hexdigest())
        tot_time = time.time() - start
        print("Time to retrieve {} loose objects: {:.4} s".format(num_files, tot_time))

        for filename in retrieved:
            assert retrieved[filename] == files[filename], "Mismatch for {}".format(filename)

        # Check that num_files new loose files are present now
        counts = container.count_objects()
        assert counts['loose'] == start_counts['loose'] + num_files

        start = time.time()
        container.pack_all_loose(compress=compress_packs)
        tot_time = time.time() - start
        print("Time to pack all loose objects: {:.4} s".format(tot_time))

        # Check that all loose files are gone
        counts = container.count_objects()
        assert not counts['loose'], os.listdir(container._get_loose_folder())  # pylint: disable=protected-access

    size_info = container.get_total_size()
    print("Object store size info:")
    for key in sorted(size_info.keys()):
        print("- {:30s}: {}".format(key, size_info[key]))

    # In all cases, retrieve all objects

    retrieved = {}
    random_keys = list(files.keys())
    random.shuffle(random_keys)
    start = time.time()
    for filename in random_keys:
        obj_uuid = uuid_mapping[filename]
        retrieved_content = container.get_object_content(obj_uuid)
        retrieved[filename] = retrieved_content
        #retrieved = str(hashlib.md5(retrieved_content).hexdigest())
    tot_time = time.time() - start
    print("Time to retrieve {} packed objects in random order: {} s".format(num_files, tot_time))

    for filename in retrieved:
        assert retrieved[filename] == files[filename], "Mismatch for {}".format(filename)

    print("All tests passed")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
