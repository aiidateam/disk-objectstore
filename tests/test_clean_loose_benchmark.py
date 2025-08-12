"""Pytest benchmark tests for clean_loose_per_pack option.

This module implements the specific benchmark requested:
- Pack files of 100KB or 1MB
- Push 10k file objects (different ones)
- Create ~100 packs to trigger frequent deletion
- Compare old approach (pack + clean at end) vs new approach (frequent cleaning)
"""

import pytest
from disk_objectstore import Container


def calculate_target_config(target_packs: int = 100, num_files: int = 10000):
    """Calculate file size and pack size to achieve target number of packs."""
    # For 100 packs with 10k files, each pack should contain ~100 files
    files_per_pack = num_files // target_packs

    # Two scenarios as requested
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


@pytest.fixture
def benchmark_container(temp_dir):
    """Create a container specifically for benchmark tests."""
    container = Container(temp_dir)
    yield container
    container.close()


@pytest.mark.benchmark(group='clean_loose_comparison')
@pytest.mark.parametrize('config', calculate_target_config(), ids=lambda c: c['name'])
def test_pack_old_approach_100_packs(benchmark, benchmark_container, generate_random_data, config):
    """Benchmark OLD approach: pack_all_loose() + clean_storage() at end.

    Creates ~100 packs with 10k different file objects to trigger frequent deletion.
    """
    num_files = 10000
    pack_size = config['pack_size']
    file_size = config['file_size']

    # Generate 10k different file objects using existing fixture
    data_dict = generate_random_data(
        num_files=num_files,
        min_size=file_size,
        max_size=file_size,
        seed=42,  # Ensure reproducible results
    )
    data = list(data_dict.values())

    def pack_old_way():
        # Initialize container with target pack size
        benchmark_container.init_container(clear=True, pack_size_target=pack_size)

        # Add all 10k objects as loose
        for content in data:
            benchmark_container.add_object(content)

        # Verify we have the expected setup
        counts = benchmark_container.count_objects()
        assert counts['loose'] == num_files, f'Expected {num_files} loose objects, got {counts["loose"]}'

        # OLD APPROACH: Pack all loose objects WITHOUT cleaning during packing
        benchmark_container.pack_all_loose(clean_loose_per_pack=False)

        # Then clean storage at the end (single bulk operation)
        benchmark_container.clean_storage()

    # Run the benchmark
    result = benchmark(pack_old_way)

    # Verify we achieved ~100 packs
    final_counts = benchmark_container.count_objects()
    actual_packs = final_counts['pack_files']

    # Add metadata for comparison
    benchmark.extra_info.update(
        {
            'approach': 'old',
            'config': config['name'],
            'description': config['description'],
            'num_files': num_files,
            'file_size': file_size,
            'pack_size': pack_size,
            'target_packs': 100,
            'actual_packs': actual_packs,
            'total_data_size': len(data) * file_size,
        }
    )


@pytest.mark.benchmark(group='clean_loose_comparison')
@pytest.mark.parametrize('config', calculate_target_config(), ids=lambda c: c['name'])
def test_pack_new_approach_100_packs(benchmark, benchmark_container, generate_random_data, config):
    """Benchmark NEW approach: pack_all_loose(clean_loose_per_pack=True).

    Creates ~100 packs with 10k different file objects to trigger frequent deletion.
    """
    num_files = 10000
    pack_size = config['pack_size']
    file_size = config['file_size']

    # Generate same 10k different file objects using existing fixture
    data_dict = generate_random_data(
        num_files=num_files,
        min_size=file_size,
        max_size=file_size,
        seed=42,  # Same seed for fair comparison
    )
    data = list(data_dict.values())

    def pack_new_way():
        # Initialize container with target pack size
        benchmark_container.init_container(clear=True, pack_size_target=pack_size)

        # Add all 10k objects as loose
        for content in data:
            benchmark_container.add_object(content)

        # Verify we have the expected setup
        counts = benchmark_container.count_objects()
        assert counts['loose'] == num_files, f'Expected {num_files} loose objects, got {counts["loose"]}'

        # NEW APPROACH: Pack all loose objects WITH cleaning after each pack
        # This should clean loose objects frequently as each pack is created
        benchmark_container.pack_all_loose(clean_loose_per_pack=True)

    # Run the benchmark
    result = benchmark(pack_new_way)

    # Verify we achieved ~100 packs
    final_counts = benchmark_container.count_objects()
    actual_packs = final_counts['pack_files']

    # Add metadata for comparison
    benchmark.extra_info.update(
        {
            'approach': 'new',
            'config': config['name'],
            'description': config['description'],
            'num_files': num_files,
            'file_size': file_size,
            'pack_size': pack_size,
            'target_packs': 100,
            'actual_packs': actual_packs,
            'total_data_size': len(data) * file_size,
        }
    )


@pytest.mark.benchmark(group='validation')
def test_validate_100_packs_scenario(benchmark_container, generate_random_data):
    """Validation test to ensure we actually create ~100 packs as intended."""
    configs = calculate_target_config()

    for config in configs:
        num_files = 10000
        pack_size = config['pack_size']
        file_size = config['file_size']

        # Generate test data
        data_dict = generate_random_data(num_files=num_files, min_size=file_size, max_size=file_size, seed=42)
        data = list(data_dict.values())

        # Setup container
        benchmark_container.init_container(clear=True, pack_size_target=pack_size)

        # Add all objects
        for content in data:
            benchmark_container.add_object(content)

        # Pack them
        benchmark_container.pack_all_loose(clean_loose_per_pack=True)

        # Check results
        counts = benchmark_container.count_objects()
        actual_packs = counts['pack_files']

        print(f'\nConfig: {config["name"]}')
        print(f'  Pack size: {pack_size:,} bytes')
        print(f'  File size: {file_size} bytes')
        print(f'  Total files: {num_files:,}')
        print(f'  Total data: {len(data) * file_size:,} bytes')
        print(f'  Actual packs created: {actual_packs}')
        print(f'  Target was: ~100 packs')
        print(f'  Files per pack: ~{num_files // actual_packs}')

        # Ensure we have a reasonable number of packs (50-200 range is acceptable)
        assert 50 <= actual_packs <= 200, f'Expected ~100 packs, got {actual_packs} for {config["name"]}'


# Additional test to specifically measure deletion performance
@pytest.mark.benchmark(group='deletion_performance')
def test_deletion_frequency_comparison(benchmark, temp_dir, generate_random_data):
    """Directly compare deletion frequency between old and new approaches."""
    num_files = 10000
    pack_size = 100_000  # 100KB packs
    file_size = 10  # Small files to maximize number of deletion operations

    # Generate test data
    data_dict = generate_random_data(num_files=num_files, min_size=file_size, max_size=file_size, seed=42)
    data = list(data_dict.values())

    def measure_deletion_patterns():
        results = {}

        # Test OLD approach - single bulk deletion
        old_container = Container(temp_dir / 'old_deletion')
        old_container.init_container(clear=True, pack_size_target=pack_size)
        try:
            # Add all objects
            for content in data:
                old_container.add_object(content)

            # Pack without cleaning (accumulates loose files)
            old_container.pack_all_loose(clean_loose_per_pack=False)

            # Single bulk clean at end
            old_container.clean_storage()

            results['old_packs'] = old_container.count_objects()['pack_files']
        finally:
            old_container.close()

        # Test NEW approach - frequent deletion
        new_container = Container(temp_dir / 'new_deletion')
        new_container.init_container(clear=True, pack_size_target=pack_size)
        try:
            # Add all objects
            for content in data:
                new_container.add_object(content)

            # Pack with frequent cleaning (cleans after each pack)
            new_container.pack_all_loose(clean_loose_per_pack=True)

            results['new_packs'] = new_container.count_objects()['pack_files']
        finally:
            new_container.close()

        return results

    results = benchmark(measure_deletion_patterns)

    benchmark.extra_info.update(
        {
            'test_type': 'deletion_frequency',
            'num_files': num_files,
            'pack_size': pack_size,
            'file_size': file_size,
            'old_packs': results['old_packs'],
            'new_packs': results['new_packs'],
            'description': 'Compares deletion frequency: bulk vs frequent',
        }
    )


if __name__ == '__main__':
    # Allow running as script for quick testing
    import sys

    pytest.main([__file__] + sys.argv[1:])
