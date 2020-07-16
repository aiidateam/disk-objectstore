"""Test the performance of the container implementation."""
import hashlib
import random

import pytest


@pytest.mark.benchmark(group='write', min_rounds=3)
def test_pack_write(temp_container, benchmark):
    """Add 10'000 objects to the container in packed form, and benchmark write and read speed."""
    num_files = 10000
    data_content = [str(i).encode('ascii') for i in range(num_files)]
    expected_hashkeys = [hashlib.sha256(content).hexdigest() for content in data_content]

    hashkeys = benchmark(temp_container.add_objects_to_pack, data_content, compress=False)

    assert len(hashkeys) == len(data_content)
    assert expected_hashkeys == hashkeys


@pytest.mark.benchmark(group='write', min_rounds=3)
def test_loose_write(temp_container, benchmark):
    """Add 1'000 objects to the container in packed form, and benchmark write and read speed."""
    num_files = 1000
    data_content = [str(i).encode('ascii') for i in range(num_files)]
    expected_hashkeys = [hashlib.sha256(content).hexdigest() for content in data_content]

    def write_loose(container, contents):
        retval = []
        for content in contents:
            retval.append(container.add_object(content))
        return retval

    hashkeys = benchmark(write_loose, temp_container, data_content)

    assert len(hashkeys) == len(data_content)
    assert expected_hashkeys == hashkeys


@pytest.mark.benchmark(group='read')
def test_pack_read(temp_container, benchmark):
    """Add 10'000 objects to the container in packed form, and benchmark write and read speed."""
    num_files = 10000
    data_content = [str(i).encode('ascii') for i in range(num_files)]
    expected_hashkeys = [hashlib.sha256(content).hexdigest() for content in data_content]
    expected_results_dict = dict(zip(expected_hashkeys, data_content))

    hashkeys = temp_container.add_objects_to_pack(data_content, compress=False)
    random.shuffle(hashkeys)
    # Note that here however the OS will be using the disk caches
    results = benchmark(temp_container.get_objects_content, hashkeys)

    assert results == expected_results_dict


@pytest.mark.benchmark(group='read')
def test_loose_read(temp_container, benchmark):
    """Add 1'000 objects to the container in loose form, and benchmark write and read speed."""
    num_files = 1000
    data_content = [str(i).encode('ascii') for i in range(num_files)]
    hashkeys = []
    for content in data_content:
        hashkeys.append(temp_container.add_object(content))
    expected_results = dict(zip(hashkeys, data_content))

    random.shuffle(hashkeys)
    # Note that here however the OS will be using the disk caches
    results = benchmark(temp_container.get_objects_content, hashkeys)

    assert results == expected_results


@pytest.mark.benchmark(group='check', min_rounds=3)
def test_has_objects(temp_container, benchmark):
    """Benchmark speed to check object existence.

    Add 10'000 objects to the container (half packed, half loose), and benchmark speed to check existence
    of these 10'000 and of 5'000 more that do not exist.
    """
    num_files_half = 5000
    data_content_packed = [str(i).encode('ascii') for i in range(num_files_half)]

    hashkeys_packed = temp_container.add_objects_to_pack(data_content_packed, compress=False)

    # Different set of data for the loose objects, not colliding
    data_content_loose = [b'LOOSE' + str(i).encode('ascii') for i in range(num_files_half)]

    hashkeys_loose = []
    for content in data_content_loose:
        hashkeys_loose.append(temp_container.add_object(content))

    # Will contain tuples `(hashkey, exists)`` [where `exists` is a Boolean]
    existence_array = []
    for hashkey in hashkeys_packed:
        existence_array.append((hashkey, True))
    for hashkey in hashkeys_loose:
        existence_array.append((hashkey, True))
    for idx in range(num_files_half):
        existence_array.append(('UNKNOWN{}'.format(idx), False))

    # Shuffle pairs
    random.shuffle(existence_array)

    hashkeys_to_check, expected_result = zip(*existence_array)

    result = benchmark(temp_container.has_objects, hashkeys_to_check)

    # I use `set(data)` because if they are identical, they get the same UUID
    assert result == list(expected_result)


@pytest.mark.benchmark(group='read')
def test_list_all_packed(temp_container, benchmark):
    """Add 100'000 objects to the container in packed form, and benchmark list speed."""
    num_files = 100000
    data_content = [str(i).encode('ascii') for i in range(num_files)]

    hashkeys = temp_container.add_objects_to_pack(data_content, compress=False)

    # Note that here however the OS will be using the disk caches
    results = benchmark(temp_container.list_all_objects)

    assert set(results) == set(hashkeys)


@pytest.mark.benchmark(group='read')
def test_list_all_loose(temp_container, benchmark):
    """Add 10'000 loose objects to the container in packed form, and benchmark list speed."""
    num_files = 10000
    data_content = [str(i).encode('ascii') for i in range(num_files)]

    hashkeys = []
    for content in data_content:
        hashkeys.append(temp_container.add_object(content))

    # Note that here however the OS will be using the disk caches
    results = benchmark(temp_container.list_all_objects)

    assert set(results) == set(hashkeys)
