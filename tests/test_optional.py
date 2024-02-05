"""Additional optional tests to check additional functionality, such as
if the library works also with other external optional modules."""

from pathlib import Path

import numpy as np
import pytest


@pytest.mark.parametrize(
    "do_pack,compress", [[False, False], [True, False], [True, True]]
)
@pytest.mark.parametrize("hdf5_compression", [None, "gzip"])
def test_hdf5(temp_container, temp_dir, hdf5_compression, do_pack, compress):
    """Write and read a h5py file.

    This test is relevnt because when reading a HDF5 file, the library uses whence=1 or 2,
    we thus want to check that this works correctly also when using various versions of
    the disk-objectstore."""
    h5py = pytest.importorskip("h5py")

    ref = np.random.rand(100, 100)

    # Create an h5 file
    filepath = Path(temp_dir) / "array.h5"
    with h5py.File(filepath, "w") as h5obj:
        h5obj.create_dataset("array", data=ref, compression=hdf5_compression)

    with open(filepath, "rb") as fhandle:
        hashkey = temp_container.add_streamed_object(fhandle)

    if do_pack:
        temp_container.pack_all_loose(compress=compress)
        temp_container.clean_storage()

    # Read from the file
    with temp_container.get_object_stream(hashkey) as stream:
        with h5py.File(stream, "r") as h5obj:
            # Read the data back, the [:] is needed to return
            # the numpy array (in memory)
            data = h5obj["array"][:]

    assert np.allclose(data, ref)
