"""
Utilities to back up a container.
"""

import logging
import shutil
import sqlite3
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from disk_objectstore.container import Container

logger = logging.getLogger(__name__)


def _log(msg, end="\n"):
    print(msg, end=end)


def split_remote_and_path(dest: str):
    """extract remote and path from <remote>:<path>"""
    split_dest = dest.split(":")
    if len(split_dest) == 1:
        return None, Path(dest)
    if len(split_dest) == 2:
        return split_dest[0], Path(split_dest[1])
    # more than 1 colon:
    raise ValueError


def is_exe_found(exe: str) -> bool:
    return shutil.which(exe) is not None


def run_cmd(args: list, remote: Optional[str] = None, check: bool = True) -> bool:
    """
    Run a command locally or remotely.
    """
    all_args = args[:]
    if remote:
        all_args = ["ssh", remote] + all_args

    try:
        res = subprocess.run(all_args, capture_output=True, text=True, check=check)
    except subprocess.CalledProcessError as exc:
        _log("Error: " + str(exc))
        return False

    _log(f"stdout: {all_args}\n{res.stdout}")
    _log(f"stderr: {all_args}\n{res.stderr}")

    success = not bool(res.returncode)

    return success


def check_if_remote_accessible(remote: str) -> bool:
    """Check if remote host is accessible via ssh"""
    _log(f"Checking if '{remote}' is accessible...", end="")
    success = run_cmd(["exit"], remote=remote)
    if not success:
        _log(f"Error: Remote '{remote}' is not accessible!")
        return False
    _log(f"Success! '{remote}' is accessible!")
    return True


def check_path_exists(path: Path, remote: Optional[str] = None) -> bool:
    cmd = ["[", "-e", str(path), "]"]
    return run_cmd(cmd, remote=remote, check=False)


def call_rsync(  # pylint: disable=too-many-arguments
    args: list,
    src: Path,
    dest: Path,
    link_dest: Optional[Path] = None,
    remote: Optional[str] = None,
    src_trailing_slash: bool = False,
    dest_trailing_slash: bool = False,
) -> bool:
    """Call rsync with specified arguments and handle possible errors & stdout/stderr

    :param link_dest:
        Path to the hardlinked files location (previous backup).

    :param src_trailing_slash:
        Add a trailing slash to the source path. This makes rsync copy the contents
        of the folder instead of the folder itself.

    :param dest_trailing_slash:
        Add a trailing slash to the destination path. This makes rsync interpret the
        destination as a folder and create it if it doesn't exists.

    :return:
        True if successful and False if unsuccessful.
    """

    all_args = args[:]
    if link_dest:
        if not remote:
            # for local paths, use resolve() to get absolute path
            link_dest_str = str(link_dest.resolve())
        else:
            # for remote paths, we require absolute paths anyways
            link_dest_str = str(link_dest)
        all_args += [f"--link-dest={link_dest_str}"]

    if src_trailing_slash:
        all_args += [str(src) + "/"]
    else:
        all_args += [str(src)]

    dest_str = str(dest)
    if dest_trailing_slash:
        dest_str += "/"

    if not remote:
        all_args += [dest_str]
    else:
        all_args += [f"{remote}:{dest_str}"]

    try:
        res = subprocess.run(all_args, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as exc:
        _log(f"Error: {exc}")
        return False

    _log(f"stdout: {all_args}\n{res.stdout}")
    _log(f"stderr: {all_args}\n{res.stderr}")

    success = not bool(res.returncode)

    return success


def validate_inputs(
    path: Path,
    remote: Optional[str] = None,
    rsync_exe: str = "rsync",
) -> bool:
    """Validate inputs to the backup cli command

    :return:
        True if validation passes, False otherwise.
    """
    if remote:
        if not check_if_remote_accessible(remote):
            return False

    if not is_exe_found(rsync_exe):
        _log(f"Error: {rsync_exe} not accessible.")
        return False

    path_exists = check_path_exists(path, remote)

    if not path_exists:
        success = run_cmd(["mkdir", str(path)], remote=remote)
        if not success:
            _log(f"Error: Couldn't access/create '{str(path)}'!")
            return False

    return True


def backup_container(  # pylint: disable=too-many-return-statements, too-many-branches
    container: Container,
    path: Path,
    remote: Optional[str] = None,
    prev_backup: Optional[Path] = None,
    rsync_exe: str = "rsync",
) -> bool:
    """Create a backup of the disk-objectstore container

    This is safe to perform when the container is being used.

    It should be done in the following order:
        1) loose files;
        2) sqlite database;
        3) packed files.

    :return:
        True if successful and False if unsuccessful.
    """

    # subprocess arguments shared by all rsync calls:
    rsync_args = [rsync_exe, "-azh", "-vv", "--no-whole-file"]

    container_root_path = container.get_folder()
    loose_path = container._get_loose_folder()  # pylint: disable=protected-access
    packs_path = container._get_pack_folder()  # pylint: disable=protected-access
    sqlite_path = container._get_pack_index_path()  # pylint: disable=protected-access

    # step 1: back up loose files
    loose_path_rel = loose_path.relative_to(container_root_path)
    prev_backup_loose = prev_backup / loose_path_rel if prev_backup else None
    success = call_rsync(
        rsync_args, loose_path, path, remote=remote, link_dest=prev_backup_loose
    )
    if not success:
        return False

    # step 2: back up sqlite db

    # make a temporary directory to dump sqlite db locally
    with tempfile.TemporaryDirectory() as temp_dir_name:
        sqlite_temp_loc = Path(temp_dir_name) / "packs.idx"

        # Safe way to make a backup of the sqlite db, while it might potentially be accessed
        # https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.backup
        src = sqlite3.connect(str(sqlite_path))
        dst = sqlite3.connect(str(sqlite_temp_loc))
        with dst:
            src.backup(dst)
        dst.close()
        src.close()

        if sqlite_temp_loc.is_file():
            _log(f"Dumped the SQLite database to {str(sqlite_temp_loc)}")
        else:
            _log(f"Error: '{str(sqlite_temp_loc)}' was not created.")
            return False

        # step 3: transfer the SQLITE database file
        success = call_rsync(
            rsync_args, sqlite_temp_loc, path, remote=remote, link_dest=prev_backup
        )
        if not success:
            return False

    # step 4: transfer the packed files
    packs_path_rel = packs_path.relative_to(container_root_path)
    success = call_rsync(
        rsync_args, packs_path, path, remote=remote, link_dest=prev_backup
    )
    if not success:
        return False

    # step 5: transfer anything else in the container folder
    success = call_rsync(
        rsync_args
        + [
            "--exclude",
            str(loose_path_rel),
            "--exclude",
            "packs.idx",
            "--exclude",
            str(packs_path_rel),
        ],
        container_root_path,
        path,
        link_dest=prev_backup,
        remote=remote,
        src_trailing_slash=True,
    )
    if not success:
        return False

    return True


def backup_auto_folders(
    container: Container,
    path: Path,
    remote: Optional[str] = None,
    rsync_exe: str = "rsync",
):
    """Create a backup, managing live and previous backup folders automatically

    The running backup is done to `<path>/live-backup`. When it completes, it is moved to
    the final path: `<path>/last-backup`. This done so that the last backup wouldn't be
    corrupted, in case the live one crashes or gets interrupted. Rsync `link-dest` is used between
    the two folders to keep the backups incremental and performant.

    :param path:
        Path to where the backup will be created. If 'remote' is specified, must be an absolute path,
        otherwise can be relative.

    :param remote:
        Remote host of the backup location. 'ssh' executable is called via subprocess and therefore remote
        hosts configured for it are supported (e.g. via .ssh/config file).

    :param kwargs:
        * Executable paths if not default, e.g. 'rsync'

    :return:
        True is successful and False if unsuccessful.
    """

    live_folder = path / "live-backup"
    last_folder = path / "last-backup"

    prev_exists = check_path_exists(last_folder, remote)

    success = backup_container(
        container,
        live_folder,
        remote=remote,
        prev_backup=last_folder if prev_exists else None,
        rsync_exe=rsync_exe,
    )
    if not success:
        return False

    # move live-backup -> last-backup in a safe manner
    # (such that if the process stops at any point, that we wouldn't lose data)
    # step 1: last-backup -> last-backup-old
    if prev_exists:
        success = run_cmd(
            ["mv", str(last_folder), str(last_folder) + "-old"], remote=remote
        )
        if not success:
            return False
    # step 2: live-backup -> last-backup
    success = run_cmd(["mv", str(live_folder), str(last_folder)], remote=remote)
    if not success:
        return False
    # step 3: remote last-backup-old
    if prev_exists:
        success = run_cmd(["rm", "-rf", str(last_folder) + "-old"], remote=remote)
        if not success:
            return False

    _log(f"Backup moved from '{str(live_folder)}' to '{str(last_folder)}'.")
    return True
