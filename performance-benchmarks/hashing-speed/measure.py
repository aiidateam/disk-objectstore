#!/usr/bin/env python

import hashlib
import os
import random
import uuid
import time

# Number of objects
num_files_list = [1]
# Hash functions
hash_functions = [hashlib.md5, hashlib.sha1, hashlib.sha224, hashlib.sha256, hashlib.sha384, hashlib.sha512, hashlib.blake2b, hashlib.blake2s]

## Number of objects
#num_files_list = [1, 100, 1000, 10000, 100000, 1000000]
## Hash functions
#hash_functions = [hashlib.sha1]

# Total target size
total_size_target = 100000000


for hash_function in hash_functions:
    print('TESTING FOR HASHING FUNCTION {}'.format(hash_function.__name__))
    for num_files in num_files_list:
        size = total_size_target // num_files
        data = {}
        start = time.time()
        for _ in range(num_files):
            filename = str(uuid.uuid4().hex)
            content = os.urandom(size)
            data[filename] = content
        tot_time = time.time() - start
        total_size = sum(len(content) for content in data.values())
        print('{} objects generated in {} s. Total size: {} bytes (~{:.3f} MB).'.format(num_files, tot_time, total_size, (total_size // 1024) / 1024))

        v = {}
        start = time.time()
        for key, val in data.items():
            v[key] = hash_function(val).hexdigest()
        tot_time = time.time() - start

        print('Total time to compute hash for {} objects: {} s (speed: {} MB/s)'.format(num_files, tot_time, total_size/1024/1024/tot_time))
        print('-'*72)
    print('='*72)
