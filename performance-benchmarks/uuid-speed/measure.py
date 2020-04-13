#!/usr/bin/env python

import uuid
import time

N = 10000

v = []

start = time.time()
for i in range(N):
    v.append(str(uuid.uuid4()))
tot_time = time.time() - start

print('Total time to generate {} UUID4 (str): {} s'.format(N, tot_time))
print('Time per UUID (microseconds): {}'.format(tot_time / float(N) *
                                                1000000.))

start = time.time()
for i in range(N):
    v.append(uuid.uuid4().hex)
tot_time = time.time() - start

print('Total time to generate {} UUID4 (.hex): {} s'.format(N, tot_time))
print('Time per UUID (microseconds): {}'.format(tot_time / float(N) *
                                                1000000.))
