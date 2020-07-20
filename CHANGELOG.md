# v0.4.0 (20 July 2020)
- Major robustness improvements and new functionality (possibility to pack while using the repository, tested on all platforms)
- Not deleting loose files when packing; now there is a `clean_storage()` function to do it afterwards, as a maintenance operation
- Backward-incompatible change to the Container format (now it expects a `duplicates` folder, so old repositories do not work out of the box)
- Added various functionality to delete objects, validate the packs, list all objects, possibility to seek() into returned objects
- Added continuous-integation benchmarks
- Various bugfixes

# v0.3.0 (22 June 2020)
- Changed the logic of packing: now packs are not determined anymore from the first few characters of the UUID/hash, but they are sequential integers with capped max size
- Complete major rewrite of the library, where now objects are deduplicated and use a SHA256 hash to be identified. This is a backward-incompatible version, but provides much higher robustness and features, making it almost production ready (only a few useful functions need still to be implemented to facilitate repository management, like the option to perform a full repack of a repository.

# v0.2.1 (13 April 2020)
- Improving testing and continuous integration, badges, and homepage

# v0.2.0 (10 April 2020)
- Rename of the project and implementation of a number of functions

# v0.1.0 (1 April 2020)
- This is the very first version. Uses random UUIDs to identify objects.

