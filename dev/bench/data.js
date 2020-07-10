window.BENCHMARK_DATA = {
  "lastUpdate": 1594399514277,
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
          "id": "0f55bed73ac1f06b7aaac5a3fc28ac2359530ac4",
          "message": "Merge pull request #44 from giovannipizzi/object_meta\n\nReadme change for the previous change and fix in test",
          "timestamp": "2020-06-29T14:54:11+02:00",
          "tree_id": "f596f20d7180d9d03843fdd7bbebd22e028348ea",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/0f55bed73ac1f06b7aaac5a3fc28ac2359530ac4"
        },
        "date": 1593435310365,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.4247731487034907,
            "unit": "iter/sec",
            "range": "stddev: 0.047830669424205184",
            "extra": "mean: 2.3541977713333324 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.491925872271792,
            "unit": "iter/sec",
            "range": "stddev: 0.009009785899389264",
            "extra": "mean: 286.37492219999956 msec\nrounds: 5"
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
          "id": "d76727c1cfc2bd09a1dc0623fdaaafe1a37e9361",
          "message": "Merge pull request #47 from giovannipizzi/fix_45\n\nAdd `has_object` and `has_objects` methods",
          "timestamp": "2020-07-08T23:37:07+02:00",
          "tree_id": "bb2c71eb780474decfeed149f228b7cb2d4f5c60",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/d76727c1cfc2bd09a1dc0623fdaaafe1a37e9361"
        },
        "date": 1594244303359,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.29268846615123645,
            "unit": "iter/sec",
            "range": "stddev: 0.07790088733686087",
            "extra": "mean: 3.416602003999998 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.7735530001510016,
            "unit": "iter/sec",
            "range": "stddev: 0.011556316957077262",
            "extra": "mean: 360.5483652000004 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.5303802486219373,
            "unit": "iter/sec",
            "range": "stddev: 0.017569426908008064",
            "extra": "mean: 653.4323746666691 msec\nrounds: 3"
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
          "id": "2fb506418941ce59f8978c2ae47968d4e484ea37",
          "message": "Merge pull request #49 from giovannipizzi/add_simple_docs\n\nAdding a simple how-to guide to go through the API interface",
          "timestamp": "2020-07-10T18:41:52+02:00",
          "tree_id": "556717932b6d1de938efe63b0b81b21a4fc73b49",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/2fb506418941ce59f8978c2ae47968d4e484ea37"
        },
        "date": 1594399377416,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.41916164198429673,
            "unit": "iter/sec",
            "range": "stddev: 0.024293885879337937",
            "extra": "mean: 2.385714483000006 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.612533278159796,
            "unit": "iter/sec",
            "range": "stddev: 0.006616387697415076",
            "extra": "mean: 276.814059000003 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 2.025261272881027,
            "unit": "iter/sec",
            "range": "stddev: 0.015197485654280522",
            "extra": "mean: 493.7634533333342 msec\nrounds: 3"
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
          "id": "0f55bed73ac1f06b7aaac5a3fc28ac2359530ac4",
          "message": "Merge pull request #44 from giovannipizzi/object_meta\n\nReadme change for the previous change and fix in test",
          "timestamp": "2020-06-29T14:54:11+02:00",
          "tree_id": "f596f20d7180d9d03843fdd7bbebd22e028348ea",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/0f55bed73ac1f06b7aaac5a3fc28ac2359530ac4"
        },
        "date": 1593435391477,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.30489894275518165,
            "unit": "iter/sec",
            "range": "stddev: 0.028810502051465833",
            "extra": "mean: 3.2797752296666673 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.4977782000643662,
            "unit": "iter/sec",
            "range": "stddev: 0.009722049070577457",
            "extra": "mean: 400.3558042000009 msec\nrounds: 5"
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
          "id": "d76727c1cfc2bd09a1dc0623fdaaafe1a37e9361",
          "message": "Merge pull request #47 from giovannipizzi/fix_45\n\nAdd `has_object` and `has_objects` methods",
          "timestamp": "2020-07-08T23:37:07+02:00",
          "tree_id": "bb2c71eb780474decfeed149f228b7cb2d4f5c60",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/d76727c1cfc2bd09a1dc0623fdaaafe1a37e9361"
        },
        "date": 1594244344083,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.2935004652740095,
            "unit": "iter/sec",
            "range": "stddev: 0.07446688481677756",
            "extra": "mean: 3.4071496243333335 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.4519402522458646,
            "unit": "iter/sec",
            "range": "stddev: 0.009572421643208772",
            "extra": "mean: 407.8402804 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 0.8505371359325654,
            "unit": "iter/sec",
            "range": "stddev: 0.2595299084299431",
            "extra": "mean: 1.1757276169999997 sec\nrounds: 3"
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
          "id": "0f55bed73ac1f06b7aaac5a3fc28ac2359530ac4",
          "message": "Merge pull request #44 from giovannipizzi/object_meta\n\nReadme change for the previous change and fix in test",
          "timestamp": "2020-06-29T14:54:11+02:00",
          "tree_id": "f596f20d7180d9d03843fdd7bbebd22e028348ea",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/0f55bed73ac1f06b7aaac5a3fc28ac2359530ac4"
        },
        "date": 1593435390689,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.2262943778172613,
            "unit": "iter/sec",
            "range": "stddev: 0.068860451548065",
            "extra": "mean: 4.419022733333333 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.880688784211059,
            "unit": "iter/sec",
            "range": "stddev: 0.009673027892805412",
            "extra": "mean: 347.13920000000013 msec\nrounds: 5"
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
          "id": "d76727c1cfc2bd09a1dc0623fdaaafe1a37e9361",
          "message": "Merge pull request #47 from giovannipizzi/fix_45\n\nAdd `has_object` and `has_objects` methods",
          "timestamp": "2020-07-08T23:37:07+02:00",
          "tree_id": "bb2c71eb780474decfeed149f228b7cb2d4f5c60",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/d76727c1cfc2bd09a1dc0623fdaaafe1a37e9361"
        },
        "date": 1594244413896,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.2549701804724832,
            "unit": "iter/sec",
            "range": "stddev: 0.017174190526873023",
            "extra": "mean: 3.922027266666666 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.7889255781345126,
            "unit": "iter/sec",
            "range": "stddev: 0.013955256260348915",
            "extra": "mean: 358.56101999999976 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.1605989650087893,
            "unit": "iter/sec",
            "range": "stddev: 0.033294229418964975",
            "extra": "mean: 861.6240666666689 msec\nrounds: 3"
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
          "id": "2fb506418941ce59f8978c2ae47968d4e484ea37",
          "message": "Merge pull request #49 from giovannipizzi/add_simple_docs\n\nAdding a simple how-to guide to go through the API interface",
          "timestamp": "2020-07-10T18:41:52+02:00",
          "tree_id": "556717932b6d1de938efe63b0b81b21a4fc73b49",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/2fb506418941ce59f8978c2ae47968d4e484ea37"
        },
        "date": 1594399512821,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.2628689441205554,
            "unit": "iter/sec",
            "range": "stddev: 0.04695523819174394",
            "extra": "mean: 3.804177033333333 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.8611206322847647,
            "unit": "iter/sec",
            "range": "stddev: 0.01129436793207183",
            "extra": "mean: 349.51340000000073 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.154641879738505,
            "unit": "iter/sec",
            "range": "stddev: 0.016538264184912627",
            "extra": "mean: 866.0694000000007 msec\nrounds: 3"
          }
        ]
      }
    ]
  }
}