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
        existence_array.append((f'UNKNOWN{idx}', False))

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


def add_objects_in_batches(temp_container, data, batch_size=1000):
    """Add objects to temp_container in batches of 1000."""
    for i in range(0, len(data), batch_size):
        batch = data[i : i + batch_size]
        for content in batch:
            temp_container.add_object(content)


def calculate_target_config(target_packs: int = 100, num_files: int = 10000):
    """Calculate file size and pack size to achieve target number of packs."""
    files_per_pack = num_files // target_packs

    scenarios = [
        {
            'name': '100KB_packs',
            'pack_size': 100_000,  # 100KB
            'file_size': 100_000 // files_per_pack,  # ~1KB per file
            'description': '100KB packs with ~1KB files',
        },
        {
            'name': '1MB_packs',
            'pack_size': 1_000_000,  # 1MB
            'file_size': 1_000_000 // files_per_pack,  # ~10KB per file
            'description': '1MB packs with ~10KB files',
        },
    ]
    return scenarios


def setup_container_with_data(temp_container, generate_random_data, num_files, file_size, pack_size):
    """Helper function to set up container with test data."""
    data_dict = generate_random_data(
        num_files=num_files,
        min_size=file_size,
        max_size=file_size,
        seed=42,
    )
    data = list(data_dict.values())

    temp_container.init_container(clear=True, pack_size_target=pack_size)
    add_objects_in_batches(temp_container, data)

    # Verify setup
    counts = temp_container.count_objects()
    assert counts['loose'] == num_files, f'Expected {num_files} loose objects, got {counts["loose"]}'

    return data


def run_clean_final_approach(temp_container):
    """Helper function to run the clean_final approach."""
    temp_container.pack_all_loose(clean_loose_per_pack=False)
    temp_container.clean_storage()


def run_clean_each_approach(temp_container):
    """Helper function to run the clean_each approach."""
    temp_container.pack_all_loose(clean_loose_per_pack=True)


def add_benchmark_metadata(
    benchmark, approach, config_name, description, num_files, file_size, pack_size, temp_container
):
    """Helper function to add metadata to benchmark results."""
    final_counts = temp_container.count_objects()
    actual_packs = final_counts['pack_files']

    benchmark.extra_info.update(
        {
            'approach': approach,
            'config': config_name,
            'description': f'{description} - {num_files} files - {approach}',
            'num_files': num_files,
            'file_size': file_size,
            'pack_size': pack_size,
            'actual_packs': actual_packs,
            'total_data_size': num_files * file_size,
        }
    )


def create_benchmark_test(config_name, pack_size, file_size, description, num_files, approach):
    """Generic helper to create a benchmark test."""

    def test_function(benchmark, temp_container, generate_random_data):
        _ = setup_container_with_data(temp_container, generate_random_data, num_files, file_size, pack_size)

        if approach == 'clean_final':
            result = benchmark(run_clean_final_approach, temp_container)
        else:  # clean_each
            result = benchmark(run_clean_each_approach, temp_container)

        add_benchmark_metadata(
            benchmark, approach, config_name, description, num_files, file_size, pack_size, temp_container
        )
        return result

    return test_function


# =============================================================================
# TESTS FOR 10 FILES
# =============================================================================


@pytest.mark.benchmark(group='10_files_100KB_packs')
@pytest.mark.parametrize('approach', ['clean_final', 'clean_each'])
def test_clean_loose_10_files_100KB_packs(benchmark, temp_container, generate_random_data, approach):
    """10 files, 100KB packs - Compare both approaches"""
    _ = setup_container_with_data(temp_container, generate_random_data, 10, 10000, 100000)

    if approach == 'clean_final':
        _ = benchmark(run_clean_final_approach, temp_container)
    else:  # clean_each
        _ = benchmark(run_clean_each_approach, temp_container)

    add_benchmark_metadata(
        benchmark, approach, '100KB_packs', '100KB packs with ~10KB files', 10, 10000, 100000, temp_container
    )


@pytest.mark.benchmark(group='10_files_1MB_packs')
@pytest.mark.parametrize('approach', ['clean_final', 'clean_each'])
def test_clean_loose_10_files_1MB_packs(benchmark, temp_container, generate_random_data, approach):
    """10 files, 1MB packs - Compare both approaches"""
    _ = setup_container_with_data(temp_container, generate_random_data, 10, 100000, 1000000)

    if approach == 'clean_final':
        _ = benchmark(run_clean_final_approach, temp_container)
    else:  # clean_each
        _ = benchmark(run_clean_each_approach, temp_container)

    add_benchmark_metadata(
        benchmark, approach, '1MB_packs', '1MB packs with ~100KB files', 10, 100000, 1000000, temp_container
    )


# =============================================================================
# TESTS FOR 100 FILES
# =============================================================================


@pytest.mark.benchmark(group='100_files_100KB_packs')
@pytest.mark.parametrize('approach', ['clean_final', 'clean_each'])
def test_clean_loose_100_files_100KB_packs(benchmark, temp_container, generate_random_data, approach):
    """100 files, 100KB packs - Compare both approaches"""
    _ = setup_container_with_data(
        temp_container=temp_container,
        generate_random_data=generate_random_data,
        num_files=100,
        file_size=1000,
        pack_size=100000,
    )

    if approach == 'clean_final':
        _ = benchmark(run_clean_final_approach, temp_container)
    else:  # clean_each
        _ = benchmark(run_clean_each_approach, temp_container)

    add_benchmark_metadata(
        benchmark, approach, '100KB_packs', '100KB packs with ~1KB files', 100, 1000, 100000, temp_container
    )


@pytest.mark.benchmark(group='100_files_1MB_packs')
@pytest.mark.parametrize('approach', ['clean_final', 'clean_each'])
def test_clean_loose_100_files_1MB_packs(benchmark, temp_container, generate_random_data, approach):
    """100 files, 1MB packs - Compare both approaches"""
    _ = setup_container_with_data(
        temp_container=temp_container,
        generate_random_data=generate_random_data,
        num_files=100,
        file_size=10000,
        pack_size=1000000,
    )

    if approach == 'clean_final':
        _ = benchmark(run_clean_final_approach, temp_container)
    else:  # clean_each
        _ = benchmark(run_clean_each_approach, temp_container)

    add_benchmark_metadata(
        benchmark, approach, '1MB_packs', '1MB packs with ~10KB files', 100, 10000, 1000000, temp_container
    )


# =============================================================================
# TESTS FOR 1000 FILES
# =============================================================================


@pytest.mark.benchmark(group='1000_files_100KB_packs')
@pytest.mark.parametrize('approach', ['clean_final', 'clean_each'])
def test_clean_loose_1000_files_100KB_packs(benchmark, temp_container, generate_random_data, approach):
    """1000 files, 100KB packs - Compare both approaches"""
    _ = setup_container_with_data(
        temp_container=temp_container,
        generate_random_data=generate_random_data,
        num_files=1000,
        file_size=10000,
        pack_size=100000,
    )

    if approach == 'clean_final':
        _ = benchmark(run_clean_final_approach, temp_container)
    else:  # clean_each
        _ = benchmark(run_clean_each_approach, temp_container)

    add_benchmark_metadata(
        benchmark, approach, '100KB_packs', '100KB packs with ~1KB files', 1000, 1000, 100000, temp_container
    )


@pytest.mark.benchmark(group='1000_files_1MB_packs')
@pytest.mark.parametrize('approach', ['clean_final', 'clean_each'])
def test_clean_loose_1000_files_1MB_packs(benchmark, temp_container, generate_random_data, approach):
    """100 files, 1MB packs - Compare both approaches"""
    _ = setup_container_with_data(
        temp_container=temp_container,
        generate_random_data=generate_random_data,
        num_files=1000,
        file_size=100000,
        pack_size=1000000,
    )

    if approach == 'clean_final':
        _ = benchmark(run_clean_final_approach, temp_container)
    else:  # clean_each
        _ = benchmark(run_clean_each_approach, temp_container)

    add_benchmark_metadata(
        benchmark, approach, '1MB_packs', '1MB packs with ~10KB files', 1000, 10000, 1000000, temp_container
    )
