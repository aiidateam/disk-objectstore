"""Test of the object-store container module."""
import hashlib
import io
import os
import random
import shutil
import tempfile
import uuid
import zlib

import psutil
import pytest

from disk_objectstore import Container
import disk_objectstore.utils as utils
import disk_objectstore.exceptions as exc


class UnopenableBytesIO(io.BytesIO):

    def __enter__(self):
        raise AttributeError('__enter__ method disabled for UnopenableBytesIO')


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


def _add_objects_directly_to_pack(container, data, compress):
    """Add objects directly to pack files.

    :param container: a Container
    :param data: a dictionary where the key is an arbitrary identifier, and the value is a byte string.
    :return: a dictionary where the keys are the object UUIDs as returned by the container, and the values
      are the keys in the original ``data`` dictionary.
    :param compress: whether to use compression or not.
    """
    # Store sorted lists of keys and values
    keys = list(data.keys())
    values = [data[key] for key in keys]

    obj_uuids = container.add_objects_to_pack(values, compress=compress)

    return dict(zip(obj_uuids, keys))


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

    # Check that the keys are the same
    assert set(obj_md5s) == set(retrieved_md5s)
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

    # Check that the keys are the same
    assert set(obj_md5s) == set(retrieved_md5s)
    # Check that the MD5 are correct
    for obj_uuid in obj_md5s:
        assert obj_md5s[obj_uuid] == retrieved_md5s[obj_uuid], "Object '{}' has wrong MD5s ({} vs {})".format(
            obj_uuid, obj_md5s[obj_uuid], retrieved_md5s[obj_uuid]
        )


@pytest.mark.parametrize('use_compression', [True, False])
def test_directly_to_pack_content(temp_container, generate_random_data, use_compression):
    """Add a number of objects directly to packs.

    Then retrieve them and check the content is correct (always bulk retrieve for simplicity)."""
    _assert_empty_repo(temp_container)

    data = generate_random_data()

    obj_md5s = _add_objects_directly_to_pack(temp_container, data, compress=use_compression)

    counts = temp_container.count_objects()
    assert counts['packed'] == len(data), (
        'The container should have {} packed objects '
        '(but there are {} instead)'.format(len(data), counts['packed'])
    )
    assert counts['loose'] == 0, (
        'The container should have 0 loose objects '
        '(but there are {} instead)'.format(counts['loose'])
    )

    # Retrieve objects (loose), in random order
    random_keys = list(obj_md5s.keys())
    random.shuffle(random_keys)

    # Retrieve data in a loop
    retrieved_md5s = _get_data_and_md5_bulk(temp_container, random_keys)

    # Check that the keys are the same
    assert set(obj_md5s) == set(retrieved_md5s)
    # Check that the MD5 are correct
    for obj_uuid in obj_md5s:
        assert obj_md5s[obj_uuid] == retrieved_md5s[obj_uuid], "Object '{}' has wrong MD5s ({} vs {})".format(
            obj_uuid, obj_md5s[obj_uuid], retrieved_md5s[obj_uuid]
        )


@pytest.mark.parametrize('use_compression,open_streams', [(True, True), (True, False), (False, True), (False, False)])
def test_directly_to_pack_streamed(temp_container, generate_random_data, use_compression, open_streams):
    """Add a number of objects directly to packs, using streams.

    Then retrieve them and check the content is correct (always bulk retrieve for simplicity)."""
    _assert_empty_repo(temp_container)

    data = generate_random_data()

    # Store sorted lists of keys and values
    keys = list(data.keys())
    values = [data[key] for key in keys]

    if open_streams:
        streams = []
        streams_copy = []
        with tempfile.TemporaryDirectory() as temp_dir:
            # Read a given fixed order, otherwise later when reconstructing obj_md5s we would have a problem
            for key, content in zip(keys, values):
                file_path = os.path.join(temp_dir, key)
                with open(file_path, 'bw') as fhandle:
                    fhandle.write(content)
                streams.append(utils.LazyOpener(file_path, mode='rb'))
                streams_copy.append(utils.LazyOpener(file_path, mode='rb'))
            obj_uuids = temp_container.add_streamed_objects_to_pack(
                streams, compress=use_compression, open_streams=True
            )
            # I check that instead it fails if I forget to open the streams (and that it does not create side effects)
            # The error that I get here would be: "LazyOpener' object has no attribute 'read'"
            with pytest.raises(AttributeError):
                temp_container.add_streamed_objects_to_pack(streams_copy, compress=use_compression, open_streams=False)

    else:
        streams = [UnopenableBytesIO(value) for value in values]
        streams_copy = [UnopenableBytesIO(value) for value in values]
        obj_uuids = temp_container.add_streamed_objects_to_pack(streams, compress=use_compression, open_streams=False)
        # I check that instead it fails if I try to open but I am not allowed to
        # (and that it does not create side effects). Note that I disabled explicitly the __enter__ method
        # in the class UnopenableBytesIO to make sure that this raises
        with pytest.raises(AttributeError):
            temp_container.add_streamed_objects_to_pack(streams_copy, compress=use_compression, open_streams=True)

    obj_md5s = dict(zip(obj_uuids, keys))

    counts = temp_container.count_objects()
    assert counts['packed'] == len(data), (
        'The container should have {} packed objects '
        '(but there are {} instead)'.format(len(data), counts['packed'])
    )
    assert counts['loose'] == 0, (
        'The container should have 0 loose objects '
        '(but there are {} instead)'.format(counts['loose'])
    )

    # Retrieve objects (loose), in random order
    random_keys = list(obj_md5s.keys())
    random.shuffle(random_keys)

    # Retrieve data in a loop
    retrieved_md5s = _get_data_and_md5_bulk(temp_container, random_keys)

    # Check that the keys are the same
    assert set(obj_md5s) == set(retrieved_md5s)
    # Check that the MD5 are correct
    for obj_uuid in obj_md5s:
        assert obj_md5s[obj_uuid] == retrieved_md5s[obj_uuid], "Object '{}' has wrong MD5s ({} vs {})".format(
            obj_uuid, obj_md5s[obj_uuid], retrieved_md5s[obj_uuid]
        )


@pytest.mark.parametrize('loose_prefix_len,pack_prefix_len', [(0, 2), (2, 2), (3, 2), (0, 3), (2, 3), (3, 3)])
def test_prefix_lengths(temp_dir, generate_random_data, pack_prefix_len, loose_prefix_len):
    """Check if the prefix lengths are honored."""
    container = Container(temp_dir)
    container.init_container(clear=True, pack_prefix_len=pack_prefix_len, loose_prefix_len=loose_prefix_len)
    # Check that the `get_folder` method returns the expected folder name
    assert container.get_folder() == os.path.realpath(temp_dir)

    assert container.loose_prefix_len == loose_prefix_len
    assert container.pack_prefix_len == pack_prefix_len

    _assert_empty_repo(container)
    data = generate_random_data()

    # Store
    obj_md5s = _add_objects_loose_loop(container, data)

    loose_firstlevel = os.listdir(container._get_loose_folder())  # pylint: disable=protected-access
    assert len(loose_firstlevel) > 0
    if loose_prefix_len == 0:
        assert all(len(inode) == 32 for inode in loose_firstlevel)
    else:
        assert all(len(inode) == loose_prefix_len for inode in loose_firstlevel)

    counts = container.count_objects()
    assert counts['packed'] == 0, (
        'The container should have 0 packed objects '
        '(but there are {} instead)'.format(counts['packed'])
    )
    assert counts['loose'] == len(obj_md5s), (
        'The container should have {} loose objects '
        '(but there are {} instead)'.format(len(obj_md5s), counts['loose'])
    )

    retrieved_md5s = _get_data_and_md5_bulk(container, obj_md5s.keys())
    # Check that the MD5 are correct
    for obj_uuid in obj_md5s:
        assert obj_md5s[obj_uuid] == retrieved_md5s[obj_uuid], "Object '{}' has wrong MD5s ({} vs {})".format(
            obj_uuid, obj_md5s[obj_uuid], retrieved_md5s[obj_uuid]
        )

    # Pack all loose objects
    container.pack_all_loose()

    pack_firstlevel = os.listdir(container._get_pack_folder())  # pylint: disable=protected-access
    assert len(pack_firstlevel) > 0
    assert all(len(inode) == pack_prefix_len for inode in pack_firstlevel)

    counts = container.count_objects()
    assert counts['packed'] == len(obj_md5s), (
        'The container should have {} packed objects '
        '(but there are {} instead)'.format(len(obj_md5s), counts['packed'])
    )
    assert counts['loose'] == 0, (
        'The container should have 0 loose objects '
        '(but there are {} instead)'.format(counts['loose'])
    )

    retrieved_md5s = _get_data_and_md5_bulk(container, obj_md5s.keys())
    # Check that the MD5 are correct
    for obj_uuid in obj_md5s:
        assert obj_md5s[obj_uuid] == retrieved_md5s[obj_uuid], "Object '{}' has wrong MD5s ({} vs {})".format(
            obj_uuid, obj_md5s[obj_uuid], retrieved_md5s[obj_uuid]
        )

    # Test also the validation functions
    valid_pack_ids = ['0' * pack_prefix_len, 'a' * pack_prefix_len]
    invalid_pack_ids = ['0' * (pack_prefix_len + 1), 'a' * (pack_prefix_len + 1), 'g' * pack_prefix_len]
    valid_loose_prefixes = ['0' * loose_prefix_len, 'a' * loose_prefix_len]
    invalid_loose_prefixes = [
        '0' * (loose_prefix_len + 1), 'a' * (loose_prefix_len + 1), 'g' * loose_prefix_len if loose_prefix_len else 'g'
    ]

    for pack_id in valid_pack_ids:
        assert container._is_valid_pack_id(  # pylint: disable=protected-access
            pack_id
        ), "'{}' should be valid".format(pack_id)
    for pack_id in invalid_pack_ids:
        assert not container._is_valid_pack_id(  # pylint: disable=protected-access
            pack_id
        ), "'{}' should be invalid".format(pack_id)
    for loose_prefix in valid_loose_prefixes:
        assert container._is_valid_loose_prefix(  # pylint: disable=protected-access
            loose_prefix
        ), "'{}' should be valid".format(loose_prefix)
    for loose_prefix in invalid_loose_prefixes:
        assert not container._is_valid_loose_prefix(  # pylint: disable=protected-access
            loose_prefix
        ), "'{}' should be invalid".format(loose_prefix)

    # I close the container, as this is needed on Windows
    container.close()


@pytest.mark.parametrize('loose_prefix_len,pack_prefix_len', [(-1, 2), (2, -1), (2, 0)])
def test_invalid_prefix_lengths(temp_dir, pack_prefix_len, loose_prefix_len):
    """Check if the prefix lengths are honored."""
    container = Container(temp_dir)
    with pytest.raises(ValueError):
        container.init_container(clear=True, pack_prefix_len=pack_prefix_len, loose_prefix_len=loose_prefix_len)


def test_initialisation(temp_dir):
    """Test that the initialisation function works as expected."""
    container = Container(temp_dir)
    assert not container.is_initialised

    with pytest.raises(exc.NotInitialised):
        _ = container.loose_prefix_len
    with pytest.raises(exc.NotInitialised):
        _ = container.pack_prefix_len

    # Check that the session cannot be obtained before initialising
    with pytest.raises(FileNotFoundError):
        container._get_session(create=False, raise_if_missing=True)  # pylint: disable=protected-access
    assert container._get_session(create=False, raise_if_missing=False) is None  # pylint: disable=protected-access

    container.init_container()
    assert container.is_initialised

    #This call should go through
    container.init_container(clear=True)
    assert container.is_initialised

    with pytest.raises(FileExistsError) as excinfo:
        container.init_container()
    assert 'already exists' in str(excinfo.value)

    # I artificially remove one of the folders: it should notice and say it's not initialised
    os.rmdir(os.path.join(container.get_folder(), 'sandbox'))
    assert not container.is_initialised

    # Close open files (the DB)
    container.close()

    # Remove the folder
    shutil.rmtree(temp_dir)
    assert not container.is_initialised
    # Make back the folder: I leave temp_dir in a consistent state, and moreover I
    # check that the empty folder is again considered non-initialised
    os.mkdir(temp_dir)
    assert not container.is_initialised

    # Create an empty file
    with open(os.path.join(container.get_folder(), 'somefile'), 'w'):
        pass
    # Final re-initialisation
    with pytest.raises(FileExistsError) as excinfo:
        container.init_container()
    assert 'already some file or folder' in str(excinfo.value)


# Only three options: if pack_objects is False, the values of compress_packs is ignored
@pytest.mark.parametrize('pack_objects,compress_packs', [(True, True), (True, False), (False, False)])
def test_unknown_uuids(temp_container, generate_random_data, pack_objects, compress_packs):
    """Put some data in the container, then check that unknown UUIDs raise the correct error."""
    # Generate and store some data, just not to have an empty container
    data = generate_random_data()
    obj_md5s = _add_objects_loose_loop(temp_container, data)

    if pack_objects:
        temp_container.pack_all_loose(compress=compress_packs)

    # Pick any valid UUID
    obj_uuids = list(obj_md5s.keys())

    # 5 unknown UUIDs + one invalid string
    unknown_uuids = [uuid.uuid4().hex for _ in range(5)] + ['invalid-uuid-string']

    # Loop read
    for unknown_uuid in unknown_uuids:
        with pytest.raises(exc.NotExistent):
            temp_container.get_object_content(unknown_uuid)

        # Currently, the exception is actually raised when accessing the stream,
        # not at stream creation
        stream = temp_container.get_object_stream(unknown_uuid)
        with pytest.raises(exc.NotExistent):
            with stream:
                pass

    # 6 invalid UUIDs + all valid ones
    uuids_list = unknown_uuids + obj_uuids
    # I shuffle so they are really in random order
    random.shuffle(uuids_list)

    ##### Bulk reads from here on
    # skip_if_missing=True, get contents
    contents = temp_container.get_object_contents(uuids_list, skip_if_missing=True)
    # The retrieved values should be only the valid ones
    assert set(contents.keys()) == set(obj_uuids)
    check_md5s = {key: hashlib.md5(val).hexdigest() for key, val in contents.items()}
    assert obj_md5s == check_md5s

    # skip_if_missing=True, get streams
    missing = []
    check_md5s = {}
    with temp_container.get_object_streams_and_size(uuids_list, skip_if_missing=True) as triplets:
        for obj_uuid, stream, size in triplets:
            if stream is None:
                assert size == 0
                missing.append(obj_uuid)
            else:
                check_md5s[obj_uuid] = stream.read()
                assert len(check_md5s[obj_uuid]) == size
    # The retrieved values should be only the valid ones
    assert missing == []
    check_md5s = {key: hashlib.md5(val).hexdigest() for key, val in contents.items()}
    assert obj_md5s == check_md5s

    # skip_if_missing=False, get objects
    contents = temp_container.get_object_contents(uuids_list, skip_if_missing=False)
    # There should be only one return value
    for unknown_uuid in unknown_uuids:
        # Check that it's there, that it's noe, and pop it
        assert contents.pop(unknown_uuid) is None
    # After popping, I should be left with the same case as above
    assert set(contents.keys()) == set(obj_uuids)
    check_md5s = {key: hashlib.md5(val).hexdigest() for key, val in contents.items()}
    assert obj_md5s == check_md5s

    # skip_if_missing=False, get streams
    missing = []
    check_md5s = {}
    with temp_container.get_object_streams_and_size(uuids_list, skip_if_missing=False) as triplets:
        for obj_uuid, stream, size in triplets:
            if stream is None:
                assert size == 0
                missing.append(obj_uuid)
            else:
                check_md5s[obj_uuid] = stream.read()
                assert len(check_md5s[obj_uuid]) == size
    # The retrieved values should be only the valid ones
    assert set(missing) == set(unknown_uuids)
    check_md5s = {key: hashlib.md5(val).hexdigest() for key, val in contents.items()}
    assert obj_md5s == check_md5s


@pytest.mark.parametrize('compress_packs', [True, False])
def test_sizes(temp_container, generate_random_data, compress_packs):
    """Check that the information on size is reliable."""
    size_info = temp_container.get_total_size()
    assert size_info['total_size_packed'] == 0
    assert size_info['total_size_packed_on_disk'] == 0
    assert size_info['total_size_packfiles_on_disk'] == 0
    assert size_info['total_size_packindexes_on_disk'] == os.path.getsize(temp_container._get_pack_index_path())  # pylint: disable=protected-access
    assert size_info['total_size_loose'] == 0

    data = generate_random_data()
    total_object_size = sum(len(value) for value in data.values())
    obj_md5s = _add_objects_loose_loop(temp_container, data)
    # Try to count size after retrieving, just to be sure
    assert sum(
        len(content) for content in temp_container.get_object_contents(obj_md5s.keys()).values()
    ) == total_object_size

    # Check the size for loose objects
    size_info = temp_container.get_total_size()
    assert size_info['total_size_packed'] == 0
    assert size_info['total_size_packed_on_disk'] == 0
    assert size_info['total_size_packfiles_on_disk'] == 0
    assert size_info['total_size_packindexes_on_disk'] == os.path.getsize(temp_container._get_pack_index_path())  # pylint: disable=protected-access
    assert size_info['total_size_loose'] == total_object_size

    # Pack without compression
    temp_container.pack_all_loose(compress=compress_packs)
    # Try to count size after retrieving, just to be sure
    assert sum(
        len(content) for content in temp_container.get_object_contents(obj_md5s.keys()).values()
    ) == total_object_size

    if compress_packs:
        # Compress data manually to get compressed size
        # In the current version, compression level is hardcoded.
        # If this becomes a parameter, we need to change this test
        # Note that until when we want to support py3.5, we cannot specify the
        # level as a keyword argument, as this was added only in python 3.6
        compressed_data = {
            key: zlib.compress(val, temp_container._COMPRESSLEVEL)  # pylint: disable=protected-access
            for key, val in data.items()
        }
        total_compressed_size = sum(len(value) for value in compressed_data.values())

        size_info = temp_container.get_total_size()
        assert size_info['total_size_packed'] == total_object_size
        assert size_info['total_size_packed_on_disk'] == total_compressed_size
        assert size_info['total_size_packfiles_on_disk'] == total_compressed_size
        assert size_info['total_size_packindexes_on_disk'] == os.path.getsize(temp_container._get_pack_index_path())  # pylint: disable=protected-access
        assert size_info['total_size_loose'] == 0
    else:
        size_info = temp_container.get_total_size()
        assert size_info['total_size_packed'] == total_object_size
        assert size_info['total_size_packed_on_disk'] == total_object_size
        assert size_info['total_size_packfiles_on_disk'] == total_object_size
        assert size_info['total_size_packindexes_on_disk'] == os.path.getsize(temp_container._get_pack_index_path())  # pylint: disable=protected-access
        assert size_info['total_size_loose'] == 0


def test_get_object_streams_closes(temp_container, generate_random_data):
    """Test that get_object_streams_and_size closes intermediate streams."""
    data = generate_random_data()
    # Store
    obj_md5s = _add_objects_loose_loop(temp_container, data)

    # I get all objects first - this will actually internally go through the same function
    # `get_object_streams_and_size`, but I need to do it as this might open additional files,
    # namely the SQLite DB (possibly more than one file due to the fact it's open in WAL mode).
    # The following checks are still meaningful, I check that if I do it again I don't open more files.
    temp_container.get_object_contents(obj_md5s.keys())

    current_process = psutil.Process()
    start_open_files = len(current_process.open_files())

    with temp_container.get_object_streams_and_size(obj_md5s.keys(), skip_if_missing=True):
        # I don't use the triplets
        pass
    # Check that at the end nothing is left open
    assert len(current_process.open_files()) == start_open_files

    print(current_process.open_files())
    with temp_container.get_object_streams_and_size(obj_md5s.keys(), skip_if_missing=True) as triplets:
        # I loop over the triplets, but I don't do anything
        for _ in triplets:
            pass
    # Check that at the end nothing is left open
    print(current_process.open_files())
    assert len(current_process.open_files()) == start_open_files

    # I actually read the content
    with temp_container.get_object_streams_and_size(obj_md5s.keys(), skip_if_missing=True) as triplets:
        # I loop over the triplets, but I don't do anything
        for _, stream, _ in triplets:
            stream.read()
    # Check that at the end nothing is left open
    assert len(current_process.open_files()) == start_open_files

    ##### Same test after packing
    temp_container.pack_all_loose()
    # I get all objects first, again - this is because it might have closed the DB files while packing
    temp_container.get_object_contents(obj_md5s.keys())
    # I now update the count
    start_open_files = len(current_process.open_files())

    with temp_container.get_object_streams_and_size(obj_md5s.keys()):
        # I don't use the triplets
        pass
    # Check that at the end nothing is left open
    assert len(current_process.open_files()) == start_open_files

    with temp_container.get_object_streams_and_size(obj_md5s.keys()) as triplets:
        # I loop over the triplets, but I don't do anything
        for _ in triplets:
            pass
    # Check that at the end nothing is left open
    assert len(current_process.open_files()) == start_open_files

    # I actually read the content
    with temp_container.get_object_streams_and_size(obj_md5s.keys(), skip_if_missing=True) as triplets:
        # I loop over the triplets, but I don't do anything
        for _, stream, _ in triplets:
            stream.read()
    # Check that at the end nothing is left open
    assert len(current_process.open_files()) == start_open_files
