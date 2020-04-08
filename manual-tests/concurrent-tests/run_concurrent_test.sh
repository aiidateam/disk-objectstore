#!/bin/bash

PYTHONUNBUFFERED=1

NUM_LOCUSTS=3
./periodic_packer.py &
for i in `seq $NUM_LOCUSTS`
do
    run_with_bulk=$(($i % 2))
    if [ "$run_with_bulk" == "0" ]
    then
	./objectstore_locust.py -r 8 -w 0 -b &
    else
	./objectstore_locust.py -r 8 -w 0 &
    fi
done

# Wait for everyting to finish
wait