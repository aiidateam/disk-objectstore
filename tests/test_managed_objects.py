"""Tests for managed objects, whose lifetime the writer owns."""

import io
import shutil
from pathlib import Path

import pytest

from disk_objectstore import Container
from disk_objectstore.exceptions import NotExistent

PAYLOAD: bytes = b'the content of a managed object'


def test_a_managed_object_round_trips(temp_container: Container) -> None:
    """Test that what was written comes back, by content and by stream."""
    hashkey = temp_container.add_managed_object(PAYLOAD)

    assert temp_container.get_managed_object_content(hashkey) == PAYLOAD

    with temp_container.get_managed_object_stream(hashkey) as handle:
        assert handle.read() == PAYLOAD


def test_a_managed_object_round_trips_from_a_stream(temp_container: Container) -> None:
    """Test that a large object is written in chunks."""
    content: bytes = PAYLOAD * 100_000
    hashkey = temp_container.add_streamed_managed_object(io.BytesIO(content))

    assert temp_container.get_managed_object_content(hashkey) == content


def test_the_same_content_yields_one_managed_object(temp_container: Container) -> None:
    """Test that writing the same content twice yields one object.

    A caller replacing an unchanged payload should not be made to delete and rewrite it.
    """
    first = temp_container.add_managed_object(PAYLOAD)
    second = temp_container.add_managed_object(PAYLOAD)

    assert first == second
    assert list(temp_container.list_managed_objects()) == [first]


def test_list_all_objects_excludes_managed_objects(temp_container: Container) -> None:
    """Test that a managed object is invisible to the sweep that collects unreferenced objects.

    This is the point of the whole thing: it lets a caller record the key wherever suits it and still keep the
    object for as long as it wants.
    """
    managed = temp_container.add_managed_object(PAYLOAD)
    ordinary = temp_container.add_object(b'an ordinary object')

    assert set(temp_container.list_all_objects()) == {ordinary}
    assert list(temp_container.list_managed_objects()) == [managed]
    assert temp_container.count_objects().loose == 1


def test_pack_all_loose_excludes_managed_objects(temp_container: Container) -> None:
    """Test that packing moves the ordinary objects and not the managed ones."""
    managed = temp_container.add_managed_object(PAYLOAD)
    temp_container.add_object(b'an ordinary object')
    temp_container.pack_all_loose()

    assert temp_container.count_objects().packed == 1
    assert list(temp_container.list_managed_objects()) == [managed]
    assert temp_container.get_managed_object_content(managed) == PAYLOAD


def test_clean_storage_retains_managed_objects(temp_container: Container) -> None:
    """Test that `clean_storage` preserves a managed object."""
    managed = temp_container.add_managed_object(PAYLOAD)
    temp_container.add_object(b'an ordinary object')
    temp_container.pack_all_loose()
    temp_container.clean_storage()

    assert temp_container.get_managed_object_content(managed) == PAYLOAD


def test_delete_returns_the_hash_keys_removed(temp_container: Container) -> None:
    """Test that deletion reports what it removed and is quiet about what was not there."""
    hashkey = temp_container.add_managed_object(PAYLOAD)

    assert temp_container.delete_managed_objects([hashkey]) == {hashkey}
    assert not temp_container.has_managed_object(hashkey)
    assert temp_container.delete_managed_objects([hashkey]) == set()
    assert list(temp_container.list_managed_objects()) == []


def test_reading_a_missing_managed_object_raises(temp_container: Container) -> None:
    """Test that reading a missing object raises."""
    with pytest.raises(NotExistent, match='No managed object with hash key'):
        temp_container.get_managed_object_content('0' * 64)


def test_namespaces_store_identical_content_independently(temp_container: Container) -> None:
    """Test that the two namespaces stay independent, even for identical content."""
    ordinary = temp_container.add_object(PAYLOAD)

    assert not temp_container.has_managed_object(ordinary)

    managed = temp_container.add_managed_object(PAYLOAD)

    assert managed == ordinary
    assert temp_container.delete_managed_objects([managed]) == {managed}
    assert temp_container.get_object_content(ordinary) == PAYLOAD


def test_a_container_without_the_managed_folder_stays_valid(temp_dir: Path) -> None:
    """Test that a container lacking the folder stays valid, and grows one when first used.

    Requiring the folder would make every container written by an earlier version report itself uninitialised.
    """
    container = Container(temp_dir)
    container.init_container(clear=True)
    shutil.rmtree(container._get_managed_folder())

    assert container.is_initialised
    assert list(container.list_managed_objects()) == []

    hashkey = container.add_managed_object(PAYLOAD)

    assert container.get_managed_object_content(hashkey) == PAYLOAD


def test_writing_a_managed_object_modifies_only_the_managed_folder(temp_container: Container) -> None:
    """Test that a managed write leaves loose, packs and duplicates exactly as it found them.

    The two namespaces stay apart. `clean_storage` resolves a duplicate against the loose objects, so a managed
    object reaching that folder would either break it for the whole container or be promoted into `loose`.
    """
    ordinary: dict[str, Path] = {
        'loose': temp_container._get_loose_folder(),
        'packs': temp_container._get_pack_folder(),
        'duplicates': temp_container._get_duplicates_folder(),
    }
    before: dict[str, list[Path]] = {name: sorted(folder.rglob('*')) for name, folder in ordinary.items()}

    temp_container.add_managed_object(PAYLOAD)
    temp_container.add_managed_object(PAYLOAD * 2)

    for name, folder in ordinary.items():
        assert sorted(folder.rglob('*')) == before[name], f'a managed write reached the {name} folder'


def test_a_failed_write_removes_its_staged_file(temp_container: Container) -> None:
    """Test that a managed write clears its staged file, including when the stream fails halfway."""

    class Failing:
        """A stream that breaks partway through being read."""

        def read(self, size: int = -1) -> bytes:
            msg = 'the stream broke'
            raise OSError(msg)

    with pytest.raises(OSError, match='the stream broke'):
        temp_container.add_streamed_managed_object(Failing())

    temp_container.add_managed_object(PAYLOAD)

    assert sorted(temp_container._get_sandbox_folder().rglob('*')) == []


def test_losing_the_rename_to_the_same_content_still_succeeds(
    temp_container: Container, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that a write whose rename fails succeeds when the object it would have written is there.

    Two writers of the same content produce the same path, and on Windows the rename raises while the winner
    holds the file open.
    """

    def replace(src: Path, dst: Path) -> None:
        Path(dst).write_bytes(PAYLOAD)
        msg = 'the destination is held open'
        raise PermissionError(msg)

    monkeypatch.setattr('os.replace', replace)
    hashkey = temp_container.add_managed_object(PAYLOAD)
    monkeypatch.undo()

    assert temp_container.get_managed_object_content(hashkey) == PAYLOAD


def test_a_rename_that_leaves_no_object_raises(temp_container: Container, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that a write whose rename fails with nothing in place reports the failure."""

    def replace(src: Path, dst: Path) -> None:
        msg = 'the disk is full'
        raise OSError(msg)

    monkeypatch.setattr('os.replace', replace)

    with pytest.raises(OSError, match='the disk is full'):
        temp_container.add_managed_object(PAYLOAD)

    monkeypatch.undo()

    assert list(temp_container.list_managed_objects()) == []
    assert sorted(temp_container._get_sandbox_folder().rglob('*')) == []
