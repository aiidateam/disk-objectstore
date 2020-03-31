#!/bin/bash

# I don't use an exact power of two so it's not aligned to blocks
bs=1000001
count1=1021
count2=2041

let SIZE1=count1*bs
let SIZE2=count2*bs

echo "bs=$bs, count1=$count1, size=$SIZE1"
echo "bs=$bs, count2=$count2, size=$SIZE2"

dd if=/dev/urandom of=/tmp/testbigfile1 count=$count1 bs=$bs
dd if=/dev/urandom of=/tmp/testbigfile2 count=$count2 bs=$bs

md5sum /tmp/testbigfile1
md5sum /tmp/testbigfile2
cat /tmp/testbigfile1 /tmp/testbigfile2 > /tmp/testbigfile
ls -l /tmp/testbigfile1 /tmp/testbigfile2 /tmp/testbigfile
rm /tmp/testbigfile1 /tmp/testbigfile2


sudo sync
sudo su -c "echo 3 > /proc/sys/vm/drop_caches"
echo "----- CACHE FLUSHED ----"
cat /proc/meminfo > step1-before-mem.txt
echo "step1-before-mem.txt written"
grep '^Cached' step1-before-mem.txt
#free
echo "******************************************"

# read 2nd part
python -c "import hashlib ; f = open('/tmp/testbigfile', 'rb') ; f.seek($SIZE1); m = hashlib.md5(); m.update(f.read($SIZE2)); f.close(); print(m.hexdigest(), 'python part 2')"

echo ""
echo "******************************************"

cat /proc/meminfo > step2-2ndhalf-mem.txt
echo "step2-2ndhalf-mem.txt written"
grep '^Cached' step2-2ndhalf-mem.txt

# FLUSH CACHE
sudo sync
sudo su -c "echo 3 > /proc/sys/vm/drop_caches"
echo "----- CACHE FLUSHED ----"

cat /proc/meminfo > step3-flush-mem.txt
echo "step3-flush-mem.txt written"
grep '^Cached' step3-flush-mem.txt


echo ""
echo "******************************************"

# read first part
python -c "import hashlib ; f = open('/tmp/testbigfile', 'rb') ; m = hashlib.md5(); m.update(f.read($SIZE1)); f.close(); print(m.hexdigest(), 'python part 1')"


cat /proc/meminfo > step4-1sthalf-mem.txt
echo "step4-1sthalf-mem.txt written"
grep '^Cached' step4-1sthalf-mem.txt
#free

echo ""
echo "******************************************"

python -c "import hashlib ; f = open('/tmp/testbigfile', 'rb') ; f.seek($SIZE1); m = hashlib.md5(); m.update(f.read($SIZE2)); f.close(); print(m.hexdigest(), 'python part 2')"

cat /proc/meminfo > step5-also2ndhalf-mem.txt
echo "step5-also2ndhalf-mem.txt written"
grep '^Cached' step5-also2ndhalf-mem.txt

rm /tmp/testbigfile
