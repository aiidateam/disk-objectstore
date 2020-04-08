#!/bin/bash

PYTHONUNBUFFERED=1

NUM_LOCUSTS=3
./periodic_packer.py &
for i in `seq $NUM_LOCUSTS`
do
    ./objectstore_locust.py -r 8 -w 0 &
done

# Wait for everyting to finish
wait