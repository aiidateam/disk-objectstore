"""A small CLI tool for managing stores."""
import json
import os
from pathlib import Path
from typing import List

import click

from disk_objectstore import __version__
from disk_objectstore.container import Container


class ContainerContext:
    """Lazy create the container when required."""

    def __init__(self, path: str):
        self._path = Path(path)

    @property
    def path(self) -> Path:
        """Get the path to the container."""
        return self._path

    @property
    def container(self) -> Container:
        """Get the container, creating if it does not exist."""
        if not self.path.exists():
            raise click.ClickException(
                f"Container does not exist (run create command): {self.path}"
            )
        return Container(str(self.path))


pass_dostore = click.make_pass_decorator(ContainerContext)


@click.group()
@click.version_option(__version__)
@click.option(
    "-p",
    "--path",
    default=os.environ.get("DOSTORE_PATH", str(Path.cwd().joinpath("dostore"))),
    show_default=True,
    help="Path to the container (or set env DOSTORE_PATH)",
)
@click.pass_context
def main(  # pylint: disable=dangerous-default-value
    ctx,
    path,
    context_settings={
        "help_option_names": ("--help",)
    },  # pylint: disable=unused-argument
):
    """Manage a disk objectstore"""
    ctx.obj = ContainerContext(path)


@main.command("create")
@click.option(
    "-a", "--algorithm", default="zlib+1", help="Compression algorithm to use"
)
@pass_dostore
def create(dostore: ContainerContext, algorithm: str):
    """Create a container"""
    if dostore.path.exists():
        raise click.ClickException(f"Container already exists: {dostore.path}")
    container = Container(str(dostore.path))
    container.init_container(compression_algorithm=algorithm)
    click.echo(f"Created container: {container.get_folder()}")


@main.command("status")
@pass_dostore
def status(dostore: ContainerContext):
    """Print details about the container"""
    with dostore.container as container:
        data: dict = {"path": container.get_folder()}
        data["id"] = container.container_id
        data["compression"] = container.compression_algorithm
        data["count"] = container.count_objects()
        data["size"] = container.get_total_size()
        click.echo(json.dumps(data, indent=2))


@main.command("add-files")
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@pass_dostore
def add_files(dostore: ContainerContext, files: List[str]):
    """Add file(s) to the container"""
    with dostore.container as container:
        click.echo(
            f"Adding {len(files)} file(s) to container: {container.get_folder()}"
        )
        for filepath in files:
            with open(filepath, "rb") as fobj:
                hashkey = container.add_streamed_object(fobj)
            click.echo(f"{hashkey}: {filepath}")


@main.command("optimize")
@click.option("-n", "--non-interactive", is_flag=True, help="Do not confirm optimize")
@click.option(
    "--compress/--no-compress",
    default=True,
    show_default=True,
    help="Compress objects before storing",
)
@click.option(
    "--vacuum/--no-vacuum", default=True, show_default=True, help="Vacuum the database"
)
@pass_dostore
def optimize(
    dostore: ContainerContext, non_interactive: bool, compress: bool, vacuum: bool
):
    """Optimize the container's memory use"""
    if not non_interactive:
        click.confirm("Is this the only process accessing the container?", abort=True)
    size = sum(f.stat().st_size for f in dostore.path.glob("**/*") if f.is_file())
    click.echo(f"Initial container size: {round(size/1000, 2)} Mb")
    with dostore.container as container:
        container.pack_all_loose(compress=compress)
        container.clean_storage(vacuum=vacuum)
    size = sum(f.stat().st_size for f in dostore.path.glob("**/*") if f.is_file())
    click.echo(f"Final container size: {round(size/1000, 2)} Mb")


@main.group("archive")
def archive():
    """
    Interface for managing archived packs.

    An archived pack is essentially an ZIP file and will no longer be considered for writing new
    data. Once an pack is archived, it can be moved to other locations, for example, networked storages.
    """


@archive.command("list")
@pass_dostore
def archive_list(dosstore: ContainerContext):
    """List all archives in the container"""

    with dosstore.container as container:
        location = container.get_archive_locations()
        click.echo(json.dumps(location, indent=2))


@archive.command("update-location")
@click.argument("pack_id")
@click.argument("new_location")
@click.option("--force", help="Skip checks if passed", is_flag=True, default=False)
@pass_dostore
def archive_update_location(
    dosstore: ContainerContext, pack_id: str, new_location: str, force: bool
):
    """
    Update the location of archive files

    NOTE: relative path is interpreted as relative to the root folder of the container.
    """

    with dosstore.container as container:
        container._update_archive_location(  # pylint: disable=protected-access
            pack_id, new_location, force
        )
        click.echo(f"Updated location of pack {pack_id} to {new_location}")


@archive.command("create")
@click.argument("pack_id")
@click.option(
    "--validate/--no-validate",
    show_default=True,
    help="Validate the created archive or not.",
)
@click.option(
    "--trim-names/--no-trim-names",
    show_default=True,
    help="Trim the filenames in the archive, reduce storage overheads.",
)
@pass_dostore
def archive_create(
    dosstore: ContainerContext, pack_id: str, validate: bool, trim_names: bool
):
    """Turn the pack_id into an archive pack"""
    with dosstore.container as container:
        archives = container.get_archived_pack_ids(return_str=True)
        if pack_id in archives:
            raise click.Abort(f"Pack {pack_id} is already archived!")
        container.archive_pack(
            pack_id, run_read_test=validate, trim_filenames=trim_names
        )
        location = container.get_archive_locations()[pack_id]
        click.echo(f"Successfully archvied pack {pack_id} at {location}")


@archive.command("extract")
@click.argument("archive_path")
@click.argument("destination", type=click.Path(exists=False))
@pass_dostore
def archive_extract(
    dosstore: ContainerContext,
    archive_path: str,
    destination: str,
):
    """
    Extract an existing archive and renames the files in the destination folder
    the same that used for the loose objects, so that they can be imported into a another container.
    """

    with dosstore.container as container:
        container.lossen_archive(archive_path, destination)
        click.echo(f"Objects from {archive_path} have been extracted to {destination}")
