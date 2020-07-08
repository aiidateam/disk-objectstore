"""Test of the object-store container module."""
# pylint: disable=too-many-lines
import hashlib
import io
import os
import random
import shutil
import tempfile
import zlib
import pathlib

import psutil
import pytest

from disk_objectstore import Container
from disk_objectstore import utils
import disk_objectstore.exceptions as exc


class UnopenableBytesIO(io.BytesIO):
    """An extension of BytesIO that cannot be used as a context manager."""

    def __enter__(self):
        raise AttributeError('__enter__ method disabled for UnopenableBytesIO')

    @property
    def mode(self):
        return 'rb'


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
    :return: a dictionary where the keys are the object hash keys as returned by the container, and the values
      are the keys in the original ``data`` dictionary.
    """
    retval = {}
    for key, content in data.items():
        obj_hashkey = container.add_object(content)
        retval[obj_hashkey] = key
    return retval


def _add_objects_directly_to_pack(container, data, compress):
    """Add objects directly to pack files.

    :param container: a Container
    :param data: a dictionary where the key is an arbitrary identifier, and the value is a byte string.
    :return: a dictionary where the keys are the object hash keys as returned by the container, and the values
      are the keys in the original ``data`` dictionary.
    :param compress: whether to use compression or not.
    """
    # Store sorted lists of keys and values
    keys = list(data.keys())
    values = [data[key] for key in keys]

    obj_hashkeys = container.add_objects_to_pack(values, compress=compress)

    return dict(zip(obj_hashkeys, keys))


def _get_data_and_md5_loop(container, obj_hashkeys):
    """Get the MD5 of the data stored under the given container, one at a time in a loop.

    :param container: a Container
    :param obj_hashkeys: a list of object hash keys
    :return: a dictionary where the keys are the object hash keys and the values are the MD5 hexdigests.
    """
    retval = {}
    for obj_hashkey in obj_hashkeys:
        retrieved_content = container.get_object_content(obj_hashkey)
        retval[obj_hashkey] = hashlib.md5(retrieved_content).hexdigest()
    return retval


def _get_data_and_md5_bulk(container, obj_hashkeys):
    """Get the MD5 of the data stored under the given container as a single bulk operation.

    :param container: a Container
    :param obj_hashkeys: a list of object hash keys
    :return: a dictionary where the keys are the object hash keys and the values are the MD5 hexdigests.
    """
    retval = {}
    retrieved_contents = container.get_objects_content(obj_hashkeys)
    for obj_hashkey in retrieved_contents:
        retval[obj_hashkey] = hashlib.md5(retrieved_contents[obj_hashkey]).hexdigest()
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
    # I check with the length of the set because I could have picked to random identical objects
    assert counts['loose'] == len(set(obj_md5s)), (
        'The container should have {} loose objects '
        '(but there are {} instead)'.format(len(set(obj_md5s)), counts['loose'])
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
    for obj_hashkey in obj_md5s:
        assert obj_md5s[obj_hashkey] == retrieved_md5s[obj_hashkey], "Object '{}' has wrong MD5s ({} vs {})".format(
            obj_hashkey, obj_md5s[obj_hashkey], retrieved_md5s[obj_hashkey]
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
    assert counts['packed'] == len(set(obj_md5s)), (
        'The container should have {} packed objects '
        '(but there are {} instead)'.format(len(set(obj_md5s)), counts['packed'])
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
    for obj_hashkey in obj_md5s:
        assert obj_md5s[obj_hashkey] == retrieved_md5s[obj_hashkey], "Object '{}' has wrong MD5s ({} vs {})".format(
            obj_hashkey, obj_md5s[obj_hashkey], retrieved_md5s[obj_hashkey]
        )


@pytest.mark.parametrize('use_compression', [True, False])
def test_directly_to_pack_content(temp_container, generate_random_data, use_compression):
    """Add a number of objects directly to packs.

    Then retrieve them and check the content is correct (always bulk retrieve for simplicity)."""
    _assert_empty_repo(temp_container)

    data = generate_random_data()

    obj_md5s = _add_objects_directly_to_pack(temp_container, data, compress=use_compression)

    counts = temp_container.count_objects()
    assert counts['packed'] == len(set(data)), (
        'The container should have {} packed objects '
        '(but there are {} instead)'.format(len(set(data)), counts['packed'])
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
    for obj_hashkey in obj_md5s:
        assert obj_md5s[obj_hashkey] == retrieved_md5s[obj_hashkey], "Object '{}' has wrong MD5s ({} vs {})".format(
            obj_hashkey, obj_md5s[obj_hashkey], retrieved_md5s[obj_hashkey]
        )


def test_num_packs_with_target_size(temp_dir, generate_random_data):
    """Add a number of objects directly to packs, with a small pack_size_target.

    Check that packs are properly generated."""
    pack_size_target = 10000
    # 100 objects, each of which of at least 100 bytes.
    num_files = 100
    min_size = 100
    data = generate_random_data(num_files=num_files, min_size=min_size, max_size=3000)
    # Append a different set of bytes (a string repr of the current index)
    # To be sure they are different, and there is no risk of duplicates, that stored
    # together if they have the same hash key
    data = [datum + str(idx).encode() for idx, datum in enumerate(data.values())]
    # This is true if there are enough small files; if it was 1 file of 10000 bytes, one would get only 1 pack
    min_expected_num_packs = (num_files * min_size) // pack_size_target

    temp_container = Container(temp_dir)
    temp_container.init_container(clear=True, pack_size_target=pack_size_target)

    counts = temp_container.count_objects()
    assert counts['pack_files'] == 0

    temp_container.add_objects_to_pack(data, compress=False)

    # Check that enough packs were created
    counts = temp_container.count_objects()
    assert counts['pack_files'] >= min_expected_num_packs
    current_num_packfiles = counts['pack_files']

    # Create a new object of 2*the pack_size_target, as a 'template'.
    # Because of the length, they are surely different from previous data
    # Also, it's bigger than the pack_size_target.
    new_obj = list(
        generate_random_data(num_files=1, min_size=pack_size_target * 2, max_size=pack_size_target * 2).values()
    )[0]
    # Create three objects from this template, with different suffix, so hash key is different
    new_obj1 = new_obj + b'1'
    new_obj2 = new_obj + b'2'
    new_obj3 = new_obj + b'3'
    # Put the first two objects
    temp_container.add_objects_to_pack([new_obj1, new_obj2], compress=False)

    # Check that at least one new pack has been created (probably the first one might have ended
    # up in the previous incomplete pack, but the second one must go definitely in a new pack)
    counts = temp_container.count_objects()
    assert counts['pack_files'] >= current_num_packfiles + 1

    # Update the current number of pack files
    current_num_packfiles = counts['pack_files']

    # Adding a new object must create a new pack, since the previous one is for sure full (it contains
    # only one object, whose size is larger than the pack_size_target)
    temp_container.add_objects_to_pack([new_obj3], compress=False)
    counts = temp_container.count_objects()
    assert counts['pack_files'] == current_num_packfiles + 1

    # I close the container, as this is needed on Windows
    temp_container.close()


# Try a large and a small one
@pytest.mark.parametrize('pack_size_target', [1000, 40000000])
@pytest.mark.parametrize('use_compression,open_streams', [(True, True), (True, False), (False, True), (False, False)])
def test_directly_to_pack_streamed(temp_dir, generate_random_data, use_compression, open_streams, pack_size_target):  # pylint: disable=too-many-locals
    """Add a number of objects directly to packs, using streams.

    Then retrieve them and check the content is correct (always bulk retrieve for simplicity)."""
    temp_container = Container(temp_dir)
    temp_container.init_container(clear=True, pack_size_target=pack_size_target)

    data = generate_random_data()

    # Store sorted lists of keys and values
    keys = list(data.keys())
    values = [data[key] for key in keys]

    if open_streams:
        streams = []
        streams_copy = []
        with tempfile.TemporaryDirectory() as temp_dir2:
            # Read a given fixed order, otherwise later when reconstructing obj_md5s we would have a problem
            for key, content in zip(keys, values):
                file_path = os.path.join(temp_dir2, key)
                with open(file_path, 'bw') as fhandle:
                    fhandle.write(content)
                streams.append(utils.LazyOpener(file_path, mode='rb'))
                streams_copy.append(utils.LazyOpener(file_path, mode='rb'))
            obj_hashkeys = temp_container.add_streamed_objects_to_pack(
                streams, compress=use_compression, open_streams=True
            )
            # I check that instead it fails if I forget to open the streams (and that it does not create side effects)
            # The error that I get here would be: "LazyOpener' object has no attribute 'read'"
            with pytest.raises(AttributeError):
                temp_container.add_streamed_objects_to_pack(streams_copy, compress=use_compression, open_streams=False)

    else:
        streams = [UnopenableBytesIO(value) for value in values]
        streams_copy = [UnopenableBytesIO(value) for value in values]
        obj_hashkeys = temp_container.add_streamed_objects_to_pack(
            streams, compress=use_compression, open_streams=False
        )
        # I check that instead it fails if I try to open but I am not allowed to
        # (and that it does not create side effects). Note that I disabled explicitly the __enter__ method
        # in the class UnopenableBytesIO to make sure that this raises
        with pytest.raises(AttributeError):
            temp_container.add_streamed_objects_to_pack(streams_copy, compress=use_compression, open_streams=True)

    obj_md5s = dict(zip(obj_hashkeys, keys))

    counts = temp_container.count_objects()
    assert counts['packed'] == len(set(data)), (
        'The container should have {} packed objects '
        '(but there are {} instead)'.format(len(set(data)), counts['packed'])
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
    for obj_hashkey in obj_md5s:
        assert obj_md5s[obj_hashkey] == retrieved_md5s[obj_hashkey], "Object '{}' has wrong MD5s ({} vs {})".format(
            obj_hashkey, obj_md5s[obj_hashkey], retrieved_md5s[obj_hashkey]
        )

    # I close the container, as this is needed on Windows
    temp_container.close()


@pytest.mark.parametrize(
    'loose_prefix_len,pack_size_target', [(0, 1000), (2, 1000), (3, 1000), (0, 40000000), (2, 40000000), (3, 40000000)]
)
def test_prefix_lengths(temp_dir, generate_random_data, pack_size_target, loose_prefix_len):
    """Check if the loose prefix length are honored, and if everything works also with vey small pack size target."""
    container = Container(temp_dir)
    container.init_container(clear=True, pack_size_target=pack_size_target, loose_prefix_len=loose_prefix_len)
    # Check that the `get_folder` method returns the expected folder name
    assert container.get_folder() == os.path.realpath(temp_dir)

    assert container.loose_prefix_len == loose_prefix_len
    assert container.pack_size_target == pack_size_target

    _assert_empty_repo(container)
    data = generate_random_data()

    # Store
    obj_md5s = _add_objects_loose_loop(container, data)

    loose_firstlevel = os.listdir(container._get_loose_folder())  # pylint: disable=protected-access
    # Check it's not an empty list
    assert loose_firstlevel
    if loose_prefix_len == 0:
        all_lengths = set(len(inode) for inode in loose_firstlevel)
        # The length of the hashkey depends on the algorithm.
        # Therefore I just check that it's always the same length, not the actual value.
        assert len(all_lengths) == 1
    else:
        assert all(len(inode) == loose_prefix_len for inode in loose_firstlevel)

    counts = container.count_objects()
    assert counts['packed'] == 0, (
        'The container should have 0 packed objects '
        '(but there are {} instead)'.format(counts['packed'])
    )
    assert counts['loose'] == len(set(obj_md5s)), (
        'The container should have {} loose objects '
        '(but there are {} instead)'.format(len(set(obj_md5s)), counts['loose'])
    )

    retrieved_md5s = _get_data_and_md5_bulk(container, obj_md5s.keys())
    # Check that the MD5 are correct
    for obj_hashkey in obj_md5s:
        assert obj_md5s[obj_hashkey] == retrieved_md5s[obj_hashkey], "Object '{}' has wrong MD5s ({} vs {})".format(
            obj_hashkey, obj_md5s[obj_hashkey], retrieved_md5s[obj_hashkey]
        )

    # Pack all loose objects
    container.pack_all_loose()

    pack_firstlevel = os.listdir(container._get_pack_folder())  # pylint: disable=protected-access
    # Check it's not an empty list
    assert pack_firstlevel
    # Pack IDs are zero-based, so the number of packs should be the current pack ID + 1
    assert len([inode for inode in pack_firstlevel if container._is_valid_pack_id(inode)]  # pylint: disable=protected-access
              ) == container._current_pack_id + 1  # pylint: disable=protected-access

    counts = container.count_objects()
    assert counts['packed'] == len(set(obj_md5s)), (
        'The container should have {} packed objects '
        '(but there are {} instead)'.format(len(set(obj_md5s)), counts['packed'])
    )
    assert counts['loose'] == 0, (
        'The container should have 0 loose objects '
        '(but there are {} instead)'.format(counts['loose'])
    )

    retrieved_md5s = _get_data_and_md5_bulk(container, obj_md5s.keys())
    # Check that the MD5 are correct
    for obj_hashkey in obj_md5s:
        assert obj_md5s[obj_hashkey] == retrieved_md5s[obj_hashkey], "Object '{}' has wrong MD5s ({} vs {})".format(
            obj_hashkey, obj_md5s[obj_hashkey], retrieved_md5s[obj_hashkey]
        )

    # Test also the validation functions
    valid_pack_ids = ['0', '1', '2', '10', '100']
    invalid_pack_ids = ['', '01', '0a', '1-']
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


@pytest.mark.parametrize('pack_size_target', [-1, -2])
def test_invalid_pack_size_target(temp_dir, pack_size_target):
    """Check that the prefix lengths and the size targets."""
    container = Container(temp_dir)
    with pytest.raises(ValueError):
        container.init_container(clear=True, pack_size_target=pack_size_target)


@pytest.mark.parametrize('loose_prefix_len', [-1, -2])
def test_invalid_prefix_length(temp_dir, loose_prefix_len):
    """Check that the prefix lengths and the size targets."""
    container = Container(temp_dir)
    with pytest.raises(ValueError):
        container.init_container(clear=True, loose_prefix_len=loose_prefix_len)


def test_invalid_hash_type(temp_dir):
    """Check that the prefix lengths and the size targets."""
    container = Container(temp_dir)
    with pytest.raises(ValueError):
        container.init_container(clear=True, hash_type='unknown-type')


def test_initialisation(temp_dir):
    """Test that the initialisation function works as expected."""
    container = Container(temp_dir)
    assert not container.is_initialised

    with pytest.raises(exc.NotInitialised):
        container.loose_prefix_len  # pylint: disable=pointless-statement
    with pytest.raises(exc.NotInitialised):
        container.pack_size_target  # pylint: disable=pointless-statement

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
def test_unknown_hashkeys(temp_container, generate_random_data, pack_objects, compress_packs):
    """Put some data in the container, then check that unknown hash keys raise the correct error."""
    # Generate and store some data, just not to have an empty container
    data = generate_random_data()
    obj_md5s = _add_objects_loose_loop(temp_container, data)

    if pack_objects:
        temp_container.pack_all_loose(compress=compress_packs)

    # Pick any valid hash key
    obj_hashkeys = list(obj_md5s.keys())

    # 2 unknown keys, one even with invalid format
    # I don't use a 'real' SHA checksum as it could be randomly picked by the
    # randomly generated data
    unknown_hashkeys = ['281ab9a49afbf4c8996fb92427ae41e4649'] + ['invalid--string']

    # Loop read
    for unknown_hashkey in unknown_hashkeys:
        with pytest.raises(exc.NotExistent):
            temp_container.get_object_content(unknown_hashkey)

        # Currently, the exception is actually raised when accessing the stream,
        # not at stream creation
        stream = temp_container.get_object_stream(unknown_hashkey)
        with pytest.raises(exc.NotExistent):
            with stream:
                pass

    # 2 invalid hash keys + all valid ones
    hashkeys_list = unknown_hashkeys + obj_hashkeys
    # I shuffle so they are really in random order
    random.shuffle(hashkeys_list)

    ##### Bulk reads from here on
    # skip_if_missing=True, get contents
    contents = temp_container.get_objects_content(hashkeys_list, skip_if_missing=True)
    # The retrieved values should be only the valid ones
    assert set(contents.keys()) == set(obj_hashkeys)
    check_md5s = {key: hashlib.md5(val).hexdigest() for key, val in contents.items()}
    assert obj_md5s == check_md5s

    # skip_if_missing=True, get streams
    missing = []
    check_md5s = {}
    with temp_container.get_objects_stream_and_meta(hashkeys_list, skip_if_missing=True) as triplets:
        for obj_hashkey, stream, meta in triplets:
            if stream is None:
                assert meta['size'] is None
                missing.append(obj_hashkey)
            else:
                check_md5s[obj_hashkey] = stream.read()
                assert len(check_md5s[obj_hashkey]) == meta['size']
    # The retrieved values should be only the valid ones
    assert missing == []
    check_md5s = {key: hashlib.md5(val).hexdigest() for key, val in contents.items()}
    assert obj_md5s == check_md5s

    # skip_if_missing=False, get objects
    contents = temp_container.get_objects_content(hashkeys_list, skip_if_missing=False)
    # There should be only one return value
    for unknown_hashkey in unknown_hashkeys:
        # Check that it's there, that it's noe, and pop it
        assert contents.pop(unknown_hashkey) is None
    # After popping, I should be left with the same case as above
    assert set(contents.keys()) == set(obj_hashkeys)
    check_md5s = {key: hashlib.md5(val).hexdigest() for key, val in contents.items()}
    assert obj_md5s == check_md5s

    # skip_if_missing=False, get streams
    missing = []
    check_md5s = {}
    with temp_container.get_objects_stream_and_meta(hashkeys_list, skip_if_missing=False) as triplets:
        for obj_hashkey, stream, meta in triplets:
            if stream is None:
                assert meta['size'] is None
                missing.append(obj_hashkey)
            else:
                check_md5s[obj_hashkey] = stream.read()
                assert len(check_md5s[obj_hashkey]) == meta['size']
    # The retrieved values should be only the valid ones
    assert set(missing) == set(unknown_hashkeys)
    check_md5s = {key: hashlib.md5(val).hexdigest() for key, val in contents.items()}
    assert obj_md5s == check_md5s


def test_same_object_loose(temp_container, generate_random_data):
    """Store a lot of times the same bytestream, check that I get only one loose object.

    This is due to the deduplication provided by the hashing function."""
    # Check that there are no objects
    counts = temp_container.count_objects()
    assert counts['packed'] == 0
    assert counts['loose'] == 0
    assert counts['pack_files'] == 0

    num_objects = 100  # Write these many identical objects

    random_data = generate_random_data()
    test_data = list(random_data.values())[0]
    obj_hashkeys = []
    for _ in range(num_objects):
        obj_hashkeys.append(temp_container.add_object(test_data))

    assert len(set(obj_hashkeys)) == 1, 'Objects are not all identical'

    # Check the number of objects again
    counts = temp_container.count_objects()
    assert counts['packed'] == 0
    assert counts['loose'] == 1
    assert counts['pack_files'] == 0


def test_same_object_direct_pack(temp_container, generate_random_data):
    """Store a lot of times the same bytestream directly in the packs, check that I get only one loose object.

    This is due to the deduplication provided by the hashing function."""
    # Check that there are no objects
    counts = temp_container.count_objects()
    assert counts['packed'] == 0
    assert counts['loose'] == 0
    assert counts['pack_files'] == 0

    num_objects = 100  # Write these many identical objects

    random_data = generate_random_data()
    test_data = list(random_data.values())[0]
    # many times the same string
    all_test_data = [test_data] * num_objects

    # Append all of them; it should understand it always the same
    obj_hashkeys = temp_container.add_objects_to_pack(all_test_data)
    assert len(set(obj_hashkeys)) == 1, 'Objects are not all identical'

    # Check the number of objects again
    counts = temp_container.count_objects()
    assert counts['packed'] == 1
    assert counts['loose'] == 0
    assert counts['pack_files'] == 1

    # Do it again; the object is already there
    new_obj_hashkeys = temp_container.add_objects_to_pack(all_test_data)
    assert len(set(obj_hashkeys)) == 1, 'Objects are not all identical'
    assert obj_hashkeys[0] == new_obj_hashkeys[0], 'In the second insertion, it generated a different hash key'

    # Check the number of objects again
    counts = temp_container.count_objects()
    assert counts['packed'] == 1
    assert counts['loose'] == 0
    assert counts['pack_files'] == 1


def test_same_object_loose_and_pack(temp_container, generate_random_data):
    """Store the same object first as loose, then pack all, then readd the same object and repack."""
    # Check that there are no objects
    counts = temp_container.count_objects()
    assert counts['packed'] == 0
    assert counts['loose'] == 0
    assert counts['pack_files'] == 0

    random_data = generate_random_data()
    test_data = list(random_data.values())[0]
    obj_hashkey = temp_container.add_object(test_data)

    # Check the number of objects: there should be a single loose object
    counts = temp_container.count_objects()
    assert counts['packed'] == 0
    assert counts['loose'] == 1
    assert counts['pack_files'] == 0

    temp_container.pack_all_loose()
    # Check the number of objects again; there should be only a single packed object in one pack file
    counts = temp_container.count_objects()
    assert counts['packed'] == 1
    assert counts['loose'] == 0
    assert counts['pack_files'] == 1

    new_obj_hashkey = temp_container.add_object(test_data)
    assert new_obj_hashkey == obj_hashkey

    # We don't check the behavior here.
    # For now, for efficiency, we just store again a loose object.
    # This will be deleted as the first thing upon packing.

    # Pack again; no new packed object should appear
    temp_container.pack_all_loose()
    counts = temp_container.count_objects()
    assert counts['packed'] == 1
    assert counts['loose'] == 0
    assert counts['pack_files'] == 1


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
        len(content) for content in temp_container.get_objects_content(obj_md5s.keys()).values()
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
        len(content) for content in temp_container.get_objects_content(obj_md5s.keys()).values()
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


def test_get_objects_stream_closes(temp_container, generate_random_data):
    """Test that get_objects_stream_and_meta closes intermediate streams."""
    data = generate_random_data()
    # Store
    obj_md5s = _add_objects_loose_loop(temp_container, data)

    # I get all objects first - this will actually internally go through the same function
    # `get_objects_stream_and_meta`, but I need to do it as this might open additional files,
    # namely the SQLite DB (possibly more than one file due to the fact it's open in WAL mode).
    # The following checks are still meaningful, I check that if I do it again I don't open more files.
    temp_container.get_objects_content(obj_md5s.keys())

    current_process = psutil.Process()
    start_open_files = len(current_process.open_files())

    with temp_container.get_objects_stream_and_meta(obj_md5s.keys(), skip_if_missing=True):
        # I don't use the triplets
        pass
    # Check that at the end nothing is left open
    assert len(current_process.open_files()) == start_open_files

    print(current_process.open_files())
    with temp_container.get_objects_stream_and_meta(obj_md5s.keys(), skip_if_missing=True) as triplets:
        # I loop over the triplets, but I don't do anything
        for _ in triplets:
            pass
    # Check that at the end nothing is left open
    print(current_process.open_files())
    assert len(current_process.open_files()) == start_open_files

    # I actually read the content
    with temp_container.get_objects_stream_and_meta(obj_md5s.keys(), skip_if_missing=True) as triplets:
        # I loop over the triplets, but I don't do anything
        for _, stream, _ in triplets:
            stream.read()
    # Check that at the end nothing is left open
    assert len(current_process.open_files()) == start_open_files

    ##### Same test after packing
    temp_container.pack_all_loose()
    # I get all objects first, again - this is because it might have closed the DB files while packing
    temp_container.get_objects_content(obj_md5s.keys())
    # I now update the count
    start_open_files = len(current_process.open_files())

    with temp_container.get_objects_stream_and_meta(obj_md5s.keys()):
        # I don't use the triplets
        pass
    # Check that at the end nothing is left open
    assert len(current_process.open_files()) == start_open_files

    with temp_container.get_objects_stream_and_meta(obj_md5s.keys()) as triplets:
        # I loop over the triplets, but I don't do anything
        for _ in triplets:
            pass
    # Check that at the end nothing is left open
    assert len(current_process.open_files()) == start_open_files

    # I actually read the content
    with temp_container.get_objects_stream_and_meta(obj_md5s.keys(), skip_if_missing=True) as triplets:
        # I loop over the triplets, but I don't do anything
        for _, stream, _ in triplets:
            stream.read()
    # Check that at the end nothing is left open
    assert len(current_process.open_files()) == start_open_files


@pytest.mark.parametrize('compress', [True, False])
@pytest.mark.parametrize('skip_if_missing', [True, False])
def test_stream_meta(temp_container, compress, skip_if_missing):
    """Validate the meta dictionary returned by the get_objects_stream_and_meta and get_object_stream_and_meta."""
    # This is the list of all known meta keys.
    # I do also an explicit check that all and only these are present
    # This is implicit since I will later also compare the exact dictionaries and not only their keys,
    # but I put this here to make sure in the future, if I change the interface and adapt the keys, I don't break
    # this guarantee if I forget to adapt the test.
    known_meta_keys = ['type', 'size', 'pack_id', 'pack_compressed', 'pack_offset', 'pack_length']

    content_packed = b'sffssdf383939'
    content_loose = b'v9fpaM'
    hashkey_packed = temp_container.add_objects_to_pack([content_packed], compress=compress)[0]
    hashkey_loose = temp_container.add_object(content_loose)
    hashkey_missing = 'unknown'
    # Assuming only zlib compression for now. Needs to be adapted when changing the possible compression libraries
    object_pack_length = len(content_packed) if not compress else len(
        zlib.compress(content_packed, temp_container._COMPRESSLEVEL)  # pylint: disable=protected-access
    )

    expected_skip_missing_true = {
        hashkey_packed: {
            'content': content_packed,
            'meta': {
                'type': 'packed',
                'size': len(content_packed),
                'pack_id': 0,  # First pack, it's a new container
                'pack_compressed': compress,
                'pack_offset': 0,  # Only one object in the pack, must start from zero
                'pack_length': object_pack_length,
            }
        },
        hashkey_loose: {
            'content': content_loose,
            'meta': {
                'type': 'loose',
                'size': len(content_loose),
                'pack_id': None,
                'pack_compressed': None,
                'pack_offset': None,
                'pack_length': None,
            }
        }
    }

    expected_skip_missing_false = expected_skip_missing_true.copy()
    expected_skip_missing_false[hashkey_missing] = {
        'content': None,
        'meta': {
            'type': 'missing',
            'size': None,
            'pack_id': None,
            'pack_compressed': None,
            'pack_offset': None,
            'pack_length': None,
        }
    }

    check_dict = {}
    with temp_container.get_objects_stream_and_meta([hashkey_packed, hashkey_loose, hashkey_missing],
                                                    skip_if_missing=skip_if_missing) as triplets:
        # I loop over the triplets, but I don't do anything
        for hashkey, stream, meta in triplets:
            retdict = {'meta': meta}
            # In any case I should return all these meta, and no more
            assert set(meta.keys()) == set(known_meta_keys)
            if stream is None:
                retdict['content'] = None
            else:
                retdict['content'] = stream.read()
            check_dict[hashkey] = retdict

    if skip_if_missing:
        assert check_dict == expected_skip_missing_true
    else:
        assert check_dict == expected_skip_missing_false


def test_length_get_objects(temp_container):
    """Check that the iterator to get the object streams does not perform unnecessary operations.

    This is mostly to check for efficiency and that I don't iterate by mistake multiple times on the same object.
    """
    # Note: I created different data, so these 4 hashkeys will always be different
    data = [b'1', b'2', b'3', b'4']
    data_dict = {}
    for val in data:
        hashkey = temp_container.add_object(val)
        data_dict[hashkey] = val

    # Test 1: I pass all the known hashkeys: I iterate (in some order) on all of them
    hashkeys = list(data_dict)
    iterated_hashkeys = []
    with temp_container.get_objects_stream_and_meta(hashkeys=hashkeys) as triplets:
        for obj_hashkey, _, _ in triplets:
            iterated_hashkeys.append(obj_hashkey)
    assert sorted(iterated_hashkeys) == sorted(hashkeys)

    # Test 2: I pass half the known hashkeys: I iterate (in some order) on all of them
    hashkeys = list(data_dict)[:2]
    iterated_hashkeys = []
    with temp_container.get_objects_stream_and_meta(hashkeys=hashkeys) as triplets:
        for obj_hashkey, _, _ in triplets:
            iterated_hashkeys.append(obj_hashkey)
    assert sorted(iterated_hashkeys) == sorted(hashkeys)

    # Test 3: I pass half the known hashkeys, twice: I iterate (in some order) on all of them, BUT ONLY ONCE
    partial_hashkeys = list(data_dict)[:2]
    hashkeys = partial_hashkeys + partial_hashkeys
    iterated_hashkeys = []
    with temp_container.get_objects_stream_and_meta(hashkeys=hashkeys) as triplets:
        for obj_hashkey, _, _ in triplets:
            iterated_hashkeys.append(obj_hashkey)
    # I should iterate on them ONLY ONCE
    assert sorted(iterated_hashkeys) == sorted(partial_hashkeys)

    # Test 4A: I pass half the known hashkeys, twice, PLUS SOME UNKNOWN HASHKEY, also twice
    # If skip_if_missing=False, I should iterate on ALL of them, BUT ONLY ONCE
    unknown_hashkeys = ['unk1', 'unk2']
    partial_hashkeys = list(data_dict)[:2]
    hashkeys = partial_hashkeys + partial_hashkeys + unknown_hashkeys + unknown_hashkeys
    iterated_hashkeys = []
    with temp_container.get_objects_stream_and_meta(hashkeys=hashkeys, skip_if_missing=False) as triplets:
        for obj_hashkey, _, _ in triplets:
            iterated_hashkeys.append(obj_hashkey)
    # I should iterate on them ONLY ONCE
    assert sorted(iterated_hashkeys) == sorted(set(hashkeys))

    # Test 4B: I pass half the known hashkeys, twice, PLUS SOME UNKNOWN HASHKEY, also twice
    # If skip_if_missing=True, I should iterate ONLY on the known one, BUT ONLY ONCE
    unknown_hashkeys = ['unk1', 'unk2']
    partial_hashkeys = list(data_dict)[:2]
    hashkeys = partial_hashkeys + partial_hashkeys + unknown_hashkeys + unknown_hashkeys
    iterated_hashkeys = []
    with temp_container.get_objects_stream_and_meta(hashkeys=hashkeys, skip_if_missing=True) as triplets:
        for obj_hashkey, _, _ in triplets:
            iterated_hashkeys.append(obj_hashkey)
    # I should iterate on them ONLY ONCE
    assert sorted(iterated_hashkeys) == sorted(set(partial_hashkeys))


def test_very_long_hashkeys_list(temp_container):
    """Test that even when asking for *a lot* of hashkeys in one shot, this does not fail.

    Indeed, in SQLite, there is a maximum number of paramaters in a given query. And SQLAlchemy
    converts `.in_()` filters to parameters.
    In the code, we chunk any request to make sure it does not crash because we're asking more
    entries than SQLite can support (the limit unfortunately is decided at compile-time (of SQLite)
    and so it's not under our control).
    """
    # A bit more than 10 times the internal maximum length of SQL queries
    # This is ~9500, and should exceed the hardcoded limits of 999 on at least some platforms
    # I put +3 to have something that is NOT a multiple
    # Note: this is already a relatively large number and the test takes a few seconds
    # (because I'm writing loose objects as well)
    num_objects = temp_container._IN_SQL_MAX_LENGTH * 10 + 3  # pylint: disable=protected-access
    # Generate a long list of objects with *different* data, so they are not deduplicated
    data = [str(i).encode('ascii') for i in range(num_objects)]

    # The container is empty: let's check that asking for unknown objects work
    # NOTE: I just generate some random 'unknown' hash key
    res = temp_container.get_objects_content(['unk{}'.format(i) for i in range(num_objects)])
    assert not res

    # I now add all objects
    hashkeys = []
    for val in data:
        hashkeys.append(temp_container.add_object(val))

    # This should always be true! I am just appending different objects
    assert len(hashkeys) == num_objects

    # Let's ask for all of them; this should work even if they are many
    values = temp_container.get_objects_content(hashkeys)
    assert values == dict(zip(hashkeys, data))

    # Let's pack everything. This should work even if there are many objects
    # (also in here there are .in_ calls)
    temp_container.pack_all_loose()

    # Let's ask back again all data, now that it's packed
    # Also for packed objects, asking for a lot of data should be OK
    values = temp_container.get_objects_content(hashkeys)
    assert values == dict(zip(hashkeys, data))

    # Create more data, different than the one before and add directly to packs, this time.
    # This should also work
    direct_pack_data = ['P{}'.format(i).encode('ascii') for i in range(num_objects)]
    direct_pack_hashkeys = temp_container.add_objects_to_pack(direct_pack_data)

    # Finally, ask back everything and check
    expected_values = dict(zip(hashkeys, data))
    expected_values.update(dict(zip(direct_pack_hashkeys, direct_pack_data)))
    values = temp_container.get_objects_content(hashkeys + direct_pack_hashkeys)
    assert values == expected_values


@pytest.mark.parametrize('compress', [True, False])
def test_simulate_concurrent_packing(temp_container, compress):  # pylint: disable=invalid-name
    """Simulate race conditions while reading and packing."""
    content = b'abc'
    hashkey = temp_container.add_object(content)

    loose_dir_path = pathlib.Path(temp_container._get_loose_folder())  # pylint: disable=protected-access
    with temp_container.get_object_stream(hashkey) as fhandle:
        fname = fhandle.name
        # Check that this is a loose object (i.e. that it is in the loose folder)
        assert loose_dir_path in pathlib.Path(fname).parents
        assert fhandle.read(1) == b'a'
        temp_container.pack_all_loose(compress=compress)
        assert fhandle.read() == b'bc'

    # On Windows, the loose file might still be there because I cannot delete an open file
    # Still, this is a valid situation and I should be able to get the correct content anyway
    # The following line should be read from the pack file. Anyway, the important thing to test
    # is that the content is properly returned
    with temp_container.get_object_stream(hashkey) as fhandle:
        assert fhandle.read() == b'abc'

    temp_container.pack_all_loose(compress=compress)
    # After a second packing, the loose file *must* have been removed
    assert not os.path.exists(fname)


@pytest.mark.parametrize('compress', [True, False])
def test_simulate_concurrent_packing_multiple(temp_container, compress):  # pylint: disable=invalid-name
    """Simulate race conditions while reading and packing."""
    content1 = b'abc'
    content2 = b'def'
    hashkey1 = temp_container.add_object(content1)
    hashkey2 = temp_container.add_object(content2)
    data = {hashkey1: content1, hashkey2: content2}

    loose_dir_path = pathlib.Path(temp_container._get_loose_folder())  # pylint: disable=protected-access
    with temp_container.get_objects_stream_and_meta([hashkey1, hashkey2]) as triplets:
        counter = 0

        for obj_hashkey, stream, meta in triplets:
            if counter == 0:
                # In the first step, I always pack the rest
                fname = stream.name
                # Check that this is a loose object (i.e. that it is in the loose folder)
                assert loose_dir_path in pathlib.Path(fname).parents
                if obj_hashkey == hashkey1:
                    assert stream.read(1) == b'a'
                    temp_container.pack_all_loose(compress=compress)
                    assert stream.read() == b'bc'
                elif obj_hashkey == hashkey2:
                    assert stream.read(1) == b'd'
                    temp_container.pack_all_loose(compress=compress)
                    assert stream.read() == b'ef'
                else:
                    # Should not happen!
                    raise ValueError('Unknown hash key {}'.format(obj_hashkey))
            elif counter == 1:
                # This should be the other object
                # This was loose when get_objects_stream_and_meta was called, but was packed in the meantime
                # I should still be able to get it correctly
                assert data[obj_hashkey] == stream.read()
            else:
                # Should not happen!
                raise ValueError('There should be only two objects!')
            counter += 1

    # On Windows, the loose file might still be there because I cannot delete an open file
    # Still, this is a valid situation and I should be able to get the correct content anyway
    # The following line should be read from the pack file. Anyway, the important thing to test
    # is that the content is properly returned
    assert data == temp_container.get_objects_content([hashkey1, hashkey2])

    temp_container.pack_all_loose(compress=compress)
    # After a second packing, the loose file *must* have been removed
    assert not os.path.exists(fname)


@pytest.mark.parametrize('compress', [True, False])
def test_simulate_concurrent_packing_multiple_existing_pack(temp_container, compress):  # pylint: disable=invalid-name
    """Simulate race conditions while reading and packing.

    In addition, this does it when the first file is not loose, but it is already packed.
    This triggers some lines of code to close the packs if already open, increasing test coverage
    and implicitly testing that open file leaks are avoided.
    """
    content1 = b'abc'
    content2 = b'def'

    hashkey1 = temp_container.add_objects_to_pack([content1], compress=compress)[0]
    hashkey2 = temp_container.add_object(content2)

    loosepath2 = temp_container._get_loose_path_from_hashkey(hashkey2)  # pylint: disable=protected-access
    # Object 2 is stored loose
    assert os.path.exists(loosepath2)

    with temp_container.get_objects_stream_and_meta([hashkey1, hashkey2]) as triplets:
        counter = 0

        for obj_hashkey, stream, meta in triplets:
            if counter == 0:
                # The first one should be the one that is aleady packed
                assert obj_hashkey == hashkey1

                # Pack the other object during the loop
                temp_container.pack_all_loose(compress=compress)
                assert stream.read() == content1
            elif counter == 1:
                # This should be the second object, packed during the first iteration
                assert stream.read() == content2
            else:
                # Should not happen!
                raise ValueError('There should be only two objects!')
            counter += 1

    # Object #2 was not open during the packing operation. Theferore, it should be deleted during packing
    # on *all* filesystems, and here it should not exist anymore
    assert not os.path.exists(loosepath2)


def test_has_object(temp_container):
    """Test the ``Container.has_object`` method."""
    assert not temp_container.has_object('object')

    # Create an object and test that `has_object` recognizes it
    hashkey = temp_container.add_object(b'')
    assert temp_container.has_object(hashkey)

    # Verify that it still works after packing the object
    temp_container.pack_all_loose()
    assert temp_container.has_object(hashkey)
