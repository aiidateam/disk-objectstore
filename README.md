# disk-objectstore

An implementation of an efficient object store that writes directly on disk
and does not require a server running.

|    | |
|-----|----------------------------------------------------------------------------|
|Latest release| [![PyPI version](https://badge.fury.io/py/disk-objectstore.svg)](https://badge.fury.io/py/disk-objectstore) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/disk-objectstore.svg)](https://pypi.python.org/pypi/disk-objectstore/) |
|Build status| [![Build Status](https://github.com/giovannipizzi/disk-objectstore/workflows/Continuous%20integration/badge.svg)](https://github.com/giovannipizzi/disk-objectstore/actions) [![Supported platforms](https://img.shields.io/badge/Supported%20platforms-windows%20%7c%20macos%20%7c%20linux-1f425f.svg)](https://github.com/giovannipizzi/disk-objectstore/actions) [![Coverage Status](https://codecov.io/gh/giovannipizzi/disk-objectstore/branch/develop/graph/badge.svg)](https://codecov.io/gh/giovannipizzi/disk-objectstore) |


## Goal

The goal of this project is to have a very efficient implementation of an "object store"
that works directly on a disk folder, does not require a server to run, and addresses
a number of performance issues, discussed also below.

This project targets objects that range from very few bytes up to tens of GB each, with
performance tuned to support tens of millions of objects or more.

This project originated from the requirements needed by an efficient repository
implementation in [AiiDA](http://www.aiida.net) (note, however, that this
package is completely independent of AiiDA).

## How to install
To install, run:
```
pip install disk-objectstore
```

To install in development mode, run, after checking out, in a (python 3) virtual environment:
```
pip install -e .[dev]
```

## Implementation considerations

This implementation, in particular, addresses the following aspects:

- objects are written, by default, in loose format. They are also uncompressed.
  This gives maximum performance when writing a file, and ensures that many writers
  can write at the same time without data corruption.

- the key of the object is its hash key. While support for multiple types of cryptographically
  strong hash keys is trivial, in the current version only `sha256` is used.
  The package assumes that there will never be hash collision.
  At a small cost for computing the hash (that is anyway small, see performance tests)
  one gets automatic de-duplication of objects written in the object store (git does something very
  similar).
  In addition, it automatically provides a way to check for corrupted data.

- loose objects are stored in a one-level sharding format: `aa/bbccddeeff00...`
  where `aabbccddeeff00...` is the hash key of the file.
  Current experience (with AiiDA) shows that it's actually not so good to use two
  levels of nesting.
  And anyway when there are too many loose objects, the idea
  is that we will pack them in few files (see below).
  The number of characters in the first part can be chosen, but a good compromise is
  2 (default, also used by git).

- for maximum performance, loose objects are simply written as they are,
  without compression.
  They are actually written first to a sandbox folder (in the same filesystem),
  and then moved in place with the correct key (being the hash key) only when the file is closed.
  This should prevent having leftover objects if the process dies, and
  the move operation should be hopefully a fast atomic operation on most filesystems.

- When the user wants, loose objects are repacked in a few pack files. Indeed,
  just the fact of storing too many files is quite expensive
  (e.g. storing 65536 empty files in the same folder took over 3 minutes to write
  and over 4 minutes to delete on a Mac SSD). This is the main reason for implementing
  this package, and not just storing each object as a file.

- packing can be triggered by the user periodically.

  **Note**: only one process can act on packs at a given time.

  **Note**: while the goal is to make it possible to pack while the object store
  is in use (possibly only with a temporary impact read performance), this is not
  yet supported (see discussion in [#4](https://github.com/giovannipizzi/disk-objectstore/issues/4)).

  This packing operation takes all loose objects and puts them together in packs.
  Pack files are just concatenation of bytes of the packed objects. Any new object
  is appended to the pack (thanks to the efficiency of opening a file for appending).
  The information for the offset and length of each pack is kept in a single SQLite
  database.

- The name of the packs is a sequential integer. A new pack is generated when the
  pack size becomes larger than a per-container configurable target size.
  (`pack_size_target`, default: 4GB).
  This means that (except for the "last" pack), packs will always have a dimension
  larger or equal than this target size (typically around the target size, but
  it could be much larger if the last object that is added to the pack is very big).

- For each packed object, the SQLite database contains: the `uuid`, the `offset` (starting
  position of the bytestream in the file), the `length` (number of bytes to read),
  a boolean `compressed` flag, meaning if the bytestream has been zlib-compressed,
  and the `size` of the actual data (equal to `length` if `compressed` is false,
  otherwise the size of the uncompressed stream, useful for statistics), and an integer
  specifying in which pack it is stored. **Note** that the SQLite DB tracks only packed
  objects. Instead, loose objects are not tracked, and their sole presence in the
  loose folder marks their existence in the container.

- Note that compression is on a per-object level. This allows much greater flexibility
  (the API still does not allow for this, but this is very easy to implement).
  The current implementation only supports zlib compression with a default hardcoded
  level of 1 (good compression at affordable computational cost).
  Future extensions envision the possibility to choose the compression algorithm.

- the repository configuration is kept in a top-level json (number of nesting levels
  for loose objects, hashing algorithm, target pack size, ...)

- API exists both to get and write a single object, but also to write directly
  to pack files (this **cannot** be done by multiple processes at the same time, though),
  and to read in bulk a given number of objects.
  This is particularly convenient when using the object store for bulk import and
  export, and very fast. Also, it is useful when getting all files of a given node.

  In normal operation, however, we expect the client to write loose objects,
  to be repacked periodically (e.g. once a week).

- **PERFORMANCE**: Some reference results for bulk operations, performed on a
  Ubuntu 16.04 machine, 16 cores, 64GBs of RAM, with two SSD disks in RAID1 configuration),
  using the `examples/example_objectstore.py` script.
  - Storing 100'000 small objects (with random size between 0 and 1000 bytes, so a total size of around
    50 MB) directly to the packs takes about 21s.
  - The time to retrieve all of them is ~3.1s when using a single bulk call,
    compared to ~54s when using 100'000 independent calls (still probably acceptable).
    Moreover, even getting, in 10 bulk calls, 10 random chunks of the objects (eventually
    covering the whole set of 100'000 objects) is equally efficient as getting them
    all in one shot (note that for this size, only one pack file is created with the default
    configuration settings). This should demonstrate that exporting a subset of the graph should
    be efficient (and the object store format could be used also inside the export file).

    **Note**: these times are measured without flushing any disk cache.
    In any case, there is only a single pack file of about 50MB, so the additional time to
    fetch it back from disk is small. Anyway, for completeness, if we instead flush the caches
    after writing and before reading, so data needs to be read back from disk:
    - the time to retrieve 100000 packed objects in random order with a single bulk call is
      of about 3.8s, and in 10 bulk calls (by just doing this operation
      right after flushing the cache) is ~3.5s.
    - the time to retrieve 100000 packed objects in random order, one by one (right after
      flushing the cache, without doing other reads that would put the data in the cache already)
      is of about 56s.

- All operations internally (storing to a loose object, storing to a pack, reading
  from a loose object or from a pack, compression) are all happening via streaming.
  So, even when dealing with huge files, these never fill the RAM (e.g. when reading
  or writing a multi-GB file, the memory usage has been tested to be capped at ~150MB).
  Convenience methods are available, anyway, to get directly an object content, if
  the user wants.

## Further design choices

In addition, the following design choices have been made:

- Each given object is tracked with its hash key.
  It's up to the caller to track this into a filename or a folder structure.
  To guarantee correctness, the hash is computed by the implementation
  and cannot be passed from the outside.

- Pack naming and strategy is not determined by the user, except for the specification
  of a `pack_size_target`. Pack are stored consecutively, so that when a pack file
  is "full", new ones will be used. In this way, once a pack it's full, it's not changed
  anymore (unless a full repack is performed), meaning that when performing backups using
  rsync, those full packs don't need to be checked every time.

- A single index file is used. Having one pack index per file turns out not
  to be very effective, mostly because for efficiency one would need to keep all
  indexes open (but then one quickly hits the maximum number of open files for a big repo with
  many pack files; this limit is small e.g. on Mac OS, where it is of the order of ~256).
  Otherwise, one would need to open the correct index at every request, that risks to
  be quite inefficient (not only to open, but also to load the DB, perform the query,
  return the results, and close again the file).

- Deletion (not implemented yet), can just occur as a deletion of the loose object or
  a removal from the index file. Later repacking of the packs can be used to recover
  the disk space still occupied in the pack files (care needs to be taken if concurrent
  processes are using the container, though).

- The current packing format is `rsync`-friendly. `rsync` has an algorithm to just
  send the new part of a file, when appending. Actually, `rsync` has a clever rolling
  algorithm that can also detect if the same block is in the file, even if at a
  different position. Therefore, even if a pack is "repacked" (e.g. reordering
  objects inside it, or removing deleted objects) does not prevent efficient
  rsync transfer.

  Some results: Let's considering a 1GB file that took ~4.5 mins to transfer fully
  the first time  over my network.
  After transferring this 1GB file, `rsync` only takes 14 seconds
  to check the difference and transfer the additional 10MB appended to the 1GB file
  (and it indeed transfers only ~10MB).

  In addition,  if the contents are randomly reshuffled, the second time the `rsync`
  process took only 14 seconds, transferring only ~32MB, with a speedup of ~30x
  (in this test, I divided the file in 1021 chunks of random size, uniformly
  distributed between 0 bytes and 2MB, so with a total size of ~1GB, and in the
  second `rsync` run I randomly reshuffled the chunks).

- Appending files to a single file does not prevent the Linux disk cache to work.
  To test this, I created a ~3GB file, composed of a ~1GB file (of which I know the MD5)
  and of a ~2GB file (of which I know the MD5).
  They are concatenated on a single file on disk.
  File sizes are not multiples of a power of 2 to avoid alignment with block size.

  After flushing the caches, if one reads only the second half, 2GB are added to the
  kernel memory cache.

  After re-flushing the caches, if one reads only the first half, only 1GB is added
  to the memory cache.
  Without further flushing the caches, if one reads also the first half,
  2 more GBs are added to the memory cache (totalling 3GB more).

  Therefore, caches are per blocks/pages in linux, not per file.
  Concatenating files does not impact performance on cache efficiency.



