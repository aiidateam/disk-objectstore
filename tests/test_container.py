"""Test of the utils wrappers."""
import hashlib
import random

import pytest


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


# Additional tests to implement
# - assert final object count in the two tests above
# - test the util classes (in a different module)
# - validation of pack names
# - various exceptions
# - test guards of packs
# - test size measurements (packed and not)

# - Add testing with the locusts

# - Add memory measurements?

# - Add performance measurements?
