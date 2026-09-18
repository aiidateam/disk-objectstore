# Advanced usage

This repository is designed both for performance and for having a low memory footprint.
Therefore, it provides bulk operations and the possibility to access objects as streams.
We **strongly suggest** to use these methods if you use the `disk-objecstore` as a library,
unless you are absolutely sure that objects always fit in memory, and you never have to
access tens of thousands of objects or more.

## Bulk access

We continue from the commands of the basic usage. We can get the content of more objects at once:

```python
container.get_objects_content([hash1, hash2])
# Output: {'6a96df63699b6fdc947177979dfd37a099c705bc509a715060dbfd3b7b605dbe': b'some_content',  'cfb487fe419250aa790bf7189962581651305fc8c42d6c16b72384f96299199d': b'some_other_content'}
```

For many objects (especially if they are packed), retrieving in bulk can give orders-of-magnitude speed-up.

## Using streams

### Interface

First, let's look at the interface:

```python
with container.get_object_stream(hash1) as stream:
    print(stream.read())
# Output: b'some_content'
```

For bulk access, the syntax is a bit more convoluted (the reason is efficiency, as discussed below):

```python
with container.get_objects_stream_and_meta([hash3, hash1, hash2]) as triplets:
    for hashkey, stream, meta in triplets:
        print("Meta for hashkey {}: {}".format(hashkey, meta))
        print("  Content: {}".format(stream.read()))
```

whose output is:

```
Meta for hashkey 6a96df63699b6fdc947177979dfd37a099c705bc509a715060dbfd3b7b605dbe: {'type': 'packed', 'size': 12, 'pack_id': 0, 'pack_compressed': False, 'pack_offset': 0, 'pack_length': 12}
  Content: b'some_content'
Meta for hashkey cfb487fe419250aa790bf7189962581651305fc8c42d6c16b72384f96299199d: {'type': 'packed', 'size': 18, 'pack_id': 0, 'pack_compressed': False, 'pack_offset': 12, 'pack_length': 18}
  Content: b'some_other_content'
Meta for hashkey d1e4103ce093e26c63ce25366a9a131d60d3555073b8424d3322accefc36bf08: {'type': 'loose', 'size': 13, 'pack_id': None, 'pack_compressed': None, 'pack_offset': None, 'pack_length': None}
  Content: b'third_content'
```

```{important}
As you see above, the order of the triplets **IS NOT** the order in which you passed the hash keys to
`get_objects_stream_and_meta`. The reason is efficiency: the library will try to keep a (pack) file open as long as possible, and read it in order, to exploit efficiently disk caches.
```

### Memory-savvy approach

If you don't know the size of the object, you don't want to just call `stream.read()` (you could have just called `get_object_content()` in that case!) because if the object does not fit in memory, your application will crash.
You will need to read it in chunks and process it chunk by chunk.

A very simple pattern:

```python
# The optimal chunk size depends on your application and needs some benchmarking
CHUNK_SIZE = 100000
with container.get_object_stream(hash1) as stream:
    chunk = stream.read(CHUNK_SIZE)
    while chunk:
        # process chunk here
        # E.g. write to a different file, pass to a method to compress it, ...
        chunk = stream.read(CHUNK_SIZE)
```

You can find various examples of this pattern in the utility wrapper classes in `disk_objectstore.utils`.

Note also that if you use `get_objects_stream_and_meta`, you can use `meta['size']` to know the size
of the object before starting to read, so you can e.g. simply do a `.read()` if you know the size is small.

Finally, when writing objects, if the objects are big, instead of reading in memory the whole content, you should use
the methods `container.add_streamed_object(stream)` (loose objects) or `add_streamed_objects_to_pack(stream_list)`
(directly to packs).

## Managed objects

An ordinary object lives as long as something refers to it: you write it, you keep its hash key somewhere the container can see, and the sweep that collects unreferenced objects keeps it.

A managed object is the other case. Its lifetime belongs to whoever wrote it, and the container holds it until that writer says otherwise.

```python
hashkey = container.add_managed_object(b'the state of something still running')
container.get_managed_object_content(hashkey)
# Output: b'the state of something still running'
container.delete_managed_objects([hashkey])
# Output: {'f140fa27a0784626a46c5efbf53f83aa7ae331a5ab3f3ee75ebd7235acd53623'}
```

They are addressed by content like everything else, so writing the same bytes twice gives one object and one key. Beyond that they stay separate from loose and packed objects:

- `list_all_objects` and `count_objects` omit them, so one survives until its writer deletes it, wherever the caller records its key
- packing and `clean_storage` skip them
- a managed and an ordinary object with the same content are separate files, and deleting one keeps the other

Use them for data a container is a convenient place to keep but whose lifetime is decided elsewhere, such as the checkpoint of a task that is still running. Use an ordinary object for content that is referred to, which is almost always what you want.

Deleting them is your job. `list_managed_objects` enumerates what is there, which is the one way to find them, and `delete_managed_objects` removes them.
