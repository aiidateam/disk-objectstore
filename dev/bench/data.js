window.BENCHMARK_DATA = {
  "lastUpdate": 1593417639971,
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
      }
    ]
  }
}