#!/bin/bash

# This script launches a number of periodic workers with one periodic packer.
# This is just to demonstrate the functionality, but these tests will be run by
# pytest without using this bash script.

PYTHONUNBUFFERED=1

NUM_WORKERS=4
./periodic_packer.py &
for i in `seq $NUM_WORKERS`
do
    run_with_bulk=$(($i % 2))
    if [ "$run_with_bulk" == "0" ]
    then
	./periodic_worker.py -r 8 -w 0 -b &
    else
	./periodic_worker.py -r 8 -w 0 &
    fi
done

# Wait for everyting to finish
wait
