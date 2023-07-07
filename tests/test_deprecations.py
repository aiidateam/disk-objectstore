"""Module to test deprecated functionality.

Both to check that they work, but also to ensure full coverage."""
import pytest

from disk_objectstore import utils


def test_get_hash():
    """Test the get_hash method."""
    hash_type = "sha256"
    content = b"523453dfvsd"
    with pytest.warns(DeprecationWarning, match="get_hash_cls"):
        hasher = utils.get_hash(hash_type=hash_type)()
    hasher.update(content)
    hashkey = hasher.hexdigest()
    assert hashkey == "11c4da82bc95154d2a3116e66c3d49568e4fd0f7184d44a9d611f2749539b7f6"
