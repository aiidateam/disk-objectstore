#!/usr/bin/env python
import json
import os
import random
import time

import click
from profilehooks import profile

from repository.objectstore.container import Container

@click.command()
@click.option('-p', '--path', default='test-container', help='The path to a test folder in which the container will be created.')
@click.option('-P', '--with-profiling', is_flag=True, help='Perform profiling')
@click.option('-B', '--batch-read', is_flag=True, help='Use batch read')
@click.help_option('-h', '--help')
def main(path, with_profiling, batch_read):  # pylint: disable=too-many-locals
    """Profile reading functionality."""
    container = Container(path)
    if not container.is_initialised:
        print("Initialising the container...")
        container.init_container()

    start_counts = container.count_objects()
    print("Currently known objects: {} packed, {} loose".format(
        start_counts['packed'], start_counts['loose']))
    print("Pack objects on disk:", start_counts['pack_files'])

    size_info = container.get_total_size()
    print("Object store size info:")
    for key in sorted(size_info.keys()):
        print("- {:30s}: {}".format(key, size_info[key]))

    ### THIS BLOCK DOES PROTECTED ACCESS - IT'S JUST FOR NOW, 
    ### MIGHT BE MOVED LATER TO A PUBLIC FUNCION
    from repository.objectstore.models import Obj
    # In all cases, retrieve all objects
    loose_uuids = list(container._list_loose())  # pylint: disable=protected-access
    pack_uuids = []
    session = container._get_cached_session()  # pylint: disable=protected-access
    for uuid, in session.query(Obj).with_entities(Obj.uuid):
        pack_uuids.append(uuid)
    #print(len(loose_uuids), loose_uuids[:10])
    #print(len(pack_uuids), pack_uuids[:10])

    # Random order
    all_uuids = loose_uuids + pack_uuids
    random.shuffle(all_uuids)

    #@profile(sort='cumtime', filename='out.prof')
    def read_data(batch_read):
        retrieved = {}

        if batch_read:
            retrieved = container.get_object_contents(all_uuids)
        else:
            for obj_uuid in all_uuids:
                retrieved_content = container.get_object_content(obj_uuid)
                retrieved[obj_uuid] = retrieved_content

        return retrieved

    start = time.time()
    if with_profiling:
        func = profile(sort='cumtime', filename='out.prof', stdout=False)(read_data)
    else:
        func = read_data
    retrieved = func(batch_read=batch_read)
    tot_time = time.time() - start
    print("Time to retrieve {} packed objects in random order: {} s".format(len(all_uuids), tot_time))

    import hashlib 
    hashes = {k: hashlib.md5(v).hexdigest() for k, v in retrieved.items()}

    if not os.path.exists('reference_md5.json'):
        print("WARNING! reference does not exist, creating")
        with open('reference_md5.json', 'w') as f:
            json.dump(hashes, f)
    else:
        with open('reference_md5.json', 'r') as f:
            reference_hashes = json.load(f)
    
        assert hashes.keys() == reference_hashes.keys(), "{}\n{}".format(
            set(hashes.keys()).difference(reference_hashes.keys()),
            set(hashes.keys()).difference(reference_hashes.keys())
            )
        assert hashes == reference_hashes
        print("Hashes are the same as the previous run (remove json file to regenerate it)")

    if with_profiling:
        print("You can check the profiling results running 'snakeviz out.prof'")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
