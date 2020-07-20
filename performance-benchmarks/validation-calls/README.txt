This folder contains results of performance measurements for a LARGE DB with ~6.7M packed objects, ~160GB.

The goal is to check the performance of `validate()` and the internal calls, to make sure they are efficient.
This reports timing for sub-parts of the calls, to show that running as this is efficient also for big DBs.

Timings are reported as comments after the python code.
