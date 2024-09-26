# Changelog

## v1.2.0 (26 September 2024)

This only enforces proper semantic versioning as the last release added a new functionality. No changes have been added.

## v1.1.1 (19 September 2024)

- Added progress bar functionality for repack and pack_all_loose [\[737f9c7\]](https://github.com/aiidateam/disk-objectstore/commit/737f9c71151bf7ac297c6431688b4a75eac91b7c)

## v1.1.0 (7 March 2024)

### Features

- Add functionality to easily create a container backup [\[23c784a\]](https://github.com/aiidateam/disk-objectstore/commit/23c784a221954a1518a3e35affdec53681f809b7)

## v1.0.0 (September 2023)

### Features

- Add support for `whence=2` in `PackedObjectReader.seek` [\[5515ab6\]](https://github.com/aiidateam/disk-objectstore/commit/5515ab6d75581b36ecb3e0b8ff37407e05abefda)
- Add support for changing compression when repacking, and add auto compression heuristics [\[599e87c\]](https://github.com/aiidateam/disk-objectstore/commit/599e87c852427e02062f04f5f3d2276013410710)
- Improve efficiency when accessing packed compressed objects [\[10edd63\]](https://github.com/aiidateam/disk-objectstore/commit/10edd6395455d7c59361e608396b672289d8de58)

### Changes

- A number of API methods changed the return type from bare dictionaries to dataclass instances [\[7a63462\]](https://github.com/aiidateam/disk-objectstore/commit/7a634626ea3e5f35aa3cdd458daf9d8b825d759a)

  - `Container.get_object_stream_and_meta -> ObjectMeta`
  - `Container.get_objects_meta -> ObjectMeta`
  - `Container.get_object_meta -> ObjectMeta`
  - `Container.count_objects -> ObjectCount`
  - `Container.get_total_size -> TotalSize`
  - `Container.validate -> ValidationIssues`

  The dataclasses are importable from `disk_objectstore.dataclasses`.

- A number of API methods replaced using `os.path` with `str` paths, for `pathlib.Path` [\[df96142\]](https://github.com/aiidateam/disk-objectstore/commit/df9614236b7d420fb610313d70ffae51e7aead75)
  The following methods now return a `pathlib.Path` instance:

  - `Container.get_folder`
  - `LazyOpener.path`

- Various improvements to docs and code [\[5ba9316\]](https://github.com/aiidateam/disk-objectstore/commit/5ba93162cd49d9b1ca7149c502349bfb06833255)

### Devops

- Moving documentation to `sphinx+myst` [\[2002f3c\]](https://github.com/aiidateam/disk-objectstore/commit/2002f3c3ec07f7ff46a04df293c8c9a7dff4db6a)
- Adopt PEP 621 and move build spec to `pyproject.toml` [\[4bd0c4e\]](https://github.com/aiidateam/disk-objectstore/commit/4bd0c4e01eaf3c149d4e11921b7ff4d42a5d5da5)
- Make types more permissive [\[c012056\]](https://github.com/aiidateam/disk-objectstore/commit/c0120568a992b41a55b325f3217d4902b5281070)

### Dependencies

- Add Python 3.11 support [\[afdae26\]](https://github.com/aiidateam/disk-objectstore/commit/afdae261a5849e994b5920ca07665fc6a19f3852)
- Unpin `sqlalchemy` adding support for `>=1.4.22` [\[a2a987f\]](https://github.com/aiidateam/disk-objectstore/commit/a2a987f02a128b7cc265982e102d210e6e17d6f6)
- Removed uneeded `ablog` dependencies [\[8165f58\]](https://github.com/aiidateam/disk-objectstore/commit/8165f58fefdd40b55555eef9a2d40ee280593232)

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
