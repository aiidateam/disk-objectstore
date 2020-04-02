#!/usr/bin/env python
import click
import os
import random
import shutil
import subprocess
import sys
import time

from aiida_objectstore.repository.repository import Repository, FileType
from aiida_objectstore.objectstore.container import Container


@click.command()
@click.option('-p', '--path', default='/tmp/test-container',
    help='The path to a test folder in which the container will be created.')
@click.option('-c', '--clear', is_flag=True, help='Clear the repository path folder before starting.')
@click.option('-U', '--db-user', required=True, help='DB user name.')
@click.option('-D', '--db-name', required=True, help='DB database name.')
@click.option('-P', '--db-password', required=True, help='DB password.')
@click.option('-r', '--repository-folder', required=True, help='Repository folder of AiiDA to import.')
@click.option('-x', '--extract-to', default='/tmp/test-repository-extract-to/', required=True,
    help='Re-extract the repository to this folder. Must not exist unless -C is specified.')
@click.option('-C', '--clear-extract-to', is_flag=True, help='Delete the extract-to folder before starting.')
@click.option('-z', '--compress', is_flag=True, help='Use compression when packing.')
@click.help_option('-h', '--help')
def main(path, clear,  # pylint: disable=too-many-arguments,too-many-locals,too-many-statements,too-many-branches
    db_user, db_name, db_password, repository_folder,
    extract_to, clear_extract_to, compress):  

    repo = Repository(folder=path, db_user=db_user, db_name=db_name, db_password=db_password)

    if clear:
        repo.drop_db()
        repo.container.init_container(clear=True)

    if clear_extract_to:
        if os.path.exists(extract_to):
            #input("Press ENTER to delete '{}'... ".format(extract_to))
            shutil.rmtree(extract_to)

    if os.path.exists(extract_to):
        print("The folder '{}' exists - either delete it, or specify the -C option")
        sys.exit(1)

    assert 'node' in os.listdir(repository_folder), "No 'node' folder in repository_folder, is this an AiiDA repository?"
    node_folder = os.path.join(repository_folder, 'node')

    print(subprocess.check_output(['du', '-hs', node_folder]).decode('utf8'))

    folder_paths = {}

    for level1 in os.listdir(node_folder):
        if len(level1) != 2 or any(char not in "0123456789abcdef" for char in level1):
            continue
        for level2 in os.listdir(os.path.join(node_folder, level1)):
            if len(level2) != 2 or any(char not in "0123456789abcdef" for char in level2):
                continue
            for node_uuid_part in os.listdir(os.path.join(node_folder, level1, level2)):
                node_uuid = level1 + level2 + node_uuid_part
                if len(node_uuid) != 36:
                    continue
                repo_node_folder = os.path.join(node_folder, level1, level2, node_uuid_part)
                #path_node_folder = os.path.join(repo_node_folder, 'path') # NOT TRUE for calcs (raw_inputs)
                #if not os.path.exists(path_node_folder):
                #    raise OSError("Path folder does not exist: {}".format(path_node_folder))
                folder_paths[node_uuid] = repo_node_folder

    # Create the new repo format (TIMING INSIDE THE FUNCTION)
    repo.create_repo_for_nodes(folder_paths=folder_paths, compress=compress)

    # Print some size statistics
    size_info = repo.container.get_total_size()
    print("Object store size info:")
    for key in sorted(size_info.keys()):
        print("- {:30s}: {}".format(key, size_info[key]))

    # Export everything in two chunks
    node_uuids = list(folder_paths.keys())
    random.shuffle(node_uuids)

    node_uuids1, node_uuids2 = node_uuids[:len(node_uuids)//2], node_uuids[len(node_uuids)//2:]
    os.mkdir(extract_to)

    export_container_extract_to = os.path.join(extract_to, 'export-container')

    output_container = Container(folder=export_container_extract_to)
    output_container.init_container()

    start = time.time()
    for idx, node_uuids_chunk in enumerate([node_uuids1, node_uuids2], start=1):
        obj_uuids = []
        for repo_node in repo.get_node_repositories(node_uuids_chunk):
            obj_uuids.extend(repo_node.get_all_obj_uuids())
        print("{} objects to write in phase {}".format(len(obj_uuids), idx))

        with repo.container.get_object_streams(obj_uuids) as uuid_and_stream_pairs:
            ## NOTE! This does not work because the object streams yielded by the 
            ## uuid_and_stream_pairs generator must be consumed immediately,
            ## as they are then closed.                
            ## old_obj_uuids = []
            # streams = []
            # for old_obj_uuid, stream in uuid_and_stream_pairs:
            #     old_obj_uuids.append(old_obj_uuid)
            #     streams.append(stream)
            # new_obj_uuids = output_container.add_streamed_objects_to_pack(
            #     streams, compress=compress)
            ## This is needed to recreate the metadata to put in the JSON
            ## I'm not doing it in this example
            # old_new_obj_uuid_mapping = dict(zip(old_obj_uuids, new_obj_uuids))
            old_obj_uuids = []
            new_obj_uuids = []
            for old_obj_uuid, stream in uuid_and_stream_pairs:
                old_obj_uuids.append(old_obj_uuid)
                new_obj_uuids.append(output_container.add_streamed_objects_to_pack(
                    [stream], compress=compress)[0])
            ## This is needed to recreate the metadata to put in the JSON
            ## I'm not doing it in this example
            #old_new_obj_uuid_mapping = dict(zip(old_obj_uuids, new_obj_uuids))

            # Print some size statistics
            size_info = output_container.get_total_size()
            print("Output object store size info after phase {}:".format(idx))
            for key in sorted(size_info.keys()):
                print("- {:30s}: {}".format(key, size_info[key]))
    tot_time = time.time() - start
    print("Time to store all objects (from packed to packed) in 2 steps: {:.3f} s".format(tot_time))

    # Let's try now to extract again
    random.shuffle(node_uuids)
    print("Extracting (shuffled) again in '{}'...".format(extract_to))
    start = time.time()
    node_repos = repo.get_node_repositories(node_uuids)
    tot_time = time.time() - start
    print("Time to get back all folder metas for {} shuffled nodes from postgres: {:.3f} s".format(len(node_uuids), tot_time))

    # Recreate the legacy repository format
    legacy_extract_to = os.path.join(extract_to, 'legacy')
    os.mkdir(legacy_extract_to)
    start = time.time()
    for node_repo in node_repos:
        repo_node_folder = os.path.join(legacy_extract_to, node_repo.node_uuid[:2], node_repo.node_uuid[2:4], node_repo.node_uuid[4:]) 
        os.makedirs(repo_node_folder)
        create_folder(base=repo_node_folder, node_repo=node_repo)
    tot_time = time.time() - start
    print("Time to recreate the repository in '{}': {:.3f} s".format(legacy_extract_to, tot_time))

    # Check that the two folders are identical
    try:
        output = subprocess.check_output(['diff', '-rq', node_folder, legacy_extract_to])
    except subprocess.CalledProcessError as exc:
        print("ERROR! NON ZERO ERROR CODE. OUTPUT:")
        print(exc.output.decode('utf8'))
        sys.exit(1)
    if output:
        print("ERROR! FOLDERS DIFFER:")
        print(output.decode('utf8'))
        sys.exit(1)

    print("All tests passed.")


def create_folder(base, node_repo, start_from=""):
    for obj in node_repo.list_objects(start_from):
        obj_relpath = os.path.join(start_from, obj.name)
        if obj.type == FileType.DIRECTORY:
            os.mkdir(os.path.join(base, obj_relpath))
            create_folder(base, node_repo, start_from=obj_relpath)
        elif obj.type == FileType.FILE:
            with node_repo.open(obj_relpath) as source_fhandle:
                # One could do streamed here
                with open(os.path.join(base, obj_relpath), 'wb') as dest_fhandle:
                    dest_fhandle.write(source_fhandle.read())
        else:
            raise RuntimeError("Unknown object type {}".format(obj.type))


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter



# node_repo = NodeRepository(
#     node_uuid=node_uuid,
#     container=self._container,
#     folder_meta=folder_meta)
# print('ls:', node_repo.list_objects())
# print('ls "":', node_repo.list_objects(""))
# print('ls .:', node_repo.list_objects(""))
# print('ls a:', node_repo.list_objects("a"))
# print('ls ./b:', node_repo.list_objects("./b"), node_repo.list_object_names("b"))
# print('ls b/c:', node_repo.list_objects("b/c"))
# try:
#     print('ls b/c/d":', node_repo.list_objects("b/c/d"))
# except IOError as exc:
#     print('  ->', str(exc))

# print("*"*72)
# print('b/c:', node_repo.get_object("b/c"))
# print('b/c/e:', node_repo.get_object("b/c/e"))

# print('content of b/c/e:', node_repo.get_object_content("b/c/e"))
# print('content of b/c/f:', node_repo.get_object_content("b/c/f"))