"""Performance benchmarks for readline() and readlines() implementations using pytest-benchmark.

Run with: pytest tests/test_benchmark_readline.py --benchmark-only
Or with grouping: pytest tests/test_benchmark_readline.py --benchmark-only --benchmark-group-by=func
"""

import io
import os

import pytest

from disk_objectstore import utils

# Test data sizes
SMALL_SIZE_KB = 100  # 100 KB
MEDIUM_SIZE_KB = 1000  # 1 MB
LARGE_SIZE_KB = 10000  # 10 MB

# For quick tests during development, use smaller size
DEFAULT_SIZE_KB = SMALL_SIZE_KB


@pytest.fixture(scope='module')
def compressible_data():
    """Create highly compressible test data with newlines."""
    pattern = b'0123456789'
    newline_every = 100
    target_size = DEFAULT_SIZE_KB * 1024
    chunks = []
    current_size = 0

    while current_size < target_size:
        chunk_size = min(newline_every, target_size - current_size)
        chunk = (pattern * ((chunk_size // len(pattern)) + 1))[:chunk_size]
        chunks.append(chunk)
        chunks.append(b'\n')
        current_size += chunk_size + 1

    return b''.join(chunks)


@pytest.fixture(scope='module')
def uncompressible_data():
    """Create uncompressible (random) test data with newlines."""
    newline_every = 100
    target_size = DEFAULT_SIZE_KB * 1024
    chunks = []
    current_size = 0

    while current_size < target_size:
        chunk_size = min(newline_every, target_size - current_size)
        chunk = os.urandom(chunk_size)
        chunks.append(chunk)
        chunks.append(b'\n')
        current_size += chunk_size + 1

    return b''.join(chunks)


@pytest.fixture(scope='module')
def compressed_compressible_data(compressible_data):
    """Compress the compressible data."""
    compresser = utils.get_compressobj_instance('zlib+1')
    compressed = compresser.compress(compressible_data)
    compressed += compresser.flush()
    return compressed


@pytest.fixture(scope='module')
def compressed_uncompressible_data(uncompressible_data):
    """Compress the uncompressible data."""
    compresser = utils.get_compressobj_instance('zlib+1')
    compressed = compresser.compress(uncompressible_data)
    compressed += compresser.flush()
    return compressed


# ============================================================================
# BytesIO (BinaryIO) Benchmarks - Baseline
# ============================================================================


def test_benchmark_bytesio_read(benchmark, compressible_data):
    """Benchmark BytesIO read() - baseline for uncompressed."""

    def read_all():
        stream = io.BytesIO(compressible_data)
        return stream.read()

    result = benchmark(read_all)
    assert len(result) == len(compressible_data)


def test_benchmark_bytesio_readline(benchmark, compressible_data):
    """Benchmark BytesIO readline() in loop."""

    def readline_loop():
        stream = io.BytesIO(compressible_data)
        lines = []
        while True:
            line = stream.readline()
            if not line:
                break
            lines.append(line)
        return lines

    result = benchmark(readline_loop)
    assert len(result) > 0


def test_benchmark_bytesio_readlines(benchmark, compressible_data):
    """Benchmark BytesIO readlines()."""

    def readlines_all():
        stream = io.BytesIO(compressible_data)
        return stream.readlines()

    result = benchmark(readlines_all)
    assert len(result) > 0


# ============================================================================
# ZlibStreamDecompresser Benchmarks - Compressed Compressible Data
# ============================================================================


def test_benchmark_zlib_compressible_read(benchmark, compressed_compressible_data):
    """Benchmark ZlibStreamDecompresser read() on compressible data."""

    def read_all():
        stream = utils.ZlibStreamDecompresser(io.BytesIO(compressed_compressible_data))
        return stream.read()

    result = benchmark(read_all)
    assert len(result) > 0


def test_benchmark_zlib_compressible_readline(benchmark, compressed_compressible_data):
    """Benchmark ZlibStreamDecompresser readline() on compressible data."""

    def readline_loop():
        stream = utils.ZlibStreamDecompresser(io.BytesIO(compressed_compressible_data))
        lines = []
        while True:
            line = stream.readline()
            if not line:
                break
            lines.append(line)
        return lines

    result = benchmark(readline_loop)
    assert len(result) > 0


def test_benchmark_zlib_compressible_readlines(benchmark, compressed_compressible_data):
    """Benchmark ZlibStreamDecompresser readlines() on compressible data."""

    def readlines_all():
        stream = utils.ZlibStreamDecompresser(io.BytesIO(compressed_compressible_data))
        return stream.readlines()

    result = benchmark(readlines_all)
    assert len(result) > 0


# ============================================================================
# ZlibStreamDecompresser Benchmarks - Compressed Uncompressible Data
# ============================================================================


def test_benchmark_zlib_uncompressible_read(benchmark, compressed_uncompressible_data):
    """Benchmark ZlibStreamDecompresser read() on uncompressible data."""

    def read_all():
        stream = utils.ZlibStreamDecompresser(io.BytesIO(compressed_uncompressible_data))
        return stream.read()

    result = benchmark(read_all)
    assert len(result) > 0


def test_benchmark_zlib_uncompressible_readline(benchmark, compressed_uncompressible_data):
    """Benchmark ZlibStreamDecompresser readline() on uncompressible data."""

    def readline_loop():
        stream = utils.ZlibStreamDecompresser(io.BytesIO(compressed_uncompressible_data))
        lines = []
        while True:
            line = stream.readline()
            if not line:
                break
            lines.append(line)
        return lines

    result = benchmark(readline_loop)
    assert len(result) > 0


def test_benchmark_zlib_uncompressible_readlines(benchmark, compressed_uncompressible_data):
    """Benchmark ZlibStreamDecompresser readlines() on uncompressible data."""

    def readlines_all():
        stream = utils.ZlibStreamDecompresser(io.BytesIO(compressed_uncompressible_data))
        return stream.readlines()

    result = benchmark(readlines_all)
    assert len(result) > 0


# ============================================================================
# CallbackStreamWrapper Benchmarks
# ============================================================================


def test_benchmark_callback_wrapper_read(benchmark, compressible_data):
    """Benchmark CallbackStreamWrapper read() with no callback."""

    def read_all():
        base = io.BytesIO(compressible_data)
        stream = utils.CallbackStreamWrapper(base, callback=None)
        return stream.read()

    result = benchmark(read_all)
    assert len(result) == len(compressible_data)


def test_benchmark_callback_wrapper_readline(benchmark, compressible_data):
    """Benchmark CallbackStreamWrapper readline() with no callback."""

    def readline_loop():
        base = io.BytesIO(compressible_data)
        stream = utils.CallbackStreamWrapper(base, callback=None)
        lines = []
        while True:
            line = stream.readline()
            if not line:
                break
            lines.append(line)
        return lines

    result = benchmark(readline_loop)
    assert len(result) > 0


def test_benchmark_callback_wrapper_readlines(benchmark, compressible_data):
    """Benchmark CallbackStreamWrapper readlines() with no callback."""

    def readlines_all():
        base = io.BytesIO(compressible_data)
        stream = utils.CallbackStreamWrapper(base, callback=None)
        return stream.readlines()

    result = benchmark(readlines_all)
    assert len(result) > 0


# ============================================================================
# PackedObjectReader Benchmarks
# ============================================================================


def test_benchmark_packed_reader_read(benchmark, compressible_data, tmp_path):
    """Benchmark PackedObjectReader read()."""
    pack_file = tmp_path / 'pack'
    pack_file.write_bytes(compressible_data)

    def read_all():
        with open(pack_file, 'rb') as fh:
            reader = utils.PackedObjectReader(fh, offset=0, length=len(compressible_data))
            return reader.read()

    result = benchmark(read_all)
    assert len(result) == len(compressible_data)


def test_benchmark_packed_reader_readline(benchmark, compressible_data, tmp_path):
    """Benchmark PackedObjectReader readline()."""
    pack_file = tmp_path / 'pack'
    pack_file.write_bytes(compressible_data)

    def readline_loop():
        with open(pack_file, 'rb') as fh:
            reader = utils.PackedObjectReader(fh, offset=0, length=len(compressible_data))
            lines = []
            while True:
                line = reader.readline()
                if not line:
                    break
                lines.append(line)
        return lines

    result = benchmark(readline_loop)
    assert len(result) > 0


def test_benchmark_packed_reader_readlines(benchmark, compressible_data, tmp_path):
    """Benchmark PackedObjectReader readlines()."""
    pack_file = tmp_path / 'pack'
    pack_file.write_bytes(compressible_data)

    def readlines_all():
        with open(pack_file, 'rb') as fh:
            reader = utils.PackedObjectReader(fh, offset=0, length=len(compressible_data))
            return reader.readlines()

    result = benchmark(readlines_all)
    assert len(result) > 0


# ============================================================================
# Composed Stream Benchmarks (realistic use case)
# ============================================================================


def test_benchmark_composed_packed_compressed_read(benchmark, compressible_data, tmp_path):
    """Benchmark composed PackedObjectReader + ZlibStreamDecompresser read()."""
    # Compress data
    compresser = utils.get_compressobj_instance('zlib+1')
    compressed = compresser.compress(compressible_data)
    compressed += compresser.flush()

    # Write to pack file
    pack_file = tmp_path / 'pack_composed'
    pack_file.write_bytes(compressed)

    def read_all():
        with open(pack_file, 'rb') as fh:
            reader = utils.PackedObjectReader(fh, offset=0, length=len(compressed))
            decompressor = utils.ZlibStreamDecompresser(reader)
            return decompressor.read()

    result = benchmark(read_all)
    assert len(result) == len(compressible_data)


def test_benchmark_composed_packed_compressed_readline(benchmark, compressible_data, tmp_path):
    """Benchmark composed PackedObjectReader + ZlibStreamDecompresser readline()."""
    # Compress data
    compresser = utils.get_compressobj_instance('zlib+1')
    compressed = compresser.compress(compressible_data)
    compressed += compresser.flush()

    # Write to pack file
    pack_file = tmp_path / 'pack_composed'
    pack_file.write_bytes(compressed)

    def readline_loop():
        with open(pack_file, 'rb') as fh:
            reader = utils.PackedObjectReader(fh, offset=0, length=len(compressed))
            decompressor = utils.ZlibStreamDecompresser(reader)
            lines = []
            while True:
                line = decompressor.readline()
                if not line:
                    break
                lines.append(line)
        return lines

    result = benchmark(readline_loop)
    assert len(result) > 0


def test_benchmark_composed_packed_compressed_readlines(benchmark, compressible_data, tmp_path):
    """Benchmark composed PackedObjectReader + ZlibStreamDecompresser readlines()."""
    # Compress data
    compresser = utils.get_compressobj_instance('zlib+1')
    compressed = compresser.compress(compressible_data)
    compressed += compresser.flush()

    # Write to pack file
    pack_file = tmp_path / 'pack_composed'
    pack_file.write_bytes(compressed)

    def readlines_all():
        with open(pack_file, 'rb') as fh:
            reader = utils.PackedObjectReader(fh, offset=0, length=len(compressed))
            decompressor = utils.ZlibStreamDecompresser(reader)
            return decompressor.readlines()

    result = benchmark(readlines_all)
    assert len(result) > 0
