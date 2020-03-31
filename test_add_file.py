#!/usr/bin/env python
import os
import uuid

from files_db.models import Obj, FileRef, get_session
from files_db.common import LOOSE_FOLDER, DB_FILE
from files_db.add_file import add_file, add_files, add_files_to_pack, get_file_content, pack_all_loose

if __name__ == "__main__":
    import random
    # import hashlib
    import time

    session = get_session(DB_FILE)

    files = {}
    # generate files
    NFILES = 100
    MIN_SIZE = 0
    MAX_SIZE = 1000
    ADD_LOOSE_IN_ONE_COMMIT = False
    ADD_DIRECTLY_TO_PACK = True

    current_number_of_loose = len(os.listdir(LOOSE_FOLDER))

    print("Currently known files:", session.query(FileRef).count())
    print("Currently known loose objects:", session.query(FileRef).join(Obj).filter(Obj.packed==False).count())
    print("Loose objects on disk:", current_number_of_loose)

    print("Generating {} files in memory...".format(NFILES))
    for _ in range(NFILES):
        filename = str(uuid.uuid4())[:8]
        size = random.randint(MIN_SIZE, MAX_SIZE)
        content = bytearray(random.getrandbits(8) for _ in range(size))
        #md5 = str(hashlib.md5(content).hexdigest())
        #files[filename] = md5
        files[filename] = content
    total_size = sum(len(content) for content in files.values())
    print("Done. Total size: {} bytes (~{:.3f} MB).".format(total_size, (total_size // 1024) / 1024))

    if ADD_DIRECTLY_TO_PACK:
        start = time.time()
        add_files_to_pack(session, files)
        tot_time = time.time() - start
        print("Time to store {} objects DIRECTLY TO THE PACKS: {:.4} s".format(
            NFILES, tot_time))

        # No loose files were created
        assert len(os.listdir(LOOSE_FOLDER)) == current_number_of_loose
    else:
        start = time.time()
        if ADD_LOOSE_IN_ONE_COMMIT:
            add_files(session, files)
        else:
            for filename, content in files.items():
                add_file(session, filename, content)
        tot_time = time.time() - start
        print("Time to store {} loose objects ({}): {:.4} s".format(
            NFILES, "IN ONE COMMIT" if ADD_LOOSE_IN_ONE_COMMIT else "IN INDEPENDENT COMMITS", tot_time))


        retrieved = {}
        random_keys = list(files.keys())
        random.shuffle(random_keys)
        start = time.time()
        for filename in random_keys:
            retrieved_content = get_file_content(session, filename)
            retrieved[filename] = retrieved_content
            #retrieved = str(hashlib.md5(retrieved_content).hexdigest())
        tot_time = time.time() - start
        print("Time to retrieve {} loose objects: {:.4} s".format(NFILES, tot_time))

        for filename in retrieved:
            assert retrieved[filename] == files[filename], "Mismatch for {}".format(filename)

        # Check that NFILES new loose files are present now
        assert len(os.listdir(LOOSE_FOLDER)) == current_number_of_loose + NFILES

        start = time.time()
        pack_all_loose(session)
        tot_time = time.time() - start
        print("Time to pack all loose objects: {:.4} s".format(tot_time))

        # Check that all loose files are gone
        assert not os.listdir(LOOSE_FOLDER)


    retrieved = {}
    random_keys = list(files.keys())
    random.shuffle(random_keys)
    start = time.time()
    for filename in random_keys:
        retrieved_content = get_file_content(session, filename)
        retrieved[filename] = retrieved_content
        #retrieved = str(hashlib.md5(retrieved_content).hexdigest())
    tot_time = time.time() - start
    print("Time to retrieve {} packed objects in random order: {} s".format(NFILES, tot_time))

    for filename in retrieved:
        assert retrieved[filename] == files[filename], "Mismatch for {}".format(filename)

    print("All tests passed")