window.BENCHMARK_DATA = {
  "lastUpdate": 1593430152846,
  "repoUrl": "https://github.com/giovannipizzi/disk-objectstore",
  "entries": {
    "Benchmark on ubuntu-latest": [
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
          "id": "37e4914e091106642af3975663590f013d0813b3",
          "message": "Merge pull request #40 from giovannipizzi/move_benchmarks_new_workflow\n\nMoving benchmarks to a different workflow",
          "timestamp": "2020-06-29T09:05:10+02:00",
          "tree_id": "21cfdf2eed33a3725bbd4cbbf25afc1b0bedfa02",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/37e4914e091106642af3975663590f013d0813b3"
        },
        "date": 1593414371696,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.36360785435652976,
            "unit": "iter/sec",
            "range": "stddev: 0.0005547910503580832",
            "extra": "mean: 2.7502156183333333 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.0819366804792083,
            "unit": "iter/sec",
            "range": "stddev: 0.01126805757191704",
            "extra": "mean: 324.4712996000004 msec\nrounds: 5"
          }
        ]
      },
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
          "id": "1080bfabe7608f846b4d91278f963d24c18c72a1",
          "message": "Merge pull request #41 from giovannipizzi/increase_coverage\n\nAdding a test that covers one missing line",
          "timestamp": "2020-06-29T09:29:13+02:00",
          "tree_id": "760b3d95f1595f870ea05a2ec9a502b9ca6c3884",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/1080bfabe7608f846b4d91278f963d24c18c72a1"
        },
        "date": 1593415809165,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.38715282348175206,
            "unit": "iter/sec",
            "range": "stddev: 0.11247699156919953",
            "extra": "mean: 2.5829593363333267 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.2800522498678366,
            "unit": "iter/sec",
            "range": "stddev: 0.017329640462180707",
            "extra": "mean: 304.8731922000002 msec\nrounds: 5"
          }
        ]
      },
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
          "id": "7eda99b2f330e4fee334381a9800d6aca1974d12",
          "message": "Merge pull request #42 from giovannipizzi/increase_coverage\n\nTrying to see if standard github token works",
          "timestamp": "2020-06-29T09:58:18+02:00",
          "tree_id": "5079e5290b4c4795ef6426c38f1a5f9fdd801159",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/7eda99b2f330e4fee334381a9800d6aca1974d12"
        },
        "date": 1593417599672,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.33870499222791906,
            "unit": "iter/sec",
            "range": "stddev: 0.08115503595088375",
            "extra": "mean: 2.952421791666675 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.5570282980666783,
            "unit": "iter/sec",
            "range": "stddev: 0.008791575078151398",
            "extra": "mean: 281.133552 msec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "giovanni.pizzi@epfl.ch",
            "name": "Giovanni Pizzi",
            "username": "giovannipizzi"
          },
          "committer": {
            "email": "giovanni.pizzi@epfl.ch",
            "name": "Giovanni Pizzi",
            "username": "giovannipizzi"
          },
          "distinct": true,
          "id": "8f93a1e9914e96e2a8892402c1faf6df2e5febb4",
          "message": "Returning more metadata when iterating over objects\n\nWe now don't return only the size, but a set of metadata.\nNote that this a backward-incompatible change (for those who\nwere using the internal get_objects_stream_and_meta (that anyway\nused to be called get_objects_stream_and_size, and does not exist anymore).\nTherefore, I upped the version to 0.4.0.\n\nI also added a get_object_stream_and_meta (at the singular) for a single object.",
          "timestamp": "2020-06-29T12:08:47+02:00",
          "tree_id": "3dfddd917f5aa1bec1e88f60b058390b416a8997",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/8f93a1e9914e96e2a8892402c1faf6df2e5febb4"
        },
        "date": 1593430098116,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3656987779239515,
            "unit": "iter/sec",
            "range": "stddev: 0.026774611001445348",
            "extra": "mean: 2.734490953666665 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.9783977650012465,
            "unit": "iter/sec",
            "range": "stddev: 0.017253188551274584",
            "extra": "mean: 335.75099060000184 msec\nrounds: 5"
          }
        ]
      }
    ],
    "Benchmark on macos-latest": [
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
          "id": "37e4914e091106642af3975663590f013d0813b3",
          "message": "Merge pull request #40 from giovannipizzi/move_benchmarks_new_workflow\n\nMoving benchmarks to a different workflow",
          "timestamp": "2020-06-29T09:05:10+02:00",
          "tree_id": "21cfdf2eed33a3725bbd4cbbf25afc1b0bedfa02",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/37e4914e091106642af3975663590f013d0813b3"
        },
        "date": 1593414400104,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3306547594895717,
            "unit": "iter/sec",
            "range": "stddev: 0.01527932818493315",
            "extra": "mean: 3.0243024523333326 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.7073370080458896,
            "unit": "iter/sec",
            "range": "stddev: 0.00864343419938554",
            "extra": "mean: 369.3666496000006 msec\nrounds: 5"
          }
        ]
      },
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
          "id": "1080bfabe7608f846b4d91278f963d24c18c72a1",
          "message": "Merge pull request #41 from giovannipizzi/increase_coverage\n\nAdding a test that covers one missing line",
          "timestamp": "2020-06-29T09:29:13+02:00",
          "tree_id": "760b3d95f1595f870ea05a2ec9a502b9ca6c3884",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/1080bfabe7608f846b4d91278f963d24c18c72a1"
        },
        "date": 1593415917719,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.29642969949814485,
            "unit": "iter/sec",
            "range": "stddev: 0.043688914559747064",
            "extra": "mean: 3.3734811380000007 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.4045279739374847,
            "unit": "iter/sec",
            "range": "stddev: 0.011744473601796923",
            "extra": "mean: 415.8820404000004 msec\nrounds: 5"
          }
        ]
      },
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
          "id": "7eda99b2f330e4fee334381a9800d6aca1974d12",
          "message": "Merge pull request #42 from giovannipizzi/increase_coverage\n\nTrying to see if standard github token works",
          "timestamp": "2020-06-29T09:58:18+02:00",
          "tree_id": "5079e5290b4c4795ef6426c38f1a5f9fdd801159",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/7eda99b2f330e4fee334381a9800d6aca1974d12"
        },
        "date": 1593417608866,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.2814645353649651,
            "unit": "iter/sec",
            "range": "stddev: 0.21080038979311236",
            "extra": "mean: 3.5528454720000004 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 1.8242120789034546,
            "unit": "iter/sec",
            "range": "stddev: 0.036399749657266105",
            "extra": "mean: 548.181876200001 msec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "giovanni.pizzi@epfl.ch",
            "name": "Giovanni Pizzi",
            "username": "giovannipizzi"
          },
          "committer": {
            "email": "giovanni.pizzi@epfl.ch",
            "name": "Giovanni Pizzi",
            "username": "giovannipizzi"
          },
          "distinct": true,
          "id": "8f93a1e9914e96e2a8892402c1faf6df2e5febb4",
          "message": "Returning more metadata when iterating over objects\n\nWe now don't return only the size, but a set of metadata.\nNote that this a backward-incompatible change (for those who\nwere using the internal get_objects_stream_and_meta (that anyway\nused to be called get_objects_stream_and_size, and does not exist anymore).\nTherefore, I upped the version to 0.4.0.\n\nI also added a get_object_stream_and_meta (at the singular) for a single object.",
          "timestamp": "2020-06-29T12:08:47+02:00",
          "tree_id": "3dfddd917f5aa1bec1e88f60b058390b416a8997",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/8f93a1e9914e96e2a8892402c1faf6df2e5febb4"
        },
        "date": 1593430124790,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.32093395931193996,
            "unit": "iter/sec",
            "range": "stddev: 0.017890063746770643",
            "extra": "mean: 3.115905846 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.6262218459714695,
            "unit": "iter/sec",
            "range": "stddev: 0.007752487368555455",
            "extra": "mean: 380.77514340000033 msec\nrounds: 5"
          }
        ]
      }
    ],
    "Benchmark on windows-latest": [
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
          "id": "37e4914e091106642af3975663590f013d0813b3",
          "message": "Merge pull request #40 from giovannipizzi/move_benchmarks_new_workflow\n\nMoving benchmarks to a different workflow",
          "timestamp": "2020-06-29T09:05:10+02:00",
          "tree_id": "21cfdf2eed33a3725bbd4cbbf25afc1b0bedfa02",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/37e4914e091106642af3975663590f013d0813b3"
        },
        "date": 1593414468681,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.20892516900757802,
            "unit": "iter/sec",
            "range": "stddev: 0.06363246228713358",
            "extra": "mean: 4.786402733333333 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.5096157181046976,
            "unit": "iter/sec",
            "range": "stddev: 0.012587767155336948",
            "extra": "mean: 398.467380000001 msec\nrounds: 5"
          }
        ]
      },
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
          "id": "1080bfabe7608f846b4d91278f963d24c18c72a1",
          "message": "Merge pull request #41 from giovannipizzi/increase_coverage\n\nAdding a test that covers one missing line",
          "timestamp": "2020-06-29T09:29:13+02:00",
          "tree_id": "760b3d95f1595f870ea05a2ec9a502b9ca6c3884",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/1080bfabe7608f846b4d91278f963d24c18c72a1"
        },
        "date": 1593415877973,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3193383105828205,
            "unit": "iter/sec",
            "range": "stddev: 0.03538082068847401",
            "extra": "mean: 3.1314752 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.548726606882923,
            "unit": "iter/sec",
            "range": "stddev: 0.007091604610876532",
            "extra": "mean: 281.79122000000024 msec\nrounds: 5"
          }
        ]
      },
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
          "id": "7eda99b2f330e4fee334381a9800d6aca1974d12",
          "message": "Merge pull request #42 from giovannipizzi/increase_coverage\n\nTrying to see if standard github token works",
          "timestamp": "2020-06-29T09:58:18+02:00",
          "tree_id": "5079e5290b4c4795ef6426c38f1a5f9fdd801159",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/7eda99b2f330e4fee334381a9800d6aca1974d12"
        },
        "date": 1593417638613,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.22383829491805599,
            "unit": "iter/sec",
            "range": "stddev: 0.07376585107548231",
            "extra": "mean: 4.467510799999999 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.818104222963003,
            "unit": "iter/sec",
            "range": "stddev: 0.02194321447513948",
            "extra": "mean: 354.84847999999903 msec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "giovanni.pizzi@epfl.ch",
            "name": "Giovanni Pizzi",
            "username": "giovannipizzi"
          },
          "committer": {
            "email": "giovanni.pizzi@epfl.ch",
            "name": "Giovanni Pizzi",
            "username": "giovannipizzi"
          },
          "distinct": true,
          "id": "8f93a1e9914e96e2a8892402c1faf6df2e5febb4",
          "message": "Returning more metadata when iterating over objects\n\nWe now don't return only the size, but a set of metadata.\nNote that this a backward-incompatible change (for those who\nwere using the internal get_objects_stream_and_meta (that anyway\nused to be called get_objects_stream_and_size, and does not exist anymore).\nTherefore, I upped the version to 0.4.0.\n\nI also added a get_object_stream_and_meta (at the singular) for a single object.",
          "timestamp": "2020-06-29T12:08:47+02:00",
          "tree_id": "3dfddd917f5aa1bec1e88f60b058390b416a8997",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/8f93a1e9914e96e2a8892402c1faf6df2e5febb4"
        },
        "date": 1593430151603,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.2780251351959775,
            "unit": "iter/sec",
            "range": "stddev: 0.06017952623102008",
            "extra": "mean: 3.596797100000001 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.1901276523199797,
            "unit": "iter/sec",
            "range": "stddev: 0.017390113964031704",
            "extra": "mean: 313.46708000000024 msec\nrounds: 5"
          }
        ]
      }
    ]
  }
}