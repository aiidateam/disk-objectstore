#!/usr/bin/env python
"""A small script that, every few seconds, repacks a container, and does it a few times.

This is used to test concurrency while using the container and packing at the same time.
"""
import datetime
import time

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
    help='The path to a test folder in which the container will be created.'
)
@click.option('-r', '--repetitions', default=10, help='Number of repetitions before stopping.')
@click.option('-w', '--wait-time', default=0.83, help='Time to wait between iterations.')
@click.help_option('-h', '--help')
def main(path, repetitions, wait_time):
    """Periodically pack container."""
    container = Container(path)
    if not container.is_initialised:
        raise ValueError('Can only pack initialised containers.')

    for iteration in range(repetitions):
        if iteration != 0:
            time.sleep(wait_time)

        compress_packs = iteration % 2 == 0
        start_counts = container.count_objects()
        container.pack_all_loose(compress=compress_packs)
        print('[PACKER {}] Done packing!'.format(timestamp()))
        end_counts = container.count_objects()

        print(
            '[PACKER {}] Packed objects (was {} loose, {} packed; now: {} loose, {} packed).'.format(
                timestamp(), start_counts['loose'], start_counts['packed'], end_counts['loose'], end_counts['packed']
            )
        )


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
