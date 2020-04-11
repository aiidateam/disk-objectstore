# disk-objectstore

An implementation of an efficient object store that writes directly on disk
and does not require a server running.

|    | |
|-----|----------------------------------------------------------------------------|
|Latest release| [![PyPI version](https://badge.fury.io/py/disk-objectstore.svg)](https://badge.fury.io/py/disk-objectstore) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/disk-objectstore.svg)](https://pypi.python.org/pypi/disk-objectstore/) |
|Build status| [![Build Status](https://github.com/giovannipizzi/disk-objectstore/workflows/Continuous%20integration/badge.svg)](https://github.com/giovannipizzi/disk-bjectstore/actions) [![Coverage Status](https://codecov.io/gh/giovannipizzi/disk-objectstore/branch/develop/graph/badge.svg)](https://codecov.io/gh/giovannipizzi/disk-objectstore) |


## Goal

The goal of this project is to have a very efficient implementation of an "object store"
that works directly on a disk folder, does not require a server to run, and addresses
a number of performance issues, discussed also below.

This project originated from the requirements needed by an efficient repository
implementation in [AiiDA](http://www.aiida.net) (note, however, that this
package is completely independent of AiiDA).

## How to install

To install in development mode, run, in a (python 3) virtual environment:
```
pip install -e .[testing]
```

## Implementation considerations

This implementation, in particular, addresses the following aspects:

- objects are written, by default, in loose format. They are also uncompressed.
  This gives maximum performance when writing a file, and ensures that many writers
  can write at the same time without data corruption.

- loose objects are stored in a one-level sharding format: aa/bbccddeeff00...
  Current experience (with AiiDA) shows that it's actually not so good to use two
  levels of nesting.
  And anyway when there are too many loose objects, the idea
  is that we will pack them in few files (see below).
  The number of characters in the first part can be chosen, but a good compromise is
  2 (default, also used by git)

- for maximum performance, loose objects are simply written as they are,
  without compression, hashing, ...
  They are actually written first to a sandbox folder (in the same filesystem),
  and then moved in place with the correct UUID only when the file is closed.
  This should prevent having leftover objects if the process dies, and
  the move operation should be hopefully a fast atomic operation on most filesystems.

- When the user wants, loose objects are repacked in a few pack files. Indeed,
  just the fact of storing too many files is quite expensive
  (e.g. storing 65536 empty files in the same folder took over 3 minutes to write
  and over 4 minutes to delete on a Mac SSD).

- packing can be triggered by the user periodically.
  It is even possible (to be stress tested, though) to pack while the object store
  is in use (this might temporarily impact read performance, though).
  This operation takes all loose objects and puts them in a controllable number
  of packs. The name of the packs is given by the first few letters of the UUID
  (by default: 2, so 256 packs in total; configurable). A value of 2 is a good balance
  between the size of each pack (on average, ~4GB/pack for a 1TB repository) and
  the number of packs (having many packs means that, even when performing bulk access,
  many different files need to be open, which slows down performance).

- pack files are just concatenation of bytes of the packed objects. Any new object
  is appended to the pack (thanks to the efficiency of opening a file for appending).
  The information for the offset and length of each pack is kept in a single SQLite
  database.

- For each object, the SQLite database contains: the `uuid`, the `offset` (starting
  position of the bytestream in the file), the `length` (number of bytes to read),
  a boolean `compressed` flag, meaning if the bytestream has been zlib-compressed,
  and the `size` of the actual data (equal to `length` if `compressed` is false,
  otherwise the size of the uncompressed stream, useful for statistics).

- Note that compression is on a per-object level. This allows much greater flexibility
  (the API still does not allow for this, but this is very easy to implement).
  One could also think to clever logic to try to compress a file, but then store it
  uncompressed if it turns out that the compression ratio is not worth the time
  needed to further uncompress it later.

- the repository configuration is kept in a top-level json (number of nesting levels
  for loose objects and for packs, ...)

- API exists both to get and write a single object, but also to write directly
  to pack files (this cannot be done by multiple processes at the same time, though),
  and to read in bulk a given number of objects.
  This is particularly convenient when using the object store for bulk import and
  export, and very fast. Also, it is useful when getting all files of a given node.

  In normal operation, however, we expect the client to write loose objects,
  to be repacked  periodically (e.g. once a week).

  Some reference results for bulk operations:
  Storing 100'000 small objects directly to the packs takes about 10s.
  The time to retrieve all of them is ~2.2s when using a single bulk call,
  compared to ~44.5s when using 100'000 independent calls (still probably acceptable).
  Moreover, even getting, in 10 bulk calls, 10 random chunks of the objects (eventually
  covering the whole set of 100'000 objects) only takes ~3.4s. This should demonstrate
  that exporting a subset of the graph should be efficient (and the object store format
  could be used also inside the export file).


- All operations internally (storing to a loose object, storing to a pack, reading
  from a loose object or from a pack, compression) are all happening via streaming.
  So, even when dealing with huge files, these never fill the RAM (e.g. when reading
  or writing a multi-GB file, the memory usage has been tested to be capped at ~150MB).
  Convenience methods are available, anyway, to get directly an object content, if
  the user wants.

## Further design choices

In addition, the following design choices have been made:

- Each given object will get a random UUID (its generation cost is negligible, about
  4 microseconds per UUID).
  It's up to the caller to track this into a filename or a folder structure.
  The UUID is generated by the implementation and cannot be passed from the outside.
  This guarantees random distribution of objects in packs, and avoids to have to
  check for files already existing.

- Pack naming and strategy is not determined by the user. Anyway it would be difficult
  to provide easy options to the user to customize the behavior, while implementing
  a packing strategy that is efficient. Moreover, with the current packing strategy,
  it is immediate to know in which pack to check without having to keep also an index
  of the packs (this, however, would be possible in case we want to extend the behavior,
  since anyway we have an index). But at the moment it does not seem necessary.

- A single index file is used. Having one pack index per file, while reducing a bit
  the size of the index (one could skip storing the first part of the UUID, determined
  by the pack naming) turns out not to be very effective. Either one would keep all
  indexes open (but then one quickly hits the maximum number of open files, that e.g.
  on Mac OS is of the order of ~256), or open the index, at every request, that risks to
  be quite inefficient (not only to open, but also to load the DB, perform the query,
  return the results, and close again the file). Also for bulk requests, anyway, this
  would prevent making very few DB requests (unless you keep all files open, that
  again is not feasible).

- I tried a different way of storing the UUID on the DB (two long long ints rather than
  1 UUID string). I put a combined index on the two columns.
  I hoped in a speed up, using ints rather than strings, but (beside making the logic
  much more cumbersome and error prone) the performance actually decreased.
  So I reverted to a UUID indexed string column.

- Deletion (not implemented yet), can just occur as a deletion of the loose object or
  a removal from the index file. Later repacking of the packs can be used to recover
  the disk space still occupied in the pack files.

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



