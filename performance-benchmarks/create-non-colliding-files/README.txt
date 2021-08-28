I test here if it's faster to generate a UUID and create a file with that name, or use the templib.NamedTemporaryFile.

From the results, it seems the UUID approach is slighly faster.

Here are some results on a MacBook Pro (15-inch, 2016):

Creating 10000 files with UUID: 1.28 s
Creating 10000 files with tempfile: 1.84 s

Creating 10000 files with UUID: 1.33 s
Creating 10000 files with tempfile: 1.78 s
