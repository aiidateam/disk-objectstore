#!/usr/bin/env python
"""A simple implementation with some testing to showcase the functionality and to run some benchmarks."""
import dataclasses
import os
import random
import time
import uuid

import click
from profilehooks import profile

from disk_objectstore import Container


@click.command(
    context_settings=dict(show_default=True)  # pylint: disable=use-dict-literal
)
@click.option("-n", "--num-files", default=100, help="Number of files to create.")
@click.option("-m", "--min-size", default=0, help="Minimum file size (bytes).")
@click.option("-M", "--max-size", default=1000, help="Maximum file size (bytes).")
@click.option(
    "-d",
    "--directly-to-pack",
    is_flag=True,
    help="Add directly files to the packs rather than as loose objects.",
)
@click.option(
    "-p",
    "--path",
    default="/tmp/test-container",
    help="The path to a test folder in which the container will be created.",
)
@click.option(
    "-c",
    "--clear",
    is_flag=True,
    help="Clear the repository path folder before starting.",
)
@click.option(
    "-B", "--num-bulk-calls", default=10, help="Number of bulk calls to get the files."
)
@click.option(
    "-z", "--compress-packs", is_flag=True, help="Compress objects while packing."
)
@click.option(
    "-P",
    "--profile-file",
    default=None,
    help="Perform the bulk read with profiling and output results onto this file name.",
)
@click.help_option("-h", "--help")
def main(
    num_files,
    min_size,
    max_size,
    directly_to_pack,
    path,
    clear,
    num_bulk_calls,
    compress_packs,
    profile_file,
):
    """Testing some basic functionality of the object-store, with timing."""
    # pylint: disable=too-many-arguments,too-many-locals,too-many-statements,too-many-branches

    container = Container(path)
    if clear:
        print("Clearing the container...")
        container.init_container(clear=clear)
    if not container.is_initialised:
        print("Initialising the container...")
        container.init_container()

    files = {}

    start_counts = container.count_objects()
    print(
        f"Currently known objects: {start_counts['packed']} packed, {start_counts['loose']} loose"
    )
    print("Pack objects on disk:", start_counts["pack_files"])

    print(f"Generating {num_files} files in memory...")
    for _ in range(num_files):
        filename = f"filename-{str(uuid.uuid4())}"
        size = random.randint(min_size, max_size)
        content = os.urandom(size)
        files[filename] = content
    total_size = sum(len(content) for content in files.values())
    print(
        f"Done. Total size: {total_size} bytes (~{total_size // 1024 / 1024:.3f} MB)."
    )

    if directly_to_pack:
        # Store objects (directly to pack)
        start = time.time()
        filenames = list(files.keys())
        files_content = [files[key] for key in filenames]
        hashkeys = container.add_objects_to_pack(files_content, compress=compress_packs)
        hashkey_mapping = dict(zip(filenames, hashkeys))
        tot_time = time.time() - start
        print(
            f"Time to store {num_files} objects DIRECTLY TO THE PACKS: {tot_time:.4} s"
        )

        # Check that no loose files were created
        counts = container.count_objects()
        assert (
            counts["loose"] == start_counts["loose"]
        ), f"Mismatch (loose in packed case): {start_counts['loose']} != {counts['loose']}"
        ## Cannot do this with the hash key implenentation - I might have stored the same object twice
        # assert counts['packed'
        #             ] == start_counts['packed'] + num_files, 'Mismatch (packed in packed case): {} + {} != {}'.format(
        #                 start_counts['packed'], num_files, counts['packed']
        #             )
    else:
        # Store objects (loose)
        start = time.time()
        hashkey_mapping = {}
        for filename, content in files.items():
            obj_hashkey = container.add_object(content)
            hashkey_mapping[filename] = obj_hashkey
        tot_time = time.time() - start
        print(f"Time to store {num_files} loose objects: {tot_time:.4} s")

        # Retrieve objects (loose)
        retrieved = {}
        random_keys = list(files.keys())
        random.shuffle(random_keys)
        start = time.time()
        for filename in random_keys:
            obj_hashkey = hashkey_mapping[filename]
            retrieved_content = container.get_object_content(obj_hashkey)
            retrieved[filename] = retrieved_content
        tot_time = time.time() - start
        print(f"Time to retrieve {num_files} loose objects: {tot_time:.4} s")

        # Check that the content is correct
        for filename, item in retrieved.items():
            assert (
                item == files[filename]
            ), f"Mismatch (content) for {filename}, {item!r} vs {files[filename]!r}"

        # Check that num_files new loose files are present now
        counts = container.count_objects()
        ## I cannot do this because I could have overlap if the object is identical and has the same hash key
        # assert counts['loose'
        #             ] == start_counts['loose'] + num_files, 'Mismatch (loose in unpacked case): {} + {} != {}'.format(
        #                 start_counts['loose'], num_files, counts['loose']
        #             )

        # Print container size info (before packing)
        size_info = container.get_total_size()
        print("Object store size info:")
        for key in sorted(dataclasses.asdict(size_info).keys()):
            print(f"- {key:30s}: {size_info[key]}")

        # Pack all loose objects
        start = time.time()
        container.pack_all_loose(compress=compress_packs)
        tot_time = time.time() - start
        print(f"Time to pack all loose objects: {tot_time:.4} s")
        start = time.time()
        container.clean_storage()
        tot_time = time.time() - start
        print(f"Time to clean storage: {tot_time:.4} s")

        # Check that all loose files are gone
        counts = container.count_objects()
        loose_folder = container._get_loose_folder()  # pylint: disable=protected-access
        assert not counts["loose"], "loose objects left: " f"{os.listdir(loose_folder)}"
        ## I cannot do this because I could have overlap if the object is identical and has the same hash key
        # assert counts['packed'] == start_counts['packed'] + start_counts[
        #    'loose'] + num_files, 'Mismatch (post-pack): {} + {} + {} != {}'.format(
        #        start_counts['packed'], start_counts['loose'], num_files, counts['packed']
        #    )

    # print container size info
    size_info = container.get_total_size()
    print("Object store size info:")
    for key in sorted(dataclasses.asdict(size_info).keys()):
        print(f"- {key:30s}: {size_info[key]}")

    # In all cases, retrieve all objects (in shuffled order)
    retrieved = {}
    random_keys = list(files.keys())
    random.shuffle(random_keys)

    # Will be needed later
    reverse_hashkey_mapping = {v: k for k, v in hashkey_mapping.items()}

    ## If you want to flush to disk and drop all disk caches, uncomment this part
    ## (note that this works on Linux only, and this requires that `sudo` has already
    ## been run earlier, so it does not ask for a password):
    # import subprocess
    # subprocess.check_output(["sync"])
    # subprocess.check_output(["sudo", "bash", "-c", "echo 3 > /proc/sys/vm/drop_caches"])

    ########################################
    # FIRST: single bulk read
    def bulk_read_data(container, hashkey_list):
        """A function to read the data in bulk.

        It's defined as a functon so it can be profiled."""
        return container.get_objects_content(hashkey_list, skip_if_missing=False)

    all_hashkeys = [hashkey_mapping[filename] for filename in random_keys]
    start = time.time()

    if profile_file is not None:
        func = profile(sort="cumtime", filename=profile_file, stdout=False)(
            bulk_read_data
        )
    else:
        func = bulk_read_data
    raw_retrieved = func(container=container, hashkey_list=all_hashkeys)
    if profile_file is not None:
        print(f"You can check the profiling results running 'snakeviz {profile_file}'")

    tot_time = time.time() - start
    print(
        f"Time to retrieve {num_files} packed objects in random order WITH ONE BULK CALL: {tot_time} s"
    )
    retrieved = {
        reverse_hashkey_mapping[key]: val for key, val in raw_retrieved.items()
    }
    for filename in retrieved:
        assert retrieved[filename] == files[filename], f"Mismatch for {filename}"

    ########################################
    # SECOND: num_bulk_calls bulk reads
    random.shuffle(random_keys)
    all_hashkeys = [hashkey_mapping[filename] for filename in random_keys]
    start = time.time()
    raw_retrieved = {}

    # Split the list into num_bulk_call even chunks
    chunk_len = len(all_hashkeys) // num_bulk_calls
    if len(all_hashkeys) % num_bulk_calls != 0:
        chunk_len += 1
    split_iterator = (
        all_hashkeys[start : start + chunk_len]
        for start in range(0, len(all_hashkeys), chunk_len)
    )

    # Retrieve in num_bulk_call chunks
    for chunk_of_hashkeys in split_iterator:
        raw_retrieved.update(
            container.get_objects_content(chunk_of_hashkeys, skip_if_missing=False)
        )

    tot_time = time.time() - start
    print(
        f"Time to retrieve {num_files} packed objects in random order WITH {num_bulk_calls} BULK CALLS: {tot_time} s"
    )
    retrieved = {
        reverse_hashkey_mapping[key]: val for key, val in raw_retrieved.items()
    }
    for filename in retrieved:
        assert retrieved[filename] == files[filename], f"Mismatch for {filename}"

    ########################################
    # THIRD: a lot of independent reads, one per object
    random.shuffle(random_keys)
    retrieved = {}
    start = time.time()
    for filename in random_keys:
        obj_hashkey = hashkey_mapping[filename]
        retrieved_content = container.get_object_content(obj_hashkey)
        retrieved[filename] = retrieved_content
    tot_time = time.time() - start
    print(f"Time to retrieve {num_files} packed objects in random order: {tot_time} s")

    for filename, content in retrieved.items():
        assert (
            content == files[filename]
        ), f"Mismatch (content) for {filename}, {content!r} vs {files[filename]!r}"

    print("All tests passed")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
