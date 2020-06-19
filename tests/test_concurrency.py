"""Test of the object-store container module."""
import os
import subprocess
import sys

import pytest

from disk_objectstore import Container

THIS_FILE_DIR = os.path.dirname(os.path.realpath(__file__))
CONCURRENT_DIR = os.path.join(THIS_FILE_DIR, 'concurrent_tests')

NUM_WORKERS = 4


@pytest.mark.xfail(reason='I know this is not yet working. This is tracked in #4')
def test_concurrency(temp_dir):
    """Test to run concurrently many workers creating objects, and at the same time one packer.

    This is needed to see that indeed these operations can happen at the same time.
    Moreover, this is needed to perform a full coverage of the code, since some code will
    be reached only during concurrent access to the object store (reading data while
    packing).
    """
    packer_script = os.path.join(CONCURRENT_DIR, 'periodic_packer.py')
    worker_script = os.path.join(CONCURRENT_DIR, 'periodic_worker.py')

    # Create folder with the container and initialise it
    container_dir = os.path.join(temp_dir, 'container')
    Container(container_dir).init_container()

    # Create folder where each worker will write the MD5 of the objects it created,
    # so that others will read them.
    shared_dir = os.path.join(temp_dir, 'shared')
    os.mkdir(shared_dir)

    # Start the packer
    packer_proc = subprocess.Popen([sys.executable, packer_script, '-p', container_dir, '-r', '5', '-w', '0.83'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

    # Start the workers
    worker_procs = []
    for worker_id in range(NUM_WORKERS):
        options = ['-r', '4', '-w', '0', '-p', container_dir, '-s', shared_dir]
        if worker_id % 2:
            # One every two will read in bulk, the other within a loop
            options += ['-b']
        worker_procs.append(
            subprocess.Popen([sys.executable, worker_script] + options, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        )

    packer_out, packer_err = packer_proc.communicate()
    worker_outs = []
    worker_errs = []
    for worker_proc in worker_procs:
        worker_out, worker_err = worker_proc.communicate()
        worker_outs.append(worker_out)
        worker_errs.append(worker_err)

    error_messages = []

    if packer_proc.returncode:
        error_messages.append('PACKER process failed with error code {}!'.format(packer_proc.returncode))
        error_messages.append('PACKER output:')
        error_messages.append(packer_out.decode('utf8'))
        error_messages.append('-' * 78)
        error_messages.append('PACKER error:')
        error_messages.append(packer_err.decode('utf8'))
        error_messages.append('=' * 78)

    for idx, (worker_proc, worker_out, worker_err) in enumerate(zip(worker_procs, worker_outs, worker_errs)):
        if worker_proc.returncode:
            error_messages.append('WORKER process #{} failed with error code {}!'.format(idx, worker_proc.returncode))
            error_messages.append('WORKER {} output:'.format(idx))
            error_messages.append(worker_out.decode('utf8'))
            error_messages.append('-' * 78)
            error_messages.append('WORKER {} error:'.format(idx))
            error_messages.append(worker_err.decode('utf8'))
            error_messages.append('=' * 78)

    error_string = 'At least one of the concurrent processes failed!\nMessages:\n' + '\n'.join(error_messages)
    assert len(error_messages) == 0, error_string
