"""Test of the object-store container module."""
import hashlib
import os
import random
import subprocess
import tempfile

import pytest

from disk_objectstore.utils import nullcontext

THIS_FILE_DIR = os.path.dirname(os.path.realpath(__file__))
EXAMPLES_DIR = os.path.join(THIS_FILE_DIR, os.pardir, 'examples-and-benchmarks')


def _assert_empty_repo(container):
    """Check that the container has no objects and no pack files.

    :param container: a Container.
    """
    counts = container.count_objects()
    assert counts['packed'] == 0, (
        'The container should be empty at the beginning '
        '(but there are {} packed objects)'.format(counts['packed'])
    )
    assert counts['loose'] == 0, (
        'The container should be empty at the beginning '
        '(but there are {} loose objects)'.format(counts['loose'])
    )
    assert counts['pack_files'] == 0, (
        'The container should be empty at the beginning '
        '(but there are {} pack files)'.format(counts['pack_files'])
    )


def _add_objects_loose_loop(container, data):
    """Add loose objects to a container, within a for loop.

    :param container: a Container
    :param data: a dictionary where the key is an arbitrary identifier, and the value is a byte string.
    :return: a dictionary where the keys are the object UUIDs as returned by the container, and the values
      are the keys in the original ``data`` dictionary.
    """
    retval = {}
    for key, content in data.items():
        obj_uuid = container.add_object(content)
        retval[obj_uuid] = key
    return retval


def _get_data_and_md5_loop(container, obj_uuids):
    """Get the MD5 of the data stored under the given container, one at a time in a loop.

    :param container: a Container
    :param obj_uuids: a list of object UUIDs
    :return: a dictionary where the keys are the object UUIDs and the values are the MD5 hexdigests.
    """
    retval = {}
    for obj_uuid in obj_uuids:
        retrieved_content = container.get_object_content(obj_uuid)
        retval[obj_uuid] = hashlib.md5(retrieved_content).hexdigest()
    return retval


def _get_data_and_md5_bulk(container, obj_uuids):
    """Get the MD5 of the data stored under the given container as a single bulk operation.

    :param container: a Container
    :param obj_uuids: a list of object UUIDs
    :return: a dictionary where the keys are the object UUIDs and the values are the MD5 hexdigests.
    """
    retval = {}
    retrieved_contents = container.get_object_contents(obj_uuids)
    for obj_uuid in retrieved_contents:
        retval[obj_uuid] = hashlib.md5(retrieved_contents[obj_uuid]).hexdigest()
    return retval


@pytest.mark.parametrize('retrieve_bulk', [True, False])
def test_add_get_loose(temp_container, generate_random_data, retrieve_bulk):
    """Add a number of objects (one by one, loose) to the container.

    Then retrieve them and check the content is correct."""
    _assert_empty_repo(temp_container)

    data = generate_random_data()

    # Store
    obj_md5s = _add_objects_loose_loop(temp_container, data)

    counts = temp_container.count_objects()
    assert counts['packed'] == 0, (
        'The container should have no packed objects '
        '(but there are {} instead)'.format(counts['packed'])
    )
    assert counts['loose'] == len(obj_md5s), (
        'The container should have {} loose objects '
        '(but there are {} instead)'.format(len(obj_md5s), counts['loose'])
    )

    # Retrieve objects (loose), in random order
    random_keys = list(obj_md5s.keys())
    random.shuffle(random_keys)

    # Retrieve data in a loop
    if retrieve_bulk:
        retrieved_md5s = _get_data_and_md5_bulk(temp_container, random_keys)
    else:
        retrieved_md5s = _get_data_and_md5_loop(temp_container, random_keys)

    # Check that the MD5 are correct
    for obj_uuid in obj_md5s:
        assert obj_md5s[obj_uuid] == retrieved_md5s[obj_uuid], "Object '{}' has wrong MD5s ({} vs {})".format(
            obj_uuid, obj_md5s[obj_uuid], retrieved_md5s[obj_uuid]
        )


@pytest.mark.parametrize('use_compression,retrieve_bulk', [(True, True), (True, False), (False, True), (False, False)])
def test_add_get_with_packing(temp_container, generate_random_data, use_compression, retrieve_bulk):
    """Add a number of objects (one by one, loose) to the container.

    Then retrieve them and check the content is correct."""
    _assert_empty_repo(temp_container)

    data = generate_random_data()

    # Store
    obj_md5s = _add_objects_loose_loop(temp_container, data)

    # Pack all loose objects
    temp_container.pack_all_loose(compress=use_compression)

    counts = temp_container.count_objects()
    assert counts['packed'] == len(obj_md5s), (
        'The container should have {} packed objects '
        '(but there are {} instead)'.format(len(obj_md5s), counts['packed'])
    )
    assert counts['loose'] == 0, (
        'The container should have 0 loose objects '
        '(but there are {} instead)'.format(counts['loose'])
    )

    # Retrieve objects (loose), in random order
    random_keys = list(obj_md5s.keys())
    random.shuffle(random_keys)

    # Retrieve data in a loop
    if retrieve_bulk:
        retrieved_md5s = _get_data_and_md5_bulk(temp_container, random_keys)
    else:
        retrieved_md5s = _get_data_and_md5_loop(temp_container, random_keys)

    # Check that the MD5 are correct
    for obj_uuid in obj_md5s:
        assert obj_md5s[obj_uuid] == retrieved_md5s[obj_uuid], "Object '{}' has wrong MD5s ({} vs {})".format(
            obj_uuid, obj_md5s[obj_uuid], retrieved_md5s[obj_uuid]
        )


@pytest.mark.parametrize(
    'idx_and_options',
    enumerate([
        [],
        ['-c'],
        ['-d'],
        ['-z'],
        ['-d', '-z'],
        ['-B', '7'],  # Odd number of bulk calls
        ['-P', 'TEMPFILE']
    ])
)
def test_example_objectstore(temp_dir, idx_and_options):
    """Test the example/profiling script 'example_objectstore'."""
    idx, options = idx_and_options

    tempfile_idx = None
    try:
        tempfile_idx = options.index('TEMPFILE')
        context = tempfile.NamedTemporaryFile()
    except ValueError:
        # no need to create a tempfile
        context = nullcontext(enter_result=None)

    with context as tmpfile:
        if tempfile_idx is not None:
            options[tempfile_idx] = tmpfile.name
        script = os.path.join(EXAMPLES_DIR, 'example_objectstore.py')
        output = subprocess.check_output(['python', script, '-p', os.path.join(temp_dir, str(idx))] + options)
        assert output != ''


@pytest.mark.parametrize('idx_and_options', enumerate([
    [],
    ['-c'],
    ['-m'],
    ['-z'],
    ['-z', '-m'],
]))
def test_example_profile_zeros(temp_dir, idx_and_options):
    """Test the example/profiling script 'profile_zeros'."""
    idx, options = idx_and_options
    script = os.path.join(EXAMPLES_DIR, 'profile_zeros.py')
    output = subprocess.check_output(['python', script, '-p', os.path.join(temp_dir, str(idx))] + options)
    assert output != ''


# Additional tests to implement
# - test initialisation with different loose and prefix lengths
# - assert final object count in the two tests above
# - test the util classes (in a different module)
# - validation of pack names
# - various exceptions
# - test guards of packs
# - test size measurements (packed and not)
# - test that stream decompresser stops if the stream is partial

# - It's not multithreaded. But check that it works with async event loops!

# - Add testing with the locusts

# - Add memory measurements?

# - Add performance measurements?
