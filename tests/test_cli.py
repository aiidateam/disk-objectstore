"""Test the CLI commands"""

import platform
from pathlib import Path

import pytest
from click.testing import CliRunner

from disk_objectstore import cli
from disk_objectstore.dataclasses import ObjectCount


def test_main_command_missing_command(temp_dir):
    """Test calling the main command."""
    result = CliRunner().invoke(cli.main, [f"--path={temp_dir}"])
    # This should fail
    assert result.exit_code != 0
    assert "Missing command" in result.stdout


def test_main_command_no_params():
    """Test calling the main command."""
    result = CliRunner().invoke(cli.main)
    # This should work and show a help/usage
    assert result.exit_code == 0
    assert "Usage:" in result.stdout
    assert "Commands:" in result.stdout


def test_create(temp_dir):
    """Test creating a container"""
    path = Path(temp_dir) / "dostore"
    obj = cli.ContainerContext(path)
    result = CliRunner().invoke(cli.create, obj=obj)
    assert result.exit_code == 0, result.output
    assert path.exists()


def test_create_with_explicit_pat(temp_dir):
    """Test creating a container

    At variance with the previous test, it passes explicitly temp_dir
    on the command line (passing as a ContainerContext will bypass some
    code in the `main` method in the `cli` module).
    """
    path = Path(temp_dir) / "dostore"
    result = CliRunner().invoke(cli.main, [f"--path={path}", "create"])
    assert result.exit_code == 0, result.output
    assert path.exists()


def test_create_exists(temp_dir):
    """Test creating a container that already exists fails"""
    path = Path(temp_dir) / "dostore"
    path.touch()
    obj = cli.ContainerContext(path)
    result = CliRunner().invoke(cli.create, obj=obj)
    assert result.exit_code != 0, result.output


def test_status(temp_container):
    """Test status command"""
    obj = cli.ContainerContext(temp_container.get_folder())
    result = CliRunner().invoke(cli.status, obj=obj)
    assert result.exit_code == 0, result.output
    assert "path" in result.output


def test_status_not_exist():
    """Test status command when container does not exist"""
    obj = cli.ContainerContext(Path("/does/not/exist"))
    result = CliRunner().invoke(cli.status, obj=obj)
    assert result.exit_code != 0, result.output
    assert "Container does not exist" in result.output


def test_add_file(temp_dir, temp_container):
    """Test add-files command"""
    path = Path(temp_dir, "test.txt")
    path.write_bytes(b"test")
    obj = cli.ContainerContext(temp_container.get_folder())
    result = CliRunner().invoke(cli.add_files, [str(path)], obj=obj)
    assert result.exit_code == 0, result.output
    assert sum(1 for _ in temp_container.list_all_objects()) == 1


def test_optimize(temp_container):
    """Test optimize command"""
    temp_container.init_container(clear=True)
    temp_container.add_object(b"test")
    assert temp_container.count_objects() == ObjectCount(
        loose=1,
        packed=0,
        pack_files=0,
    )
    temp_container.close()
    obj = cli.ContainerContext(temp_container.get_folder())
    result = CliRunner().invoke(cli.optimize, ["--non-interactive"], obj=obj)
    assert result.exit_code == 0, result.output
    assert temp_container.count_objects() == ObjectCount(
        loose=0,
        packed=1,
        pack_files=1,
    )


def test_optimize_cancel(temp_container):
    """Test cancelling optimize command"""
    obj = cli.ContainerContext(temp_container.get_folder())
    result = CliRunner().invoke(cli.optimize, obj=obj, input="n")
    assert result.exit_code == 1, result.output
    assert "Abort" in result.output


@pytest.mark.parametrize("verbose", [True, False])
def test_validate(temp_container, verbose):
    """Test validate command"""
    temp_container.init_container(clear=True)
    # Add a few objects
    for idx in range(100):
        temp_container.add_object(f"test-{idx}".encode())

    obj = cli.ContainerContext(temp_container.get_folder())
    if verbose:
        result = CliRunner().invoke(cli.validate, ["--verbose"], obj=obj)
    else:
        result = CliRunner().invoke(cli.validate, obj=obj)
    assert result.exit_code == 0
    assert "No errors found" in result.stdout
    if verbose:
        # Show progress bar
        assert "100%" in result.stdout


@pytest.mark.parametrize("verbose", [True, False])
def test_validate_fail(temp_container, verbose):
    """Test validate command"""
    temp_container.init_container(clear=True)
    # Add an object
    hashkey = temp_container.add_object(b"test")
    # Replace the object content with something different, so the hash does
    # not match anymore
    with open(
        temp_container._get_loose_path_from_hashkey(  # pylint: disable=protected-access
            hashkey
        ),
        "wb",
    ) as fhandle:
        fhandle.write(b"wrong-content")

    obj = cli.ContainerContext(temp_container.get_folder())
    if verbose:
        result = CliRunner().invoke(cli.validate, ["--verbose"], obj=obj)
    else:
        result = CliRunner().invoke(cli.validate, obj=obj)
    assert result.exit_code != 0
    assert "1 objects with error 'invalid_hashes_loose'" in result.stdout


@pytest.mark.parametrize("verbose", [True, False])
def test_validate_no_progressbar(temp_container, verbose, monkeypatch):
    """Check the output when TQDM is not available (so no progress bar)."""
    temp_container.init_container(clear=True)
    # Add an object
    temp_container.add_object(b"test")

    import builtins  # pylint: disable=import-outside-toplevel

    realimport = builtins.__import__

    ## Disable importing tqdm with a monkey patch
    def myimport(
        name, globals, locals, fromlist, level  # pylint: disable=redefined-builtin
    ):
        if name == "tqdm":
            raise ImportError("No module named 'tqdm'")
        return realimport(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", myimport)

    obj = cli.ContainerContext(temp_container.get_folder())
    if verbose:
        result = CliRunner().invoke(cli.validate, ["--verbose"], obj=obj)
    else:
        result = CliRunner().invoke(cli.validate, obj=obj)

    assert result.exit_code == 0
    assert "INFO: no `tqdm` package found" in result.stdout
    assert "No errors found" in result.stdout


@pytest.mark.skipif(
    platform.system() == "Windows", reason="Backup not supported on Windows"
)
@pytest.mark.parametrize(
    "remote, verbosity",
    [
        (False, None),
        (False, "silent"),
        (False, "info"),
        (False, "debug"),
        (True, None),
    ],
)
def test_backup(temp_container, temp_dir, remote, verbosity):
    """Test the backup command"""

    temp_container.init_container(clear=True)
    # Add a few objects
    for idx in range(100):
        temp_container.add_object(f"test-{idx}".encode())

    obj = cli.ContainerContext(temp_container.get_folder())

    path = Path(temp_dir) / "backup"

    if remote:
        destination = f"localhost:{str(path)}"
    else:
        destination = str(path)

    args = [destination]

    if verbosity:
        args += [f"--verbosity={verbosity}"]

    result = CliRunner().invoke(cli.backup, args, obj=obj)

    assert result.exit_code == 0
    assert path.exists()

    path_contents = [entry.name for entry in path.iterdir()]
    backup_dirs = [
        entry for entry in path.iterdir() if entry.name.startswith("backup_")
    ]

    assert "last-backup" in path_contents
    assert len(backup_dirs) == 1

    backup_dir_contents = [entry.name for entry in backup_dirs[0].iterdir()]

    for item in ["config.json", "duplicates", "loose", "packs", "packs.idx", "sandbox"]:
        assert item in backup_dir_contents

    # validate the backup

    obj = cli.ContainerContext(backup_dirs[0])
    result = CliRunner().invoke(cli.validate, obj=obj)

    assert result.exit_code == 0
    assert "No errors found" in result.stdout


@pytest.mark.skipif(
    platform.system() == "Windows", reason="Backup not supported on Windows"
)
@pytest.mark.parametrize("remote", [False, True])
def test_backup_repeated(temp_container, temp_dir, remote):
    """Test the backup command repeated 3 times.

    Considering --keep 1 is default, the last one should get deleted.
    """

    temp_container.init_container(clear=True)
    # Add a few objects
    for idx in range(100):
        temp_container.add_object(f"test-{idx}".encode())

    obj = cli.ContainerContext(temp_container.get_folder())

    path = Path(temp_dir) / "backup"

    if remote:
        destination = f"localhost:{str(path)}"
    else:
        destination = str(path)

    for _ in range(3):
        result = CliRunner().invoke(cli.backup, [destination], obj=obj)
        assert result.exit_code == 0

    assert path.exists()
    path_contents = [entry.name for entry in path.iterdir()]
    backup_dirs = [
        entry for entry in path.iterdir() if entry.name.startswith("backup_")
    ]

    assert "last-backup" in path_contents
    assert len(backup_dirs) == 2


@pytest.mark.skipif(
    platform.system() == "Windows", reason="Backup not supported on Windows"
)
def test_backup_failure(temp_container):
    """Test failure when providing invalid destination"""

    temp_container.init_container(clear=True)
    # Add a few objects
    for idx in range(100):
        temp_container.add_object(f"test-{idx}".encode())

    obj = cli.ContainerContext(temp_container.get_folder())

    dest = "abc:abc:"

    result = CliRunner().invoke(cli.backup, [dest], obj=obj)

    assert result.exit_code == 1
    assert "Error:" in result.stdout
