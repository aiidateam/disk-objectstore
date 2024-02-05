"""Test of the object-store container module."""

import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

import disk_objectstore
from disk_objectstore.utils import nullcontext

MODULE_DIR = Path(disk_objectstore.__file__).parent
EXAMPLES_DIR = MODULE_DIR / "examples"


@pytest.mark.parametrize(
    "idx_and_options",
    enumerate(
        [
            [],
            ["-c"],
            ["-d"],
            ["-z"],
            ["-d", "-z"],
            ["-B", "7"],  # Odd number of bulk calls
            ["-P", "TEMPFILE"],
        ]
    ),
)
def test_example_objectstore(temp_dir, idx_and_options):
    """Test the example/profiling script 'example_objectstore'."""
    idx, options = idx_and_options

    tempfile_idx = None
    try:
        tempfile_idx = options.index("TEMPFILE")
        context = tempfile.NamedTemporaryFile()
    except ValueError:
        # no need to create a tempfile
        context = nullcontext(enter_result=None)

    with context as tmpfile:
        if tempfile_idx is not None:
            options[tempfile_idx] = tmpfile.name
        script = EXAMPLES_DIR / "example_objectstore.py"
        output = subprocess.check_output(
            [sys.executable, script, "-p", str(temp_dir / str(idx))] + options
        )
        assert output != ""


@pytest.mark.parametrize(
    "idx_and_options",
    enumerate(
        [
            [],
            ["-c"],
            ["-m"],
            ["-z"],
            ["-z", "-m"],
            ["-l"],
            ["-m", "-l"],
        ]
    ),
)
def test_example_profile_zeros(temp_dir, idx_and_options):
    """Test the example/profiling script 'profile_zeros'."""
    idx, options = idx_and_options
    script = EXAMPLES_DIR / "profile_zeros.py"
    output = subprocess.check_output(
        [sys.executable, str(script), "-p", str(temp_dir / str(idx))] + options
    )
    assert output != ""
