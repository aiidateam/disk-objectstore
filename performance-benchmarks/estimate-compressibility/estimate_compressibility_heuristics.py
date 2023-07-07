#!/usr/bin/env python
import os
import sys
import time
import zlib
from disk_objectstore.utils import estimate_compression, get_compressobj_instance

with open(sys.argv[1], 'rb') as stream:
    filesize = os.fstat(stream.fileno()).st_size
    print(f"{filesize = } bytes ({filesize/1024/1024:.2f} MB)")
    t = time.monotonic()
    estimated = estimate_compression(stream, size=filesize)
    estimated_t = time.monotonic() - t
    print(f"Estimated compression: {estimated*100:.1f}% ({1000*estimated_t:.3f} ms)")

    compresser = get_compressobj_instance("zlib+1")
    t = time.monotonic()

    MAX_SIZE = min(100_000_000, filesize)

    CHUNK_SIZE = 500_000
    compressor = zlib.compressobj()
    size_compressed = 0
    position = 0
    last_progress = None
    while True:
        chunk = stream.read(CHUNK_SIZE)
        position += len(chunk)
        if position > MAX_SIZE: # actual compress size could be a bit larger than max_size, actually, depends on the last read chunk
            filesize = position
            break
        progress = int(100 * position / MAX_SIZE)
        if progress != last_progress:
            last_progress = progress
            #print(f"Compressing... {progress}%")
        if not chunk:
            size_compressed += len(compresser.flush())
            break
        size_compressed += len(compresser.compress(chunk))
        
    full_t = time.monotonic() - t
    print(f"Actual compression:    {size_compressed/filesize*100:.1f}% ({1000*full_t:.3f} ms) ({size_compressed} bytes)")
