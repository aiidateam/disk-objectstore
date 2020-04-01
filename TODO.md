# Things that still need to be done

## New features

- **IMPORTANT**: work on the 'filetracker' (i.e. a Postgres DB to track, given a node, which file
  it has). It's still very much work in progress. E.g. we need to avoid that a file and
  a subfolder in the same folder can have the same name.
  Also, QUESTION: do we really need to store all of this in such nested format?
  Maybe we just store a JSON representation of the folder (of a given node) in a column, and that's it?
  Do we need such a querying granularity level?

- add the concept of an object-store UUID to identify it (and e.g. associate it with
  the corresponding DB)

- Implement function to do a full repack, recreating each pack only with the known objects (e.g. if something was deleted)

- Implement validation of a pack (e.g. for overlapping objects)

- (Maybe) implement option to pack only a subset of the loose objects (e.g. specified with regex, explicit list, or just prefix).

- Add tests! We should aim at 100% coverage. 
  - Moreover, we need to add a few tests for concurrency (at least to check that e.g. the locking mechanism works).
  - It would be also good to stress-test this implementation with multiple readers and writers (both while unpacked, and while packed)

- Check what happens if the process writing a loose object dies. Is the object moved anyway
  from the sandbox?

## Design decisions

- Assess risk of corruption of SQLite DB (e.g. if the code crashes while repacking), and if we need to keep more information in the pack files themselves

- At the moment, it's still technically needed that packing operations happen while nobody is using the repository.
  This for instance happens if one is getting an object; this is not found in the packs, but while we go to the section of
  the code to get it from a loose object, the object is removed because it was packed in the meantime.
  Document this, or check if this can be overcome.

## Performance tests

- Add performance tests on a few real DBs of different size (e.g. including Giovanni's DB, SSSP, 3DD, SCDM, ...)

- Measure the overhead of the SQLite DBs (this is already printed in output), and maybe check if the cost if, for typical DBs, recovered by compressing

- Decide if we want to implement a clever compression strategy (i.e. try to compress, and keep uncompressed if compression ratio is
  below a given user-defined threshold). Possibly also allow to specify compression level as an option?

- decide if we want to extend this object store to pack not only single objects with a given UUID, but *list* of objects. Each UUID will then return a list of objects. Advantage; we can ensure that e.g. all files of a given node are physically co-located. The implementation is maybe a bit more cumbersome, but not too much. To check if this
is really needed.

- Test performance also on remotely-mounted object-store filesystem (in particular, efficiency
  in random-access to a given position of a file)

