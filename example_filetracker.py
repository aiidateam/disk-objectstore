#!/usr/bin/env python
import sys
import time

import click

from repository.filetracker.filetracker import FileTracker

@click.command()
@click.option('-n', '--num-folders', default=1000, help='The number of folders to create')
@click.option('-p', '--path', default='test-container', help='The path to a test folder in which the container will be created.')
@click.option('-c', '--clear', is_flag=True, help='Clear the repository path folder before starting.')
@click.help_option('-h', '--help')
@click.option('-U', '--db-user', required=True, help='DB user name.')
@click.option('-d', '--db-name', required=True, help='DB database name.')
@click.option('-p', '--db-password', required=True, help='DB password.')
@click.help_option('-h', '--help')
def main(num_folders, path, clear, db_user, db_name, db_password):  # pylint: disable=too-many-arguments,too-many-locals,too-many-statements
    """Testing some basic functionality of the object-store wrapper, with timing."""

    sample_content = b'some_content'

    ## To create the DB the frist time:
    ## First give the 'aiida' user (for instance) the permission to create new DBs 
    # sudo su - postgres
    # psql template1
    # ALTER USER aiida CREATEDB;
    ##
    ## Then as a normal user from bash, run:
    #   createdb -U aiida -W test_repo
    ## or, to drop it:
    #   dropdb -U aiida -W test_repo

    tracker = FileTracker(folder=path, db_user=db_user, db_name=db_name, db_password=db_password)

    if clear:
        tracker.drop_db()
    else:
        print("In the current version, you need to call the script with the -c/--clear option")
        sys.exit(1)

    tracker.add_file_from_path('a/b/c.txt', sample_content)
    retrieved_content = tracker.get_file_content_from_path('a/b/c.txt')

    assert sample_content == retrieved_content

    tracker.mkdir('a/b/e')
    tracker.mkdir('c/d/e', recursive=True)
    tracker.mkdir('c/d/f', recursive=True)
    tracker.mkdir('c/d/f', recursive=True, existing_ok=True)

    tracker.add_file_from_path('a/b/e/c.txt', sample_content)

    print("# ls /")
    tracker.ls('')
    print()

    print("# ls -r /")
    tracker.ls('', recursive=True)
    print()

    print("# ls /a/b/")
    tracker.ls('a/b')
    print()

    print("# ls -r /a/b/")
    tracker.ls('a/b', recursive=True)
    print()

    #base_folder = 'a/b/'
    for base_folder in ['', 'a/b/', 'e/f/g/h/']:
        folders_paths = []
        for i in range(num_folders):
            folders_paths.append('{}{}'.format(base_folder, i))
        start = time.time()
        tracker.mkdirs(folders_paths, recursive=True)
        tot_time = time.time() - start
        print("Time to create {} folders with base folder '{}': {:.3f} s".format(num_folders, base_folder, tot_time))
        print()

    folders_names = []
    for i in range(num_folders):
        folders_names.append('root{}'.format(i))
    start = time.time()
    tracker.mkdirs_root_nocheck(folders_names)
    tot_time = time.time() - start
    print("Time to create {} folders at root level, with no checks: {:.3f} s".format(num_folders, tot_time))
    print()


    print("All tests passed.")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
