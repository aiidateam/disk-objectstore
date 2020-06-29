window.BENCHMARK_DATA = {
  "lastUpdate": 1593409362844,
  "repoUrl": "https://github.com/giovannipizzi/disk-objectstore",
  "entries": {
    "Benchmark on ubuntu-latest with Python 3.8": [
      {
        "commit": {
          "author": {
            "email": "giovanni.pizzi@epfl.ch",
            "name": "Giovanni Pizzi",
            "username": "giovannipizzi"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "eaece2837daa7abe2adaedffe3309141307af01b",
          "message": "Merge pull request #39 from giovannipizzi/fix_if_github_actions\n\nFixed if conditional for runs",
          "timestamp": "2020-06-29T07:38:51+02:00",
          "tree_id": "5a416ec1162b8b9f1b0cb48c6b1ff6529f26aba7",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/eaece2837daa7abe2adaedffe3309141307af01b"
        },
        "date": 1593409357600,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.31735202489340497,
            "unit": "iter/sec",
            "range": "stddev: 0.008930207476823613",
            "extra": "mean: 3.1510748996666678 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.320767892986145,
            "unit": "iter/sec",
            "range": "stddev: 0.013639855111174074",
            "extra": "mean: 301.13516879999906 msec\nrounds: 5"
          }
        ]
      }
    ],
    "Benchmark on macos-latest with Python 3.7": [
      {
        "commit": {
          "author": {
            "email": "giovanni.pizzi@epfl.ch",
            "name": "Giovanni Pizzi",
            "username": "giovannipizzi"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "eaece2837daa7abe2adaedffe3309141307af01b",
          "message": "Merge pull request #39 from giovannipizzi/fix_if_github_actions\n\nFixed if conditional for runs",
          "timestamp": "2020-06-29T07:38:51+02:00",
          "tree_id": "5a416ec1162b8b9f1b0cb48c6b1ff6529f26aba7",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/eaece2837daa7abe2adaedffe3309141307af01b"
        },
        "date": 1593409362202,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.22946784575110954,
            "unit": "iter/sec",
            "range": "stddev: 0.052770897498388834",
            "extra": "mean: 4.357909042666666 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 1.805596308315637,
            "unit": "iter/sec",
            "range": "stddev: 0.019119665201319243",
            "extra": "mean: 553.8336533999988 msec\nrounds: 5"
          }
        ]
      }
    ]
  }
}