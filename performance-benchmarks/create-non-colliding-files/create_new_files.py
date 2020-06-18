"""Create new files avoiding collisions in two ways.

I will use the UUID because it seems to be a bit faster:

Here are some results on a MacBook Pro (15-inch, 2016):

Creating 10000 files with UUID: 1.28 s
Creating 10000 files with tempfile: 1.84 s

Creating 10000 files with UUID: 1.33 s
Creating 10000 files with tempfile: 1.78 s
"""
import os
import time
import tempfile
import uuid

N = 10000

t = time.time()
for _ in range(N):
    open(os.path.join('a', uuid.uuid4().hex), 'wb').close()
print('Creating {} files with UUID: {:.3} s'.format(N, time.time() - t))

t = time.time()
for _ in range(N):
    tempfile.NamedTemporaryFile(mode='wb', dir='a', delete=False).close()
print('Creating {} files with tempfile: {:.3} s'.format(N, time.time() - t))
