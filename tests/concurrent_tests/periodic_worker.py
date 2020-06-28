#!/usr/bin/env python
"""A small script that, every few seconds, adds a few objects to an object store, and then tries to read it again.

This is used to test concurrency while using the container and packing at the same time.

The script is supposed to be run in parallel with many other "locusts", possibly with a (single) packer at the
same time, to check if there are issues while all of these work at the same time.

The script will also write the objects it created (in a safe way also when there is concurrency) in a folder
(defined by the -s option). Then each locust will try to read back *all* files written by *all* locusts (including
itself) and check if the checksums are correct.
"""
import datetime
import hashlib
import json
import os
import random
import tempfile
import time

import click
import psutil

from disk_objectstore.container import Container, NotExistent
from disk_objectstore.models import Obj


def timestamp():
    """Return a timestamp string to print for logging."""
    return datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')


@click.command()
@click.option('-n', '--num-files', default=100, help='Number of files to create.')
@click.option('-m', '--min-size', default=0, help='Minimum file size (bytes).')
@click.option('-M', '--max-size', default=1000, help='Maximum file size (bytes).')
@click.option(
    '-p',
    '--path',
    default='/tmp/test-container',
    help='The path to a test folder in which the container will be created.'
)
@click.option('-r', '--repetitions', default=3, help='Number of repetitions before stopping.')
@click.option('-w', '--wait-time', default=0.1, help='Time to wait between iterations.')
@click.option(
    '-s',
    '--shared-folder',
    default='/tmp/test-container-shared',
    help=
    'The path to a test folder in which all locusts will write the checksums for others to read. It must already exist.'
)
@click.option('-b', '--bulk-read', is_flag=True, help='Whether to use bulk reads, or a loop on each hash key.')
@click.help_option('-h', '--help')
def main(num_files, min_size, max_size, path, repetitions, wait_time, shared_folder, bulk_read):
    """Keep writing loose objects, then read all those written by all locusts, and try to read them back."""
    # pylint: disable=too-many-arguments,too-many-locals,too-many-statements,too-many-branches
    if not os.path.isdir(shared_folder):
        raise ValueError("Create the folder '{}' first!".format(shared_folder))
    container = Container(path)
    # In the tests we pass it already initialised, so this is never called
    if not container.is_initialised:
        print('Initialising the container...')
        container.init_container()

    proc_id = psutil.Process().pid

    start_counts = container.count_objects()
    print(
        '[{} {}] Currently known objects: {} packed, {} loose'.format(
            proc_id, timestamp(), start_counts['packed'], start_counts['loose']
        )
    )
    print('[{} {}] Pack objects on disk: {}'.format(proc_id, timestamp(), start_counts['pack_files']))

    for iteration in range(repetitions):
        if iteration != 0:
            time.sleep(wait_time)

        contents = []
        print(
            '[{} {}] Iteration {}/{}, generating {} files in memory...'.format(
                proc_id, timestamp(), iteration + 1, repetitions, num_files
            )
        )
        for _ in range(num_files):
            size = random.randint(min_size, max_size)
            content = os.urandom(size)
            contents.append(content)

        # Store objects (loose)
        hashkeys = []
        for content in contents:
            hashkeys.append(container.add_object(content))

        checksums = {}
        for obj_hashkey, content in zip(hashkeys, contents):
            # I use the same sha256 algo, to check more easily which one is corrupt
            checksum = hashlib.sha256(content).hexdigest()
            try:
                # If I already found the same hash key, check that also the checksum is the same
                assert checksums[obj_hashkey] == checksum
            except KeyError:
                # Not found yet, it's OK
                pass
            checksums[obj_hashkey] = checksum

        ## Dump to file
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf8', dir=shared_folder, delete=False) as fhandle:
            fname = fhandle.name
            json.dump(checksums, fhandle)
        # Atomic move in place (so other locusts don't try to read partially written files)
        os.rename(fname, '{}.sha'.format(fname))

        # Re-read everything, also from other processes
        all_checksums = {}
        file_count = 0
        for fname in os.listdir(shared_folder):
            if not fname.endswith('.sha'):
                continue
            file_count += 1
            with open(os.path.join(shared_folder, fname)) as fhandle:
                chunk_checksums = json.load(fhandle)
            all_checksums.update(chunk_checksums)
        print(
            '[{} {}] {} object checksums read from {} files ({}).'.format(
                proc_id, timestamp(), len(all_checksums), file_count,
                'with bulk reads' if bulk_read else 'with single-object reads'
            )
        )

        ########################################
        # single bulk read
        all_hashkeys = list(all_checksums.keys())
        random.shuffle(all_hashkeys)

        if bulk_read:
            retrieved_content = container.get_objects_content(all_hashkeys, skip_if_missing=False)
        else:
            retrieved_content = {}
            for obj_hashkey in all_hashkeys:
                try:
                    retrieved_content[obj_hashkey] = container.get_object_content(obj_hashkey)
                except NotExistent:
                    retrieved_content[obj_hashkey] = None
        retrieved_checksums = {}
        for obj_hashkey, content in retrieved_content.items():
            if content is None:
                raise ValueError('No content returned for object {}!'.format(obj_hashkey))
            if not content and obj_hashkey != 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855':
                print('WARNING!!! {} is {} ({})'.format(obj_hashkey, content, type(content)))
            retrieved_checksums[obj_hashkey] = hashlib.sha256(content).hexdigest()

        only_left = set(retrieved_checksums).difference(all_checksums)
        only_right = set(all_checksums).difference(retrieved_checksums)
        assert not only_right, 'objects only in all_checksums: {}'.format(only_right)
        assert not only_left, 'objects only in retrieved_checksums: {}'.format(only_left)
        for key in retrieved_checksums:
            assert all_checksums[key] == retrieved_checksums[key], 'Mismatch for {}: {} vs. {}'.format(
                key, all_checksums[key], retrieved_checksums[key]
            )
        del retrieved_content

        random.shuffle(all_hashkeys)
        retrieved_checksums = {}
        for obj_hashkey in all_hashkeys:
            content = container.get_object_content(obj_hashkey)
            if not content and obj_hashkey != 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855':
                print('WARNING!!! {} is {} ({})'.format(obj_hashkey, content, type(content)))
            retrieved_checksums[obj_hashkey] = hashlib.sha256(content).hexdigest()

        only_left = set(retrieved_checksums).difference(all_checksums)
        only_right = set(all_checksums).difference(retrieved_checksums)
        assert not only_right, 'objects only in all_checksums: {}'.format(only_right)
        assert not only_left, 'objects only in retrieved_checksums: {}'.format(only_left)
        for key in retrieved_checksums:
            try:
                assert all_checksums[key] == retrieved_checksums[key], 'Mismatch for {}: {} vs. {}'.format(
                    key, all_checksums[key], retrieved_checksums[key]
                )
            except AssertionError:
                loose_path = container._get_loose_path_from_hashkey(key)  # pylint: disable=protected-access
                print('Exists Loose: {}'.format(os.path.exists(loose_path)))
                session = container._get_cached_session()  # pylint: disable=protected-access
                query = session.query(Obj).filter(
                    Obj.hashkey == key
                ).with_entities(Obj.pack_id, Obj.hashkey, Obj.offset, Obj.length, Obj.compressed, Obj.size)
                print(list(query))
                raise


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
