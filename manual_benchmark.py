"""Manual benchmark to test the new `clean_loose_per_pack` option.

This benchmark creates many small files to trigger the creation of multiple packs,
then compares the performance of:
1. Old approach: pack_all_loose() + clean_storage() at the end
2. New approach: pack_all_loose(clean_loose_per_pack=True) with frequent cleaning

The goal is to see if frequent cleaning has performance implications.
"""

import os
import tempfile
import time
from pathlib import Path

from disk_objectstore import Container


def create_test_data(num_files: int, file_size: int) -> list[bytes]:
    """Create test data with unique content for each file."""
    data = []
    base_content = 'x' * max(1, file_size - 20)  # Leave space for unique prefix
    
    for i in range(num_files):
        # Create unique content for each file to avoid deduplication
        prefix = f'file-{i:08d}-'
        # Adjust content to match target size
        remaining_size = file_size - len(prefix.encode('ascii'))
        if remaining_size > 0:
            content = prefix + base_content[:remaining_size]
        else:
            content = prefix[:file_size]
        data.append(content.encode('ascii'))
    return data


def print_container_info(container: Container, container_path: Path, label: str, verbose: bool = True):
    """Print detailed container information."""
    counts = container.count_objects()
    print(f'  {label}: {counts["loose"]} loose, {counts["packed"]} packed, {counts["pack_files"]} pack files')
    
    if verbose:
        # Print directory information
        loose_dir = container_path / 'loose'
        pack_dir = container_path / 'packs'
        
        loose_files = list(loose_dir.glob('*/*')) if loose_dir.exists() else []
        pack_files = list(pack_dir.glob('*')) if pack_dir.exists() else []
        
        print(f'    Container directory: {container_path}')
        print(f'    Loose files on disk: {len(loose_files)} (in {loose_dir})')
        print(f'    Pack files on disk: {len(pack_files)} (in {pack_dir})')
        
        if loose_files:
            # Show first few loose files as examples
            example_files = loose_files[:3]
            print(f'    Example loose files: {[str(f.relative_to(container_path)) for f in example_files]}')
        
        if pack_files:
            # Show pack file sizes
            pack_sizes = [(f.name, f.stat().st_size) for f in pack_files]
            print(f'    Pack file sizes: {pack_sizes[:3]}{"..." if len(pack_sizes) > 3 else ""}')


def benchmark_old_approach(container_path: Path, data: list[bytes], verbose: bool = True, pause_between_steps: bool = False) -> tuple[float, float]:
    """Benchmark the old approach: pack_all_loose() + clean_storage() at the end."""
    print('Testing OLD approach: pack_all_loose() + clean_storage() at end')

    # Initialize container with small pack size to force many packs
    container = Container(container_path)
    pack_size = max(100_000, sum(len(d) for d in data[:10]) * 2)  # Adaptive pack size
    container.init_container(clear=True, pack_size_target=pack_size)

    try:
        # Add all objects as loose
        print(f'  Adding {len(data)} loose objects...')
        add_start = time.perf_counter()
        for i, content in enumerate(data):
            container.add_object(content)
            if verbose and i % 1000 == 0 and i > 0:
                print(f'    Added {i}/{len(data)} objects...')
        add_time = time.perf_counter() - add_start

        # Check initial state
        print_container_info(container, container_path, 'Initial state', verbose)
        
        if pause_between_steps:
            input("  Press Enter to continue to packing step...")

        # Pack all loose objects (old way - no cleaning during packing)
        print('  Packing all loose objects...')
        pack_start = time.perf_counter()
        container.pack_all_loose(clean_loose_per_pack=False)
        pack_time = time.perf_counter() - pack_start

        # Check state after packing
        print_container_info(container, container_path, 'After packing', verbose)
        
        if pause_between_steps:
            input("  Press Enter to continue to cleaning step...")

        # Clean storage at the end
        print('  Cleaning storage at the end...')
        clean_start = time.perf_counter()
        container.clean_storage()
        clean_time = time.perf_counter() - clean_start

        # Final state
        print_container_info(container, container_path, 'Final state', verbose)

        total_time = pack_time + clean_time
        print(f'  Add time: {add_time:.3f}s, Pack time: {pack_time:.3f}s, Clean time: {clean_time:.3f}s, Total: {total_time:.3f}s')

        return pack_time, clean_time

    finally:
        container.close()


def benchmark_new_approach(container_path: Path, data: list[bytes], verbose: bool = True, pause_between_steps: bool = False) -> float:
    """Benchmark the new approach: pack_all_loose(clean_loose_per_pack=True)."""
    print('\nTesting NEW approach: pack_all_loose(clean_loose_per_pack=True)')

    # Initialize container with small pack size to force many packs
    container = Container(container_path)
    pack_size = max(100_000, sum(len(d) for d in data[:10]) * 2)  # Adaptive pack size
    container.init_container(clear=True, pack_size_target=pack_size)

    try:
        # Add all objects as loose
        print(f'  Adding {len(data)} loose objects...')
        add_start = time.perf_counter()
        for i, content in enumerate(data):
            container.add_object(content)
            if verbose and i % 1000 == 0 and i > 0:
                print(f'    Added {i}/{len(data)} objects...')
        add_time = time.perf_counter() - add_start

        # Check initial state
        print_container_info(container, container_path, 'Initial state', verbose)
        
        if pause_between_steps:
            input("  Press Enter to continue to packing step...")

        # Pack all loose objects (new way - clean after each pack)
        print('  Packing all loose objects with frequent cleaning...')
        pack_start = time.perf_counter()
        container.pack_all_loose(clean_loose_per_pack=True)
        pack_time = time.perf_counter() - pack_start

        # Check final state
        print_container_info(container, container_path, 'Final state', verbose)

        print(f'  Add time: {add_time:.3f}s, Total time: {pack_time:.3f}s')

        return pack_time

    finally:
        container.close()


def run_benchmark_comparison(num_files: int, file_size: int, pack_size: int, verbose: bool, pause_between_steps: bool, keep_temp: bool):
    """Run the benchmark comparison between old and new approaches."""
    print('=' * 70)
    print('Benchmark: clean_loose_per_pack performance comparison')
    print('=' * 70)

    print(f'Configuration:')
    print(f'  Number of files: {num_files:,}')
    print(f'  File size: {file_size:,} bytes')
    print(f'  Pack size target: {pack_size:,} bytes ({pack_size//1000}KB)')
    
    # Create test data
    print('\nGenerating test data...')
    data = create_test_data(num_files, file_size)
    total_size = sum(len(d) for d in data)
    expected_packs = max(1, total_size // pack_size)
    print(f'Generated {len(data):,} unique files')
    print(f'Total data size: {total_size:,} bytes ({total_size//1024:.1f} KB)')
    print(f'Expected number of packs: ~{expected_packs}')
    print()

    if keep_temp:
        # Create a named temporary directory that won't be cleaned up
        temp_dir = tempfile.mkdtemp(prefix='benchmark_')
        temp_path = Path(temp_dir)
        print(f'Using persistent temp directory: {temp_path}')
        print(f'(Remember to clean up manually: rm -rf {temp_path})')
    else:
        temp_context = tempfile.TemporaryDirectory()
        temp_path = Path(temp_context.__enter__())

    try:
        # Test old approach
        old_container_path = temp_path / 'old_approach'
        old_container_path.mkdir(parents=True, exist_ok=True)
        print(f'\nOld approach container: {old_container_path}')
        old_pack_time, old_clean_time = benchmark_old_approach(old_container_path, data, verbose, pause_between_steps)
        old_total_time = old_pack_time + old_clean_time

        # Test new approach
        new_container_path = temp_path / 'new_approach'
        new_container_path.mkdir(parents=True, exist_ok=True)
        print(f'\nNew approach container: {new_container_path}')
        new_total_time = benchmark_new_approach(new_container_path, data, verbose, pause_between_steps)

        # Compare results
        print('\n' + '=' * 70)
        print('RESULTS COMPARISON')
        print('=' * 70)
        print(f'Old approach (pack + clean at end):')
        print(f'  Pack time:  {old_pack_time:.3f}s')
        print(f'  Clean time: {old_clean_time:.3f}s')
        print(f'  Total time: {old_total_time:.3f}s')
        print()
        print(f'New approach (clean per pack):')
        print(f'  Total time: {new_total_time:.3f}s')
        print()

        # Performance analysis
        if new_total_time < old_total_time:
            improvement = ((old_total_time - new_total_time) / old_total_time) * 100
            print(f'✅ New approach is FASTER by {improvement:.1f}% ({old_total_time - new_total_time:.3f}s)')
        elif new_total_time > old_total_time:
            degradation = ((new_total_time - old_total_time) / old_total_time) * 100
            print(f'⚠️  New approach is SLOWER by {degradation:.1f}% (+{new_total_time - old_total_time:.3f}s)')
        else:
            print('🔄 Both approaches have similar performance')

        print()
        print('Analysis:')
        print('- The new approach cleans loose objects after each pack is created')
        print('- This should reduce memory pressure and disk space usage during packing')
        print('- Performance difference may depend on filesystem and I/O characteristics')
        print('- The new approach provides more predictable disk space usage')

        if keep_temp:
            print(f'\nContainer directories preserved at:')
            print(f'  Old approach: {old_container_path}')
            print(f'  New approach: {new_container_path}')

    finally:
        if not keep_temp:
            temp_context.__exit__(None, None, None)


def run_extended_benchmark(num_files: int, file_size: int, verbose: bool):
    """Run an extended benchmark with different pack sizes."""
    print('=' * 70)
    print('Extended Benchmark: Testing different pack sizes')
    print('=' * 70)

    # Calculate pack sizes relative to total data size
    total_data_size = num_files * file_size
    pack_sizes = [
        (total_data_size // 20, f'{total_data_size // 20 // 1000}KB'),  # Many small packs
        (total_data_size // 10, f'{total_data_size // 10 // 1000}KB'),  # Medium packs
        (total_data_size // 5, f'{total_data_size // 5 // 1000}KB'),   # Fewer, larger packs
    ]

    print(f'Using {num_files:,} files of {file_size} bytes each (total: {total_data_size:,} bytes)')

    for pack_size, size_desc in pack_sizes:
        print(f'\n--- Testing with {size_desc} pack size ({pack_size:,} bytes) ---')

        # Create test data
        data = create_test_data(num_files, file_size)
        estimated_packs = max(1, total_data_size // pack_size)
        print(f'Estimated packs: ~{estimated_packs}')

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Test old approach
            print('  Old approach...')
            container = Container(temp_path / 'old')
            container.init_container(clear=True, pack_size_target=pack_size)

            try:
                for content in data:
                    container.add_object(content)

                start_time = time.perf_counter()
                container.pack_all_loose(clean_loose_per_pack=False)
                container.clean_storage()
                old_time = time.perf_counter() - start_time
            finally:
                container.close()

            # Test new approach
            print('  New approach...')
            container = Container(temp_path / 'new')
            container.init_container(clear=True, pack_size_target=pack_size)

            try:
                for content in data:
                    container.add_object(content)

                start_time = time.perf_counter()
                container.pack_all_loose(clean_loose_per_pack=True)
                new_time = time.perf_counter() - start_time
            finally:
                container.close()

            # Compare
            if new_time < old_time:
                diff_pct = ((old_time - new_time) / old_time) * 100
                print(f'  Result: New approach faster by {diff_pct:.1f}% ({old_time:.3f}s vs {new_time:.3f}s)')
            else:
                diff_pct = ((new_time - old_time) / old_time) * 100
                print(f'  Result: New approach slower by {diff_pct:.1f}% ({old_time:.3f}s vs {new_time:.3f}s)')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Benchmark clean_loose_per_pack option')
    parser.add_argument('--extended', action='store_true', 
                        help='Run extended benchmark with different pack sizes')
    parser.add_argument('--num-files', type=int, default=10000,
                        help='Number of files to create (default: 10000)')
    parser.add_argument('--file-size', type=int, default=100,
                        help='Size of each file in bytes (default: 100)')
    parser.add_argument('--pack-size', type=int, default=100000,
                        help='Pack size target in bytes (default: 100000)')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Print verbose output including directory paths and file counts')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Reduce output verbosity')
    parser.add_argument('--pause-between-steps', action='store_true',
                        help='Pause between benchmark steps for manual inspection')
    parser.add_argument('--keep-temp', action='store_true',
                        help='Keep temporary directories after benchmark (for manual inspection)')

    args = parser.parse_args()

    # Determine verbosity
    verbose = args.verbose and not args.quiet

    if args.extended:
        run_extended_benchmark(args.num_files, args.file_size, verbose)
    else:
        run_benchmark_comparison(
            num_files=args.num_files,
            file_size=args.file_size, 
            pack_size=args.pack_size,
            verbose=verbose,
            pause_between_steps=args.pause_between_steps,
            keep_temp=args.keep_temp
        )
