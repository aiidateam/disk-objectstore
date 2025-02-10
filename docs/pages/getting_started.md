# Getting started

Here we show a minimal example of how to use the API of the `disk-objectstore` to store and retrieve objects.

## Basic API usage

Let us run a quick demo of how to store and retrieve objects in a container:

```python
from disk_objectstore import Container, CompressMode

# Let's create a new container in the local folder `temp_container`, and initialise it
container = Container("temp_container")
container.init_container(clear=True)

# Let's add two objects
hash1 = container.add_object(b"some_content")
hash2 = container.add_object(b"some_other_content")

# Let's look at the hashes
print(hash1)
# Output: 6a96df63699b6fdc947177979dfd37a099c705bc509a715060dbfd3b7b605dbe
print(hash2)
# Output: cfb487fe419250aa790bf7189962581651305fc8c42d6c16b72384f96299199d

# Let's retrieve the objects from the hash
container.get_object_content(hash1)
# Output: b'some_content'
container.get_object_content(hash2)
# Output: b'some_other_content'

# Let's add a new object with the same content of an existing one: it will get the same
# hash and will not be stored twice
hash1bis = container.add_object(b"some_content")
assert hash1bis == hash1

# Let's pack all objects: instead of having a lot of files, one per object, all objects
# are written in a few big files (great for performance, e.g. when using rsync) +
# internally a SQLite database is used to know where each object is in the pack files.
# In addition, we can also ask to compress files. `CompresMode.AUTO` will perform
# fast heuristics to decide, object by object, if it's worth compressing the object or not.
container.pack_all_loose(compress=CompressMode.AUTO)

# The previous operation puts loose objects into packs, but does not delete by default
# the loose objects. This function removes them (as they are not used anymore), and possibly
# performs some additional cleanup.
container.clean_storage()

# After packing, everthing works as before
container.get_object_content(hash2)
# Output: b'some_other_content'

# This third object will be stored as loose
hash3 = container.add_object(b"third_content")

# It is important to close the container after usage to free acquired as file
# handlers and SQL connections
container.close()
```

## Advanced usage

The example above works fine for small objects. We suggest that you continue with [the advanced usage](advanced_usage)
documentation if you want to use the library with large objects (that e.g. might not fit in the RAM).
