#!/usr/bin/env python
import uuid

import click

from disk_objectstore.wrapper import WrappedRepository

@click.command()
@click.option('-n', '--num-files', default=100, help='Number of files to create.')
@click.option('-m', '--min-size', default=0, help='Minimum file size (bytes).')
@click.option('-M', '--max-size', default=1000, help='Maximum file size (bytes).')
@click.option('-p', '--path', default='/tmp/test-container', help='The path to a test folder in which the container will be created.')
@click.option('-c', '--clear', is_flag=True, help='Clear the repository path folder before starting.')
@click.help_option('-h', '--help')
def main(num_files, min_size, max_size, path, clear):  # pylint: disable=too-many-arguments,too-many-locals,too-many-statements
    """Testing some basic functionality of the object-store wrapper, with timing."""
    import random
    import time

    wrapped_repository = WrappedRepository(folder=path, clear=clear)

    files = {}

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

    # Write loose objects
    start = time.time()
    uuid_mapping = {}
    filenames, contents = zip(*files.items())
    obj_uuids = wrapped_repository.put_objects(contents)
    uuid_mapping = dict(zip(filenames, obj_uuids))
    tot_time = time.time() - start
    print("Time to store {} loose objects: {:.4} s".format(
        num_files, tot_time))

    # Pack
    start = time.time()
    wrapped_repository.pack()
    tot_time = time.time() - start
    print("Time to pack all loose objects: {:.4} s".format(tot_time))

    # Retrieve all objects, in random order
    retrieved = {}
    random_keys = list(files.keys())
    random.shuffle(random_keys)

    start = time.time()
    keylist = [uuid_mapping[filename] for filename in random_keys]
    retrieved_content = wrapped_repository.get_objects(keylist)
    retrieved = {filename: content for filename, content in zip(random_keys, retrieved_content)}
    tot_time = time.time() - start
    print("Time to retrieve {} packed objects in random order: {} s".format(num_files, tot_time))

    for filename in retrieved:
        assert retrieved[filename] == files[filename], "Mismatch for {}".format(filename)

    print("All tests passed")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
