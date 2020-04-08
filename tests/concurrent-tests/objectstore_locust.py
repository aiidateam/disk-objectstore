#!/usr/bin/env python
"""A small script that, every few seconds, adds a few objects to an object store, and then tries to read it again.

This is used to test concurrency while using the container and packing at the same time.

The script is supposed to be run in parallel with many other "locusts", possibly with a (single) packer at the
same time, to check if there are issues while all of these work at the same time.

The script will also write the objects it created (in a safe way also when there is concurrency) in a folder
(defined by the -s option). Then each locust will try to read back *all* files written by *all* locusts (including
itself) and check if the MD5s are correct.
"""
import hashlib
import json
import os
import random
import shutil
import tempfile
import time

import click
import psutil

from disk_objectstore.container import Container, NotExistent


@click.command()  # noqa: MC0001
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
    help='The path to a test folder in which all locusts will write the MD5s for others to read. It must already exist.'
)
@click.option('-b', '--bulk-read', is_flag=True, help='Whether to use bulk reads, or a loop on each UUID.')
@click.help_option('-h', '--help')
def main(num_files, min_size, max_size, path, repetitions, wait_time, shared_folder, bulk_read):
    """Keep writing loose objects, then read all those written by all locusts, and try to read them back."""
    # pylint: disable=too-many-arguments,too-many-locals,too-many-statements,too-many-branches
    if not os.path.isdir(shared_folder):
        raise ValueError("Create the folder '{}' first!".format(shared_folder))
    container = Container(path)
    if not container.is_initialised:
        print('Initialising the container...')
        container.init_container()

    proc_id = psutil.Process().pid

    start_counts = container.count_objects()
    print(
        '[{}] Currently known objects: {} packed, {} loose'.format(
            proc_id, start_counts['packed'], start_counts['loose']
        )
    )
    print('[{}] Pack objects on disk: {}'.format(proc_id, start_counts['pack_files']))

    for iteration in range(repetitions):
        if iteration != 0:
            time.sleep(wait_time)

        contents = []
        print(
            '[{}] Iteration {}/{}, generating {} files in memory...'.format(
                proc_id, iteration + 1, repetitions, num_files
            )
        )
        for _ in range(num_files):
            size = random.randint(min_size, max_size)
            content = bytearray(random.getrandbits(8) for _ in range(size))
            contents.append(content)

        # Store objects (loose)
        uuids = []
        for content in contents:
            uuids.append(container.add_object(content))

        md5s = {}
        for obj_uuid, content in zip(uuids, contents):
            md5s[obj_uuid] = hashlib.md5(content).hexdigest()

        ## Dump to file
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf8', dir=shared_folder, delete=False) as fhandle:
            fname = fhandle.name
            json.dump(md5s, fhandle)
        # Atomic move in place (so other locusts don't try to read partially written files)
        shutil.move(fname, '{}.md5'.format(fname))

        # Re-read everything, also from other processes
        all_md5s = {}
        file_count = 0
        for fname in os.listdir(shared_folder):
            if not fname.endswith('.md5'):
                continue
            file_count += 1
            with open(os.path.join(shared_folder, fname)) as fhandle:
                chunk_md5s = json.load(fhandle)
            all_md5s.update(chunk_md5s)
        print(
            '[{}] {} object MD5s read from {} files ({}).'.format(
                proc_id, len(all_md5s), file_count, 'with bulk reads' if bulk_read else 'with single-object reads'
            )
        )

        ########################################
        # single bulk read
        all_uuids = list(all_md5s.keys())
        random.shuffle(all_uuids)

        if bulk_read:
            retrieved_content = container.get_object_contents(all_uuids, skip_if_missing=False)
        else:
            retrieved_content = {}
            for obj_uuid in all_uuids:
                try:
                    retrieved_content[obj_uuid] = container.get_object_content(obj_uuid)
                except NotExistent:
                    retrieved_content[obj_uuid] = None
        retrieved_md5s = {}
        for obj_uuid, content in retrieved_content.items():
            if content is None:
                raise ValueError('No content returned for object {}!'.format(obj_uuid))
            retrieved_md5s[obj_uuid] = hashlib.md5(content).hexdigest()

        assert retrieved_md5s == all_md5s
        del retrieved_content

        random.shuffle(all_uuids)
        retrieved_md5s = {}
        for obj_uuid in all_uuids:
            retrieved_md5s[obj_uuid] = hashlib.md5(container.get_object_content(obj_uuid)).hexdigest()
        assert retrieved_md5s == all_md5s


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
