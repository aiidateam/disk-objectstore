"""Test the CLI commands"""
from pathlib import Path

from click.testing import CliRunner

from disk_objectstore import cli


def test_create(temp_dir):
    """Test creating a container"""
    path = Path(temp_dir) / "dostore"
    obj = cli.ContainerContext(path)
    result = CliRunner().invoke(cli.create, obj=obj)
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


def test_optimize_cancel(temp_container):
    """Test cancelling optimize command"""
    obj = cli.ContainerContext(temp_container.get_folder())
    result = CliRunner().invoke(cli.optimize, obj=obj, input="n")
    assert result.exit_code == 1, result.output
    assert "Abort" in result.output
