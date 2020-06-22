#!/usr/bin/env python
import random
import os
import shutil
import time

average_file_size = 1_000_000
count = 1021

contents = []

start = time.time()
for fileid in range(count):
    size = random.randint(1, average_file_size * 2)
    # This is slow, better to use the following line
    #contents.append(bytearray(random.getrandbits(8) for _ in range(size)))
    contents.append(os.urandom(size))
tot_time = time.time() - start
print('Files created in memory in {:.2f} s'.format(tot_time))

with open('/tmp/file1.dat', 'bw') as f:
    for content in contents:
        f.write(content)
print('FILE1 written:')
os.system('ls -l /tmp/file1.dat')

random.shuffle(contents)
with open('/tmp/file2.dat', 'bw') as f:
    for content in contents:
        f.write(content)
print('FILE2 written:')
os.system('ls -l /tmp/file2.dat')

print('*** TRANSFERRING FILE1 WITH RSYNC')
print()
os.system(
    'bash -c "time rsync -v --stats /tmp/file1.dat pc36viajumphost:/tmp/bigfile"'
)

print('*** REPLACING FILE1 WITH RESHUFFLED FILE2:')
os.remove('/tmp/file1.dat')
shutil.move('/tmp/file2.dat', '/tmp/file1.dat')

print('*** TRANSFERRING AGAIN THE (NOW RESHUFFLED) FILE1:')
os.system(
    'bash -c "time rsync -v --stats /tmp/file1.dat pc36viajumphost:/tmp/bigfile"'
)

# Cleanup
os.remove('/tmp/file1.dat')
os.system('''bash -c "ssh pc36viajumphost 'rm /tmp/bigfile'"''')
