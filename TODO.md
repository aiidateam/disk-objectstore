# Things that still need to be done

- add the concept of an object-store UUID to identify it (and e.g. associate it with
  the corresponding DB)

- Implement function to do a full repack, recreating each pack only with the known objects (e.g. if something was deleted)

- Implement validation of a pack (e.g. for overlapping objects)

- (Maybe) implement option to pack only a subset of the loose objects (e.g. specified with regex, explicit list, or just prefix).

- Add tests! We should aim at 100% coverage.
  - Moreover, we need to add a few tests for concurrency (at least to check that e.g. the locking mechanism works).
  - It would be also good to stress-test this implementation with multiple readers and writers (both while unpacked, and while packed) -> see 'test-concurrent subfolder'

- Check what happens if the process writing a loose object dies. Is the object moved anyway
  from the sandbox?

## Design decisions

- Assess risk of corruption of SQLite DB (e.g. if the code crashes while repacking), and if we need to keep more information in the pack files themselves

## Performance tests

- Measure the overhead of the SQLite DBs (this is already printed in output), and maybe check if the cost if, for typical DBs, recovered by compressing

- Decide if we want to implement a clever compression strategy (i.e. try to compress, and keep uncompressed if compression ratio is
  below a given user-defined threshold). Possibly also allow to specify compression level as an option?

- Test performance also on remotely-mounted object-store filesystem (in particular, efficiency
  in random-access to a given position of a file)

