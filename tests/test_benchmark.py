"""Test the performance of the container implementation."""
import random

import pytest


@pytest.mark.benchmark(group='write', min_rounds=3)
def test_pack_write(temp_container, generate_random_data, benchmark):
    """Add a number of objects to the container in packed form, and benchmark write and read speed."""
    num_files = 10000
    data = generate_random_data(num_files=num_files, min_size=0, max_size=1000)
    data_content = list(data.values())

    hashkeys = benchmark(temp_container.add_objects_to_pack, data_content, compress=False)

    assert len(hashkeys) == len(data_content)
    # In case I have the same object more than once
    assert len(set(hashkeys)) == len(set(data_content))


@pytest.mark.benchmark(group='read')
def test_pack_read(temp_container, generate_random_data, benchmark):
    """Add a number of objects to the container in packed form, and benchmark write and read speed."""
    num_files = 10000
    data = generate_random_data(num_files=num_files, min_size=0, max_size=1000)
    data_content = list(data.values())

    hashkeys = temp_container.add_objects_to_pack(data_content, compress=False)

    # the length of this dict can be smaller than the length of data_content
    # if there are repeated objects
    expected_results_dict = dict(zip(hashkeys, data_content))

    random.shuffle(hashkeys)

    results = benchmark(temp_container.get_objects_content, hashkeys)

    # I use `set(data)` because if they are identical, they get the same UUID
    assert results == expected_results_dict
