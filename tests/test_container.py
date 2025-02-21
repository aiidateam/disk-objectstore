"""Test of the object-store container module."""
# pylint: disable=too-many-lines,protected-access
import dataclasses
import functools
import hashlib
import io
import os
import pathlib
import random
import shutil
import stat
import tempfile
from pathlib import Path

import psutil
import pytest

import disk_objectstore.exceptions as exc
from disk_objectstore import CompressMode, Container, ObjectType, database, utils
from disk_objectstore.dataclasses import ObjectMeta

COMPRESSION_ALGORITHMS_TO_TEST = ["zlib+1", "zlib+9"]


class UnopenableBytesIO(io.BytesIO):
    """An extension of BytesIO that cannot be used as a context manager."""

    def __enter__(self):
        raise AttributeError("__enter__ method disabled for UnopenableBytesIO")

    @property
    def mode(self):
        return "rb"


def _assert_empty_repo(container):
    """Check that the container has no objects and no pack files.

    :param container: a Container.
    """
    counts = container.count_objects()
    assert (
        counts["packed"] == 0
    ), f"The container should be empty at the beginning (but there are {counts['packed']} packed objects)"
    assert (
        counts["loose"] == 0
    ), f"The container should be empty at the beginning (but there are {counts['loose']} loose objects)"
    assert (
        counts["pack_files"] == 0
    ), f"The container should be empty at the beginning (but there are {counts['pack_files']} pack files)"


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


@pytest.mark.parametrize("retrieve_bulk", [True, False])
def test_add_get_loose(temp_container, generate_random_data, retrieve_bulk):
    """Add a number of objects (one by one, loose) to the container.

    Then retrieve them and check the content is correct."""
    _assert_empty_repo(temp_container)

    data = generate_random_data()

    # Store
    obj_md5s = _add_objects_loose_loop(temp_container, data)

    counts = temp_container.count_objects()
    assert (
        counts["packed"] == 0
    ), f"The container should have no packed objects (but there are {counts['packed']} instead)"
    # I check with the length of the set because I could have picked to random identical objects
    assert counts["loose"] == len(
        set(obj_md5s)
    ), f"The container should have {len(set(obj_md5s))} loose objects (but there are {counts['loose']} instead)"

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
    for obj_hashkey in obj_md5s:  # pylint: disable=consider-using-dict-items
        assert (
            obj_md5s[obj_hashkey] == retrieved_md5s[obj_hashkey]
        ), f"Object '{obj_hashkey}' has wrong MD5s ({obj_md5s[obj_hashkey]} vs {retrieved_md5s[obj_hashkey]})"


def test_add_loose_from_stream(temp_container):
    """Test adding an object from a stream (from an open file, for instance)."""
    # Write 10*100000 = 1 million bytes, larger than a chunk
    content = b"0123456789" * 1000000

    with tempfile.NamedTemporaryFile(mode="wb", delete=False) as temp_handle:
        temp_handle.write(content)

    with open(temp_handle.name, "rb") as read_handle:
        hashkey = temp_container.add_streamed_object(read_handle)

    read_content = temp_container.get_object_content(hashkey)

    assert read_content == content

    os.remove(temp_handle.name)


@pytest.mark.parametrize(
    "use_compression,retrieve_bulk",
    [(True, True), (True, False), (False, True), (False, False)],
)
def test_add_get_with_packing(
    temp_container, generate_random_data, use_compression, retrieve_bulk
):
    """Add a number of objects (one by one, loose) to the container.

    Then retrieve them and check the content is correct."""
    _assert_empty_repo(temp_container)

    data = generate_random_data()

    # Store
    obj_md5s = _add_objects_loose_loop(temp_container, data)

    # Pack all loose objects
    temp_container.pack_all_loose(compress=use_compression)

    counts = temp_container.count_objects()
    assert counts["packed"] == len(
        set(obj_md5s)
    ), f"The container should have {len(set(obj_md5s))} packed objects (but there are {counts['packed']} instead)"
    # Loose objects are not immediately deleted
    assert counts["loose"] == len(set(obj_md5s)), (
        f"The container should still have all {len(set(obj_md5s))} loose objects "
        f"(but there are {counts['loose']} instead)"
    )

    # Clean up and remove loose objects that are already packed
    temp_container.clean_storage()
    counts = temp_container.count_objects()
    # Now there shouldn't be any more loose objects
    assert (
        counts["loose"] == 0
    ), f"The container should have 0 loose objects (but there are {counts['loose']} instead)"

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
    for obj_hashkey in obj_md5s:  # pylint: disable=consider-using-dict-items
        assert (
            obj_md5s[obj_hashkey] == retrieved_md5s[obj_hashkey]
        ), f"Object '{obj_hashkey}' has wrong MD5s ({obj_md5s[obj_hashkey]} vs {retrieved_md5s[obj_hashkey]})"


@pytest.mark.parametrize("use_compression", [True, False])
def test_directly_to_pack_content(
    temp_container, generate_random_data, use_compression
):
    """Add a number of objects directly to packs.

    Then retrieve them and check the content is correct (always bulk retrieve for simplicity).
    """
    _assert_empty_repo(temp_container)

    data = generate_random_data()

    obj_md5s = _add_objects_directly_to_pack(
        temp_container, data, compress=use_compression
    )

    counts = temp_container.count_objects()
    assert counts["packed"] == len(
        set(data)
    ), f"The container should have {len(set(data))} packed objects (but there are {counts['packed']} instead)"
    assert (
        counts["loose"] == 0
    ), f"The container should have 0 loose objects (but there are {counts['loose']} instead)"

    # Retrieve objects (loose), in random order
    random_keys = list(obj_md5s.keys())
    random.shuffle(random_keys)

    # Retrieve data in a loop
    retrieved_md5s = _get_data_and_md5_bulk(temp_container, random_keys)

    # Check that the keys are the same
    assert set(obj_md5s) == set(retrieved_md5s)
    # Check that the MD5 are correct
    for obj_hashkey in obj_md5s:
        assert (
            obj_md5s[obj_hashkey] == retrieved_md5s[obj_hashkey]
        ), f"Object '{obj_hashkey}' has wrong MD5s ({obj_md5s[obj_hashkey]} vs {retrieved_md5s[obj_hashkey]})"


@pytest.mark.parametrize(
    "use_compression,use_packing,clean_storage",
    [
        (True, True, True),
        (True, True, False),
        (True, False, False),
        (False, False, False),
    ],
)
def test_stream_seek(temp_container, use_compression, use_packing, clean_storage):
    """Test that stream returned by `Container.get_object_stream` is properly seekable."""
    content = b"0123456789abcdef"
    hashkey = temp_container.add_object(content)

    if use_packing:
        temp_container.pack_all_loose(compress=use_compression)

    # I also clean the storage when using compression, since I want to trigger the
    # regeneration of a loose file
    if clean_storage:
        temp_container.clean_storage()

    with temp_container.get_object_stream(hashkey) as stream:
        assert stream.read() == content

        # Test whence=0, seeking to the fifth byte and reading all remaining bytes
        offset = 5
        stream.seek(offset, 0)
        assert stream.read() == content[offset:]

        # Test whence=1, by first seeking to the tenth byte, seeking 5 negative bytes and reading the rest

        # This should trigger the creation of a loose uncompressed copy of the file when called.
        if clean_storage:
            # File should not be there yet at this point
            assert not temp_container._get_loose_path_from_hashkey(hashkey).is_file()
        stream.seek(10)
        offset = -5
        stream.seek(offset, 1)
        # Check that we have loosened the file
        assert temp_container._get_loose_path_from_hashkey(hashkey).is_file()

        assert stream.tell() == 10 - 5
        assert stream.read() == content[(10 + -5) :]

    # I exit the context manager - this should close the object

    if clean_storage:
        # Clean again to remove uncompressed cache
        temp_container.clean_storage()

        # File should not be there yet at this point - this should be always
        # OK on Unix/Mac (I can always delete an open file), but also on Windows
        # (the idea is that I am actually indirectly checking that closing the
        # context manager is actually closing the underlying loose version of
        # the object that was autogenerated internally to have fast access).
        assert not temp_container._get_loose_path_from_hashkey(hashkey).is_file()

    # I reopen the stream - in this way internal streams (including the
    # LazyLooseStream) should be closed
    with temp_container.get_object_stream(hashkey) as stream:
        # Test whence=1, by first seeking to the tenth byte, seeking 3 further bytes and reading the rest
        # Note: going forward should not uncompress the whole file
        stream.seek(10)
        offset = 3
        stream.seek(offset, 1)
        assert stream.read() == content[(10 + 3) :]

        # Test whence=2, by first seeking to the tenth byte, seeking 3 from the end
        stream.seek(10)
        offset = -3
        stream.seek(offset, 2)
        assert stream.tell() == len(content) - 3
        assert stream.read() == content[offset:]
        # Check that we have loosened the file again
        assert temp_container._get_loose_path_from_hashkey(hashkey).is_file()

        if use_packing:
            # I check only the exceptions I raise from my code.
            # A 'standard' stream on a file might not raise here.
            with pytest.raises(ValueError):
                # Invalid whence value
                stream.seek(0, 3)


def test_container_context_manager(temp_dir):
    """Check that the context manager works.

    In particular, it should correctly close the internal session to the DB.
    """
    with Container(folder=temp_dir) as container:
        container.init_container(clear=True)
        container.add_object(b"abc")
        container.pack_all_loose()
        assert container._operation_session is not None, "Session should be open"
    assert (
        container._operation_session is None
    ), "Session should be closed when going out of the context manager"


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

    # Will track what I store for a final check: hash keys and object content
    hashkeys = []
    object_data = []

    temp_container = Container(temp_dir)
    temp_container.init_container(clear=True, pack_size_target=pack_size_target)

    counts = temp_container.count_objects()
    assert counts["pack_files"] == 0

    hashkeys += temp_container.add_objects_to_pack(data, compress=False)
    object_data += data

    # Check that enough packs were created
    counts = temp_container.count_objects()
    assert counts["pack_files"] >= min_expected_num_packs
    current_num_packfiles = counts["pack_files"]

    # Create a new object of 2*the pack_size_target, as a 'template'.
    # Because of the length, they are surely different from previous data
    # Also, it's bigger than the pack_size_target.
    new_obj = list(
        generate_random_data(
            num_files=1, min_size=pack_size_target * 2, max_size=pack_size_target * 2
        ).values()
    )[0]
    # Create three objects from this template, with different suffix, so hash key is different
    new_obj1 = new_obj + b"1"
    new_obj2 = new_obj + b"2"
    new_obj3 = new_obj + b"3"
    # Put the first two objects
    hashkeys += temp_container.add_objects_to_pack([new_obj1, new_obj2], compress=False)
    object_data += [new_obj1, new_obj2]

    # Check that at least one new pack has been created (probably the first one might have ended
    # up in the previous incomplete pack, but the second one must go definitely in a new pack)
    counts = temp_container.count_objects()
    assert counts["pack_files"] >= current_num_packfiles + 1

    # Update the current number of pack files
    current_num_packfiles = counts["pack_files"]

    # Adding a new object must create a new pack, since the previous one is for sure full (it contains
    # only one object, whose size is larger than the pack_size_target)
    hashkeys += temp_container.add_objects_to_pack([new_obj3], compress=False)
    object_data += [new_obj3]
    counts = temp_container.count_objects()
    assert counts["pack_files"] == current_num_packfiles + 1

    # Read all objects, and check content.
    # This also triggers all the logic to close open files, with more than one pack.
    content = temp_container.get_objects_content(hashkeys)
    assert content == dict(zip(hashkeys, object_data))

    # I close the container, as this is needed on Windows
    temp_container.close()


# Try a large and a small one
@pytest.mark.parametrize("pack_size_target", [1000, 40000000])
@pytest.mark.parametrize(
    "use_compression,open_streams",
    [(True, True), (True, False), (False, True), (False, False)],
)
def test_directly_to_pack_streamed(
    temp_dir, generate_random_data, use_compression, open_streams, pack_size_target
):  # pylint: disable=too-many-locals
    """Add a number of objects directly to packs, using streams.

    Then retrieve them and check the content is correct (always bulk retrieve for simplicity).
    """
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
                file_path = Path(temp_dir2) / key
                with open(file_path, "bw") as fhandle:
                    fhandle.write(content)
                streams.append(utils.LazyOpener(file_path))
                streams_copy.append(utils.LazyOpener(file_path))
            obj_hashkeys = temp_container.add_streamed_objects_to_pack(
                streams, compress=use_compression, open_streams=True
            )
            # I check that instead it fails if I forget to open the streams (and that it does not create side effects)
            # The error that I get here would be: "LazyOpener' object has no attribute 'read'"
            with pytest.raises(AttributeError):
                temp_container.add_streamed_objects_to_pack(
                    streams_copy, compress=use_compression, open_streams=False
                )

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
            temp_container.add_streamed_objects_to_pack(
                streams_copy, compress=use_compression, open_streams=True
            )

    obj_md5s = dict(zip(obj_hashkeys, keys))

    counts = temp_container.count_objects()
    assert counts["packed"] == len(
        set(data)
    ), f"The container should have {len(set(data))} packed objects (but there are {counts['packed']} instead)"
    assert (
        counts["loose"] == 0
    ), f"The container should have 0 loose objects (but there are {counts['loose']} instead)"

    # Retrieve objects (loose), in random order
    random_keys = list(obj_md5s.keys())
    random.shuffle(random_keys)

    # Retrieve data in a loop
    retrieved_md5s = _get_data_and_md5_bulk(temp_container, random_keys)

    # Check that the keys are the same
    assert set(obj_md5s) == set(retrieved_md5s)
    # Check that the MD5 are correct
    for obj_hashkey in obj_md5s:
        assert (
            obj_md5s[obj_hashkey] == retrieved_md5s[obj_hashkey]
        ), f"Object '{obj_hashkey}' has wrong MD5s ({obj_md5s[obj_hashkey]} vs {retrieved_md5s[obj_hashkey]})"

    # I close the container, as this is needed on Windows
    temp_container.close()


@pytest.mark.parametrize(
    "loose_prefix_len,pack_size_target",
    [(0, 1000), (2, 1000), (3, 1000), (0, 40000000), (2, 40000000), (3, 40000000)],
)
def test_prefix_lengths(
    temp_dir, generate_random_data, pack_size_target, loose_prefix_len
):
    """Check if the loose prefix length are honored, and if everything works also with vey small pack size target."""
    container = Container(temp_dir)
    container.init_container(
        clear=True, pack_size_target=pack_size_target, loose_prefix_len=loose_prefix_len
    )
    # Check that the `get_folder` method returns the expected folder name
    assert container.get_folder() == temp_dir.resolve()

    assert container.loose_prefix_len == loose_prefix_len
    assert container.pack_size_target == pack_size_target

    _assert_empty_repo(container)
    data = generate_random_data()

    # Store
    obj_md5s = _add_objects_loose_loop(container, data)

    loose_firstlevel = os.listdir(container._get_loose_folder())
    # Check it's not an empty list
    assert loose_firstlevel
    if loose_prefix_len == 0:
        all_lengths = {len(inode) for inode in loose_firstlevel}
        # The length of the hashkey depends on the algorithm.
        # Therefore I just check that it's always the same length, not the actual value.
        assert len(all_lengths) == 1
    else:
        assert all(len(inode) == loose_prefix_len for inode in loose_firstlevel)

    counts = container.count_objects()
    assert (
        counts["packed"] == 0
    ), f"The container should have 0 packed objects (but there are {counts['packed']} instead)"
    assert counts["loose"] == len(
        set(obj_md5s)
    ), f"The container should have {len(set(obj_md5s))} loose objects (but there are {counts['loose']} instead)"

    retrieved_md5s = _get_data_and_md5_bulk(container, obj_md5s.keys())
    # Check that the MD5 are correct
    for obj_hashkey in obj_md5s:  # pylint: disable=consider-using-dict-items
        assert (
            obj_md5s[obj_hashkey] == retrieved_md5s[obj_hashkey]
        ), f"Object '{obj_hashkey}' has wrong MD5s ({obj_md5s[obj_hashkey]} vs {retrieved_md5s[obj_hashkey]})"

    # Pack all loose objects
    container.pack_all_loose()

    pack_firstlevel = os.listdir(container._get_pack_folder())
    # Check it's not an empty list
    assert pack_firstlevel
    # Pack IDs are zero-based, so the number of packs should be the current pack ID + 1
    assert (
        len([inode for inode in pack_firstlevel if container._is_valid_pack_id(inode)])
        == container._current_pack_id + 1
    )

    counts = container.count_objects()
    assert counts["packed"] == len(
        set(obj_md5s)
    ), f"The container should have {len(set(obj_md5s))} packed objects (but there are {counts['packed']} instead)"
    # Loose objects are not immediately deleted
    assert counts["loose"] == len(set(obj_md5s)), (
        f"The container should still have all {len(set(obj_md5s))} loose objects "
        f"(but there are {counts['loose']} instead)"
    )

    # Clean up and remove loose objects that are already packed
    container.clean_storage()
    counts = container.count_objects()
    # Now there shouldn't be any more loose objects
    assert (
        counts["loose"] == 0
    ), f"The container should have 0 loose objects (but there are {counts['loose']} instead)"

    retrieved_md5s = _get_data_and_md5_bulk(container, obj_md5s.keys())
    # Check that the MD5 are correct
    for obj_hashkey in obj_md5s:  # pylint: disable=consider-using-dict-items
        assert (
            obj_md5s[obj_hashkey] == retrieved_md5s[obj_hashkey]
        ), f"Object '{obj_hashkey}' has wrong MD5s ({obj_md5s[obj_hashkey]} vs {retrieved_md5s[obj_hashkey]})"

    # Test also the validation functions
    valid_pack_ids = ["0", "1", "2", "10", "100"]
    invalid_pack_ids = ["", "01", "0a", "1-"]
    valid_loose_prefixes = ["0" * loose_prefix_len, "a" * loose_prefix_len]
    invalid_loose_prefixes = [
        "0" * (loose_prefix_len + 1),
        "a" * (loose_prefix_len + 1),
        "g" * loose_prefix_len if loose_prefix_len else "g",
    ]

    for pack_id in valid_pack_ids:
        assert container._is_valid_pack_id(pack_id), f"'{pack_id}' should be valid"
    for pack_id in invalid_pack_ids:
        assert not container._is_valid_pack_id(
            pack_id
        ), f"'{pack_id}' should be invalid"
    for loose_prefix in valid_loose_prefixes:
        assert container._is_valid_loose_prefix(
            loose_prefix
        ), f"'{loose_prefix}' should be valid"
    for loose_prefix in invalid_loose_prefixes:
        assert not container._is_valid_loose_prefix(
            loose_prefix
        ), f"'{loose_prefix}' should be invalid"

    # I close the container, as this is needed on Windows
    container.close()


@pytest.mark.parametrize("pack_size_target", [-1, -2])
def test_invalid_pack_size_target(temp_dir, pack_size_target):
    """Check that the prefix lengths and the size targets."""
    container = Container(temp_dir)
    with pytest.raises(ValueError):
        container.init_container(clear=True, pack_size_target=pack_size_target)


@pytest.mark.parametrize("loose_prefix_len", [-1, -2])
def test_invalid_prefix_length(temp_dir, loose_prefix_len):
    """Check that the prefix lengths and the size targets."""
    container = Container(temp_dir)
    with pytest.raises(ValueError):
        container.init_container(clear=True, loose_prefix_len=loose_prefix_len)


def test_invalid_hash_type(temp_dir):
    """Check that the prefix lengths and the size targets."""
    container = Container(temp_dir)
    with pytest.raises(ValueError):
        container.init_container(clear=True, hash_type="unknown-type")


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
        container._get_operation_session()

    container.init_container()
    assert container.is_initialised
    container.close()

    # This call should go through
    container.init_container(clear=True)
    assert container.is_initialised
    container.close()

    with pytest.raises(FileExistsError) as excinfo:
        container.init_container()
    assert "already exists" in str(excinfo.value)

    # I artificially remove one of the folders: it should notice and say it's not initialised
    os.rmdir(container.get_folder() / "sandbox")
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
    with open(container.get_folder() / "somefile", "w"):
        pass
    # Final re-initialisation
    with pytest.raises(FileExistsError) as excinfo:
        container.init_container()
    assert "already some file or folder" in str(excinfo.value)


@pytest.mark.parametrize("hash_type", ["sha256", "sha1"])
@pytest.mark.parametrize("compress", [True, False])
def test_check_hash_computation(temp_dir, hash_type, compress):
    """Check that the hashes are correctly computed, when storing loose,
    directly to packs, and while repacking all loose.

    Check both compressed and uncompressed packed objects.
    """
    # Re-init the container with the correct hash type
    container = Container(temp_dir)
    container.init_container(hash_type=hash_type, clear=True)
    content1 = b"1"
    content2 = b"222"
    content3 = b"n2fwd"

    expected_hasher = getattr(hashlib, hash_type)

    hashkey1 = container.add_object(content1)
    assert hashkey1 == expected_hasher(content1).hexdigest()

    hash_keys = container.add_objects_to_pack([content2, content3], compress=compress)
    assert len(hash_keys) == 2
    hashkey2, hashkey3 = hash_keys[0], hash_keys[1]
    assert hashkey2 == expected_hasher(content2).hexdigest()
    assert hashkey3 == expected_hasher(content3).hexdigest()

    # No exceptions should be aised
    container.pack_all_loose(compress=compress, validate_objects=True)


@pytest.mark.parametrize("validate_objects", [True, False])
@pytest.mark.parametrize("corrupt", [True, False])
@pytest.mark.parametrize("compress", [True, False])
def test_validation_while_packing(temp_container, compress, corrupt, validate_objects):
    """Check that, if while packing loose objects, the validation (when asked for) works."""
    content1 = b"34gq34"
    content2 = b"jsdklvjvldk"

    corrupted_content2 = b"CORRUPTED"

    hashkey1 = temp_container.add_object(content1)
    hashkey2 = temp_container.add_object(content2)

    # Corrupt the content of a loose object
    if corrupt:
        with open(
            temp_container._get_loose_path_from_hashkey(hashkey2), "wb"
        ) as fhandle:
            fhandle.write(corrupted_content2)

    if corrupt and validate_objects:
        with pytest.raises(exc.InconsistentContent):
            temp_container.pack_all_loose(
                compress=compress, validate_objects=validate_objects
            )
        # hashkey2 should have been left as 'loose'. Hashkey1 could be either packed or loose, so we don't check.
        assert temp_container.get_object_meta(hashkey2)["type"] == ObjectType.LOOSE
    else:
        temp_container.pack_all_loose(
            compress=compress, validate_objects=validate_objects
        )
        # Both should have been packed
        assert temp_container.get_object_meta(hashkey1)["type"] == ObjectType.PACKED
        assert temp_container.get_object_meta(hashkey2)["type"] == ObjectType.PACKED

    # Check content
    assert temp_container.get_object_content(hashkey1) == content1
    if corrupt:
        # We can't do much, the content should be corrupt (not good, but that's it...)
        assert temp_container.get_object_content(hashkey2) == corrupted_content2
    else:
        assert temp_container.get_object_content(hashkey2) == content2


# Only three options: if pack_objects is False, the values of compress_packs is ignored
@pytest.mark.parametrize(
    "pack_objects,compress_packs", [(True, True), (True, False), (False, False)]
)
def test_unknown_hashkeys(
    temp_container, generate_random_data, pack_objects, compress_packs
):
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
    unknown_hashkeys = ["281ab9a49afbf4c8996fb92427ae41e4649"] + ["invalid--string"]

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
    with temp_container.get_objects_stream_and_meta(
        hashkeys_list, skip_if_missing=True
    ) as triplets:
        for obj_hashkey, stream, meta in triplets:
            if stream is None:
                assert meta["size"] is None
                missing.append(obj_hashkey)
            else:
                check_md5s[obj_hashkey] = stream.read()
                assert len(check_md5s[obj_hashkey]) == meta["size"]
    # The retrieved values should be only the valid ones
    assert not missing  # check that the list is empty
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
    with temp_container.get_objects_stream_and_meta(
        hashkeys_list, skip_if_missing=False
    ) as triplets:
        for obj_hashkey, stream, meta in triplets:
            if stream is None:
                assert meta["size"] is None
                missing.append(obj_hashkey)
            else:
                check_md5s[obj_hashkey] = stream.read()
                assert len(check_md5s[obj_hashkey]) == meta["size"]
    # The retrieved values should be only the valid ones
    assert set(missing) == set(unknown_hashkeys)
    check_md5s = {key: hashlib.md5(val).hexdigest() for key, val in contents.items()}
    assert obj_md5s == check_md5s


def test_same_object_loose(temp_container, generate_random_data):
    """Store a lot of times the same bytestream, check that I get only one loose object.

    This is due to the deduplication provided by the hashing function."""
    # Check that there are no objects
    counts = temp_container.count_objects()
    assert counts["packed"] == 0
    assert counts["loose"] == 0
    assert counts["pack_files"] == 0

    num_objects = 100  # Write these many identical objects

    random_data = generate_random_data()
    test_data = list(random_data.values())[0]
    obj_hashkeys = []
    for _ in range(num_objects):
        obj_hashkeys.append(temp_container.add_object(test_data))

    assert len(set(obj_hashkeys)) == 1, "Objects are not all identical"

    # Check the number of objects again
    counts = temp_container.count_objects()
    assert counts["packed"] == 0
    assert counts["loose"] == 1
    assert counts["pack_files"] == 0


def test_same_object_direct_pack(temp_container, generate_random_data):
    """Store a lot of times the same bytestream directly in the packs, check that I get only one loose object.

    This is due to the deduplication provided by the hashing function."""
    # Check that there are no objects
    counts = temp_container.count_objects()
    assert counts["packed"] == 0
    assert counts["loose"] == 0
    assert counts["pack_files"] == 0

    num_objects = 100  # Write these many identical objects

    random_data = generate_random_data()
    test_data = list(random_data.values())[0]
    # many times the same string
    all_test_data = [test_data] * num_objects

    # Append all of them; it should understand it always the same
    obj_hashkeys = temp_container.add_objects_to_pack(all_test_data)
    assert len(set(obj_hashkeys)) == 1, "Objects are not all identical"

    # Check the number of objects again
    counts = temp_container.count_objects()
    assert counts["packed"] == 1
    assert counts["loose"] == 0
    assert counts["pack_files"] == 1

    # Do it again; the object is already there
    new_obj_hashkeys = temp_container.add_objects_to_pack(all_test_data)
    assert len(set(obj_hashkeys)) == 1, "Objects are not all identical"
    assert (
        obj_hashkeys[0] == new_obj_hashkeys[0]
    ), "In the second insertion, it generated a different hash key"

    # Check the number of objects again
    counts = temp_container.count_objects()
    assert counts["packed"] == 1
    assert counts["loose"] == 0
    assert counts["pack_files"] == 1


def test_same_object_loose_and_pack(temp_container):
    """Store the same object first as loose, then pack all, then readd the same object and repack."""
    # Check that there are no objects
    counts = temp_container.count_objects()
    assert counts["packed"] == 0
    assert counts["loose"] == 0
    assert counts["pack_files"] == 0

    test_data = b"fsdjkldf"
    obj_hashkey = temp_container.add_object(test_data)

    # Check the number of objects: there should be a single loose object
    counts = temp_container.count_objects()
    assert counts["packed"] == 0
    assert counts["loose"] == 1
    assert counts["pack_files"] == 0

    temp_container.pack_all_loose()
    # Check the number of objects again; there should be only a single packed object in one pack file
    counts = temp_container.count_objects()
    assert counts["packed"] == 1
    assert counts["loose"] == 1  # still undeleted
    assert counts["pack_files"] == 1

    # Clean up and remove loose objects that are already packed
    temp_container.clean_storage()
    counts = temp_container.count_objects()
    assert counts["packed"] == 1
    assert counts["loose"] == 0  # now removed
    assert counts["pack_files"] == 1

    new_obj_hashkey = temp_container.add_object(test_data)
    assert new_obj_hashkey == obj_hashkey

    # We don't check the behavior here.
    # For now, for efficiency, we just store again a loose object.
    # This will be deleted as the first thing upon packing.

    # Pack again and clean storage; no new packed object should appear
    temp_container.pack_all_loose()
    temp_container.clean_storage()
    counts = temp_container.count_objects()
    assert counts["packed"] == 1
    assert counts["loose"] == 0
    assert counts["pack_files"] == 1


@pytest.mark.skipif(os.name != "nt", reason="This test only makes sense on Windows")
@pytest.mark.parametrize("compress", [True, False])
@pytest.mark.parametrize("open_only", [True, False])
def test_locked_object_while_packing(  # pylint: disable=invalid-name
    temp_container, lock_file_on_windows, open_only, compress
):
    """Check that the information on size is reliable.

    :param open_only: if True, just open; if False, lock also for reading.
    """
    content1 = b"2332"
    content2 = b"wegaewf"

    counts = temp_container.count_objects()
    assert counts["packed"] == 0
    assert counts["loose"] == 0

    hashkey1 = temp_container.add_object(content1)
    hashkey2 = temp_container.add_object(content2)

    counts = temp_container.count_objects()
    assert counts["packed"] == 0
    assert counts["loose"] == 2

    file_descriptor = os.open(
        temp_container._get_loose_path_from_hashkey(hashkey1),
        os.O_RDONLY,
    )
    try:
        if not open_only:
            lock_file_on_windows(file_descriptor)

        temp_container.pack_all_loose(compress=compress)
    finally:
        # Should also unlock
        os.close(file_descriptor)

    counts = temp_container.count_objects()
    # Both should have been packed if the loose object was simply open.
    # Otherwise, if it was locked, I couldn't do anything so it's still loose
    assert counts["packed"] == (2 if open_only else 1)

    # Check I can get the content
    assert temp_container.get_object_content(hashkey1) == content1
    assert temp_container.get_object_content(hashkey2) == content2

    # Let's pack again, no locks
    temp_container.pack_all_loose(compress=compress)
    counts = temp_container.count_objects()
    # Now should be both packed
    assert counts["packed"] == 2

    # Check I can get the content
    assert temp_container.get_object_content(hashkey1) == content1
    assert temp_container.get_object_content(hashkey2) == content2


# Note that until when we want to support py3.5, we cannot specify the
# level as a keyword argument, as this was added only in python 3.6
@pytest.mark.parametrize("compression_algorithm", COMPRESSION_ALGORITHMS_TO_TEST)
@pytest.mark.parametrize("compress_packs", [True, False])
def test_sizes(
    temp_container, generate_random_data, compress_packs, compression_algorithm
):
    """Check that the information on size is reliable."""
    temp_container.init_container(
        clear=True, compression_algorithm=compression_algorithm
    )
    size_info = temp_container.get_total_size()
    assert size_info["total_size_packed"] == 0
    assert size_info["total_size_packed_on_disk"] == 0
    assert size_info["total_size_packfiles_on_disk"] == 0
    assert (
        size_info["total_size_packindexes_on_disk"]
        == temp_container._get_pack_index_path().stat().st_size
    )
    assert size_info["total_size_loose"] == 0

    data = generate_random_data()
    total_object_size = sum(len(value) for value in data.values())
    obj_md5s = _add_objects_loose_loop(temp_container, data)
    # Try to count size after retrieving, just to be sure
    assert (
        sum(
            len(content)
            for content in temp_container.get_objects_content(obj_md5s.keys()).values()
        )
        == total_object_size
    )

    # Check the size for loose objects
    size_info = temp_container.get_total_size()
    assert size_info["total_size_packed"] == 0
    assert size_info["total_size_packed_on_disk"] == 0
    assert size_info["total_size_packfiles_on_disk"] == 0
    assert (
        size_info["total_size_packindexes_on_disk"]
        == temp_container._get_pack_index_path().stat().st_size
    )
    assert size_info["total_size_loose"] == total_object_size

    # Pack without compression
    temp_container.pack_all_loose(compress=compress_packs)
    # Also reclaim space and remove loose objects
    temp_container.clean_storage()

    # Try to count size after retrieving, just to be sure
    assert (
        sum(
            len(content)
            for content in temp_container.get_objects_content(obj_md5s.keys()).values()
        )
        == total_object_size
    )

    if compress_packs:
        compressed_data = {}
        for key, val in data.items():
            compresser = utils.get_compressobj_instance(compression_algorithm)
            compressed = compresser.compress(val)
            compressed += compresser.flush()
            compressed_data[key] = compressed
        total_compressed_size = sum(len(value) for value in compressed_data.values())

        size_info = temp_container.get_total_size()
        assert size_info["total_size_packed"] == total_object_size
        assert size_info["total_size_packed_on_disk"] == total_compressed_size
        assert size_info["total_size_packfiles_on_disk"] == total_compressed_size
        assert (
            size_info["total_size_packindexes_on_disk"]
            == temp_container._get_pack_index_path().stat().st_size
        )
        assert size_info["total_size_loose"] == 0
    else:
        size_info = temp_container.get_total_size()
        assert size_info["total_size_packed"] == total_object_size
        assert size_info["total_size_packed_on_disk"] == total_object_size
        assert size_info["total_size_packfiles_on_disk"] == total_object_size
        assert (
            size_info["total_size_packindexes_on_disk"]
            == temp_container._get_pack_index_path().stat().st_size
        )
        assert size_info["total_size_loose"] == 0


def test_close_twice(temp_dir):
    """Tests if the container can be closed twice without raising an error."""
    temp_container = Container(temp_dir)
    try:
        temp_container.close()
    finally:
        temp_container.close()


def test_get_objects_stream_closes(temp_dir, generate_random_data):
    """Test that get_objects_stream_and_meta closes intermediate streams.

    I also check that at most one additional file is open at any given time.

    .. note: apparently, at least on my Mac, even if I forget to close a file, this is automatically closed
       when it goes out of scope - so I add also the test that, inside the loop, at most one more file is open.
       The final check seems to always pass even if I forget to do close some file.
    """
    current_process = psutil.Process()
    # We note the number of open of files, since Windows by default has some files open independent of the container
    begin_test_open_files = len(current_process.open_files())

    temp_container = Container(temp_dir)
    try:
        temp_container.init_container()

        data = generate_random_data()
        # Store
        obj_md5s = _add_objects_loose_loop(temp_container, data)

        # I get all objects first - this will actually internally go through the same function
        # `get_objects_stream_and_meta`, but I need to do it as this might open additional files,
        # namely the SQLite DB (possibly more than one file due to the fact it's open in WAL mode).
        # The following checks are still meaningful, I check that if I do it again I don't open more files.
        temp_container.get_objects_content(obj_md5s.keys())

        start_open_files = len(current_process.open_files())

        with temp_container.get_objects_stream_and_meta(
            obj_md5s.keys(), skip_if_missing=True
        ):
            # I don't use the triplets
            assert len(current_process.open_files()) <= start_open_files + 1

        # Check that at the end nothing is left open
        assert len(current_process.open_files()) == start_open_files

        with temp_container.get_objects_stream_and_meta(
            obj_md5s.keys(), skip_if_missing=True
        ) as triplets:
            # I loop over the triplets, but I don't do anything
            for _ in triplets:  # pylint: disable=not-an-iterable
                assert len(current_process.open_files()) <= start_open_files + 1

        # Check that at the end nothing is left open
        assert len(current_process.open_files()) == start_open_files

        # I actually read the content
        with temp_container.get_objects_stream_and_meta(
            obj_md5s.keys(), skip_if_missing=True
        ) as triplets:
            # I loop over the triplets, but I don't do anything
            for _, stream, _ in triplets:  # pylint: disable=not-an-iterable
                assert len(current_process.open_files()) <= start_open_files + 1
                stream.read()

        # Check that at the end nothing is left open
        assert len(current_process.open_files()) == start_open_files

        ##############################
        ##### Same test after packing
        ##############################
        temp_container.pack_all_loose()
        # I get all objects first, again - this is because it might have closed the DB files while packing
        temp_container.get_objects_content(obj_md5s.keys())
        # I now update the count
        start_open_files = len(current_process.open_files())

        with temp_container.get_objects_stream_and_meta(obj_md5s.keys()):
            # I don't use the triplets
            assert len(current_process.open_files()) <= start_open_files + 1

        # Check that at the end nothing is left open
        assert len(current_process.open_files()) == start_open_files

        with temp_container.get_objects_stream_and_meta(obj_md5s.keys()) as triplets:
            # I loop over the triplets, but I don't do anything
            for _ in triplets:  # pylint: disable=not-an-iterable
                assert len(current_process.open_files()) <= start_open_files + 1

        # Check that at the end nothing is left open
        assert len(current_process.open_files()) == start_open_files

        # I actually read the content
        with temp_container.get_objects_stream_and_meta(
            obj_md5s.keys(), skip_if_missing=True
        ) as triplets:
            # I loop over the triplets, but I don't do anything
            for _, stream, _ in triplets:  # pylint: disable=not-an-iterable
                assert len(current_process.open_files()) <= start_open_files + 1
                stream.read()
        # Check that at the end nothing is left open
        assert len(current_process.open_files()) == start_open_files

        ##############################
        ##### Same test after adding at least one loose object
        ##############################
        new_object_content = (
            b"1" * 20000
        )  # This should be long enough not to collide with the generated random data
        new_hashkey = temp_container.add_object(new_object_content)
        obj_md5s[new_hashkey] = new_object_content

        # I get all objects first, again - this is because it might have closed the DB files
        temp_container.get_objects_content(obj_md5s.keys())
        # I now update the count
        start_open_files = len(current_process.open_files())

        with temp_container.get_objects_stream_and_meta(obj_md5s.keys()):
            # I don't use the triplets
            assert len(current_process.open_files()) <= start_open_files + 1

        # Check that at the end nothing is left open
        assert len(current_process.open_files()) == start_open_files

        with temp_container.get_objects_stream_and_meta(obj_md5s.keys()) as triplets:
            # I loop over the triplets, but I don't do anything
            for _ in triplets:  # pylint: disable=not-an-iterable
                assert len(current_process.open_files()) <= start_open_files + 1

        # Check that at the end nothing is left open
        assert len(current_process.open_files()) == start_open_files

        # I actually read the content
        with temp_container.get_objects_stream_and_meta(
            obj_md5s.keys(), skip_if_missing=True
        ) as triplets:
            # I loop over the triplets, but I don't do anything
            for _, stream, _ in triplets:  # pylint: disable=not-an-iterable
                assert len(current_process.open_files()) <= start_open_files + 1
                stream.read()
        # Check that at the end nothing is left open
        assert len(current_process.open_files()) == start_open_files

    finally:
        # Check if it goes back to 0
        temp_container.close()
        assert len(current_process.open_files()) == begin_test_open_files


def test_deletion_closes_file_descriptors(temp_dir, generate_random_data):
    """Test if deletion of container closes correctly open file descriptors."""

    current_process = psutil.Process()
    # We note the number of open of files, since Windows by default has some files open independent of the container
    begin_test_open_files = len(current_process.open_files())

    # Open files
    temp_container = Container(temp_dir)
    try:
        temp_container.init_container(clear=True)
        # For Linux to open files it is required to reading from container, on macOS
        # the initialization of container is enough
        data = generate_random_data()
        obj_md5s = _add_objects_loose_loop(temp_container, data)
        _ = temp_container.get_objects_content(obj_md5s.keys())

        # Checks if initalisation actually opens files
        assert 0 < len(
            current_process.open_files()
        ), "No files have been opened during initalisation"

        # Checks if deleting the container will close the files
        del temp_container

        assert begin_test_open_files == len(current_process.open_files())
    finally:
        if "temp_container" in locals():
            locals()["temp_container"].close()


def test_get_objects_meta_doesnt_open(
    temp_container, generate_random_data
):  # pylint: disable=invalid-name
    """Test that get_objects_meta does not open any file."""
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

    for _, _ in temp_container.get_objects_meta(obj_md5s.keys()):
        # No new files should be open while iterating
        assert len(current_process.open_files()) == start_open_files

    # Check that at the end nothing is left open
    assert len(current_process.open_files()) == start_open_files

    ##############################
    ##### Same test after packing
    ##############################
    temp_container.pack_all_loose()

    # I get all objects first, again - this is because it might have closed the DB files while packing
    temp_container.get_objects_content(obj_md5s.keys())
    # I now update the count
    start_open_files = len(current_process.open_files())

    for _, _ in temp_container.get_objects_meta(obj_md5s.keys()):
        # No new files should be open while iterating
        assert len(current_process.open_files()) == start_open_files

    # Check that at the end nothing is left open
    assert len(current_process.open_files()) == start_open_files

    ##############################
    ##### Same test after adding at least one loose object
    ##############################
    new_object_content = (
        b"1" * 20000
    )  # This should be long enough not to collide with the generated random data
    new_hashkey = temp_container.add_object(new_object_content)
    obj_md5s[new_hashkey] = new_object_content

    # I get all objects first, again - this is because it might have closed the DB files
    temp_container.get_objects_content(obj_md5s.keys())
    # I now update the count
    start_open_files = len(current_process.open_files())

    for _, _ in temp_container.get_objects_meta(obj_md5s.keys()):
        # No new files should be open while iterating
        assert len(current_process.open_files()) == start_open_files

    # Check that at the end nothing is left open
    assert len(current_process.open_files()) == start_open_files


# Note that until when we want to support py3.5, we cannot specify the
# level as a keyword argument, as this was added only in python 3.6
@pytest.mark.parametrize("compression_algorithm", COMPRESSION_ALGORITHMS_TO_TEST)
@pytest.mark.parametrize("compress", [True, False])
@pytest.mark.parametrize("skip_if_missing", [True, False])
def test_stream_meta(  # pylint: disable=too-many-locals
    temp_container, compress, skip_if_missing, compression_algorithm
):
    """Validate the meta dictionary returned by the get_objects_stream_and_meta and get_objects_meta."""
    temp_container.init_container(
        clear=True, compression_algorithm=compression_algorithm
    )
    # This is the list of all known meta keys.
    # I do also an explicit check that all and only these are present
    # This is implicit since I will later also compare the exact dictionaries and not only their keys,
    # but I put this here to make sure in the future, if I change the interface and adapt the keys, I don't break
    # this guarantee if I forget to adapt the test.
    known_meta_keys = [
        "type",
        "size",
        "pack_id",
        "pack_compressed",
        "pack_offset",
        "pack_length",
    ]

    content_packed = b"sffssdf383939"
    content_loose = b"v9fpaM"
    hashkey_packed = temp_container.add_objects_to_pack(
        [content_packed], compress=compress
    )[0]
    hashkey_loose = temp_container.add_object(content_loose)
    hashkey_missing = "unknown"
    compresser = utils.get_compressobj_instance(compression_algorithm)
    content_packed_compressed = compresser.compress(content_packed)
    content_packed_compressed += compresser.flush()
    object_pack_length = (
        len(content_packed) if not compress else len(content_packed_compressed)
    )

    expected_skip_missing_true = {
        hashkey_packed: {
            "content": content_packed,
            "meta": ObjectMeta(
                type=ObjectType.PACKED,
                size=len(content_packed),
                pack_id=0,  # First pack, it's a new container
                pack_compressed=compress,
                pack_offset=0,  # Only one object in the pack, must start from zero
                pack_length=object_pack_length,
            ),
        },
        hashkey_loose: {
            "content": content_loose,
            "meta": ObjectMeta(
                type=ObjectType.LOOSE,
                size=len(content_loose),
                pack_id=None,
                pack_compressed=None,
                pack_offset=None,
                pack_length=None,
            ),
        },
    }

    expected_skip_missing_false = expected_skip_missing_true.copy()
    expected_skip_missing_false[hashkey_missing] = {
        "content": None,
        "meta": ObjectMeta(
            type=ObjectType.MISSING,
            size=None,
            pack_id=None,
            pack_compressed=None,
            pack_offset=None,
            pack_length=None,
        ),
    }

    check_dict = {}
    with temp_container.get_objects_stream_and_meta(
        [hashkey_packed, hashkey_loose, hashkey_missing],
        skip_if_missing=skip_if_missing,
    ) as triplets:
        # I loop over the triplets, but I don't do anything
        for hashkey, stream, meta in triplets:
            retdict = {"meta": meta}
            # In any case I should return all these meta, and no more
            assert set(dataclasses.asdict(meta).keys()) == set(known_meta_keys)
            if stream is None:
                retdict["content"] = None
            else:
                retdict["content"] = stream.read()
            check_dict[hashkey] = retdict

    if skip_if_missing:
        assert check_dict == expected_skip_missing_true
    else:
        assert check_dict == expected_skip_missing_false

    # Do the same without opening the streams
    check_dict = {}
    for hashkey, meta in temp_container.get_objects_meta(
        [hashkey_packed, hashkey_loose, hashkey_missing],
        skip_if_missing=skip_if_missing,
    ):
        check_dict[hashkey] = meta

    if skip_if_missing:
        assert check_dict == {
            k: v["meta"] for k, v in expected_skip_missing_true.items()
        }
    else:
        assert check_dict == {
            k: v["meta"] for k, v in expected_skip_missing_false.items()
        }


# Note that until when we want to support py3.5, we cannot specify the
# level as a keyword argument, as this was added only in python 3.6
@pytest.mark.parametrize("compression_algorithm", COMPRESSION_ALGORITHMS_TO_TEST)
@pytest.mark.parametrize("compress", [True, False])
def test_stream_meta_single(temp_container, compress, compression_algorithm):
    """Validate the meta dictionary returned by the single-object methods.

    (i.e., get_object_stream_and_meta and get_object_meta)."""
    temp_container.init_container(
        clear=True, compression_algorithm=compression_algorithm
    )
    # This is the list of all known meta keys.
    # I do also an explicit check that all and only these are present
    # This is implicit since I will later also compare the exact dictionaries and not only their keys,
    # but I put this here to make sure in the future, if I change the interface and adapt the keys, I don't break
    # this guarantee if I forget to adapt the test.
    known_meta_keys = [
        "type",
        "size",
        "pack_id",
        "pack_compressed",
        "pack_offset",
        "pack_length",
    ]

    content_packed = b"sffssdf383939"
    content_loose = b"v9fpaM"
    hashkey_packed = temp_container.add_objects_to_pack(
        [content_packed], compress=compress
    )[0]
    hashkey_loose = temp_container.add_object(content_loose)
    hashkey_missing = "unknown"
    compresser = utils.get_compressobj_instance(compression_algorithm)
    content_packed_compressed = compresser.compress(content_packed)
    content_packed_compressed += compresser.flush()
    object_pack_length = (
        len(content_packed) if not compress else len(content_packed_compressed)
    )

    expected_skip_missing_true = {
        hashkey_packed: {
            "content": content_packed,
            "meta": ObjectMeta(
                type=ObjectType.PACKED,
                size=len(content_packed),
                pack_id=0,  # First pack, it's a new container
                pack_compressed=compress,
                pack_offset=0,  # Only one object in the pack, must start from zero
                pack_length=object_pack_length,
            ),
        },
        hashkey_loose: {
            "content": content_loose,
            "meta": ObjectMeta(
                type=ObjectType.LOOSE,
                size=len(content_loose),
                pack_id=None,
                pack_compressed=None,
                pack_offset=None,
                pack_length=None,
            ),
        },
    }

    check_dict = {}

    for hashkey in [hashkey_packed, hashkey_loose]:
        with temp_container.get_object_stream_and_meta(hashkey) as (stream, meta):
            retdict = {"meta": meta}
            # In any case I should return all these meta, and no more
            assert set(dataclasses.asdict(meta).keys()) == set(known_meta_keys)
            if stream is None:
                retdict["content"] = None
            else:
                retdict["content"] = stream.read()
            check_dict[hashkey] = retdict
    assert check_dict == expected_skip_missing_true

    with pytest.raises(exc.NotExistent):
        with temp_container.get_object_stream_and_meta(hashkey_missing) as (
            stream,
            meta,
        ):
            pass

    # Do the same without opening the streams
    for hashkey in [hashkey_packed, hashkey_loose]:
        check_dict[hashkey] = temp_container.get_object_meta(hashkey)

    assert check_dict == {k: v["meta"] for k, v in expected_skip_missing_true.items()}

    with pytest.raises(exc.NotExistent):
        meta = temp_container.get_object_meta(hashkey_missing)


def test_length_get_objects(temp_container):
    """Check that the iterator to get the object streams does not perform unnecessary operations.

    This is mostly to check for efficiency and that I don't iterate by mistake multiple times on the same object.
    """
    # Note: I created different data, so these 4 hashkeys will always be different
    data = [b"1", b"2", b"3", b"4"]
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
    unknown_hashkeys = ["unk1", "unk2"]
    partial_hashkeys = list(data_dict)[:2]
    hashkeys = partial_hashkeys + partial_hashkeys + unknown_hashkeys + unknown_hashkeys
    iterated_hashkeys = []
    with temp_container.get_objects_stream_and_meta(
        hashkeys=hashkeys, skip_if_missing=False
    ) as triplets:
        for obj_hashkey, _, _ in triplets:
            iterated_hashkeys.append(obj_hashkey)
    # I should iterate on them ONLY ONCE
    assert sorted(iterated_hashkeys) == sorted(set(hashkeys))

    # Test 4B: I pass half the known hashkeys, twice, PLUS SOME UNKNOWN HASHKEY, also twice
    # If skip_if_missing=True, I should iterate ONLY on the known one, BUT ONLY ONCE
    unknown_hashkeys = ["unk1", "unk2"]
    partial_hashkeys = list(data_dict)[:2]
    hashkeys = partial_hashkeys + partial_hashkeys + unknown_hashkeys + unknown_hashkeys
    iterated_hashkeys = []
    with temp_container.get_objects_stream_and_meta(
        hashkeys=hashkeys, skip_if_missing=True
    ) as triplets:
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
    num_objects = temp_container._IN_SQL_MAX_LENGTH * 10 + 3
    # Generate a long list of objects with *different* data, so they are not deduplicated
    data = [str(i).encode("ascii") for i in range(num_objects)]

    # The container is empty: let's check that asking for unknown objects work
    # NOTE: I just generate some random 'unknown' hash key
    res = temp_container.get_objects_content([f"unk{i}" for i in range(num_objects)])
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
    direct_pack_data = [f"P{i}".encode("ascii") for i in range(num_objects)]
    direct_pack_hashkeys = temp_container.add_objects_to_pack(direct_pack_data)

    # Finally, ask back everything and check
    expected_values = dict(zip(hashkeys, data))
    expected_values.update(dict(zip(direct_pack_hashkeys, direct_pack_data)))
    values = temp_container.get_objects_content(hashkeys + direct_pack_hashkeys)
    assert values == expected_values


@pytest.mark.parametrize("compress", [True, False])
def test_simulate_concurrent_packing(
    temp_container, compress
):  # pylint: disable=invalid-name
    """Simulate race conditions while reading and packing."""
    content = b"abc"
    hashkey = temp_container.add_object(content)

    loose_dir_path = pathlib.Path(temp_container._get_loose_folder())
    with temp_container.get_object_stream(hashkey) as fhandle:
        fpath = pathlib.Path(fhandle.name)
        # Check that this is a loose object (i.e. that it is in the loose folder)
        assert loose_dir_path in fpath.parents
        assert fhandle.read(1) == b"a"
        temp_container.pack_all_loose(compress=compress)
        assert fhandle.read() == b"bc"

        # Remove loose files
        temp_container.clean_storage()

    # On Windows, the loose file will still be there because I cannot delete an open file.
    # Still, this is a valid situation and I should be able to get the correct content anyway
    # On POSIX, it will already have been deleted. Anyway, this is not something we really need to test.

    # The following line should be read from the pack file. Anyway, the important thing to test
    # is that the content is properly returned.
    with temp_container.get_object_stream(hashkey) as fhandle:
        assert fhandle.read() == b"abc"

    # After a second cleaning of the storage, the loose file *must* have been removed on all OSs
    temp_container.clean_storage()
    assert not fpath.exists()


@pytest.mark.parametrize("do_vacuum", [True, False])
@pytest.mark.parametrize("compress", [True, False])
def test_simulate_concurrent_packing_multiple(
    temp_container, compress, do_vacuum
):  # pylint: disable=invalid-name
    """Simulate race conditions while reading and packing."""
    content1 = b"abc"
    content2 = b"def"
    hashkey1 = temp_container.add_object(content1)
    hashkey2 = temp_container.add_object(content2)
    data = {hashkey1: content1, hashkey2: content2}

    loose_dir_path = pathlib.Path(temp_container._get_loose_folder())
    with temp_container.get_objects_stream_and_meta([hashkey1, hashkey2]) as triplets:
        counter = 0

        for obj_hashkey, stream, _ in triplets:
            if counter == 0:
                # In the first step, I always pack the rest
                fpath = pathlib.Path(stream.name)
                # Check that this is a loose object (i.e. that it is in the loose folder)
                assert loose_dir_path in fpath.parents
                if obj_hashkey == hashkey1:
                    assert stream.read(1) == b"a"
                    temp_container.pack_all_loose(compress=compress)
                    # Remove loose files
                    temp_container.clean_storage(vacuum=do_vacuum)
                    assert stream.read() == b"bc"
                elif obj_hashkey == hashkey2:
                    assert stream.read(1) == b"d"
                    temp_container.pack_all_loose(compress=compress)
                    # Remove loose files
                    temp_container.clean_storage(vacuum=do_vacuum)
                    assert stream.read() == b"ef"
                else:
                    # Should not happen!
                    raise ValueError(f"Unknown hash key {obj_hashkey}")
            elif counter == 1:
                # This should be the other object
                # This was loose when get_objects_stream_and_meta was called, but was packed in the meantime
                # I should still be able to get it correctly
                assert data[obj_hashkey] == stream.read()
            else:
                # Should not happen!
                raise ValueError("There should be only two objects!")
            counter += 1

    # On Windows, the loose file might still be there because I cannot delete an open file
    # Still, this is a valid situation and I should be able to get the correct content anyway
    # The following line should be read from the pack file. Anyway, the important thing to test
    # is that the content is properly returned
    assert data == temp_container.get_objects_content([hashkey1, hashkey2])

    # After a second cleaning of the storage, the loose file *must* have been removed
    temp_container.clean_storage(vacuum=do_vacuum)
    assert not fpath.exists()


def test_simulate_concurrent_packing_multiple_many(
    temp_container,
):  # pylint: disable=invalid-name
    """Simulate race conditions while reading and packing, with more than objects _MAX_CHUNK_ITERATE_LENGTH changing."""
    expected = {}

    # I put at least one object already packed
    preliminary_content = b"AAA"
    preliminary_hashkey = temp_container.add_object(preliminary_content)
    temp_container.pack_all_loose()
    temp_container.clean_storage()
    expected[preliminary_hashkey] = preliminary_content

    for idx in range(temp_container._MAX_CHUNK_ITERATE_LENGTH + 10):
        content = f"{idx}".encode("ascii")
        expected[temp_container.add_object(content)] = content

    retrieved = {}
    first = True
    with temp_container.get_objects_stream_and_meta(expected.keys()) as triplets:
        for obj_hashkey, stream, meta in triplets:
            retrieved[obj_hashkey] = stream.read()
            if first:
                # I should have found only one packed object (preliminary_content).
                assert obj_hashkey == preliminary_hashkey
                assert meta["type"] == ObjectType.PACKED
                # I will not look for the loose until I exhaust the packed objects.
                # In the meantime, therefore, I pack all the rest, and I clean the storage:
                # this will trigger the fallback logic to check again if there are
                # objects that have been packed in the meantime.
                temp_container.pack_all_loose()
                temp_container.clean_storage()
                first = False

    assert expected == retrieved


@pytest.mark.parametrize("compress", [True, False])
def test_simulate_concurrent_packing_multiple_meta_only(
    temp_container, compress
):  # pylint: disable=invalid-name
    """Simulate race conditions while reading and packing (as earlier function, but no streams)."""
    content1 = b"abc"
    content2 = b"def"
    hashkey1 = temp_container.add_object(content1)
    hashkey2 = temp_container.add_object(content2)

    counter = 0
    for _, meta in temp_container.get_objects_meta([hashkey1, hashkey2]):
        if counter == 0:
            # In the first step, I always pack the rest

            # Check that this is a loose object
            assert meta["type"] == ObjectType.LOOSE
            temp_container.pack_all_loose(compress=compress)
            # Remove loose files
            temp_container.clean_storage()
        elif counter == 1:
            # This should be the other object
            # This was loose when get_objects_stream_and_meta was called, but was packed in the meantime
            # I should still be able to get it correctly and discover it's packed
            assert meta["type"] == ObjectType.PACKED
        else:
            # Should not happen!
            raise ValueError("There should be only two objects!")
        counter += 1


@pytest.mark.parametrize("compress", [True, False])
def test_simulate_concurrent_packing_multiple_existing_pack(
    temp_container, compress
):  # pylint: disable=invalid-name
    """Simulate race conditions while reading and packing.

    In addition, this does it when the first file is not loose, but it is already packed.
    This triggers some lines of code to close the packs if already open, increasing test coverage
    and implicitly testing that open file leaks are avoided.
    """
    content1 = b"abc"
    content2 = b"def"

    hashkey1 = temp_container.add_objects_to_pack([content1], compress=compress)[0]
    hashkey2 = temp_container.add_object(content2)

    loosepath2 = temp_container._get_loose_path_from_hashkey(hashkey2)
    # Object 2 is stored loose
    assert loosepath2.exists()

    with temp_container.get_objects_stream_and_meta([hashkey1, hashkey2]) as triplets:
        counter = 0

        for obj_hashkey, stream, _ in triplets:
            if counter == 0:
                # The first one should be the one that is aleady packed
                assert obj_hashkey == hashkey1

                # Pack the other object during the loop
                temp_container.pack_all_loose(compress=compress)
                # Also, delete the loose files
                temp_container.clean_storage()
                assert stream.read() == content1
            elif counter == 1:
                # This should be the second object, packed during the first iteration
                assert stream.read() == content2
            else:
                # Should not happen!
                raise ValueError("There should be only two objects!")
            counter += 1

    # Object #2 was not open during the packing operation. Theferore, it should be deleted during packing
    # on *all* filesystems, and here it should not exist anymore
    assert not loosepath2.exists()


def test_has_objects(temp_container):
    """Test the ``Container.has_objects`` method."""
    unknown_hashkey = "unk"

    # Create an object and test that `has_object` recognizes it
    hashkey_pack1 = temp_container.add_object(b"1")
    hashkey_pack2 = temp_container.add_object(b"2")
    assert temp_container.has_objects([hashkey_pack1, hashkey_pack2]) == [True, True]
    assert temp_container.has_objects(
        [hashkey_pack2, unknown_hashkey, hashkey_pack1]
    ) == [True, False, True]

    # Verify that it still works after packing the object
    temp_container.pack_all_loose()
    assert temp_container.has_objects([hashkey_pack1, hashkey_pack2]) == [True, True]
    assert temp_container.has_objects(
        [hashkey_pack2, unknown_hashkey, hashkey_pack1]
    ) == [True, False, True]

    # Add a few more loose objects, and check that all works also with mixed loose and packed objects
    hashkey_loose1 = temp_container.add_object(b"3")
    hashkey_loose2 = temp_container.add_object(b"4")
    assert temp_container.has_objects([hashkey_pack1, hashkey_pack2]) == [True, True]
    assert temp_container.has_objects(
        [hashkey_pack2, unknown_hashkey, hashkey_pack1]
    ) == [True, False, True]
    assert temp_container.has_objects([hashkey_loose1, hashkey_loose2]) == [True, True]
    assert temp_container.has_objects(
        [hashkey_loose2, unknown_hashkey, hashkey_loose1]
    ) == [True, False, True]
    assert temp_container.has_objects(
        [hashkey_loose2, hashkey_pack1, unknown_hashkey, hashkey_loose1, hashkey_pack2]
    ) == [True, True, False, True, True]


def test_has_object(temp_container):
    """Test the ``Container.has_object`` method."""
    assert not temp_container.has_object("unk")

    # Create an object and test that `has_object` recognizes it
    hashkey = temp_container.add_object(b"1")
    assert temp_container.has_object(hashkey)

    # Verify that it still works after packing the object
    temp_container.pack_all_loose()
    assert temp_container.has_object(hashkey)


@pytest.mark.parametrize("compress", [True, False])
def test_seek_tell(temp_container, compress):
    """Test the tell and seek methods of returned objects."""
    content = b"0123456789"
    hashkey = temp_container.add_object(content)

    seek_pos = 3
    read_length = 4

    # Check that the seek and tell method work for loose objects
    with temp_container.get_object_stream_and_meta(hashkey) as (fhandle, meta):
        assert meta["type"] == ObjectType.LOOSE
        fhandle.seek(seek_pos)
        assert fhandle.tell() == seek_pos
        read_data = fhandle.read(read_length)
        assert fhandle.tell() == seek_pos + read_length
        assert read_data == content[seek_pos : seek_pos + read_length]

    # Pack the object, and remove old loose objects
    temp_container.pack_all_loose(compress=compress)

    # Check that the seek and tell method work for packed objects (either compressed or not)
    with temp_container.get_object_stream_and_meta(hashkey) as (fhandle, meta):
        assert meta["type"] == ObjectType.PACKED
        assert meta["pack_compressed"] == compress
        fhandle.seek(seek_pos)
        assert fhandle.tell() == seek_pos
        read_data = fhandle.read(read_length)
        assert fhandle.tell() == seek_pos + read_length
        assert read_data == content[seek_pos : seek_pos + read_length]


def test_get_objects_meta_to_dict(temp_container):
    """Check that you can just wrap `get_objects_meta` into a dict."""
    expected_sizes = {}
    for content in [b"a", b"aa", b"aaaa"]:  # Data of diffenent length
        hashkey = temp_container.add_object(content)
        expected_sizes[hashkey] = len(content)

    # Check that I can convert to dict
    hashkeys = list(expected_sizes)
    meta_dict = dict(temp_container.get_objects_meta(hashkeys))
    # Check tha the dict contains the right data
    assert all(meta["type"] == ObjectType.LOOSE for meta in meta_dict.values())

    assert expected_sizes == {
        hashkey: meta["size"] for hashkey, meta in meta_dict.items()
    }


@pytest.mark.parametrize("loose_prefix_len", [0, 2, 3])
def test_list_all_objects(temp_dir, loose_prefix_len):
    """Test listing all objects in the container."""
    temp_container = Container(temp_dir)
    temp_container.init_container(clear=True, loose_prefix_len=loose_prefix_len)

    num_files = 1000

    data_content = [f"{i}".encode("ascii") for i in range(num_files)]
    hashkeys = []
    for content in data_content:
        hashkeys.append(temp_container.add_object(content))

    # Check when all objects are loose
    retval = list(temp_container.list_all_objects())
    # Check that they are the same except for the order
    assert sorted(hashkeys) == sorted(retval)

    temp_container.pack_all_loose()
    assert temp_container.count_objects()["packed"] > 0

    # Pack all objects, loose objects will remain in place
    # Check that all works and that I don't get duplicates
    retval = list(temp_container.list_all_objects())
    # Check that they are the same except for the order
    assert sorted(hashkeys) == sorted(retval)

    # Clean up the loose objects
    temp_container.clean_storage()
    # Check that all works and that I don't loose objects
    retval = list(temp_container.list_all_objects())
    # Check that they are the same except for the order
    assert sorted(hashkeys) == sorted(retval)

    # New data, different values
    data_content2 = [f"second-{i}".encode("ascii") for i in range(num_files)]
    hashkeys2 = []
    for content in data_content2:
        hashkeys2.append(temp_container.add_object(content))

    # Check that I see both loose and packed objects
    retval = list(temp_container.list_all_objects())
    # Check that they are the same except for the order
    assert sorted(hashkeys + hashkeys2) == sorted(retval)

    # Add again packed objects
    hashkeys3 = []
    for content in data_content:
        hashkeys3.append(temp_container.add_object(content))
    # This should have given us the same hash keys (just checking to be sure)
    assert hashkeys == hashkeys3

    # Even in this case, where I might have create duplicate (loose and packed) objects,
    # I shouldn't get more results or duplicates
    retval = list(temp_container.list_all_objects())
    # Check that they are the same except for the order
    assert sorted(hashkeys + hashkeys2) == sorted(retval)

    temp_container.close()


@pytest.mark.parametrize("loose_prefix_len", [0, 2, 3])
def test_list_all_objects_extraneous(
    temp_dir, loose_prefix_len
):  # pylint: disable=invalid-name
    """Test `list_all_objects` and check that files that do not match the format of a hash key are ignored."""
    temp_container = Container(temp_dir)
    temp_container.init_container(clear=True, loose_prefix_len=loose_prefix_len)

    num_files = 1000

    data_content = [f"{i}".encode("ascii") for i in range(num_files)]
    hashkeys = []
    for content in data_content:
        hashkeys.append(temp_container.add_object(content))

    # Check when all objects are loose
    retval = list(temp_container.list_all_objects())
    assert sorted(hashkeys) == sorted(retval)

    # I now add extraneous files that do not contain hex strings or have the wrong length
    os.mkdir(temp_container._get_loose_folder() / "INVALID_NAME")

    if loose_prefix_len != 0:
        prefix = "0" * 2 * loose_prefix_len
        suffix = "0" * 10

        # This is not really needed (actually, in the future we might also want to check the length)
        # but in that case we want to adapt the test to have a valid suffix: what I want to test is
        # that even if the concatenation is valid, any first-level folder of wrong length is skipped
        assert temp_container._is_valid_hashkey(prefix + suffix)

        # Creating a folder with valid characters, but wrong length: the content should be ignored
        invalid_first_level = temp_container._get_loose_folder() / prefix
        os.mkdir(invalid_first_level)
        # Create an empty file
        with open(invalid_first_level / suffix, "wb"):
            pass

        # creating now a valid first_level folder (if not present already), and an invalid name inside it
        first_level_subfolder = temp_container._get_loose_folder() / (
            "0" * loose_prefix_len
        )
        try:
            # Creating if it does not exist - this is a valid name
            os.mkdir(first_level_subfolder)
        except FileExistsError:
            pass
        with open(first_level_subfolder / "INVALID_NAME", "wb"):
            pass

    # We list again: all invalid objects should just be ignored
    retval = list(temp_container.list_all_objects())
    assert sorted(hashkeys) == sorted(retval)

    # Closing (needed in Windows)
    temp_container.close()


# With the default memory of 100MB, we always use the cache and flush at the end;
# with a memory of 9, we put the first object in the cache (6 bytes) and the second
# will need to flush the cache. With a single byte, all objects don't fit the cache so
# we need to copy directly from stream to stream, without going via the cache.
@pytest.mark.parametrize("target_memory_bytes", [1, 9, 100 * 1024 * 1024])
@pytest.mark.parametrize("compress_dest", [True, False])
@pytest.mark.parametrize("compress_source", [True, False])
# Test both the same hash and another one
@pytest.mark.parametrize("other_container_hash_type", ["sha256", "sha1"])
def test_import_to_pack(
    temp_container,
    compress_source,
    compress_dest,
    target_memory_bytes,
    other_container_hash_type,
):
    """Test the functionality to import from another container."""
    obj1 = b"111111"
    obj2 = b"222222"
    obj3 = b"333332"

    with tempfile.TemporaryDirectory() as tmpdir:
        other_container = Container(tmpdir)
        # Use the same hash type
        other_container.init_container(clear=True, hash_type=other_container_hash_type)

        hashkey1 = temp_container.add_object(obj1)
        hashkey2, hashkey3 = temp_container.add_objects_to_pack(
            [obj2, obj3], compress=compress_source
        )

        # Initial state
        assert temp_container.count_objects()["loose"] == 1
        assert temp_container.count_objects()["packed"] == 2
        assert other_container.count_objects()["loose"] == 0
        assert other_container.count_objects()["packed"] == 0

        # Put only two objects
        old_new_mapping = other_container.import_objects(
            [hashkey1, hashkey2],
            temp_container,
            compress=compress_dest,
            target_memory_bytes=target_memory_bytes,
        )
        # Two objects should appear
        assert other_container.count_objects()["loose"] == 0
        assert other_container.count_objects()["packed"] == 2

        # Check the content, and that they are all the objects that exist
        assert other_container.get_object_content(old_new_mapping[hashkey1]) == obj1
        assert other_container.get_object_content(old_new_mapping[hashkey2]) == obj2
        assert set(other_container.list_all_objects()) == {
            old_new_mapping[hashkey1],
            old_new_mapping[hashkey2],
        }

        # Add two more, one of which is already in the destination
        old_new_mapping.update(
            other_container.import_objects(
                [hashkey2, hashkey3],
                temp_container,
                compress=compress_dest,
                target_memory_bytes=target_memory_bytes,
            )
        )
        # All three objects should be there, no duplicates
        assert other_container.count_objects()["loose"] == 0
        assert other_container.count_objects()["packed"] == 3
        assert set(other_container.list_all_objects()) == {
            old_new_mapping[hashkey1],
            old_new_mapping[hashkey2],
            old_new_mapping[hashkey3],
        }

        assert other_container.get_object_content(old_new_mapping[hashkey1]) == obj1
        assert other_container.get_object_content(old_new_mapping[hashkey2]) == obj2
        assert other_container.get_object_content(old_new_mapping[hashkey3]) == obj3

        old_hashkeys, new_hashkeys = zip(*old_new_mapping.items())
        if other_container_hash_type == temp_container.hash_type:
            # Since we are using the same hash algorithm, the hashes ashould be the same!
            assert old_hashkeys == new_hashkeys

        # close before exiting the context manager, so files are closed.
        other_container.close()


@pytest.mark.parametrize("compress", [True, False])
def test_validate(temp_container, compress):
    """Test the validation function."""
    obj1 = b"324r3w"  # Will be packed (from loose)
    obj2 = b"jklf2wv"  # Will be loose
    obj3 = b"9z0vx0"  # Will be stored directly packed
    obj4 = b"jkljkljlk"  # Will be stored directly packed

    # An empy container should be valid
    issues = temp_container.validate()
    assert issues.is_valid()

    temp_container.add_object(obj1)
    temp_container.pack_all_loose(compress=compress)
    temp_container.add_object(obj2)
    temp_container.add_objects_to_pack([obj3], compress=compress)

    # Should not raise
    issues = temp_container.validate()
    assert issues.is_valid()

    # Add the same object
    temp_container.add_objects_to_pack([obj3])
    issues = temp_container.validate()
    assert issues.is_valid()

    # Add a fourth object directly to packs
    temp_container.add_objects_to_pack([obj4], compress=compress)
    temp_container.validate()
    issues = temp_container.validate()
    assert issues.is_valid()


def test_validate_corrupt_loose(temp_container):
    """Test the validation function."""
    obj1 = b"jklsfjsdlkdj"

    hashkey1 = temp_container.add_object(obj1)

    # No errors yet
    temp_container.validate()
    issues = temp_container.validate()
    assert issues.is_valid()

    # Corrupt the object
    with open(temp_container._get_loose_path_from_hashkey(hashkey1), "wb") as fhandle:
        fhandle.write(b"CORRUPT")

    # I don't use the dataclass .is_valid() method of ValidationIssues because I want to
    # pop the error and check that there are no other issues but only the one I'm aware of
    errors = dataclasses.asdict(temp_container.validate())
    problems = errors.pop("invalid_hashes_loose")

    assert set(problems) == {hashkey1}

    # There shouldn't be any other error
    assert not any(errors.values())


def test_validate_corrupt_packed(temp_container):
    """Test the validation function."""
    obj1 = b"jklsfjsdlkdj"

    hashkey1 = temp_container.add_objects_to_pack([obj1], compress=False)[0]
    meta = temp_container.get_object_meta(hashkey1)
    assert meta["type"] == ObjectType.PACKED

    # No errors yet
    temp_container.validate()
    issues = temp_container.validate()
    assert issues.is_valid()

    # Corrupt the object
    with open(
        temp_container._get_pack_path_from_pack_id(str(meta["pack_id"])), "wb"
    ) as fhandle:
        fhandle.write(b"CORRU890890890809PT")

    # I don't use the dataclass .is_valid() method of ValidationIssues because I want to
    # pop the error and check that there are no other issues but only the one I'm aware of
    errors = dataclasses.asdict(temp_container.validate())
    problems = errors.pop("invalid_hashes_packed")

    assert set(problems) == {hashkey1}

    # There shouldn't be any other error
    assert not any(errors.values())


def test_validate_overlapping_packed(temp_container):  # pylint: disable=invalid-name
    """Test the validation function."""
    # Both of length 10
    obj1 = b"0123456789"
    obj2 = b"a123456789"

    hashkey1, hashkey2 = temp_container.add_objects_to_pack([obj1, obj2])
    meta1 = temp_container.get_object_meta(hashkey1)
    meta2 = temp_container.get_object_meta(hashkey2)
    assert meta1["type"] == ObjectType.PACKED
    assert meta2["type"] == ObjectType.PACKED

    # Hashkey of the object stored later in the pack
    hashkey_second = (
        hashkey2 if meta1["pack_offset"] < meta2["pack_offset"] else hashkey1
    )

    # No errors yet
    temp_container.validate()
    issues = temp_container.validate()
    assert issues.is_valid()

    # Change the offset of the second object so that it's overlapping
    temp_container._get_operation_session().query(database.Obj).filter(
        database.Obj.hashkey == hashkey_second
    ).update({database.Obj.offset: database.Obj.offset - 1})

    errors = dataclasses.asdict(temp_container.validate())
    problems = errors.pop("overlapping_packed")

    assert set(problems) == {hashkey_second}

    # There are also other errors for the way I changed the set - I don't check those


def test_validate_corrupt_packed_size(temp_container):  # pylint: disable=invalid-name
    """Test the validation function."""
    obj1 = b"jklsfjsdlkdj"

    hashkey1 = temp_container.add_objects_to_pack([obj1], compress=False)[0]
    meta = temp_container.get_object_meta(hashkey1)
    assert meta["type"] == ObjectType.PACKED

    # No errors yet
    temp_container.validate()
    issues = temp_container.validate()
    assert issues.is_valid()

    # Corrupt the object
    with open(
        temp_container._get_pack_path_from_pack_id(str(meta["pack_id"])), "wb"
    ) as fhandle:
        # Short corrupted string so also the size is wrong
        fhandle.write(b"COR")

    # I don't use the dataclass .is_valid() method of ValidationIssues because I want to
    # pop the error and check that there are no other issues but only the one I'm aware of
    errors = dataclasses.asdict(temp_container.validate())
    problems = errors.pop("invalid_hashes_packed")
    assert set(problems) == {hashkey1}

    problems = errors.pop("invalid_sizes_packed")
    assert set(problems) == {hashkey1}

    # There shouldn't be any other error
    assert not any(errors.values())


def test_validate_callback(temp_container, callback_instance):
    """Test the correctness of the callbacks.

    Stores the calls to check at the end that everything was called correctly."""
    # Add packed objects (2001, 10 chars each), *not* a multiple of 400 (that is the internal value
    # of how many events should be triggered as a maximum)
    len_packed = 2001
    data = [f"p{i:09d}".encode("ascii") for i in range(len_packed)]
    temp_container.add_objects_to_pack(data)

    # Add loose objects (1x)
    len_loose = 101
    data = [f"l{i:09d}".encode("ascii") for i in range(len_loose)]
    for content in data:
        temp_container.add_object(content)

    temp_container.validate(callback=callback_instance.callback)

    assert (
        callback_instance.current_action is None
    ), "The 'validate' call did not perform a final callback with a 'close' event"

    # I convert to dict because I the order of the actions can change
    performed_actions_dict = {
        action["start_value"]["description"]: action
        for action in callback_instance.performed_actions
    }

    assert performed_actions_dict == {
        "Loose objects": {
            "start_value": {"total": len_loose, "description": "Loose objects"},
            "value": len_loose,
        },
        "Pack 0": {
            "start_value": {"total": len_packed, "description": "Pack 0"},
            "value": len_packed,
        },
    }


@pytest.mark.parametrize("use_size_hint", [True, False])
def test_add_streamed_object_to_pack_callback(  # pylint: disable=invalid-name
    temp_container, use_size_hint, callback_instance
):
    """Test the correctness of the callback of add_streamed_object_to_pack."""
    length = 1000000
    content = b"0" * length
    stream = io.BytesIO(content)

    if use_size_hint:
        hashkey = temp_container.add_streamed_object_to_pack(
            stream, callback_size_hint=length, callback=callback_instance.callback
        )
    else:
        hashkey = temp_container.add_streamed_object_to_pack(
            stream, callback=callback_instance.callback
        )

    assert temp_container.get_object_content(hashkey) == content

    assert (
        callback_instance.current_action is None
    ), "The 'validate' call did not perform a final callback with a 'close' event"

    assert callback_instance.performed_actions == [
        {
            "start_value": {
                "total": length if use_size_hint else 0,
                "description": "Streamed object",
            },
            "value": length,
        }
    ]


@pytest.mark.parametrize(
    "no_holes,no_holes_read_twice", [[True, True], [True, False], [False, False]]
)
def test_add_streamed_objects_to_pack_callback(  # pylint: disable=invalid-name
    temp_container, callback_instance, no_holes, no_holes_read_twice
):
    """Test the correctness of the callback of add_streamed_objects_to_pack."""
    # Add packed objects (2001, 10 chars each)
    len_packed = 2001
    stream_list = [io.BytesIO(f"p{i:09d}".encode("ascii")) for i in range(len_packed)]

    temp_container.add_streamed_objects_to_pack(
        stream_list,
        no_holes=no_holes,
        no_holes_read_twice=no_holes_read_twice,
        callback=callback_instance.callback,
    )

    # Add another 4001 packed objects with 2001 already-existing objects
    len_packed2 = 4001
    stream_list = [io.BytesIO(f"2p{i:09d}".encode("ascii")) for i in range(len_packed2)]

    temp_container.add_streamed_objects_to_pack(
        stream_list,
        no_holes=no_holes,
        no_holes_read_twice=no_holes_read_twice,
        callback=callback_instance.callback,
    )

    assert (
        callback_instance.current_action is None
    ), "The 'add_streamed_objects_to_pack' call did not perform a final callback with a 'close' event"

    expected_actions = []
    # First call
    expected_actions.append(
        {
            "start_value": {"total": len_packed, "description": "Bulk storing"},
            "value": len_packed,
        }
    )
    # Second call
    if no_holes:
        # If no_holes is True, i.e. we do not want holes, we compute an initial list of the existing ones
        expected_actions.append(
            {
                "start_value": {"total": len_packed, "description": "List existing"},
                "value": len_packed,
            }
        )
    expected_actions.append(
        {
            "start_value": {"total": len_packed2, "description": "Bulk storing"},
            "value": len_packed2,
        }
    )

    assert callback_instance.performed_actions == expected_actions


# Check both with the same hash type and with a different one
@pytest.mark.parametrize("other_container_hash_type", ["sha256", "sha1"])
def test_import_objects_callback(
    temp_container, callback_instance, other_container_hash_type
):
    """Test the correctness of the callback of import_objects."""
    # Add packed objects (2001, 10 chars each)
    len_packed = 2001
    stream_list = [io.BytesIO(f"p{i:09d}".encode("ascii")) for i in range(len_packed)]
    hashkeys = temp_container.add_streamed_objects_to_pack(stream_list)

    with tempfile.TemporaryDirectory() as tmpdir:
        other_container = Container(tmpdir)
        # Use the same hash type
        other_container.init_container(clear=True, hash_type=other_container_hash_type)

        # Import objects
        other_container.import_objects(
            hashkeys, temp_container, callback=callback_instance.callback
        )

        assert (
            other_container.count_objects()["loose"]
            == temp_container.count_objects()["loose"]
        )
        assert (
            other_container.count_objects()["packed"]
            == temp_container.count_objects()["packed"]
        )

        # close before exiting the context manager, so files are closed.
        other_container.close()

    expected_actions = []
    if other_container_hash_type == temp_container.hash_type:
        expected_actions.append(
            {
                "start_value": {"description": "Listing objects", "total": len_packed},
                "value": len_packed,
            }
        )
    expected_actions.append(
        {
            "start_value": {"description": "Copy objects", "total": len_packed},
            "value": len_packed,
        }
    )
    # len_packed is small (and the objects are small)
    # so they all end up in the final flush
    expected_actions.append(
        {
            "start_value": {"description": "Final flush", "total": len_packed},
            "value": len_packed,
        }
    )

    assert callback_instance.performed_actions == expected_actions


@pytest.mark.parametrize("ask_deleting_unknown", [True, False])
@pytest.mark.parametrize("compress", [True, False])
def test_delete(
    temp_container, compress, ask_deleting_unknown
):  # pylint: disable=too-many-statements
    """Test the deletion logic."""
    obj1 = b"324r3w"  # Will be packed (from loose)
    obj2 = b"jklf2wv"  # Will be loose
    obj3 = b"9z0vx0"  # Will be stored directly packed

    unknown_hashkey = utils.get_hash_cls(temp_container.hash_type)(
        b"NOT_EXISTING_OBJECT_CONTENT"
    ).hexdigest()

    hashkey1 = temp_container.add_object(obj1)
    temp_container.pack_all_loose(compress=compress)
    hashkey2 = temp_container.add_object(obj2)
    hashkey3 = temp_container.add_objects_to_pack([obj3], compress=compress)[0]

    # Add again the same object, so it's both packed *and* loose - I check this is the case (the type is packed,
    # but the loose object is there)
    temp_container.add_object(obj1)
    assert temp_container._get_loose_path_from_hashkey(hashkey1).exists()

    # Assert the objects are of the expected type
    assert temp_container.get_object_meta(hashkey1)["type"] == ObjectType.PACKED
    assert temp_container.get_object_meta(hashkey2)["type"] == ObjectType.LOOSE
    assert temp_container.get_object_meta(hashkey3)["type"] == ObjectType.PACKED
    with pytest.raises(exc.NotExistent):
        temp_container.get_object_meta(unknown_hashkey)

    assert set(temp_container.list_all_objects()) == {hashkey1, hashkey2, hashkey3}

    #####################################
    # Delete the packed object (hashkey3)
    if ask_deleting_unknown:
        deleted = temp_container.delete_objects([hashkey3, unknown_hashkey])
    else:
        deleted = temp_container.delete_objects([hashkey3])

    # In any case, only one object should have been deleted
    assert list(deleted) == [hashkey3]
    # Assert the objects are of the expected type
    assert temp_container.get_object_meta(hashkey1)["type"] == ObjectType.PACKED
    assert temp_container.get_object_meta(hashkey2)["type"] == ObjectType.LOOSE
    with pytest.raises(exc.NotExistent):
        temp_container.get_object_meta(hashkey3)
    with pytest.raises(exc.NotExistent):
        temp_container.get_object_meta(unknown_hashkey)

    assert set(temp_container.list_all_objects()) == {hashkey1, hashkey2}

    #####################################
    # Delete the object that is both loose and packed object (hashkey1)
    if ask_deleting_unknown:
        deleted = temp_container.delete_objects([hashkey1, unknown_hashkey])
    else:
        deleted = temp_container.delete_objects([hashkey1])

    # In any case, only one object should have been deleted
    assert list(deleted) == [hashkey1]
    # Assert the objects are of the expected type
    with pytest.raises(exc.NotExistent):
        temp_container.get_object_meta(hashkey1)
    assert temp_container.get_object_meta(hashkey2)["type"] == ObjectType.LOOSE
    with pytest.raises(exc.NotExistent):
        temp_container.get_object_meta(hashkey3)
    with pytest.raises(exc.NotExistent):
        temp_container.get_object_meta(unknown_hashkey)
    # Check that also the loose version has been deleted
    assert not temp_container._get_loose_path_from_hashkey(hashkey1).exists()

    assert set(temp_container.list_all_objects()) == {hashkey2}

    #####################################
    # Delete the object that is loose (hashkey2)
    if ask_deleting_unknown:
        deleted = temp_container.delete_objects([hashkey2, unknown_hashkey])
    else:
        deleted = temp_container.delete_objects([hashkey2])

    # In any case, only one object should have been deleted
    assert list(deleted) == [hashkey2]
    # Assert the objects are of the expected type
    with pytest.raises(exc.NotExistent):
        temp_container.get_object_meta(hashkey1)
    with pytest.raises(exc.NotExistent):
        temp_container.get_object_meta(hashkey2)
    with pytest.raises(exc.NotExistent):
        temp_container.get_object_meta(hashkey3)
    with pytest.raises(exc.NotExistent):
        temp_container.get_object_meta(unknown_hashkey)

    assert set(temp_container.list_all_objects()) == set()


def test_delete_with_duplicates(temp_container):
    """Test the deletion logic."""
    content = b"324r3w"
    hashkey = temp_container.add_object(content)

    content2 = b"dsfsa"
    # Add a second object
    hashkey2 = temp_container.add_object(content2)

    assert not os.listdir(temp_container._get_duplicates_folder())

    with open(temp_container._get_loose_path_from_hashkey(hashkey), "wb") as fhandle:
        # Write some corrupted content
        fhandle.write(b"CORRUPTED")
    with open(temp_container._get_loose_path_from_hashkey(hashkey2), "wb") as fhandle:
        # Write some corrupted content
        fhandle.write(b"CORRUPTED")

    # I should get the corrupted content
    assert temp_container.get_object_content(hashkey) != content
    assert temp_container.get_object_content(hashkey2) != content2

    # Change permissions to the loose object so I cannot rename it and so (since the file is corrupt)
    # I will create duplicates. Note that I will need to change permissions on the parent folder (on POSIX)
    # so I cannot rewrite it. S_IEXEC is needed on folders on Unix, is ignored on Windows. On Windows, I need
    # to change the permissions on the file, instead.
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey).parent,
        stat.S_IREAD | stat.S_IEXEC,
    )
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey2).parent,
        stat.S_IREAD | stat.S_IEXEC,
    )
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey),
        stat.S_IREAD,
    )
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey2),
        stat.S_IREAD,
    )

    # This should create two duplicates
    temp_container.add_object(content)
    temp_container.add_object(content)
    # This should create another duplicate for the other object
    temp_container.add_object(content2)

    # For this test I want that it wasn't writable so I still get the corrupted content
    assert temp_container.get_object_content(hashkey) != content
    assert temp_container.get_object_content(hashkey2) != content2

    assert len(os.listdir(temp_container._get_duplicates_folder())) == 3

    # Put back write permissions on the folder - it's also needed to be able to delete the temp_dir at the end
    # of the test, but also to run the delete() call
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey).parent,
        stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC,
    )
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey2).parent,
        stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC,
    )
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey),
        stat.S_IREAD | stat.S_IWRITE,
    )
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey2),
        stat.S_IREAD | stat.S_IWRITE,
    )

    # Also put back the correct content - this was just to trigger the creation of a duplicate
    with open(temp_container._get_loose_path_from_hashkey(hashkey), "wb") as fhandle:
        # Write some corrupted content
        fhandle.write(content)
    with open(temp_container._get_loose_path_from_hashkey(hashkey2), "wb") as fhandle:
        # Write some corrupted content
        fhandle.write(content2)
    assert temp_container.get_object_content(hashkey) == content
    assert temp_container.get_object_content(hashkey2) == content2

    # Let's delete the object
    temp_container.delete_objects([hashkey])
    # The container should be empty
    assert list(temp_container.list_all_objects()) == [hashkey2]
    # The object should not be there
    with pytest.raises(exc.NotExistent):
        temp_container.get_object_content(hashkey)
    assert temp_container.get_object_content(hashkey2) == content2

    # I should also have deleted the corresponding duplicates, but only for the object I deleted
    duplicates = os.listdir(temp_container._get_duplicates_folder())
    assert len(duplicates) == 1
    # The only duplicate left should be for the second object
    duplicate = duplicates[0]
    assert duplicate.startswith(f"{hashkey2}.")

    # I delete also the second object: also those files should go away
    temp_container.delete_objects([hashkey2])
    assert not list(temp_container.list_all_objects())
    with pytest.raises(exc.NotExistent):
        temp_container.get_object_content(hashkey2)
    assert not os.listdir(temp_container._get_duplicates_folder())


def test_clean_storage_with_duplicates(
    temp_container,
):  # pylint: disable=too-many-statements, invalid-name
    """Check the logic when using the clean storage method and where there are duplicates."""
    duplicates_folder = temp_container._get_duplicates_folder()
    content1 = b"324r3w"
    hashkey1 = temp_container.add_object(content1)

    content2 = b"dsfsa"
    # Add a second object
    hashkey2 = temp_container.add_object(content2)

    content3 = b"wejvlweekf"
    # Add a second object
    hashkey3 = temp_container.add_object(content3)

    assert not os.listdir(duplicates_folder)

    with open(temp_container._get_loose_path_from_hashkey(hashkey1), "wb") as fhandle:
        # Write some corrupted content
        fhandle.write(b"CORRUPTED")
    with open(temp_container._get_loose_path_from_hashkey(hashkey2), "wb") as fhandle:
        # Write some corrupted content
        fhandle.write(b"CORRUPTED")
    with open(temp_container._get_loose_path_from_hashkey(hashkey3), "wb") as fhandle:
        # Write some corrupted content
        fhandle.write(b"CORRUPTED")

    # I should get the corrupted content
    assert temp_container.get_object_content(hashkey1) != content1
    assert temp_container.get_object_content(hashkey2) != content2
    assert temp_container.get_object_content(hashkey3) != content3

    # Change permissions to the loose object so I cannot rename it and so (since the file is corrupt)
    # I will create duplicates. Note that I will need to change permissions on the parent folder (on POSIX)
    # so I cannot rewrite it. S_IEXEC is needed on folders on Unix, is ignored on Windows. On Windows, I need
    # to change the permissions on the file, instead.
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey1).parent,
        stat.S_IREAD | stat.S_IEXEC,
    )
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey2).parent,
        stat.S_IREAD | stat.S_IEXEC,
    )
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey3).parent,
        stat.S_IREAD | stat.S_IEXEC,
    )
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey1),
        stat.S_IREAD,
    )
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey2),
        stat.S_IREAD,
    )
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey3),
        stat.S_IREAD,
    )

    # Let's create three duplicates of each object
    temp_container.add_object(content1)
    temp_container.add_object(content1)
    temp_container.add_object(content1)
    # This should create another duplicate for the other object
    temp_container.add_object(content2)
    temp_container.add_object(content2)
    temp_container.add_object(content2)
    # This should create another duplicate for the other object
    temp_container.add_object(content3)
    temp_container.add_object(content3)
    temp_container.add_object(content3)

    # For this test I want that it wasn't writable so I still get the corrupted content
    assert temp_container.get_object_content(hashkey1) != content1
    assert temp_container.get_object_content(hashkey2) != content2
    assert temp_container.get_object_content(hashkey3) != content3

    assert len(os.listdir(duplicates_folder)) == 9

    # Put back write permissions on the folder - it's also needed to be able to delete the temp_dir at the end
    # of the test, but also to run the delete() call
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey1).parent,
        stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC,
    )
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey2).parent,
        stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC,
    )
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey3).parent,
        stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC,
    )
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey1),
        stat.S_IREAD | stat.S_IWRITE,
    )
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey2),
        stat.S_IREAD | stat.S_IWRITE,
    )
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey3),
        stat.S_IREAD | stat.S_IWRITE,
    )

    # Let's now do the following
    # - for the first object I put back the correct content: all duplicates should be deleted
    # - for the second object I put back the correct content but corrupt all duplicates:
    #   all duplicates should be deleted
    # - for the third object I leave the corrupted object, and corrupt all duplicates but one: the correct
    #   object should be restored, not duplicates should be left behind
    # Also put back the correct content - this was just to trigger the creation of a duplicate
    with open(temp_container._get_loose_path_from_hashkey(hashkey1), "wb") as fhandle:
        # Write back correct content
        fhandle.write(content1)
    with open(temp_container._get_loose_path_from_hashkey(hashkey2), "wb") as fhandle:
        # Write back correct content
        fhandle.write(content2)
    assert temp_container.get_object_content(hashkey1) == content1
    assert temp_container.get_object_content(hashkey2) == content2
    assert temp_container.get_object_content(hashkey3) != content3

    hash3_corrupt_count = 0
    for duplicate in os.listdir(duplicates_folder):
        if duplicate.startswith(f"{hashkey2}."):
            # All duplicates of object 2 are corrupt
            with open(duplicates_folder / duplicate, "wb") as fhandle:
                fhandle.write(b"CORRUPT")

        if duplicate.startswith(f"{hashkey3}."):
            hash3_corrupt_count += 1
            if hash3_corrupt_count <= 2:
                # I corrupt 2 out of three duplicates of object three
                with open(duplicates_folder / duplicate, "wb") as fhandle:
                    fhandle.write(b"CORRUPT")

    # No exception here
    temp_container.clean_storage()

    # All duplicates should have been deleted
    assert not os.listdir(duplicates_folder)

    # All objects are there and no new ones
    assert set(temp_container.list_all_objects()) == {hashkey1, hashkey2, hashkey3}

    # All contents have been restored, and no mistake has been done by replacing the content of wrong objects
    assert {
        hashkey: temp_container.get_object_content(hashkey)
        for hashkey in [hashkey1, hashkey2, hashkey3]
    } == {hashkey1: content1, hashkey2: content2, hashkey3: content3}


def test_clean_storage_with_duplicates_all_corrupt(
    temp_container,
):  # pylint: disable=invalid-name
    """Check the logic when using the clean storage method and where there are duplicates,
    and object and all duplicates are corrupt."""
    duplicates_folder = temp_container._get_duplicates_folder()
    content1 = b"324r3w"
    hashkey1 = temp_container.add_object(content1)

    assert not os.listdir(duplicates_folder)

    with open(temp_container._get_loose_path_from_hashkey(hashkey1), "wb") as fhandle:
        # Write some corrupted content
        fhandle.write(b"CORRUPTED")

    # I should get the corrupted content
    assert temp_container.get_object_content(hashkey1) != content1

    # Change permissions to the loose object so I cannot rename it and so (since the file is corrupt)
    # I will create duplicates. Note that I will need to change permissions on the parent folder (on POSIX)
    # so I cannot rewrite it. S_IEXEC is needed on folders on Unix, is ignored on Windows. On Windows, I need
    # to change the permissions on the file, instead.
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey1).parent,
        stat.S_IREAD | stat.S_IEXEC,
    )
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey1),
        stat.S_IREAD,
    )

    # Let's create three duplicates of each object
    temp_container.add_object(content1)
    temp_container.add_object(content1)
    temp_container.add_object(content1)

    # For this test I want that it wasn't writable so I still get the corrupted content
    assert temp_container.get_object_content(hashkey1) != content1

    assert len(os.listdir(duplicates_folder)) == 3

    # Put back write permissions on the folder - it's also needed to be able to delete the temp_dir at the end
    # of the test, but also to run the delete() call
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey1).parent,
        stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC,
    )
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey1),
        stat.S_IREAD | stat.S_IWRITE,
    )

    # Let's now do the following
    # - I leave the object corrupted, and I corrupt *ALL* duplicates

    for duplicate in os.listdir(duplicates_folder):
        assert duplicate.startswith(f"{hashkey1}.")  # Just to check the behavior
        with open(duplicates_folder / duplicate, "wb") as fhandle:
            fhandle.write(b"CORRUPT")

    # I check that I get an error because everything is inconsistent
    with pytest.raises(exc.InconsistentContent) as excinfo:
        temp_container.clean_storage()
    assert "all corrupt" in str(excinfo.value)


def test_clean_storage_with_duplicates_original_deleted(
    temp_container,
):  # pylint: disable=invalid-name
    """Check the logic when using the clean storage method and where there are duplicates."""
    duplicates_folder = temp_container._get_duplicates_folder()
    content1 = b"324r3w"
    hashkey1 = temp_container.add_object(content1)

    assert not os.listdir(duplicates_folder)

    with open(temp_container._get_loose_path_from_hashkey(hashkey1), "wb") as fhandle:
        # Write some corrupted content
        fhandle.write(b"CORRUPTED")

    # I should get the corrupted content
    assert temp_container.get_object_content(hashkey1) != content1

    # Change permissions to the loose object so I cannot rename it and so (since the file is corrupt)
    # I will create duplicates. Note that I will need to change permissions on the parent folder (on POSIX)
    # so I cannot rewrite it. S_IEXEC is needed on folders on Unix, is ignored on Windows. On Windows, I need
    # to change the permissions on the file, instead.
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey1).parent,
        stat.S_IREAD | stat.S_IEXEC,
    )
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey1),
        stat.S_IREAD,
    )

    # Let's create a duplicate
    temp_container.add_object(content1)

    # For this test I want that it wasn't writable so I still get the corrupted content
    assert temp_container.get_object_content(hashkey1) != content1
    assert len(os.listdir(duplicates_folder)) == 1

    # Put back write permissions on the folder - it's also needed to be able to delete the temp_dir at the end
    # of the test, but also to run the delete() call
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey1).parent,
        stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC,
    )
    os.chmod(
        temp_container._get_loose_path_from_hashkey(hashkey1),
        stat.S_IREAD | stat.S_IWRITE,
    )

    # Let's now do the following: I delete the loose object by hand
    os.remove(temp_container._get_loose_path_from_hashkey(hashkey1))

    # The object should not exist anymore
    with pytest.raises(exc.NotExistent):
        temp_container.get_object_content(hashkey1)

    # I check that I get an error because the original is not there but there are duplicates
    with pytest.raises(exc.InconsistentContent) as excinfo:
        temp_container.clean_storage()
    assert "does not exist anymore" in str(excinfo.value)

    # Deleting the object should be enough to clean up the issue
    temp_container.delete_objects([hashkey1])

    # This should now not raise
    temp_container.clean_storage()

    # There should be no duplicates anymore, nor objects in the container
    assert not os.listdir(duplicates_folder)
    assert not list(temp_container.list_all_objects())


@pytest.mark.parametrize(
    "no_holes, no_holes_read_twice", [[True, True], [True, False], [False, True]]
)
@pytest.mark.parametrize("use_streams", [True, False])
@pytest.mark.parametrize("compress", [True, False])
def test_packs_no_holes(
    temp_container, no_holes, no_holes_read_twice, use_streams, compress, monkeypatch
):
    """Test what happens when writing directly to packs and asking not to leave back holes."""
    content1 = b"1234567"
    content2 = b"wefvmafsf"
    content3 = b"224f"

    hashkey1 = utils.get_hash_cls(temp_container.hash_type)(content1).hexdigest()
    hashkey2 = utils.get_hash_cls(temp_container.hash_type)(content2).hexdigest()
    hashkey3 = utils.get_hash_cls(temp_container.hash_type)(content3).hexdigest()

    # Add twice each object, in some order, in the same call, with at least one at the very end (to check truncation)
    contents_to_add = [content1, content1, content2, content3, content2, content3]
    expected_hashkeys = [hashkey1, hashkey1, hashkey2, hashkey3, hashkey2, hashkey3]

    # They should provide the same behavior
    if use_streams:
        streams_list = [io.BytesIO(content) for content in contents_to_add]
        hashkeys = temp_container.add_streamed_objects_to_pack(
            streams_list,
            no_holes=no_holes,
            no_holes_read_twice=no_holes_read_twice,
            compress=compress,
        )
    else:
        hashkeys = temp_container.add_objects_to_pack(
            contents_to_add,
            no_holes=no_holes,
            no_holes_read_twice=no_holes_read_twice,
            compress=compress,
        )

    assert hashkeys == expected_hashkeys
    assert set(temp_container.list_all_objects()) == set(hashkeys)

    sizes = temp_container.get_total_size()
    assert sizes["total_size_packed"] == len(content1) + len(content2) + len(content3)

    if no_holes:
        assert (
            sizes["total_size_packed_on_disk"] == sizes["total_size_packfiles_on_disk"]
        )
    else:
        # We have added twice each object. Note: we cannot use total_size_packed because this would be
        # before compression
        assert (
            2 * sizes["total_size_packed_on_disk"]
            == sizes["total_size_packfiles_on_disk"]
        )

    # Add again the same objects, in a new call
    # I first monkeypatch the method `_write_data_to_packfile`. This writes to disk, and should never be called
    # if no_holes is True and no_holes_read_twice is True, because I am just adding existing objects.
    # So I assert in it.

    # This is a list with a counter. It's a list because we want to get the integer by reference so we can increment it
    # from inside the function.
    call_counter = [0]

    def new_write_data_to_packfile(self, call_counter, *args, **kwargs):
        """Just pass through to the original call."""
        assert not (no_holes and no_holes_read_twice)
        call_counter[0] += 1
        return self._tmp_write_to_packfile(*args, **kwargs)

    temp_container._tmp_write_to_packfile = temp_container._write_data_to_packfile
    monkeypatch.setattr(
        temp_container,
        "_write_data_to_packfile",
        functools.partial(
            new_write_data_to_packfile, self=temp_container, call_counter=call_counter
        ),
    )

    if use_streams:
        streams_list = [io.BytesIO(content) for content in contents_to_add]
        hashkeys = temp_container.add_streamed_objects_to_pack(
            streams_list,
            no_holes=no_holes,
            no_holes_read_twice=no_holes_read_twice,
            compress=compress,
        )
    else:
        hashkeys = temp_container.add_objects_to_pack(
            contents_to_add,
            no_holes=no_holes,
            no_holes_read_twice=no_holes_read_twice,
            compress=compress,
        )

    # Check that the mocked function was indeeed called (and it was called the right number of times)
    # This is an indirect way to check the internal behavior, i.e. if the `no_holes_read_twice` is honored and
    # nothing was written on disk.
    if no_holes and no_holes_read_twice:
        assert call_counter[0] == 0
    else:
        assert call_counter[0] == len(contents_to_add)

    assert hashkeys == expected_hashkeys

    new_sizes = temp_container.get_total_size()
    # No new objects, so same size
    assert new_sizes["total_size_packed"] == len(content1) + len(content2) + len(
        content3
    )

    if no_holes:
        # Shouldn't have created more space on disk
        assert (
            new_sizes["total_size_packed_on_disk"] == sizes["total_size_packed_on_disk"]
        )
        assert (
            new_sizes["total_size_packfiles_on_disk"]
            == sizes["total_size_packfiles_on_disk"]
        )
    else:
        # We have doubled the space on disk
        assert (
            new_sizes["total_size_packfiles_on_disk"]
            == 2 * sizes["total_size_packfiles_on_disk"]
        )
        # (but shouldn't have increased the size of packed objects on disk)
        assert (
            new_sizes["total_size_packed_on_disk"] == sizes["total_size_packed_on_disk"]
        )


def test_packs_read_in_order(temp_dir):
    """Test that when reading the objects from packs, they are read grouped by packs, and in offset order.

    This is very important for performance.

    .. note:: IMPORTANT: This is not running with concurrent packing, so only the first internal loop of
       get_objects_stream_and_meta is triggered and the order is the one described above.
       The application should NOT make any assumption on this because, during concurrent packing of loose objects,
       the recently packed/clean_stored objects might be returned later.

    .. note:: We are not checking the order in which packs are considered
    """
    num_objects = 10000  # Number of objects
    obj_size = 999
    # This will generate N objects of size obj_size each
    # They are different because the at least the first characters until the first dash are different

    temp_container = Container(temp_dir)
    # A apck should accomodate ~100 objects, and there should be > 90 packs
    temp_container.init_container(clear=True, pack_size_target=100000)

    data = [(f"{i}-".encode("ascii") * obj_size)[:obj_size] for i in range(num_objects)]
    hashkeys = temp_container.add_objects_to_pack(data, compress=False)

    # Check that I indeed created num_objects (different) objects
    assert len(set(hashkeys)) == num_objects

    # Shuffle the array. When retrieving data, I should still fetch them per pack, and then in offset order
    # (so the pack file is read sequentially rather than randomly)
    random.shuffle(hashkeys)

    last_offset = None
    last_pack = None
    seen_packs = set()

    with temp_container.get_objects_stream_and_meta(
        hashkeys, skip_if_missing=False
    ) as triplets:
        for _, _, meta in triplets:  # pylint: disable=not-an-iterable
            assert meta["type"] == ObjectType.PACKED
            if last_pack is None:
                last_pack = meta["pack_id"]
                seen_packs.add(meta["pack_id"])
                last_offset = 0
            elif meta["pack_id"] != last_pack:
                assert meta["pack_id"] not in seen_packs, (
                    f"Objects were already retrieved from pack {meta['pack_id']}, "
                    f"the last pack was {last_pack} "
                    f"and we are trying to retrieve again from pack {meta['pack_id']}"
                )
                last_pack = meta["pack_id"]
                seen_packs.add(meta["pack_id"])
                last_offset = 0
            # We are still in the same pack
            assert last_offset <= meta["pack_offset"], (
                f"in pack {meta['pack_id']} we are reading offset "
                f"{meta['pack_offset']}, but before we were reading "
                f"a later offset {last_offset}"
            )
            last_offset = meta["pack_offset"]

    # I want to make sure to have generated enough packs, meaning this function is actually testing the behavior
    # This should generated 90 packs
    # NOTE: if you use compress = True, you get many less packs since the data is very compressible! (only 2)
    # So we only test with compress=False
    largest_pack = max(seen_packs)
    assert largest_pack > 80

    # Check that all packs were scanned through
    assert sorted(seen_packs) == list(range(largest_pack + 1))

    # Important before exiting from the tests
    temp_container.close()


@pytest.mark.parametrize("compress_mode", list(CompressMode))
def test_repack(temp_dir, compress_mode):
    """Test the repacking functionality."""
    temp_container = Container(temp_dir)
    temp_container.init_container(clear=True, pack_size_target=39)

    # data of 10 bytes each. Will fill two packs.
    data = [
        b"-123456789",
        b"a123456789",
        b"b123456789",
        b"c123456789",
        b"d123456789",
        b"e123456789",
        b"f123456789",
        b"g123456789",
        b"h123456789",
    ]

    hashkeys = []
    # Add them one by one, so I am sure in wich pack they go
    for datum in data:
        hashkeys.append(temp_container.add_objects_to_pack([datum])[0])

    assert temp_container.get_object_meta(hashkeys[0])["pack_id"] == 0
    assert temp_container.get_object_meta(hashkeys[1])["pack_id"] == 0
    assert temp_container.get_object_meta(hashkeys[2])["pack_id"] == 0
    assert temp_container.get_object_meta(hashkeys[3])["pack_id"] == 0
    assert temp_container.get_object_meta(hashkeys[4])["pack_id"] == 1
    assert temp_container.get_object_meta(hashkeys[5])["pack_id"] == 1
    assert temp_container.get_object_meta(hashkeys[6])["pack_id"] == 1
    assert temp_container.get_object_meta(hashkeys[7])["pack_id"] == 1
    assert temp_container.get_object_meta(hashkeys[8])["pack_id"] == 2

    # I check which packs exist
    assert sorted(temp_container._list_packs()) == [
        "0",
        "1",
        "2",
    ]

    counts = temp_container.count_objects()
    assert counts["packed"] == len(data)
    size = temp_container.get_total_size()
    assert size["total_size_packed"] == 10 * len(data)
    assert size["total_size_packfiles_on_disk"] == 10 * len(data)

    # I delete an object in the middle, an object at the end of a pack, and an object at the beginning.
    # I also delete the only object
    idx_to_delete = [1, 3, 4, 8]
    to_delete = [hashkeys[idx] for idx in idx_to_delete]
    temp_container.delete_objects(to_delete)

    # I check that all packs are still there
    assert sorted(temp_container._list_packs()) == [
        "0",
        "1",
        "2",
    ]

    counts = temp_container.count_objects()
    assert counts["packed"] == len(data) - len(to_delete)
    size = temp_container.get_total_size()
    # I deleted 4 objects
    assert size["total_size_packed"] == 10 * (len(data) - len(to_delete))
    # Still full size on disk
    assert size["total_size_packfiles_on_disk"] == 10 * len(data)

    # I now repack
    temp_container.repack(compress_mode=compress_mode)

    # I check that all packs are still there, but pack 2 was deleted
    assert sorted(temp_container._list_packs()) == [
        "0",
        "1",
    ]

    counts = temp_container.count_objects()
    assert counts["packed"] == len(data) - len(to_delete)
    size = temp_container.get_total_size()
    assert size["total_size_packed"] == 10 * (len(data) - len(to_delete))
    # This time also the size on disk should be adapted (it's the main goal of repacking)
    objects_meta = dict(
        temp_container.get_objects_meta(
            [hashkeys[idx] for idx in range(len(hashkeys)) if idx not in idx_to_delete]
        )
    )
    assert size["total_size_packfiles_on_disk"] == sum(
        list(meta["pack_length"] for meta in objects_meta.values())
    )

    # Check that the content is still correct
    # Should not raise
    issues = temp_container.validate()
    assert issues.is_valid()

    # Important before exiting from the tests
    temp_container.close()


@pytest.mark.parametrize("repack_compress_mode", list(CompressMode))
@pytest.mark.parametrize("compress_pack", [True, False])
@pytest.mark.parametrize("small_size", [True, False])
def test_repack_compress_modes(
    temp_container: Container, small_size, compress_pack, repack_compress_mode
):
    """Check that repack() uses the correct compression mode."""

    # Write 10*1_000_000 = 10 million bytes, larger than a chunk
    # this should be quite compressible even with the heuristics
    content_compr = b"0123456789" * 100
    if not small_size:
        content_compr *= 10_000
    # This instead is 10 million random bytes, probably uncompressible
    if small_size:
        content_uncompr = os.urandom(10_000)
    else:
        content_uncompr = os.urandom(10_000_000)

    hashkey_compr = temp_container.add_object(content_compr)
    hashkey_uncompr = temp_container.add_object(content_uncompr)

    temp_container.pack_all_loose(compress=compress_pack)
    # Both should have the expected compression mode from the variable `compress_mode`
    assert (
        temp_container.get_object_meta(hashkey_compr)["pack_compressed"]
        == compress_pack
    )
    assert (
        temp_container.get_object_meta(hashkey_uncompr)["pack_compressed"]
        == compress_pack
    )

    # We now repack, and check if everything is correct
    temp_container.repack(compress_mode=repack_compress_mode)

    # Let's just check that results are correct after repacking
    issues = temp_container.validate()
    assert issues.is_valid()

    # We now check the expected compression mode
    if repack_compress_mode == CompressMode.NO:
        # All should be uncompressed
        assert temp_container.get_object_meta(hashkey_compr)["pack_compressed"] is False
        assert (
            temp_container.get_object_meta(hashkey_uncompr)["pack_compressed"] is False
        )
    elif repack_compress_mode == CompressMode.YES:
        # All should be compressed
        assert temp_container.get_object_meta(hashkey_compr)["pack_compressed"] is True
        assert (
            temp_container.get_object_meta(hashkey_uncompr)["pack_compressed"] is True
        )
    elif repack_compress_mode == CompressMode.KEEP:
        # Should not have changed
        assert (
            temp_container.get_object_meta(hashkey_compr)["pack_compressed"]
            == compress_pack
        )
        assert (
            temp_container.get_object_meta(hashkey_uncompr)["pack_compressed"]
            == compress_pack
        )
    elif repack_compress_mode == CompressMode.AUTO:
        # Only really compressible streams should be compressed
        assert temp_container.get_object_meta(hashkey_compr)["pack_compressed"] is True
        assert (
            temp_container.get_object_meta(hashkey_uncompr)["pack_compressed"] is False
        )
    else:
        raise AssertionError(
            f"Unknown {repack_compress_mode=}, most probably you added a new CompressMode and need to update the tests"
        )

    # Try to repack to non-compressed, then to compressed, then again to this mode,
    # to see that it all works
    temp_container.repack(compress_mode=CompressMode.NO)
    issues = temp_container.validate()
    assert issues.is_valid()

    temp_container.repack(compress_mode=CompressMode.YES)
    issues = temp_container.validate()
    assert issues.is_valid()

    temp_container.repack(compress_mode=repack_compress_mode)
    issues = temp_container.validate()
    assert issues.is_valid()


@pytest.mark.parametrize("start_compressed", [True, False])
def test_repack_auto_many_sizes(temp_container: Container, start_compressed):
    """Check repack()+CompressMode.AUTO with various object sizes."""

    objects = []
    for length in range(0, 10_000):
        # All possible small lengths up to 10_000
        objects.append(b"a" * length)
    # A few larger lengths - otherwise it takes ages to create all
    # in memory and compress them!
    for length in range(10_001, 10_000_000, 300_000):
        objects.append(b"a" * length)
    temp_container.add_objects_to_pack(objects, compress=start_compressed)

    # We now repack, and check if everything is correct
    temp_container.repack(compress_mode=CompressMode.AUTO)
    issues = temp_container.validate()
    assert issues.is_valid()


def test_repack_progress_bar(temp_container: Container):
    """Check that the progress bar is correctly updated when packing all loose objects."""
    objects = []
    for length in range(0, 100):
        objects.append(b"a" * length)

    temp_container.add_objects_to_pack(objects, compress=False)

    passed_updates = 0
    passed_total = 0

    def progress(action, value):
        """A dummy progress function."""
        if action == "init":
            assert (
                value["total"] == temp_container.get_total_size()["total_size_packed"]
            )
            nonlocal passed_total
            passed_total = value["total"]
            assert value["description"] == "Repack 0"
        elif action == "update":
            isinstance(value, (int, float))
            nonlocal passed_updates
            passed_updates += value
        elif action == "close":
            assert passed_updates == passed_total

    temp_container.repack(callback=progress)


@pytest.mark.parametrize("compress_mode", [True, False] + list(CompressMode))
def test_pack_all_loose_compress_modes(temp_container: Container, compress_mode):
    """Check that pack_all_loose() uses the correct compression mode.

    Note that pack_all_loose accepts also booleans, for backwards-compatibility.
    """
    # Write 10*1_000_000 = 10 million bytes, larger than a chunk
    # this should be quite compressible even with the heuristics
    content_compr = b"0123456789" * 1_000_000
    # This instead is 10 million random bytes, probably uncompressible
    content_uncompr = os.urandom(10_000_000)

    hashkey_compr = temp_container.add_object(content_compr)
    hashkey_uncompr = temp_container.add_object(content_uncompr)

    temp_container.pack_all_loose(compress=compress_mode)

    # Let's just check that results are correct
    issues = temp_container.validate()
    assert issues.is_valid()

    # We now check the expected compression mode
    if compress_mode == CompressMode.NO or compress_mode is False:
        # All should be uncompressed
        assert temp_container.get_object_meta(hashkey_compr)["pack_compressed"] is False
        assert (
            temp_container.get_object_meta(hashkey_uncompr)["pack_compressed"] is False
        )
    elif compress_mode == CompressMode.YES or compress_mode is True:
        # All should be compressed
        assert temp_container.get_object_meta(hashkey_compr)["pack_compressed"] is True
        assert (
            temp_container.get_object_meta(hashkey_uncompr)["pack_compressed"] is True
        )
    elif compress_mode == CompressMode.KEEP:
        # Should not have changed - so it should be False since loose objects are always uncompressed
        assert temp_container.get_object_meta(hashkey_compr)["pack_compressed"] is False
        assert (
            temp_container.get_object_meta(hashkey_uncompr)["pack_compressed"] is False
        )
    elif compress_mode == CompressMode.AUTO:
        # Only really compressible streams should be compressed
        assert temp_container.get_object_meta(hashkey_compr)["pack_compressed"] is True
        assert (
            temp_container.get_object_meta(hashkey_uncompr)["pack_compressed"] is False
        )
    else:
        raise AssertionError(
            f"Unknown {compress_mode=}, most probably you added a new CompressMode and need to update the tests"
        )


def test_pack_all_loose_many(temp_container):
    """Check the pack_all_loose when there are many objects to pack, more than _MAX_CHUNK_ITERATE_LENGTH."""
    expected = {}
    for idx in range(temp_container._MAX_CHUNK_ITERATE_LENGTH + 10):
        content = f"{idx}".encode()
        expected[temp_container.add_object(content)] = content

    # Pack all loose objects
    temp_container.pack_all_loose()

    retrieved = temp_container.get_objects_content(expected.keys())
    assert retrieved == expected

    # Pack again, nothing should happen, but it should trigger the logic in pack_all_loose at the beginning,
    # with `if where == Location.BOTH`
    temp_container.pack_all_loose()
    retrieved = temp_container.get_objects_content(expected.keys())
    assert retrieved == expected


def test_pack_all_loose_progress_bar(temp_container):
    """Check that the progress bar is correctly updated when packing all loose objects."""
    # Add 10 objects
    for idx in range(10):
        content = f"{idx}".encode()
        temp_container.add_object(content)

    passed_updates = 0
    passed_total = 0

    def progress(action, value):
        """A dummy progress function."""
        if action == "init":
            assert value["total"] == temp_container.get_total_size()["total_size_loose"]
            nonlocal passed_total
            passed_total = value["total"]
            assert value["description"] == "Packing loose objects"
        elif action == "update":
            isinstance(value, (int, float))
            nonlocal passed_updates
            passed_updates += value
        elif action == "close":
            assert passed_updates == passed_total

    temp_container.pack_all_loose(callback=progress)


def test_container_id(temp_container):
    """Check the creation of unique container IDs."""
    old_container_id = temp_container.container_id
    assert old_container_id is not None
    assert isinstance(old_container_id, str)

    # Re-initialize: it should get a new container_id
    temp_container.init_container(clear=True)
    assert old_container_id != temp_container.container_id


@pytest.mark.parametrize(
    "compression_algorithm",
    [
        "gzip",  # unknown
        "zlib",  # no variant
        "zlib+a",
        "zlib+-1",
        "zlib+10",
        "unknown-method",  # Invalid variant
    ],
)
def test_unknown_compressers(temp_container, compression_algorithm):
    """Check that unknown or invalid compressers give a ValueError."""
    with pytest.raises(ValueError):
        temp_container.init_container(
            clear=True, compression_algorithm=compression_algorithm
        )


## I add tests for the LazyLooseStream here - even if it's in the `utils`,
## it really needs a Container to be functional.
def test_lazy_loose_stream(temp_container):
    """Basic tests of the methods of a LazyLooseStream."""
    content = b"b123456789"

    temp_container.init_container(clear=True, compression_algorithm="zlib+9")
    hashkey = temp_container.add_object(content)

    temp_container.pack_all_loose(compress=True)
    temp_container.clean_storage()
    # Should be empty
    loosepath = temp_container._get_loose_path_from_hashkey(hashkey)
    assert not loosepath.exists()
    # Check that it's in a pack and it's compressed
    meta = temp_container.get_object_meta(hashkey)
    assert meta["type"] == ObjectType.PACKED
    assert meta["pack_compressed"]

    lazy_loose = temp_container.get_lazy_loose_stream(hashkey=hashkey)
    assert lazy_loose.mode == "rb"
    assert lazy_loose.seekable()
    with pytest.raises(ValueError):
        # Shouldn't be allowed to work on a non-open stream
        lazy_loose.seek(0)
    with pytest.raises(ValueError):
        # Shouldn't be allowed to work on a non-open stream
        lazy_loose.tell()
    with pytest.raises(ValueError):
        # Shouldn't be allowed to work on a non-open stream
        lazy_loose.read(1)

    # Above operations should not have created a file
    assert not loosepath.exists()

    # Now, I open the stream; this should materialize the loose uncompressed
    # object again
    lazy_loose.open_stream()
    assert not lazy_loose.closed
    assert loosepath.exists()

    # Check that calling it again doesn't harm
    lazy_loose.open_stream()
    assert not lazy_loose.closed

    # check that tell, seek, read work as intended
    pos = 5
    length = 3
    lazy_loose.seek(pos, 0)
    assert lazy_loose.tell() == pos
    assert lazy_loose.read(length) == content[pos : pos + length]

    # test also whence = 1
    offset = -4
    lazy_loose.seek(offset, 1)
    # Compute new position
    pos = pos + length + offset
    assert lazy_loose.tell() == pos
    assert lazy_loose.read(length) == content[pos : pos + length]

    # test also whence = 2
    offset = -4
    lazy_loose.seek(offset, 2)
    # Compute new position (whence=2 => from the end of the file)
    pos = len(content) + offset
    assert lazy_loose.tell() == pos
    assert lazy_loose.read(length) == content[pos : pos + length]

    # Close the stream
    lazy_loose.close_stream()
    assert lazy_loose.closed

    # Check that closing again does not harm
    lazy_loose.close_stream()
    assert lazy_loose.closed

    # Check that now that everything is closed, the storage can actually
    # be cleaned (on Windows this would not work if the underlying loose file
    # is still open)
    temp_container.clean_storage()
    assert not loosepath.exists()


def test_lazy_loose_stream_missing(temp_container):
    """Test behaviour of LazyLooseStream of a non-existing hashkey."""
    temp_container.init_container(clear=True, compression_algorithm="zlib+9")
    content = b"b123456789"
    # It is loose, not packed
    hashkey = temp_container.add_object(content)

    # Try with a missing/wrong hashkey
    missing_lazy = temp_container.get_lazy_loose_stream(hashkey="WRONGHASHKEY")
    # Note: error is delayed to the opening of the stream
    with pytest.raises(exc.NotExistent):
        missing_lazy.open_stream()

    # Try with a hashkey of an object that is only loose (not packed)
    # The current behavior is that it just works
    unpacked_lazy = temp_container.get_lazy_loose_stream(hashkey=hashkey)
    unpacked_lazy.open_stream()
    assert unpacked_lazy.read() == content
    unpacked_lazy.close_stream()

    # Check that after closing nothing very wrong happened (such as deletion of
    # only copy of the loose object)
    loosepath = temp_container._get_loose_path_from_hashkey(hashkey)
    assert loosepath.exists()


def test_lazy_loose_stream_context_man(temp_container):
    """Basic tests of the methods of a LazyLooseStream."""
    content = b"b123456789"

    temp_container.init_container(clear=True, compression_algorithm="zlib+9")
    hashkey = temp_container.add_object(content)

    temp_container.pack_all_loose(compress=True)
    temp_container.clean_storage()
    # Should be empty
    loosepath = temp_container._get_loose_path_from_hashkey(hashkey)
    assert not loosepath.exists()

    lazy_loose = temp_container.get_lazy_loose_stream(hashkey=hashkey)
    assert lazy_loose.closed

    with lazy_loose:
        # Using in context manager opens it
        assert not lazy_loose.closed
        pos = 5
        length = 3
        lazy_loose.seek(pos, 0)
        assert lazy_loose.tell() == pos
        assert lazy_loose.read(length) == content[pos : pos + length]

    # Out of the context manager it is closed
    assert lazy_loose.closed


@pytest.mark.parametrize("num_iterations_delete", [3, 10])
def test_lazy_loose_loosen_and_delete(
    temp_container, num_iterations_delete, monkeypatch
):
    """
    Test what happens if a loose file is deleted right after it's loosened.

    This also ensures to test that specific code path.
    """
    content = b"b123456789"
    hashkey = temp_container.add_object(content)

    temp_container.pack_all_loose(compress=True)
    temp_container.clean_storage()
    # Should be empty
    loosepath = temp_container._get_loose_path_from_hashkey(hashkey)
    assert not loosepath.exists()

    lazy_loose = temp_container.get_lazy_loose_stream(hashkey=hashkey)

    # Monkeypatch to actually clean the loose object as soon as it's created
    def new_loosen_object(hashkey):
        """Pass to the original call"""
        self = temp_container
        if hasattr(self, "call_counter"):
            self.call_counter += 1
        else:
            self.call_counter = 1
        retval = self._old_loosen_object(hashkey)
        # A loose object was created
        assert self._get_loose_path_from_hashkey(hashkey).exists()

        # As soon as the loose object is created, I actually delete it!
        # But only for a maximum number of times
        if self.call_counter < num_iterations_delete:
            self.clean_storage()
            assert not self._get_loose_path_from_hashkey(hashkey).exists()

        return retval

    Container._old_loosen_object = Container.loosen_object
    monkeypatch.setattr(temp_container, "loosen_object", new_loosen_object)

    if num_iterations_delete < 5:  # for the case of 3 it should work
        # this should work
        lazy_loose.open_stream()
        assert lazy_loose.read() == content
        lazy_loose.close_stream()
    else:  # for the case of 10 it should fail as it's more than the MAX_RETRIES
        with pytest.raises(RuntimeError) as excinfo:
            lazy_loose.open_stream()
        assert "Unable to open the loose object" in str(excinfo.value)
