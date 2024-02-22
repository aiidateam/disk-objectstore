"""A small CLI tool for managing stores."""

import dataclasses
import json
import logging
import os
import sys
from pathlib import Path
from typing import List, Optional

import click

from disk_objectstore import __version__, backup_utils
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


@click.group(context_settings={"help_option_names": ["--help"]})
@click.version_option(__version__)
@click.option(
    "-p",
    "--path",
    default=os.environ.get("DOSTORE_PATH", str(Path.cwd().joinpath("dostore"))),
    show_default=True,
    help="Path to the container (or set env DOSTORE_PATH)",
)
@click.pass_context
def main(ctx, path):
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
        data: dict = {"path": str(container.get_folder())}
        data["id"] = container.container_id
        data["compression"] = container.compression_algorithm
        data["count"] = dataclasses.asdict(container.count_objects())
        data["size"] = dataclasses.asdict(container.get_total_size())
        click.echo(json.dumps(data, indent=2))


@main.command("validate")
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Print the full list of errors with respective hashkeys",
)
@pass_dostore
def validate(dostore: ContainerContext, verbose: bool):
    """Validate the container"""

    try:
        # Import here so I don't have to depend on this library
        import tqdm  # pylint: disable=import-outside-toplevel

        class CallbackTqdm:
            """Provides a callback to show a progress bar with TQDM."""

            def __init__(self):
                self.progress_bar: Optional[tqdm.tqdm] = None

            def callback(self, action, value):
                """Callback method called periodically to update the progress bar."""
                if action == "init":
                    if self.progress_bar is not None:
                        self.progress_bar.close()  # pragma: no cover
                    self.progress_bar = tqdm.tqdm(
                        total=value["total"], desc=value["description"]
                    )
                elif action == "update":
                    value = value or 1  # If 0 or None
                    if self.progress_bar is None:
                        # Update without every initializing it?
                        return  # pragma: no cover
                    self.progress_bar.update(n=value)
                elif action == "close":
                    if self.progress_bar is not None:  # If not already closed
                        self.progress_bar.close()
                        self.progress_bar = None

        callback_tqdm = CallbackTqdm()
        callback = callback_tqdm.callback
    except ImportError:
        callback = None
        click.echo(
            "INFO: no `tqdm` package found. If you want to show a progress bar, install `pip tqdm` first.",
            err=True,
        )

    with dostore.container as container:
        results = dataclasses.asdict(container.validate(callback=callback))

    errors_found = False
    for key, value in results.items():
        if value:
            errors_found = True
            click.echo(f"Error! {len(value)} objects with error '{key}'")
    if not errors_found:
        click.echo("No errors found, the container is valid.")
    if verbose and errors_found:
        click.echo(json.dumps(results, indent=2))
    if errors_found:
        sys.exit(1)


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


@main.command("backup")
@click.argument("dest", nargs=1, type=click.Path())
@click.option(
    "--keep",
    default=1,
    show_default=True,
    help="Number of previous backups to keep in the destination.",
)
@click.option(
    "--rsync-exe",
    default="rsync",
    help="Specify the 'rsync' executable, if not in PATH. Used for both local and remote destinations.",
)
@click.option(
    "--verbosity",
    default="info",
    type=click.Choice(("silent", "info", "debug")),
    help="Set verbosity of the logger.",
)
@pass_dostore
def backup(
    dostore: ContainerContext, dest: str, keep: int, rsync_exe: str, verbosity: str
):
    """Create a backup of the container.

    The backup is created at the `DEST` destination, in a subfolder
    backup_<timestamp>_<randstr> and a symlink `last-backup` is created to it in the same folder.

    NOTE: This is safe to run while the container is being used.

    NOTE: the symlink `last-backup` is omitted if the filesystem doesn't support it.

    Destination (DEST) can either be a local path, or a remote destination (reachable via ssh).
    In the latter case, remote destination needs to have the following syntax:

       [<remote_user>@]<remote_host>:<path>

    i.e., contain the remote host name and the remote path, separated by a colon (and optionally the
    remote user separated by an @ symbol). You can tune SSH parameters using the standard options given
    by OpenSSH, such as adding configuration options to ~/.ssh/config (e.g. to allow for passwordless
    login - recommended, since this script might ask multiple times for the password).

    NOTE: 'rsync' and other UNIX-specific commands are called, thus the command will likely not work on
    non-UNIX environments.
    """

    logging.basicConfig(format="%(levelname)s:%(message)s")
    logger = logging.getLogger("disk_objectstore")

    if verbosity == "silent":
        logger.setLevel(logging.ERROR)
    elif verbosity == "info":
        logger.setLevel(logging.INFO)
    elif verbosity == "debug":
        logger.setLevel(logging.DEBUG)

    with dostore.container as container:
        try:
            backup_manager = backup_utils.BackupManager(
                dest,
                keep=keep,
                rsync_exe=rsync_exe,
            )
            backup_manager.backup_auto_folders(
                lambda path, prev: backup_utils.backup_container(
                    backup_manager, container, path, prev
                )
            )
        except (ValueError, backup_utils.BackupError) as e:
            click.echo(f"Error: {e}")
            sys.exit(1)
