"""Configuration file for pytest tests."""
import hashlib
import os
import random
import shutil
import tempfile

import pytest

from disk_objectstore import Container


def pytest_addoption(parser):
    """Parse a new option for the number of repetitions for the concurrency tests."""
    parser.addoption(
        '--concurrency-repetitions', type=int, default=1, help='Specify how many time to repeat the concurrency tests'
    )


def pytest_generate_tests(metafunc):
    """Define a new fixture `concurrency_repetition_index` with the index of the repetition for concurrency tests.

    The number of repetitions can be specified on the command line with ``--concurrency-repetitions=3``."""
    if 'concurrency_repetition_index' in metafunc.fixturenames:
        metafunc.parametrize('concurrency_repetition_index', range(metafunc.config.option.concurrency_repetitions))


@pytest.fixture(scope='function')
def callback_instance():
    """Return the CallbackClass for the tests."""

    class CallbackClass:
        """Class that manages the callback and checks that it is correctly called."""

        def __init__(self):
            """Initialise the class."""
            self.current_action = None
            self.performed_actions = []

        def callback(self, action, value):
            """Check how the callback is called."""

            if action == 'init':
                assert self.current_action is None, "Starting a new action '{}' without closing the old one {}".format(
                    action, self.current_action
                )
                self.current_action = {'start_value': value, 'value': 0}
            elif action == 'update':
                # Track the current position
                self.current_action['value'] += value
            elif action == 'close':
                # Add to list of performed actions
                self.performed_actions.append(self.current_action)
                self.current_action = None
            else:
                raise AssertionError("Unknown action '{}'".format(action))

    yield CallbackClass()


@pytest.fixture(scope='function')
def temp_container(temp_dir):  # pylint: disable=redefined-outer-name
    """Return an object-store container in a given temporary directory.

    This has a function scope, so it's a new container for every test function.
    It's deleted at the end of the test function.
    """
    container = Container(temp_dir)
    container.init_container(clear=True)
    yield container
    # Close open files, if they are open
    container.close()


@pytest.fixture(scope='function')
def temp_dir():
    """Get a temporary directory.

    :return: The path to the directory
    :rtype: str
    """
    try:
        dirpath = tempfile.mkdtemp()
        yield dirpath
    finally:
        # after the test function has completed, remove the directory again
        shutil.rmtree(dirpath)


@pytest.fixture(scope='function')
def generate_random_data():
    """Return a function to generate a number of random byte strings.

    They have random content (binary) and random length (in a given range).
    A dictionary is returned, where the key is the data MD5 and the value is the bytes content.
    """

    def _generate_random_data(num_files=100, min_size=0, max_size=1000, seed=None):
        """Generate a number of byte strings with random content (binary) and random length (in a given range).

        :param num_files: the number of files to generate
        :param min_size: the smallest allowed file size
        :param max_size: the smallest allowed file size
        :param seed: if not None, set that seed for random generation (for reproducible runs)
        :return: a dictionary where the key is the data MD5 and the value is the bytes content
        """
        if seed is not None:
            # Save the state before changing the seed
            saved_state = random.getstate()
            random.seed(seed)
        try:
            files = {}
            for _ in range(num_files):
                size = random.randint(min_size, max_size)
                content = os.urandom(size)
                md5 = hashlib.md5(content).hexdigest()
                files[md5] = content
            return files
        finally:
            # Reset the state if a seed was provided
            if seed is not None:
                random.setstate(saved_state)

    yield _generate_random_data


@pytest.fixture(scope='function')
def lock_file_on_windows():
    """
    Return a function that, given a file desciptor (as returned by ``os.open``, locks it (on Windows)
    also for read-only opening).

    Note: The returned function can be called only on Windows.
    """

    def _locker(file_descriptor):
        """Given a file descriptor, it locks.

        .. note:: This function asserts if we are not on Windows.

        :param file_descriptor: a file descriptor, opened with `os.open()`
        """
        assert os.name == 'nt', 'This fixture can only be used on Windows'

        # This should run on Windows, but the linter runs on Ubuntu where these modules
        # do not exist. Therefore, ignore errors in this function.
        # pylint: disable=import-error
        import win32file
        import pywintypes
        import win32con

        winfd = win32file._get_osfhandle(file_descriptor)  # pylint: disable=protected-access
        mode = win32con.LOCKFILE_EXCLUSIVE_LOCK | win32con.LOCKFILE_FAIL_IMMEDIATELY
        overlapped = pywintypes.OVERLAPPED()
        # additional parameters
        # int : nbytesLow - low-order part of number of bytes to lock
        # int : nbytesHigh - high-order part of number of bytes to lock
        # ol=None : PyOVERLAPPED - An overlapped structure
        # after the first two params: reserved, and nNumberOfBytesToLock
        # then, overlapped
        win32file.LockFileEx(winfd, mode, 0, -0x10000, overlapped)

    yield _locker
