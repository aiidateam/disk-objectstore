#!/usr/bin/env python

import os
import uuid
import time
import zlib
import random
import numpy as np
from string import ascii_lowercase

list_chars = list(c.encode('utf8') for c in ascii_lowercase)

# Number of objects
#num_files_list = [1]
num_files_list = [1, 100, 1000, 10000, 100000, 1000000]
# Hash functions
#compression_levels = [0, 1, 3, 5, 7, 9]
compression_levels = [1]

# Total target size
total_size_target = 100000000


for num_files in num_files_list:
    size = total_size_target // num_files
    data = {}
    start = time.time()
    for _ in range(num_files):
        filename = str(uuid.uuid4().hex)
        ## Method 1
        content = os.urandom(size)

        ## Method 2
        #content = b"".join(np.random.choice(list_chars, size))

        ## Method 3
        #with open('test.dat', 'rb') as fhandle:
        #    content = fhandle.read(size)
        #content = (content + content)[:size]
        #assert len(content) == size

        data[filename] = content
    tot_time = time.time() - start
    total_size = sum(len(content) for content in data.values())
    print('{} objects generated in {} s. Total size: {} bytes (~{:.3f} MB).'.format(num_files, tot_time, total_size, (total_size / 1024) / 1024))

    for compression_level in compression_levels:
        print('TESTING FOR ZLIB COMPRESSION WITH LEVEL {}'.format(compression_level))
        v = {}
        start = time.time()
        for key, val in data.items():
            v[key] = zlib.compress(val, compression_level)
        tot_time = time.time() - start
        tot_compressed_size = sum(len(compressed_string) for compressed_string in v.values())

        print('Total time to compress {} objects: {} s (final size: {} MB, speed: {} MB/s)'.format(num_files, tot_time, tot_compressed_size / 1024  / 1024, total_size/1024/1024/tot_time))


        # Decompress
        start = time.time()
        for compressed_string in v.values():
            zlib.decompress(compressed_string)
        tot_time = time.time() - start
        print('Total time to decompress back: {} s (speed: {} MB/s)'.format(tot_time, total_size/1024/1024/tot_time))
        print('-'*72)

    print('='*72)
