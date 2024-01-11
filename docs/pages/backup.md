# Making backups

## User instructions

A disk-objectstore container is fully contained in its root folder. If the container is not being modified, a backup can be made by just making a copy of this folder. The recommended way is to use the `rsync` tool, as the library was designed to be performant with it and make use of the incremental copying capabilities.

However, the preferred way to make a backup, that is also safe while the container is being used (except for when repacking or deleting files), is to use the built-in CLI command:

```console
$ dostore backup --help
Usage: dostore backup [OPTIONS] DEST

  Create a backup of the container to destination location DEST, in a
  subfolder backup_<timestamp>_<randstr> and point a symlink called `last-
  backup` to it.

  NOTE: This is safe to run while the container is being used.

  NOTE: the symlink `last-backup` is omitted if the filesystem doesn't support
  it.

  Destination (DEST) can either be a local path, or a remote destination
  (reachable via ssh). In the latter case, remote destination needs to have
  the following syntax:

     [<remote_user>@]<remote_host>:<path>

  i.e., contain the remote host name and the remote path, separated by a colon
  (and optionally the remote user separated by an @ symbol). You can tune SSH
  parameters using the standard options given by OpenSSH, such as adding
  configuration options to ~/.ssh/config (e.g. to allow for passwordless login
  - recommended, since this script might ask multiple times for the password).

  NOTE: 'rsync' and other UNIX-specific commands are called, thus the command
  will not work on non-UNIX environments.

Options:
  --keep INTEGER    Number of previous backups to keep in the destination.
                    (default: 1)
  --rsync-exe TEXT  Specify the 'rsync' executable, if not in PATH. Used for
                    both local and remote destinations.
  --verbosity TEXT  Set verbosity [silent|info|debug], default is 'info'.
  --help            Show this message and exit.

```

Example usage:

```console
$ dostore --path /path/to/container backup /path/to/backup
INFO:Last backup is '/path/to/backup/backup_20231207142602_ymqf', using it for rsync --link-dest.
INFO:Transferred /path/to/container/loose to /path/to/backup/live-backup
INFO:Dumped the SQLite database to /tmp/tmpgewwse3f/packs.idx
INFO:Transferred SQLite database to /path/to/backup/live-backup
INFO:Transferred /path/to/container/packs to /path/to/backup/live-backup
INFO:Backup moved from '/path/to/backup/live-backup' to '/path/to/backup/backup_20231207142913_pz7m'.
INFO:Added symlink 'last-backup' to 'backup_20231207142913_pz7m'.
INFO:Deleted old backup: /path/to/backup/backup_20231207131741_zar7
```

For more detailed information about how the backup is made, see the next section.

## Detailed info/design

The primary purpose of the backup functionality is to copy the content of the container in a specific order that prevents data corruption due to the container being updated. This order is the following

1. loose files;
2. sqlite database that contains the packed file indexes;
3. packed files.

To understand why, let's consider ways the backup could become corrupted:

- In the case of packing files (`optimize`) or adding directly packed files, the library first adds data to the pack file and then writes the metadata to the sqlite database. The backup becomes corrupted if the following happens

  1. data is being added to a pack file;
  2. backup copies the pack file, containing the incomplete section;
  3. packfile is completed & the sqlite database is updated;
  4. backup copies the sqlite database.

  This results in the backup containing an index that references an incomplete section in a pack file. To prevent this, is to always copy first the sqlite db and then the pack files. This can still result in an incomplete section in the pack files but it effectively doesn't exist for the backup.

- If loose files are packed up at the end, the following might happen:

  1. backup copies pack files & sqlite db;
  2. user runs optimize & clean_storage, which adds loose files to a pack & deletes the original files;
  3. backup copies loose files.

  This results in files missing in the backup. Therefore, loose files should be copied first.

Note: one should not run the backup while repacking and deleting files.

Implementation details:

- The backup command runs operating-system-level commands on the destination machine by using the python subprocess library. These currently include

  1. running rsync.
  2. For remote destinations, checking if it is accessible (`ssh <remote> exit`);
  3. checking if destination path exists (`[ -e <path> ]`);
  4. checking if destination directory can be made, if it doesn't exist (`mkdir <path>`);
  5. moving and removing folders.

  For 3-5, remote cases just append `ssh <remote>` in front of the command, while rsync is used via its native interface to access a remote destination. For both of these cases of remote access, the standard configuration options of OpenSSH are used (such as configuration in `~/.ssh/config`)

- Steps in order:
  - Input validation:
    - is remote accessible?
    - is `DEST` accessible?
    - is `rsync` executable found?
  - Check if a backup already exists in `DEST`
    - if yes, use the most recent one (based on timestamp in name) for `rsync --link-dest` argument in all `rsync` calls
  - Create `DEST/live-backup` folder
  - rsync loose folder to `DEST/live-backup`
  - dump sqlite database in a safe manner to a `tempfile.TemporaryDirectory()`
  - rsync the sqlite database to `DEST/live-backup`
  - rsync the packed files to `DEST/live-backup`
  - rsync everything else to `DEST/live-backup`
  - rename `DEST/live-backup` to `DEST/backup_<timestamp>_<randstr>`
  - update `DEST/last-backup` symlink to point to `DEST/backup_<timestamp>_<randstr>`
  - delete number of previous backups down to `--keep` argument
