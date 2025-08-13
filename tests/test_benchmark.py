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
        batch = data[i:i + batch_size]
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


@pytest.mark.benchmark(group='clean_loose_comparison')
@pytest.mark.parametrize('num_files', [10, 100, 1000])
@pytest.mark.parametrize('config', calculate_target_config(), ids=lambda c: c['name'])
def test_pack_clean_final_approach_100_packs(benchmark, temp_container, generate_random_data, config, num_files):
    """Benchmark CLEAN_FINAL approach: pack_all_loose() + clean_storage() at end."""

    pack_size = config['pack_size']
    file_size = config['file_size']

    # Use existing fixture - much cleaner!
    data_dict = generate_random_data(
        num_files=num_files,
        min_size=file_size,
        max_size=file_size,
        seed=42,
    )
    data = list(data_dict.values())

    def pack_clean_final_way():
        # Use standard temp_container fixture
        temp_container.init_container(clear=True, pack_size_target=pack_size)

        # Add objects in batches
        add_objects_in_batches(temp_container, data)

        # Verify setup
        counts = temp_container.count_objects()
        assert counts['loose'] == num_files, f'Expected {num_files} loose objects, got {counts["loose"]}'

        # CLEAN_FINAL APPROACH: Pack without cleaning during packing
        temp_container.pack_all_loose(clean_loose_per_pack=False)

        # Then clean storage at the end
        temp_container.clean_storage()

    result = benchmark(pack_clean_final_way)

    # Verify and add metadata
    final_counts = temp_container.count_objects()
    actual_packs = final_counts['pack_files']

    benchmark.extra_info.update({
        'approach': 'clean_final',
        'config': config['name'],
        'description': f"{config['description']} - {num_files} files",
        'num_files': num_files,
        'file_size': file_size,
        'pack_size': pack_size,
        'actual_packs': actual_packs,
        'total_data_size': len(data) * file_size,
    })


@pytest.mark.benchmark(group='clean_loose_comparison')
@pytest.mark.parametrize('num_files', [10, 100, 1000])
@pytest.mark.parametrize('config', calculate_target_config(), ids=lambda c: c['name'])
def test_pack_clean_each_approach_100_packs(benchmark, temp_container, generate_random_data, config, num_files):
    """Benchmark CLEAN_EACH approach: pack_all_loose(clean_loose_per_pack=True)."""

    pack_size = config['pack_size']
    file_size = config['file_size']

    # Use existing fixture
    data_dict = generate_random_data(
        num_files=num_files,
        min_size=file_size,
        max_size=file_size,
        seed=42,  # Same seed for fair comparison
    )
    data = list(data_dict.values())

    def pack_clean_each_way():
        temp_container.init_container(clear=True, pack_size_target=pack_size)

        # Add objects in batches
        add_objects_in_batches(temp_container, data)

        # Verify setup
        counts = temp_container.count_objects()
        assert counts['loose'] == num_files, f'Expected {num_files} loose objects, got {counts["loose"]}'

        # CLEAN_EACH APPROACH: Pack with cleaning after each pack
        temp_container.pack_all_loose(clean_loose_per_pack=True)

    result = benchmark(pack_clean_each_way)

    # Verify and add metadata
    final_counts = temp_container.count_objects()
    actual_packs = final_counts['pack_files']

    benchmark.extra_info.update({
        'approach': 'clean_each',
        'config': config['name'],
        'description': f"{config['description']} - {num_files} files",
        'num_files': num_files,
        'file_size': file_size,
        'pack_size': pack_size,
        'actual_packs': actual_packs,
        'total_data_size': len(data) * file_size,
    })

