# Changelog

## v0.6.0 (September 2021)

- ⬆️ UPGRADE: Remove Python support for 3.5 and 3.6, and add support for 3.9.
- ⬆️ UPGRADE: SQLAlchemy v1.4 (with v2 API) [\[#114\]](https://github.com/aiidateam/disk-objectstore/pull/114)
- ✨ NEW: Add basic CLI [\[#117\]](https://github.com/aiidateam/disk-objectstore/pull/117) (see README.md for details)
- 🔧 MAINTAIN: Add type annotations and mypy type checking [\[#113\]](https://github.com/aiidateam/disk-objectstore/pull/113)

## v0.5.0 (November 2020)

- Various general (but very important) speed improvements [\[#96\]](https://github.com/aiidateam/disk-objectstore/pull/96) [\[#102\]](https://github.com/aiidateam/disk-objectstore/pull/102)
- Add callbacks to a number of functions (e.g. export, add_objects_to_pack, ... to allow showing progress bars or similar indicators [\[#96\]](https://github.com/aiidateam/disk-objectstore/pull/96)
- Implement repacking (at least when not changing hashing or compression) [\[#96\]](https://github.com/aiidateam/disk-objectstore/pull/96)
- Remove `export` function, implement `import_objects` function instead, to be called on the other side (it's more efficient) [\[#96\]](https://github.com/aiidateam/disk-objectstore/pull/96)
- Add support for VACUUMing operations on the SQLite database (very important for efficiency) [\[#96\]](https://github.com/aiidateam/disk-objectstore/pull/96)
- Add support for multiple hashing algorithms [\[#96\]](https://github.com/aiidateam/disk-objectstore/pull/96)
- Add concept of (unique) `container_id` [\[#97\]](https://github.com/aiidateam/disk-objectstore/pull/97)
- Generalize the compression algorithm implementation, and multiple algorithms are supported now [\[#99\]](https://github.com/aiidateam/disk-objectstore/pull/99)

## v0.4.0 (20 July 2020)

- Major robustness improvements and new functionality (possibility to pack while using the repository, tested on all platforms)
- Not deleting loose files when packing; now there is a `clean_storage()` function to do it afterwards, as a maintenance operation
- Backward-incompatible change to the Container format (now it expects a `duplicates` folder, so old repositories do not work out of the box)
- Added various functionality to delete objects, validate the packs, list all objects, possibility to seek() into returned objects
- Added continuous-integation benchmarks
- Various bugfixes

## v0.3.0 (22 June 2020)

- Changed the logic of packing: now packs are not determined anymore from the first few characters of the UUID/hash, but they are sequential integers with capped max size
- Complete major rewrite of the library, where now objects are deduplicated and use a SHA256 hash to be identified. This is a backward-incompatible version, but provides much higher robustness and features, making it almost production ready (only a few useful functions need still to be implemented to facilitate repository management, like the option to perform a full repack of a repository.

## v0.2.1 (13 April 2020)

- Improving testing and continuous integration, badges, and homepage

## v0.2.0 (10 April 2020)

- Rename of the project and implementation of a number of functions

## v0.1.0 (1 April 2020)

- This is the very first version. Uses random UUIDs to identify objects.
