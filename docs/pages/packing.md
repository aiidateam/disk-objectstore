# Packing

As said above, from the user point of view, accessing a `Container` where objects are all loose, all packed, or partially loose and partially packed, does not change anything from the user-interface point of view, but performance might improve a lot after packing.

Note that only one process can pack (or write in packs in general) at a given time, while any number of
processes can write concurrently loose objects, and read objects (both loose and packed).

The continuous integration tests check also that any number of processes can continue to write concurrently loose objects and read from packs even while a *single process* is performing the packing operation.

Finally, in specific applications (for which you have to write a lot of objects, and you know that there
are no concurrent processes accessing the packs) you can directly write to the packs for performance reasons.

The interface is the following:

```python
container.add_objects_to_pack([b"obj1", b"obj2"])
# Output: ['7e485fc048df85f62cb1ec17174072380519e3064a0510ec00daaa381a680942', '71d00f404e92546cba0e69b27b13394af4592e4da22bf24c58a95ec3f4f45584']
```

or, better, for big objects using streams, you can use `add_streamed_objects_to_pack`.

As an example, let's create two files:

```python
with open("file1.txt", "wb") as fhandle:
    fhandle.write(b"file1content")
with open("file2.txt", "wb") as fhandle:
    fhandle.write(b"file2content")
```

Now you can exploit the `LazyOpener` wrapper to lazily create handles to files, that are actually open only when accessed.
Let's now add their content to the `Container`, in a way that works even for TB files without filling up all your RAM:

```python
from disk_objectstore.utils import LazyOpener

container.add_streamed_objects_to_pack(
    [LazyOpener("file1.txt"), LazyOpener("file2.txt")], open_streams=True
)
```

Output:

```python
[
    "ce3e75d02effb66eda58779e3b0f9e454aad218b9d5a38903a105f177f2dde23",
    "eeeb27c2f0348e327ec8e66e7f5667798df601e6d1c62209dde749d370732a48",
]
```

Note that we use the `LazyOpener` here, because there is an operating-system limit on the number of
open files you can have at the same time (and this limit is quite low e.g. on Mac OS). The snippet above works with any number of files thanks to the use of the `LazyOpener` and the fact that `add_streamed_objects_to_pack()` will open the files only when needed (thanks to the `open_streams=True` parameter) and close them as soon as not needed anymore.

If you instead don't need to "open" the streams, but you can just call `.read(SIZE)` on them,
you can simply do:

```python
from io import BytesIO

stream1 = BytesIO(b"file1content")
stream2 = BytesIO(b"file2content")
container.add_streamed_objects_to_pack([stream1, stream2])
```

which has the same output as before.
Note that this is just to demonstrate the interface: the `BytesIO` object will store the whole data in memory!

## Reclaiming space

To avoid race conditions, while packing the corresponding loose files are not deleted.
In order to reclaim that space, after making sure that no process is still accessing the loose objects, one can do

```python
container.clean_storage()
```

Note: Technically processes can still continue using the container during this operation, with the following caveats:

- on Linux, the operation should be callable at any time; files will be deleted, but if they are open can still be
  accessed correctly. Once closed, they will actually be removed from disk and don't occupy space anymore.
- on Windows, the operation should be callable at any time; if a loose object is open, it will not be deleted.
  A future `clean_storage` call will delete it once it's not used anymore.
- on Mac OS X, it is better not to call it while processes are still accessing the file, because there are race
  conditions under which the file might be read as empty. If the file is already open, the same notes as Linux apply.
  However, once objects are packed, new implementations will prefer the packed version and open that one. So, it is
  OK to call the `clean_storage`. However, one should be careful with concurrently continuing to write loose objects and
  accessing them for the aforementioned race condition.
