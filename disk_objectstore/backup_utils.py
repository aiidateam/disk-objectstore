"""
Utilities to back up a container.
"""

import shutil
import sqlite3
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from disk_objectstore.container import Container


def _log(msg, end="\n"):
    print(msg, end=end)


def _is_exe_found(exe) -> bool:
    return shutil.which(exe) is not None


def _run_cmd(args: list, remote: Optional[str] = None, check: bool = True) -> bool:
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


def _check_if_remote_accessible(remote: str) -> bool:
    _log(f"Checking if '{remote}' is accessible...", end="")
    success = _run_cmd(["exit"], remote=remote)
    if not success:
        _log(f"Error: Remote '{remote}' is not accessible!")
        return False
    _log(f"Success! '{remote}' is accessible!")
    return True


def _check_path_exists(path: Path, remote: Optional[str] = None) -> bool:
    cmd = ["[", "-e", str(path), "]"]
    return _run_cmd(cmd, remote=remote, check=False)


def _call_rsync(  # pylint: disable=too-many-arguments
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


def backup(  # pylint: disable=too-many-return-statements, too-many-branches
    container: Container,
    path: Path,
    remote: Optional[str] = None,
    prev_backup: Optional[Path] = None,
    rsync_exe: str = "rsync",
) -> bool:
    """Create a backup of the disk-objectstore container

    It should be done in the following order:
        1) loose files;
        2) sqlite database;
        3) packed files.

    :return:
        True is successful and False if unsuccessful.
    """

    # ------------------
    # input validation:
    if remote:
        if not _check_if_remote_accessible(remote):
            return False

    if not _is_exe_found(rsync_exe):
        _log(f"Error: {rsync_exe} not accessible.")
        return False

    path_exists = _check_path_exists(path, remote)

    if not path_exists:
        success = _run_cmd(["mkdir", str(path)], remote=remote)
        if not success:
            _log(f"Error: Couldn't access/create '{str(path)}'!")
            return False

    if prev_backup:
        if not _check_path_exists(prev_backup, remote):
            _log(f"Error: {str(prev_backup)} not found.")
            return False
    # ------------------

    # subprocess arguments shared by all rsync calls:
    rsync_args = [rsync_exe, "-azh", "-vv", "--no-whole-file"]

    container_root_path = container.get_folder()
    loose_path = container._get_loose_folder()  # pylint: disable=protected-access
    packs_path = container._get_pack_folder()  # pylint: disable=protected-access
    sqlite_path = container._get_pack_index_path()  # pylint: disable=protected-access

    # step 1: back up loose files
    loose_path_rel = loose_path.relative_to(container_root_path)
    prev_backup_loose = prev_backup / loose_path_rel if prev_backup else None
    success = _call_rsync(
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
        success = _call_rsync(
            rsync_args, sqlite_temp_loc, path, remote=remote, link_dest=prev_backup
        )
        if not success:
            return False

    # step 4: transfer the packed files
    packs_path_rel = packs_path.relative_to(container_root_path)
    prev_backup_packs = prev_backup / packs_path_rel if prev_backup else None
    success = _call_rsync(
        rsync_args, packs_path, path, remote=remote, link_dest=prev_backup_packs
    )
    if not success:
        return False

    # step 5: transfer anything else in the container folder
    success = _call_rsync(
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
