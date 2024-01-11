"""Test the backup functionality.

"""

import platform
import random
import string
from pathlib import Path

import pytest

from disk_objectstore import backup_utils
from disk_objectstore.backup_utils import BackupError, BackupManager

pytestmark = pytest.mark.skipif(
    platform.system() == "Windows", reason="Backup not supported on Windows"
)


def _random_string(n=10):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=n))


def test_invalid_destination():
    """Test invalid destination with two colons."""
    dest = "localhost:/tmp/test:"
    with pytest.raises(ValueError, match="Invalid destination format"):
        BackupManager(dest, backup_utils.backup_logger)


def test_inaccessible_remote():
    """Test a remote destination of random characters that will not be accessible."""
    dest = f"_{_random_string()}:/tmp/test"
    with pytest.raises(BackupError, match="is not accessible"):
        BackupManager(dest, backup_utils.backup_logger)


def test_negative_keep():
    """Test a negative keep value."""
    dest = "/tmp/test"
    with pytest.raises(ValueError, match="keep variable can't be negative"):
        BackupManager(dest, backup_utils.backup_logger, keep=-1)


def test_inaccessible_exe():
    """Test case where rsync is not accessible."""
    dest = "/tmp/test"
    rsync_exe = f"_{_random_string()}"
    with pytest.raises(ValueError, match=f"{rsync_exe} not accessible."):
        BackupManager(dest, backup_utils.backup_logger, exes={"rsync": rsync_exe})


def test_inaccessible_path():
    """Test case where path is not accessible."""
    dest = f"/_{_random_string()}"  # I assume there will be a permission error for this path
    with pytest.raises(ValueError, match=f"Couldn't access/create '{dest}'"):
        BackupManager(dest, backup_utils.backup_logger)


def test_rsync_failure():
    """Test case where rsync fails."""
    dest = "/tmp/test"
    with pytest.raises(BackupError, match="rsync failed"):
        manager = BackupManager(dest, backup_utils.backup_logger)
        # pick a src that doesn't exists
        manager.call_rsync(Path(f"/_{_random_string()}"), Path(dest))


def test_rsync_dest_trailing_slash(temp_dir):
    """Test case for dest_trailing_slash."""
    dest1 = Path(temp_dir) / "dest1"
    dest2 = Path(temp_dir) / "dest2"
    # manager will create dest1 folder
    manager = BackupManager(str(dest1), backup_utils.backup_logger)
    # dest_trailing_slash=True will create dest2
    manager.call_rsync(dest1, dest2, dest_trailing_slash=True)
    assert dest2.exists()


def test_existing_backups_failure():
    """Test case where existing backups fail to be determined."""
    dest = "/tmp/test"
    with pytest.raises(BackupError, match="Existing backups determination failed"):
        manager = BackupManager(dest, backup_utils.backup_logger)
        # override the path to something that will fail
        manager.path = f"/_{_random_string()}"
        manager.get_existing_backup_folders()


def test_sqlite_failure(monkeypatch, temp_container, temp_dir):
    """Test case where sqlite fails to make a backup file."""

    # monkeypatch sqlite backup to do nothing
    def mock_sqlite_backup(src, dst):  # pylint: disable=unused-argument
        pass

    monkeypatch.setattr(
        backup_utils,
        "_sqlite_backup",
        mock_sqlite_backup,
    )

    # make a container
    temp_container.init_container(clear=True)
    # Add a few objects
    for idx in range(100):
        temp_container.add_object(f"test-{idx}".encode())

    dest = Path(temp_dir) / "backup"
    with pytest.raises(BackupError, match="'.*' failed to be created."):
        manager = BackupManager(str(dest), backup_utils.backup_logger)
        manager.backup_auto_folders(
            lambda path, prev: backup_utils.backup_container(
                manager, temp_container, path, prev
            )
        )


def test_mv_failure(monkeypatch, temp_container, temp_dir):
    """
    Test case where mv command fails by monkeypatching.
    Make sure correct BackupError is raised.
    """

    # save a reference to the original run_cmd command
    original_run_cmd = backup_utils.BackupManager.run_cmd

    # monkeypatch the run_cmd command to fail when "mv" is used
    def mock_run_cmd(self, args):
        if "mv" in args:
            return False, ""
        return original_run_cmd(self, args)

    monkeypatch.setattr(
        backup_utils.BackupManager,
        "run_cmd",
        mock_run_cmd,
    )

    # make a container and back it up
    temp_container.init_container(clear=True)
    # Add a few objects
    for idx in range(100):
        temp_container.add_object(f"test-{idx}".encode())

    dest = Path(temp_dir) / "backup"
    with pytest.raises(BackupError, match="Failed to move"):
        manager = BackupManager(str(dest), backup_utils.backup_logger)
        manager.backup_auto_folders(
            lambda path, prev: backup_utils.backup_container(
                manager, temp_container, path, prev
            )
        )


def test_ln_failure(monkeypatch, temp_container, temp_dir, caplog):
    """
    Test case where ln command fails by monkeypatching.
    Make sure correct warning is logged.
    """

    # save a reference to the original run_cmd command
    original_run_cmd = backup_utils.BackupManager.run_cmd

    # monkeypatch the run_cmd command to fail when "mv" is used
    def mock_run_cmd(self, args):
        if "ln" in args:
            return False, ""
        return original_run_cmd(self, args)

    monkeypatch.setattr(
        backup_utils.BackupManager,
        "run_cmd",
        mock_run_cmd,
    )

    # make a container and back it up
    temp_container.init_container(clear=True)
    # Add a few objects
    for idx in range(100):
        temp_container.add_object(f"test-{idx}".encode())

    dest = Path(temp_dir) / "backup"
    manager = BackupManager(str(dest), backup_utils.backup_logger)
    manager.backup_auto_folders(
        lambda path, prev: backup_utils.backup_container(
            manager, temp_container, path, prev
        )
    )
    assert "Couldn't create symlink" in caplog.text


def test_rm_failure(monkeypatch, temp_container, temp_dir, caplog):
    """
    Test case where rm command fails by monkeypatching.
    Make sure correct warning is logged.
    Note, this is used for deleting old backups, so create two with keep=0.
    """

    # save a reference to the original run_cmd command
    original_run_cmd = backup_utils.BackupManager.run_cmd

    # monkeypatch the run_cmd command to fail when "mv" is used
    def mock_run_cmd(self, args):
        if "rm" in args:
            return False, ""
        return original_run_cmd(self, args)

    monkeypatch.setattr(
        backup_utils.BackupManager,
        "run_cmd",
        mock_run_cmd,
    )

    # make a container and back it up
    temp_container.init_container(clear=True)
    # Add a few objects
    for idx in range(100):
        temp_container.add_object(f"test-{idx}".encode())

    dest = Path(temp_dir) / "backup"
    manager = BackupManager(str(dest), backup_utils.backup_logger, keep=0)
    for _ in range(2):
        manager.backup_auto_folders(
            lambda path, prev: backup_utils.backup_container(
                manager, temp_container, path, prev
            )
        )
    assert "Warning: couldn't delete old backup" in caplog.text
