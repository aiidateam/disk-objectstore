# disk-objectstore

An implementation of an efficient key-value store that writes directly on disk
and does not require a server running.

|                |                                                                                              |
| -------------- | -------------------------------------------------------------------------------------------- |
| Latest release | [![PyPI version][pypi-badge]][pypi-link] [![PyPI pyversions][pypi-pyversions]][pypi-link]    |
| Build status   | [![Build Status][build-badge]][build-link] [![Coverage Status][codecov-badge]][codecov-link] |
| Getting help   | [![Docs status][rtd-badge]][rtd-link]                                                        |
| Performance    | [Benchmarks][bench-link]                                                                     |

## Goal

The goal of this project is to have a very efficient implementation of an "object store"
that works directly on a disk folder, does not require a server to run, and addresses
a number of performance issues, discussed also below.

This project targets objects that range from very few bytes up to tens of GB each, with
performance tuned to support tens of millions of objects or more.

This project originated from the requirements needed by an efficient repository
implementation in [AiiDA](http://www.aiida.net) (note, however, that this
package is completely independent of AiiDA).

## How to install

To install, just run:

```
pip install disk-objectstore
```

This will also install a simple `dostore` command line utility together with the library itself.

## Documentation

For instructions on how to use it, some quick start guide, and more detailed information
on the design of the library and its performance, you can check [the documentation](https://disk-objectstore.readthedocs.io/).

[bench-link]: https://aiidateam.github.io/disk-objectstore/dev/bench/
[build-badge]: https://github.com/aiidateam/disk-objectstore/workflows/Continuous%20integration/badge.svg
[build-link]: https://github.com/aiidateam/disk-objectstore/actions
[codecov-badge]: https://codecov.io/gh/aiidateam/disk-objectstore/branch/main/graph/badge.svg
[codecov-link]: https://codecov.io/gh/aiidateam/disk-objectstore
[pypi-badge]: https://badge.fury.io/py/disk-objectstore.svg
[pypi-link]: https://pypi.python.org/pypi/disk-objectstore
[pypi-pyversions]: https://img.shields.io/badge/Supported%20platforms-windows%20%7c%20macos%20%7c%20linux-1f425f.svg
[rtd-badge]: https://readthedocs.org/projects/disk-objectstore/badge
[rtd-link]: http://disk-objectstore.readthedocs.io/
