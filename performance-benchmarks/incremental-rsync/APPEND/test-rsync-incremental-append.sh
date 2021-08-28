#!/bin/bash

# I don't use an exact power of two so it's not aligned to blocks
bs=1000001
count=1021
let SIZE=count*bs
echo "bs=$bs, count=$count, size=$SIZE"
dd if=/dev/urandom of=/tmp/bigfile count=$count bs=$bs

echo "*** FILE CREATED"
ls -l /tmp/bigfile

echo "*** TRANSFERRING FILE WITH RSYNC:"
time rsync -v --stats /tmp/bigfile pc36viajumphost:/tmp/bigfile

echo "*** CREATING A SMALL FILE AND APPENDING IT TO THE SAME FILE:"
bs=10001
count=1021
let SIZE=count*bs
echo "bs=$bs, count=$count, size=$SIZE"
dd if=/dev/urandom of=/tmp/testaddition count=$count bs=$bs
cat /tmp/testaddition >> /tmp/bigfile
rm /tmp/testaddition

echo "*** TRANSFERRING AGAIN THE BIG FILE (WITH SMALL APPENDED CONTENT) WITH RSYNC:"
time rsync -v --stats /tmp/bigfile pc36viajumphost:/tmp/bigfile

rm /tmp/bigfile
ssh pc36viajumphost "rm /tmp/bigfile"
