#!/usr/bin/env python
"""A small script that, every few seconds, reads random known objects from an object store.

This is used to test concurrency while using the container, writers, and a packer at the same time.
"""

import datetime
import json
import os
import random
import sys
import time
from pathlib import Path

import click

from disk_objectstore import Container


def timestamp():
    """Return a timestamp string to print for logging."""
    return datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')


@click.command()
@click.option(
    '-p',
    '--path',
    default='/tmp/test-container',
    help='The path to a test folder in which the container will be created.',
)
@click.option(
    '-s',
    '--shared-folder',
    default='/tmp/test-container-shared',
    help='Test folder path where writers dump their checksums. Must already exist.',
)
@click.option('-r', '--repetitions', default=10, help='Number of repetitions before stopping.')
@click.option('-w', '--wait-time', default=0.5, help='Time to wait between iterations.')
@click.help_option('-h', '--help')
def main(path, shared_folder, repetitions, wait_time):
    """Periodically read objects previously written by writers."""
    container = Container(path)
    if not container.is_initialised:
        raise ValueError('Can only read from initialised containers.')

    for iteration in range(repetitions):
        if iteration != 0:
            time.sleep(wait_time)

        # Gather all known checksums from shared folder
        all_hashkeys = []
        for fname in os.listdir(shared_folder):
            if not fname.endswith('.sha'):
                continue
            try:
                with open(Path(shared_folder) / fname) as handle:
                    chunk = json.load(handle)
                all_hashkeys.extend(chunk.keys())
            except Exception as exc:  # pylint: disable=broad-except
                print(f'[READER {timestamp()}] Failed reading {fname}: {exc}', file=sys.stderr)

        if all_hashkeys:
            md5 = random.choice(all_hashkeys)
            try:
                _ = container.get_object_content(md5)
                print(f'[READER {timestamp()}] Successfully read {md5}')
            except Exception as exc:  # pylint: disable=broad-except
                print(f'[READER {timestamp()}] Failed to read {md5}: {exc}', file=sys.stderr)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
