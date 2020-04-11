# Things that still need to be done

- add the concept of an object-store UUID to identify it (and e.g. associate it with
  the corresponding DB)

- Implement function to do a full repack, recreating each pack only with the known objects (e.g. if something was deleted)

- Implement validation of a pack (e.g. for overlapping objects)

- Add a @maintenance decorator that marks all writing operations to the
  packs (writing directly to packs, repacking, ...) so that only
  one process can do it at a given time.

- (Maybe) implement option to pack only a subset of the loose objects (e.g. specified with regex, explicit list, or just prefix).

- Implement deletion.

- Implement clever compression logic, i.e. try to compress, and keep uncompressed if compression ratio is
  below a given user-defined threshold. Possibly also allow to specify compression level as an option.


- Complete test suite, aiming at 100% coverage, and then increase thresholds of codecov.
  - Moreover, we need to add a few tests for concurrency (at least to check that e.g. the locking mechanism works)
    with multiple readers and writers (both while unpacked, and while packed) -> see 'test-concurrent subfolder'

- Check what happens if the process writing a loose object dies. Is the object moved anyway
  from the sandbox?

## Design decisions

- Assess risk of corruption of SQLite DB (e.g. if the code crashes while repacking), and if we need to keep more information in the pack files themselves. Or preliminarily backup the DB? Decide what to do in case the backup is open in .wal mode?

- Decide how to ensure that if the backup (via rsync) happens while packing, there is no risk of having a corrupted DB.

## Performance tests

- Perform again performance tests, including also the time in case of missing objects.

- Measure the overhead of the SQLite DBs (this is already printed in output), and maybe check if the cost if, for typical DBs, recovered by compressing

- Test performance also on remotely-mounted object-store filesystem (in particular, efficiency
  in random-access to a given position of a file)

