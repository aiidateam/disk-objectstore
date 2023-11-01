"""
Utilities to back up a container.
"""

import datetime
import logging
import random
import shutil
import sqlite3
import string
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


def run_cmd(args: list, remote: Optional[str] = None):
    """
    Run a command locally or remotely.
    """
    all_args = args[:]
    if remote:
        all_args = ["ssh", remote] + all_args

    res = subprocess.run(all_args, capture_output=True, text=True, check=False)
    exit_code = res.returncode

    _log(
        f"Command: {all_args}\n"
        f"  Exit Code: {exit_code}\n"
        f"  stdout/stderr: {res.stdout}\n{res.stderr}"
    )

    success = exit_code == 0

    return success, res.stdout


def check_if_remote_accessible(remote: str) -> bool:
    """Check if remote host is accessible via ssh"""
    _log(f"Checking if '{remote}' is accessible...")
    success = run_cmd(["exit"], remote=remote)[0]
    if not success:
        _log(f"Error: Remote '{remote}' is not accessible!")
        return False
    _log(f"Success! '{remote}' is accessible!")
    return True


def check_path_exists(path: Path, remote: Optional[str] = None) -> bool:
    cmd = ["[", "-e", str(path), "]"]
    return run_cmd(cmd, remote=remote)[0]


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
    exit_code = res.returncode
    _log(
        f"Command: {all_args}\n"
        f"  Exit Code: {exit_code}\n"
        f"  stdout/stderr: {res.stdout}\n{res.stderr}"
    )

    success = exit_code == 0

    return success


def validate_inputs(
    path: Path,
    remote: Optional[str],
    keep: int,
    rsync_exe: str = "rsync",
) -> bool:
    """Validate inputs to the backup cli command

    :return:
        True if validation passes, False otherwise.
    """
    if keep < 0:
        _log("Error: keep variable can't be negative!")
        return False

    if remote:
        if not check_if_remote_accessible(remote):
            return False

    if not is_exe_found(rsync_exe):
        _log(f"Error: {rsync_exe} not accessible.")
        return False

    path_exists = check_path_exists(path, remote)

    if not path_exists:
        success = run_cmd(["mkdir", str(path)], remote=remote)[0]
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


def delete_old_backups(path: Path, remote: Optional[str] = None, keep: int = 1) -> bool:
    """Get all folders matching the backup pattern, and delete oldest ones."""
    success, stdout = run_cmd(
        [
            "find",
            str(path),
            "-maxdepth",
            "1",
            "-type",
            "d",
            "-name",
            "backup_*_*",
            "-print",
        ],
        remote=remote,
    )
    if not success:
        return False

    sorted_folders = sorted(stdout.splitlines())
    to_delete = sorted_folders[: -(keep + 1)]
    for folder in to_delete:
        success = run_cmd(["rm", "-rf", folder], remote=remote)[0]
        if success:
            _log(f"Deleted old backup: {folder}")
        else:
            _log(f"Warning: couldn't delete old backup: {folder}")
    return True


def backup_auto_folders(
    container: Container,
    path: Path,
    remote: Optional[str] = None,
    keep: int = 1,
    rsync_exe: str = "rsync",
):
    """Create a backup, managing live and previous backup folders automatically

    The running backup is done to `<path>/live-backup`. When it completes, it is moved to
    the final path: `<path>/backup_<timestamp>_<randstr>` and the symlink `<path>/last-backup will
    be set to point to it. Rsync `link-dest` is used between live-backup and last-backup
    to keep the backups incremental and performant.

    :param path:
        Path to where the backup will be created. If 'remote' is specified, must be an absolute path,
        otherwise can be relative.

    :param remote:
        Remote host of the backup location. 'ssh' executable is called via subprocess and therefore remote
        hosts configured for it are supported (e.g. via .ssh/config file).

    :return:
        True is successful and False if unsuccessful.
    """

    live_folder = path / "live-backup"
    last_symlink = path / "last-backup"

    prev_exists = check_path_exists(last_symlink, remote)

    success = backup_container(
        container,
        live_folder,
        remote=remote,
        prev_backup=last_symlink if prev_exists else None,
        rsync_exe=rsync_exe,
    )
    if not success:
        return False

    # move live-backup -> backup_<timestamp>_<randstr>
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    randstr = "".join(random.choices(string.ascii_lowercase + string.digits, k=4))
    folder_name = f"backup_{timestamp}_{randstr}"

    success = run_cmd(["mv", str(live_folder), str(path / folder_name)], remote=remote)[
        0
    ]
    if not success:
        return False

    # update last-backup symlink
    success = run_cmd(
        ["ln", "-sfn", str(folder_name), str(last_symlink)], remote=remote
    )[0]
    if not success:
        return False
    _log(f"Backup moved from '{str(live_folder)}' to '{str(path / folder_name)}'.")

    delete_old_backups(path, remote=remote, keep=keep)

    return True
