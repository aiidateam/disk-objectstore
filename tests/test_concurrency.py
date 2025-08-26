"""Test of the object-store container module."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

from disk_objectstore import Container

THIS_FILE_DIR = Path(__file__).parent
CONCURRENT_DIR = THIS_FILE_DIR / 'concurrent_tests'

NUM_WORKERS = 4


# Do the same test multiple times (repetition*2*2); can be set to > 1 to increase probability of seeing problems.
# This is specified on the command line when running pytest with ``--concurrency-repetitions=VALUE``
# (VALUE=1 by default) and passed as `concurrency_repetition_index`.
@pytest.mark.parametrize('with_packing', [True, False])  # If it works with packing, no need to test also without
@pytest.mark.parametrize('max_size', [1, 1000])
@pytest.mark.usefixture('concurrency_repetition_index')
def test_concurrency(  # pylint: disable=too-many-statements, too-many-locals, unused-argument
    temp_dir,
    with_packing,
    max_size,
):
    """Test to run concurrently many workers creating (loose) objects and (possibly) a single concurrent packer.

    This is needed to see that indeed these operations can happen at the same time.
    Moreover, this is needed to perform a full coverage of the code, since some code will
    be reached only during concurrent access to the object store (reading data while
    packing).

    .. note:: With max_size=1 I only have a maximum of 256+1 = 257 objects.
      In this way I stress-test also the creation of concurrent identical objects.

    ``concurrency_repetition_index`` is an integer looking over the specified repetitions on the pytest command line.
    We don't use this variable, it's just used to repeat the run multiple times.
    """
    packer_script = CONCURRENT_DIR / 'periodic_packer.py'
    worker_script = CONCURRENT_DIR / 'periodic_worker.py'

    # Create folder with the container and initialise it
    container_dir = temp_dir / 'container'
    Container(container_dir).init_container()

    # Create folder where each worker will write the MD5 of the objects it created,
    # so that others will read them.
    shared_dir = temp_dir / 'shared'
    os.mkdir(shared_dir)

    if with_packing:
        # Start the packer
        packer_proc = subprocess.Popen(  # pylint: disable=consider-using-with
            [
                sys.executable,
                packer_script,
                '-p',
                container_dir,
                '-r',
                '7',
                '-w',
                '0.83',
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    # Start the workers
    worker_procs = []
    for worker_id in range(NUM_WORKERS):
        options = [
            '-r',
            '6',
            '-w',
            '0',
            '-p',
            container_dir,
            '-s',
            shared_dir,
            '-M',
            str(max_size),
        ]
        if worker_id % 2:
            # One every two will read in bulk, the other within a loop
            options += ['-b']
        worker_procs.append(
            subprocess.Popen(  # pylint: disable=consider-using-with
                [sys.executable, worker_script] + options,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        )

    if with_packing:
        packer_out, packer_err = packer_proc.communicate()
        if packer_out:
            print('** STDOUT OF PACKER')
            print(packer_out.decode('utf8'))
        if packer_err:
            print('** STDERR OF PACKER')
            print(packer_err.decode('utf8'), file=sys.stderr)

    worker_outs = []
    worker_errs = []
    for worker_id, worker_proc in enumerate(worker_procs):
        worker_out, worker_err = worker_proc.communicate()
        worker_outs.append(worker_out)
        worker_errs.append(worker_err)
        if worker_out:
            print(f'** STDOUT OF WORKER {worker_id}')
            print(worker_out.decode('utf8'))
        if worker_err:
            print(f'** STDERR OF WORKER {worker_id}', file=sys.stderr)
            print(worker_err.decode('utf8'), file=sys.stderr)

    error_messages = []

    if with_packing and packer_proc.returncode:
        error_messages.append(f'PACKER process failed with error code {packer_proc.returncode}!')
        error_messages.append('PACKER output:')
        error_messages.append(packer_out.decode('utf8'))
        error_messages.append('-' * 78)
        error_messages.append('PACKER error:')
        error_messages.append(packer_err.decode('utf8'))
        error_messages.append('=' * 78)

    for idx, (worker_proc, worker_out, worker_err) in enumerate(zip(worker_procs, worker_outs, worker_errs)):
        if worker_proc.returncode:
            error_messages.append(f'WORKER process #{idx} failed with error code {worker_proc.returncode}!')
            error_messages.append(f'WORKER {idx} output:')
            error_messages.append(worker_out.decode('utf8'))
            error_messages.append('-' * 78)
            error_messages.append(f'WORKER {idx} error:')
            error_messages.append(worker_err.decode('utf8'))
            error_messages.append('=' * 78)

    error_string = 'At least one of the concurrent processes failed!\nMessages:\n' + '\n'.join(error_messages)
    assert len(error_messages) == 0, error_string


@pytest.mark.parametrize('clean_loose_per_pack', [False, True])
@pytest.mark.parametrize('max_size', [1, 1000])
@pytest.mark.usefixture('concurrency_repetition_index')
def test_concurrency_with_clean_loose_per_pack(temp_dir, max_size, clean_loose_per_pack):
    """Concurrent writers, readers, and a packer, optionally cleaning loose objects per pack."""

    packer_script = CONCURRENT_DIR / 'periodic_packer.py'
    worker_script = CONCURRENT_DIR / 'periodic_worker.py'
    reader_script = CONCURRENT_DIR / 'periodic_reader.py'

    container_dir = temp_dir / 'container'
    container = Container(container_dir)
    container.init_container()

    shared_dir = temp_dir / 'shared'
    os.mkdir(shared_dir)

    # Pack command with optional clean_loose_per_pack
    packer_args = [
        sys.executable,
        packer_script,
        '-p',
        container_dir,
        '-r',
        '5',
        '-w',
        '0.5',
    ]
    if clean_loose_per_pack:
        packer_args.append('--clean-per-pack')

    packer_proc = subprocess.Popen(packer_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Start workers
    worker_procs = []
    for worker_id in range(2):  # minimal writers
        options = [
            '-r',
            '5',
            '-w',
            '0.5',
            '-p',
            container_dir,
            '-s',
            shared_dir,
            '-M',
            str(max_size),
        ]
        worker_procs.append(
            subprocess.Popen([sys.executable, worker_script] + options, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        )

    # Start a reader
    reader_proc = subprocess.Popen(
        [sys.executable, reader_script, '-p', container_dir, '-s', shared_dir, '-r', '5', '-w', '0.5'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Wait for all processes
    all_procs = [packer_proc] + worker_procs + [reader_proc]
    outs_errs = [proc.communicate() for proc in all_procs]

    error_messages = []
    for idx, proc in enumerate(all_procs):
        out, err = outs_errs[idx]
        if proc.returncode:
            error_messages.append(f'Process #{idx} failed with return code {proc.returncode}')
            error_messages.append('STDOUT:\n' + out.decode())
            error_messages.append('STDERR:\n' + err.decode())
        elif err:
            # capture non-fatal stderr output
            error_messages.append(f'Process #{idx} reported warnings on stderr:\n' + err.decode())

    assert not error_messages, 'Concurrent processes had errors/warnings:\n' + '\n'.join(error_messages)

    # Basic integrity checks
    counts = container.count_objects()
    total_objects = counts['loose'] + counts['pack_files']
    assert total_objects > 0, 'No objects written at all'
    assert counts['pack_files'] > 0, 'Expected at least one pack file after concurrent run'
