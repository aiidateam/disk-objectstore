Here, we want to check that attempting to delete empty files (in empty folders) is still efficient.

NOTE: before running the tests, I created 256 empty folders 00, 01, 02, ..., fe, ff

The time to attempt to delete 1 million nodes is ~12 seconds, roughly the same as generating 1 million UUID4.

Therefore I think it's an acceptable cost and this means that, if there are no loose objects,
attempting to delete 1000000 objects will only incur in ~12 seconds overhead for attempting to delete any
loose object left around, before going to delete the packed ones.
