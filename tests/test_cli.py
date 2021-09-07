"""Test the CLI commands"""
import os
from pathlib import Path

from click.testing import CliRunner

from disk_objectstore import Container, cli


def test_create(temp_dir):
    """Test creating a container"""
    path = os.path.join(temp_dir, "dostore")
    obj = cli.ContainerContext(path)
    result = CliRunner().invoke(cli.create, obj=obj)
    assert result.exit_code == 0, result.output
    assert os.path.exists(path)


def test_status(temp_container):
    """Test status command"""
    obj = cli.ContainerContext(temp_container.get_folder())
    result = CliRunner().invoke(cli.status, obj=obj)
    assert result.exit_code == 0, result.output
    assert "path" in result.output


def test_add_file(temp_dir, temp_container):
    """Test adding a file to a container"""
    path = Path(temp_dir, "test.txt")
    path.write_bytes(b"test")
    obj = cli.ContainerContext(temp_container.get_folder())
    result = CliRunner().invoke(cli.add_files, [str(path)], obj=obj)
    print(result.output)
    assert result.exit_code == 0, result.output
    assert sum(1 for _ in temp_container.list_all_objects()) == 1


def test_optimize(temp_container):
    """Test optimizing a container"""
    temp_container.init_container(clear=True)
    temp_container.add_object(b"test")
    assert temp_container.count_objects() == {
        "loose": 1,
        "packed": 0,
        "pack_files": 0,
    }
    temp_container.close()
    obj = cli.ContainerContext(temp_container.get_folder())
    result = CliRunner().invoke(cli.optimize, ["--non-interactive"], obj=obj)
    assert result.exit_code == 0, result.output
    assert temp_container.count_objects() == {
        "loose": 0,
        "packed": 1,
        "pack_files": 1,
    }
