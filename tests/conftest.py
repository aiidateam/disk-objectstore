"""Configuration file for pytest tests."""
import hashlib
import os
import random
import shutil
import tempfile

import pytest

from disk_objectstore import Container


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

    def _generate_random_data(num_files=100, min_size=0, max_size=1000):
        """Generate a number of byte strings with random content (binary) and random length (in a given range).

        :param num_files: the number of files to generate
        :param min_size: the smallest allowed file size
        :param max_size: the smallest allowed file size
        :return: a dictionary where the key is the data MD5 and the value is the bytes content
        """
        files = {}
        for _ in range(num_files):
            size = random.randint(min_size, max_size)
            content = os.urandom(size)
            md5 = hashlib.md5(content).hexdigest()
            files[md5] = content
        return files

    yield _generate_random_data
