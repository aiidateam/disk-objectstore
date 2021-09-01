window.BENCHMARK_DATA = {
  "lastUpdate": 1630493334534,
  "repoUrl": "https://github.com/aiidateam/disk-objectstore",
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
          "id": "4d493174c1354603b21ed8d623f487660a050d24",
          "message": "Merge pull request #50 from giovannipizzi/better_debugging_concurrency\n\nSlightly more detailed debugging in case of problems with the concurrent tests",
          "timestamp": "2020-07-10T19:48:46+02:00",
          "tree_id": "36d0accdc00b7f7b1eb3e3b01401bfb7c227471f",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/4d493174c1354603b21ed8d623f487660a050d24"
        },
        "date": 1594403398450,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3706970036280086,
            "unit": "iter/sec",
            "range": "stddev: 0.008086401829544837",
            "extra": "mean: 2.6976209416666657 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.1316609822332797,
            "unit": "iter/sec",
            "range": "stddev: 0.0106559717396749",
            "extra": "mean: 319.3193661999999 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.7661317220481936,
            "unit": "iter/sec",
            "range": "stddev: 0.00906977484509298",
            "extra": "mean: 566.2091833333326 msec\nrounds: 3"
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
          "id": "91ea646558962736530f212654fd83927f650c87",
          "message": "Merge pull request #53 from giovannipizzi/further_multiprocess_basic_tests\n\nFurther multiprocess basic tests",
          "timestamp": "2020-07-12T09:02:23+02:00",
          "tree_id": "e0d576ca01ebee5c8b61e515d997482d318529fb",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/91ea646558962736530f212654fd83927f650c87"
        },
        "date": 1594537426136,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.29105527835823686,
            "unit": "iter/sec",
            "range": "stddev: 0.05261663366183249",
            "extra": "mean: 3.4357734573333496 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.9816576827633745,
            "unit": "iter/sec",
            "range": "stddev: 0.007333146547935133",
            "extra": "mean: 335.38390599997 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.6591294728280859,
            "unit": "iter/sec",
            "range": "stddev: 0.011307301149092125",
            "extra": "mean: 602.725716333301 msec\nrounds: 3"
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
          "id": "6fae5f875c73bf4b5f2eb69e28467efa731c2aa3",
          "message": "Merge pull request #58 from sphuber/feature/057/packed-object-reader-mode\n\nAdd the `mode` property to the `PackedObjectReader`",
          "timestamp": "2020-07-12T21:53:29+02:00",
          "tree_id": "f32c32f225344579ea82d4787e2e232ead7dfa2c",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/6fae5f875c73bf4b5f2eb69e28467efa731c2aa3"
        },
        "date": 1594583896506,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3655111536355975,
            "unit": "iter/sec",
            "range": "stddev: 0.055409372745984814",
            "extra": "mean: 2.7358946233333463 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.1215574956684775,
            "unit": "iter/sec",
            "range": "stddev: 0.011043624687423549",
            "extra": "mean: 320.352901199999 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.763192535237077,
            "unit": "iter/sec",
            "range": "stddev: 0.015811573334728418",
            "extra": "mean: 567.1530363333469 msec\nrounds: 3"
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
          "id": "6025360bb8a030b1103e7d40da4f7bde7938dd4c",
          "message": "Merge pull request #55 from giovannipizzi/fix_open_files\n\nFix lost open files and implement FULLSYNC for pack files on Mac OS",
          "timestamp": "2020-07-12T22:29:09+02:00",
          "tree_id": "571d031d2c95a14eb9fc9289031f93a62b9693f8",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/6025360bb8a030b1103e7d40da4f7bde7938dd4c"
        },
        "date": 1594585835321,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3133440497750384,
            "unit": "iter/sec",
            "range": "stddev: 0.015961716686027153",
            "extra": "mean: 3.1913802119999986 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.6367372281748848,
            "unit": "iter/sec",
            "range": "stddev: 0.06683760279796909",
            "extra": "mean: 1.570506569666667 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.1018976459997245,
            "unit": "iter/sec",
            "range": "stddev: 0.017055833441805165",
            "extra": "mean: 322.3833001999992 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.5749282691832691,
            "unit": "iter/sec",
            "range": "stddev: 0.017403865868654386",
            "extra": "mean: 634.9495526666639 msec\nrounds: 3"
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
          "id": "09cc7a9539aa68f3417bf4ef2e80b520a1b4ba41",
          "message": "Merge pull request #60 from giovannipizzi/fix_56_seek\n\nAdded seek method to both the PackedObjectReader and the StreamDecompresser",
          "timestamp": "2020-07-13T01:27:47+02:00",
          "tree_id": "cf2de3df905a56e5ca39dbd1155b206012989f9f",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/09cc7a9539aa68f3417bf4ef2e80b520a1b4ba41"
        },
        "date": 1594596737023,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.4111534815372448,
            "unit": "iter/sec",
            "range": "stddev: 0.010808042346792534",
            "extra": "mean: 2.4321817640000063 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 1.1704957066055501,
            "unit": "iter/sec",
            "range": "stddev: 0.06476093959634442",
            "extra": "mean: 854.3388876666711 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.484589490094764,
            "unit": "iter/sec",
            "range": "stddev: 0.007051620181556978",
            "extra": "mean: 286.9778500000024 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.8883724255349097,
            "unit": "iter/sec",
            "range": "stddev: 0.00878800907560073",
            "extra": "mean: 529.556556999997 msec\nrounds: 3"
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
          "id": "df368df957ecb9cf2a4a308c0b2baccfa7669638",
          "message": "Merge pull request #61 from giovannipizzi/check_concurrency\n\nFix concurrency problems in Mac OS",
          "timestamp": "2020-07-13T10:14:15+02:00",
          "tree_id": "2483876c2ad6de311dce821cd69d08efc5662ed0",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/df368df957ecb9cf2a4a308c0b2baccfa7669638"
        },
        "date": 1594628149633,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.2823745915074549,
            "unit": "iter/sec",
            "range": "stddev: 0.054622876375385286",
            "extra": "mean: 3.541395118666685 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.8379789468566016,
            "unit": "iter/sec",
            "range": "stddev: 0.24300536214787377",
            "extra": "mean: 1.1933474029999995 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.9844027015150587,
            "unit": "iter/sec",
            "range": "stddev: 0.014581573215028752",
            "extra": "mean: 335.0754237999922 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.544362407038266,
            "unit": "iter/sec",
            "range": "stddev: 0.018283385328627492",
            "extra": "mean: 647.5164089999907 msec\nrounds: 3"
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
          "id": "cec284e3680abc6105e80d0098da030a6cc3509e",
          "message": "Merge pull request #62 from giovannipizzi/fix_58_performance_has\n\nAdding methods to just fetch metas without opening streams",
          "timestamp": "2020-07-13T20:34:37+02:00",
          "tree_id": "3318cf4caa826238d95afbbb139840cb292a6f0e",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/cec284e3680abc6105e80d0098da030a6cc3509e"
        },
        "date": 1594665358737,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3123206535409789,
            "unit": "iter/sec",
            "range": "stddev: 0.021892806626957972",
            "extra": "mean: 3.201837562333329 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.8420264612990318,
            "unit": "iter/sec",
            "range": "stddev: 0.0693568905257965",
            "extra": "mean: 1.1876111333333341 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.2769470517835866,
            "unit": "iter/sec",
            "range": "stddev: 0.0086683159448169",
            "extra": "mean: 305.16208660000075 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.944132404173119,
            "unit": "iter/sec",
            "range": "stddev: 0.006174715078857079",
            "extra": "mean: 514.368258999994 msec\nrounds: 3"
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
          "id": "dab40d1d73c8515a5900560c656d04bdbae5fdf0",
          "message": "Merge pull request #63 from giovannipizzi/fix_10_performance\n\nAdding performance tests for loose read",
          "timestamp": "2020-07-13T22:09:53+02:00",
          "tree_id": "da463ed266c11b51b86ed097afedaa7a018bec82",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/dab40d1d73c8515a5900560c656d04bdbae5fdf0"
        },
        "date": 1594671180417,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.29552897005092754,
            "unit": "iter/sec",
            "range": "stddev: 0.03821451817159414",
            "extra": "mean: 3.383763019333344 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.12239856274956476,
            "unit": "iter/sec",
            "range": "stddev: 0.40706087658147255",
            "extra": "mean: 8.170030574999998 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.1311498248340435,
            "unit": "iter/sec",
            "range": "stddev: 0.009631709794647007",
            "extra": "mean: 319.3714947999979 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 23.103873852407325,
            "unit": "iter/sec",
            "range": "stddev: 0.0027749201828988802",
            "extra": "mean: 43.282784799995966 msec\nrounds: 20"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.7260069148071961,
            "unit": "iter/sec",
            "range": "stddev: 0.01745986032755727",
            "extra": "mean: 579.3719546666504 msec\nrounds: 3"
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
          "id": "801df0c0b90f09e910c7f822ae87e548446bce7a",
          "message": "Merge pull request #66 from giovannipizzi/fix_65_list_all\n\nAdding a function to list all objects",
          "timestamp": "2020-07-14T00:46:13+02:00",
          "tree_id": "0587cf74d5f99911d7ac55811765a11dfa23aeab",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/801df0c0b90f09e910c7f822ae87e548446bce7a"
        },
        "date": 1594680459226,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3407282728420675,
            "unit": "iter/sec",
            "range": "stddev: 0.030732608728199103",
            "extra": "mean: 2.9348899980000027 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.887406726923332,
            "unit": "iter/sec",
            "range": "stddev: 0.10328516777558798",
            "extra": "mean: 1.1268789943333342 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.5582405298479753,
            "unit": "iter/sec",
            "range": "stddev: 0.008018733729260234",
            "extra": "mean: 281.03777460000003 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 24.8164169411121,
            "unit": "iter/sec",
            "range": "stddev: 0.0030482376044967544",
            "extra": "mean: 40.29590582608848 msec\nrounds: 23"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 2.0975351509957254,
            "unit": "iter/sec",
            "range": "stddev: 0.007610195331470287",
            "extra": "mean: 476.7500556666657 msec\nrounds: 3"
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
          "id": "5a256e013b16d6a7044f7584114e7261dba5d1f6",
          "message": "Merge pull request #71 from giovannipizzi/fix_69_efficient_list_all\n\nImprove performance of list_all_objects for packed objects",
          "timestamp": "2020-07-16T14:37:20+02:00",
          "tree_id": "4038bcb9cafb4dbb2cf25ee20ef0750f1bbf4912",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/5a256e013b16d6a7044f7584114e7261dba5d1f6"
        },
        "date": 1594903177451,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3004030691224289,
            "unit": "iter/sec",
            "range": "stddev: 0.04269828734374587",
            "extra": "mean: 3.3288607966666652 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.905155688232661,
            "unit": "iter/sec",
            "range": "stddev: 0.08642906821544802",
            "extra": "mean: 1.1047823186666648 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.0316290189021444,
            "unit": "iter/sec",
            "range": "stddev: 0.020103950203245232",
            "extra": "mean: 329.8556629999979 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 22.758189949989365,
            "unit": "iter/sec",
            "range": "stddev: 0.004405397083542302",
            "extra": "mean: 43.9402255714307 msec\nrounds: 21"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.7688762536826594,
            "unit": "iter/sec",
            "range": "stddev: 0.0161023562762177",
            "extra": "mean: 565.3306713333279 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1888878.567270332,
            "unit": "iter/sec",
            "range": "stddev: 0.000003185877479995676",
            "extra": "mean: 529.4146576320818 nsec\nrounds: 129871"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3021298.6020945045,
            "unit": "iter/sec",
            "range": "stddev: 3.832374846231474e-7",
            "extra": "mean: 330.9835046779513 nsec\nrounds: 140846"
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
          "id": "32baa140c5860150a0891937b0e4a69aa88b05e7",
          "message": "Do not fail on benchmark test alert",
          "timestamp": "2020-07-16T23:04:29+02:00",
          "tree_id": "f3721560975ad665334615ba90b19359aacbc87d",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/32baa140c5860150a0891937b0e4a69aa88b05e7"
        },
        "date": 1594933641534,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3324987206471654,
            "unit": "iter/sec",
            "range": "stddev: 0.0850756822430017",
            "extra": "mean: 3.0075303690000084 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.9204817237025208,
            "unit": "iter/sec",
            "range": "stddev: 0.10098583965718078",
            "extra": "mean: 1.086387675333332 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.4165082074216064,
            "unit": "iter/sec",
            "range": "stddev: 0.015147568213396507",
            "extra": "mean: 292.69650160000253 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 25.190921142513517,
            "unit": "iter/sec",
            "range": "stddev: 0.0036312779449805964",
            "extra": "mean: 39.6968413478278 msec\nrounds: 23"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 2.0015813039400197,
            "unit": "iter/sec",
            "range": "stddev: 0.029631294207815337",
            "extra": "mean: 499.6049863333288 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 3106011.8565648124,
            "unit": "iter/sec",
            "range": "stddev: 2.848960054948048e-7",
            "extra": "mean: 321.9562726029308 nsec\nrounds: 151516"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3136138.6991010103,
            "unit": "iter/sec",
            "range": "stddev: 4.4876865171657266e-7",
            "extra": "mean: 318.8634483184056 nsec\nrounds: 142858"
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
          "id": "2815887c622e923ab8d6eac4370488df9be8166a",
          "message": "Merge pull request #74 from giovannipizzi/fix_hash_computation\n\nFix to the hash calculation when writing to compressed packs.",
          "timestamp": "2020-07-17T15:50:51+02:00",
          "tree_id": "84fff9b9c58f7df075b9377c35ae3974517e74ea",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/2815887c622e923ab8d6eac4370488df9be8166a"
        },
        "date": 1594993987231,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3044309692245495,
            "unit": "iter/sec",
            "range": "stddev: 0.01569801639234186",
            "extra": "mean: 3.2848169243333323 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.9724038604205137,
            "unit": "iter/sec",
            "range": "stddev: 0.1765455992507271",
            "extra": "mean: 1.0283792986666593 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.8578715653999978,
            "unit": "iter/sec",
            "range": "stddev: 0.007034528651667674",
            "extra": "mean: 349.9107559999942 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 21.187962014039073,
            "unit": "iter/sec",
            "range": "stddev: 0.006453033772635363",
            "extra": "mean: 47.19661095000092 msec\nrounds: 20"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.6995727201100297,
            "unit": "iter/sec",
            "range": "stddev: 0.013475640157768193",
            "extra": "mean: 588.3831789999903 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1920414.0700124723,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018466373322663988",
            "extra": "mean: 520.721033872401 nsec\nrounds: 144928"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2758058.8943689624,
            "unit": "iter/sec",
            "range": "stddev: 0.000001428815973480844",
            "extra": "mean: 362.57383844901125 nsec\nrounds: 140846"
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
          "id": "fa85ce1b90b92989c15446fb1125e6c7840ad729",
          "message": "Merge pull request #77 from giovannipizzi/fix_37_concurrency_win\n\nFix concurrency problems on Windows",
          "timestamp": "2020-07-17T16:48:14+02:00",
          "tree_id": "45fabeaefc37015b298754e3beaf07326d2b02f2",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/fa85ce1b90b92989c15446fb1125e6c7840ad729"
        },
        "date": 1594997430559,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.32764758781756287,
            "unit": "iter/sec",
            "range": "stddev: 0.008021331062531329",
            "extra": "mean: 3.052059704333331 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.9202044400781936,
            "unit": "iter/sec",
            "range": "stddev: 0.09738029797087913",
            "extra": "mean: 1.0867150346666723 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.3693513783564844,
            "unit": "iter/sec",
            "range": "stddev: 0.010934759927570868",
            "extra": "mean: 296.79302859999837 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 22.970797360721157,
            "unit": "iter/sec",
            "range": "stddev: 0.003434106571568189",
            "extra": "mean: 43.53353452631762 msec\nrounds: 19"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.8959570333515214,
            "unit": "iter/sec",
            "range": "stddev: 0.01603079203728845",
            "extra": "mean: 527.4381129999975 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2952532.791271145,
            "unit": "iter/sec",
            "range": "stddev: 7.27600730728701e-7",
            "extra": "mean: 338.6922587130616 nsec\nrounds: 161291"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2939654.668750179,
            "unit": "iter/sec",
            "range": "stddev: 7.102616603479263e-7",
            "extra": "mean: 340.1760113629048 nsec\nrounds: 149254"
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
          "id": "6dea94015bf141e31781e4ea61f169d2b69e6b81",
          "message": "Merge pull request #75 from giovannipizzi/fix_64_export_to_container\n\nAdding a function to export directly a set of hash keys to a new container",
          "timestamp": "2020-07-17T17:16:12+02:00",
          "tree_id": "9d5cf808e9c4e748164afb805c1fb170f183c957",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/6dea94015bf141e31781e4ea61f169d2b69e6b81"
        },
        "date": 1594999123353,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.2962100674831524,
            "unit": "iter/sec",
            "range": "stddev: 0.04206926976375967",
            "extra": "mean: 3.375982485999998 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.8361011197460857,
            "unit": "iter/sec",
            "range": "stddev: 0.09654336832573297",
            "extra": "mean: 1.19602758133333 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.7192015270505023,
            "unit": "iter/sec",
            "range": "stddev: 0.010750720076129093",
            "extra": "mean: 367.7550155999995 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 19.937392577675045,
            "unit": "iter/sec",
            "range": "stddev: 0.004364324550912649",
            "extra": "mean: 50.157010055555254 msec\nrounds: 18"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.6100770514985345,
            "unit": "iter/sec",
            "range": "stddev: 0.012633436044649558",
            "extra": "mean: 621.0882883333303 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1892539.4053531508,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012762095730779739",
            "extra": "mean: 528.3905831347265 nsec\nrounds: 172414"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2717882.3026682297,
            "unit": "iter/sec",
            "range": "stddev: 2.935644933180605e-7",
            "extra": "mean: 367.9335190555617 nsec\nrounds: 144928"
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
          "id": "38bfa5ed21e99016756308569337be1cdeaeb311",
          "message": "Merge pull request #68 from sphuber/feature/067/packed-object-reader-seek-whence\n\nImplement `whence=1` for the `utils.PackedObjectReader.seek`",
          "timestamp": "2020-07-17T18:20:39+02:00",
          "tree_id": "57f4997cbdc791e0a32f9905fa065586842a7ad8",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/38bfa5ed21e99016756308569337be1cdeaeb311"
        },
        "date": 1595002966677,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3659637112330866,
            "unit": "iter/sec",
            "range": "stddev: 0.05854772526478887",
            "extra": "mean: 2.7325113646666686 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.9916751253249397,
            "unit": "iter/sec",
            "range": "stddev: 0.1366133254576877",
            "extra": "mean: 1.0083947599999874 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.087186928566587,
            "unit": "iter/sec",
            "range": "stddev: 0.015395016436868884",
            "extra": "mean: 323.9194849999933 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 22.974101953461155,
            "unit": "iter/sec",
            "range": "stddev: 0.003693499558448516",
            "extra": "mean: 43.527272666662185 msec\nrounds: 18"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.7947221081451807,
            "unit": "iter/sec",
            "range": "stddev: 0.02104941291950389",
            "extra": "mean: 557.1893250000054 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1921843.764168552,
            "unit": "iter/sec",
            "range": "stddev: 0.000001823556660911301",
            "extra": "mean: 520.333660125921 nsec\nrounds: 175439"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2773563.5676719015,
            "unit": "iter/sec",
            "range": "stddev: 4.2554785539450136e-7",
            "extra": "mean: 360.54699147896247 nsec\nrounds: 138889"
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
          "id": "dbefa5af8e4b59d8b7e35f67f4597025e7f2b60d",
          "message": "Avoid seeking back to zero for compressed streams when seeking forward\n\nFixes #81",
          "timestamp": "2020-07-17T18:31:03+02:00",
          "tree_id": "01ba21f85aaef7d3d3d31955b500af91455036bd",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/dbefa5af8e4b59d8b7e35f67f4597025e7f2b60d"
        },
        "date": 1595003635792,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.30813389671835206,
            "unit": "iter/sec",
            "range": "stddev: 0.03310196962054796",
            "extra": "mean: 3.245342400333333 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.9152734400041452,
            "unit": "iter/sec",
            "range": "stddev: 0.024006265406754507",
            "extra": "mean: 1.0925696696666638 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.967130445810851,
            "unit": "iter/sec",
            "range": "stddev: 0.008317495165243263",
            "extra": "mean: 337.02596439999866 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 21.617194244965887,
            "unit": "iter/sec",
            "range": "stddev: 0.0011169625315259",
            "extra": "mean: 46.25947237499961 msec\nrounds: 16"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.7344633658948259,
            "unit": "iter/sec",
            "range": "stddev: 0.00816363271083696",
            "extra": "mean: 576.5472016666612 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2756781.16859352,
            "unit": "iter/sec",
            "range": "stddev: 1.4829619711691907e-7",
            "extra": "mean: 362.7418858601972 nsec\nrounds: 131579"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2717012.492108335,
            "unit": "iter/sec",
            "range": "stddev: 5.008024410255316e-7",
            "extra": "mean: 368.0513074208966 nsec\nrounds: 136987"
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
          "id": "ddc612b9ceaf7f67711f7079d0f584ead8147507",
          "message": "Merge pull request #84 from giovannipizzi/fix_13_validation\n\nImplement validation routine",
          "timestamp": "2020-07-19T23:21:12+02:00",
          "tree_id": "d7baf41d8de602432d63610a50939df2fde3d94c",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/ddc612b9ceaf7f67711f7079d0f584ead8147507"
        },
        "date": 1595193992551,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.4088467420254465,
            "unit": "iter/sec",
            "range": "stddev: 0.015989885180497838",
            "extra": "mean: 2.445904289333337 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.11668183567803829,
            "unit": "iter/sec",
            "range": "stddev: 0.6551160511309678",
            "extra": "mean: 8.570314258333346 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.46458993750284,
            "unit": "iter/sec",
            "range": "stddev: 0.01053806547181396",
            "extra": "mean: 288.6344468000061 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 26.112562955101502,
            "unit": "iter/sec",
            "range": "stddev: 0.002099685219693049",
            "extra": "mean: 38.2957430000043 msec\nrounds: 23"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.9787381094370462,
            "unit": "iter/sec",
            "range": "stddev: 0.018132676959752545",
            "extra": "mean: 505.37258833333 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2023619.330062776,
            "unit": "iter/sec",
            "range": "stddev: 7.336666622429737e-7",
            "extra": "mean: 494.1640876542616 nsec\nrounds: 166667"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3163516.247183704,
            "unit": "iter/sec",
            "range": "stddev: 2.7008524642077396e-7",
            "extra": "mean: 316.10395580879384 nsec\nrounds: 156226"
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
          "id": "89a6ea1a6c87895d4cbb0c1e2c869225c31fb707",
          "message": "Adding nodes on performance for validation",
          "timestamp": "2020-07-20T14:06:57+02:00",
          "tree_id": "a1c4c31f0e67410babd839471c3349dc89f24c78",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/89a6ea1a6c87895d4cbb0c1e2c869225c31fb707"
        },
        "date": 1595246946927,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.48389120415016074,
            "unit": "iter/sec",
            "range": "stddev: 0.047784300304646",
            "extra": "mean: 2.066580238333245 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 1.308865730117301,
            "unit": "iter/sec",
            "range": "stddev: 0.06319011784359217",
            "extra": "mean: 764.0203093333184 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 4.167470015968382,
            "unit": "iter/sec",
            "range": "stddev: 0.017472161317222124",
            "extra": "mean: 239.9537360000977 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 31.639042732758426,
            "unit": "iter/sec",
            "range": "stddev: 0.00360216651493449",
            "extra": "mean: 31.606518833283797 msec\nrounds: 30"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 2.356449451021107,
            "unit": "iter/sec",
            "range": "stddev: 0.018124987252711305",
            "extra": "mean: 424.3672613332213 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 3442812.854094228,
            "unit": "iter/sec",
            "range": "stddev: 1.4963995534523907e-7",
            "extra": "mean: 290.460168002237 nsec\nrounds: 169492"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3533646.0252480186,
            "unit": "iter/sec",
            "range": "stddev: 2.4888249495753383e-7",
            "extra": "mean: 282.99382361877235 nsec\nrounds: 149254"
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
          "id": "d41ef638da9ca6958401ce010332e42cf4f988e4",
          "message": "Merge pull request #87 from giovannipizzi/fix_5_delete\n\nImplement function `delete_objects` for object deletion",
          "timestamp": "2020-07-20T14:40:53+02:00",
          "tree_id": "909ea5614905a444fc80d603a21b439da060a5a4",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/d41ef638da9ca6958401ce010332e42cf4f988e4"
        },
        "date": 1595248994471,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3131210449982181,
            "unit": "iter/sec",
            "range": "stddev: 0.02243091054102237",
            "extra": "mean: 3.1936531126666714 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.7924330571598133,
            "unit": "iter/sec",
            "range": "stddev: 0.0650547998341542",
            "extra": "mean: 1.2619362493333313 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.1149537659779263,
            "unit": "iter/sec",
            "range": "stddev: 0.015112031829529053",
            "extra": "mean: 321.0320521999961 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 21.910088760661203,
            "unit": "iter/sec",
            "range": "stddev: 0.0017651520242789249",
            "extra": "mean: 45.641074800001036 msec\nrounds: 20"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.779994035429865,
            "unit": "iter/sec",
            "range": "stddev: 0.0019339192569972875",
            "extra": "mean: 561.7996353333297 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1930752.1876717329,
            "unit": "iter/sec",
            "range": "stddev: 0.000008230882427972806",
            "extra": "mean: 517.9328586989126 nsec\nrounds: 196079"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2809332.391775082,
            "unit": "iter/sec",
            "range": "stddev: 4.993225461997166e-7",
            "extra": "mean: 355.9564553226574 nsec\nrounds: 120482"
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
          "id": "3f3cd07ea6627bbf6d0637e69e409ef4801b4f90",
          "message": "Adding nightly concurrency extensive tests\n\nThis runs only the main branch of the main fork, at 5AM UTC.\nTests are repeated 5 times to increase the change of seeing random errors.\n\nFixes #76",
          "timestamp": "2020-07-20T14:51:14+02:00",
          "tree_id": "01658224411ac3acb670ee1ef1e9d5081979f9ee",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/3f3cd07ea6627bbf6d0637e69e409ef4801b4f90"
        },
        "date": 1595249695319,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.39735167619081435,
            "unit": "iter/sec",
            "range": "stddev: 0.040590414309501485",
            "extra": "mean: 2.5166623419999987 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.9045676048034105,
            "unit": "iter/sec",
            "range": "stddev: 0.0865927666245492",
            "extra": "mean: 1.1055005669999975 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.3744434079999244,
            "unit": "iter/sec",
            "range": "stddev: 0.006395043410957255",
            "extra": "mean: 296.34516839999776 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 26.298049612198135,
            "unit": "iter/sec",
            "range": "stddev: 0.0033212160472582226",
            "extra": "mean: 38.025633640000365 msec\nrounds: 25"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.9570384615262206,
            "unit": "iter/sec",
            "range": "stddev: 0.013373092381426407",
            "extra": "mean: 510.97616099999266 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1870192.2892243543,
            "unit": "iter/sec",
            "range": "stddev: 5.797218171857238e-7",
            "extra": "mean: 534.7043754600983 nsec\nrounds: 169492"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2942638.0178022226,
            "unit": "iter/sec",
            "range": "stddev: 2.549888622902953e-7",
            "extra": "mean: 339.83112905858616 nsec\nrounds: 151516"
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
          "id": "5d977ad3ce8d4eba5ba70dfd0919282c2505e3b1",
          "message": "Merge pull request #88 from giovannipizzi/fix_78_loose_streamed\n\nAdding `add_streamed_object` function",
          "timestamp": "2020-07-20T15:47:49+02:00",
          "tree_id": "4864b702ab018ce6fa9ac195aca677f776b5bbff",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/5d977ad3ce8d4eba5ba70dfd0919282c2505e3b1"
        },
        "date": 1595253194415,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.41539147225164735,
            "unit": "iter/sec",
            "range": "stddev: 0.1444008650833028",
            "extra": "mean: 2.407367668333336 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.11462881539131504,
            "unit": "iter/sec",
            "range": "stddev: 0.7380036910894481",
            "extra": "mean: 8.723809947666666 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.6522493885870633,
            "unit": "iter/sec",
            "range": "stddev: 0.011286322672866249",
            "extra": "mean: 273.80386540002064 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 28.187035836118984,
            "unit": "iter/sec",
            "range": "stddev: 0.004061562134861666",
            "extra": "mean: 35.47730260869062 msec\nrounds: 23"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.9391713892729634,
            "unit": "iter/sec",
            "range": "stddev: 0.014968722314377353",
            "extra": "mean: 515.6841759999983 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2025462.9530355337,
            "unit": "iter/sec",
            "range": "stddev: 0.000001410122583904875",
            "extra": "mean: 493.71428813413434 nsec\nrounds: 175439"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3162446.0575554245,
            "unit": "iter/sec",
            "range": "stddev: 5.472929627595861e-7",
            "extra": "mean: 316.21092717481645 nsec\nrounds: 153823"
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
          "id": "6304d727083b3e119ba6015b89bf05ed396d63e6",
          "message": "Merge pull request #89 from giovannipizzi/fix_85_no_holes\n\nAdding the `no_holes` and `no_holes_read_twice` flags",
          "timestamp": "2020-07-20T16:52:36+02:00",
          "tree_id": "9e910cfbe5f17904d39b416b6b491cf8ba01fad4",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/6304d727083b3e119ba6015b89bf05ed396d63e6"
        },
        "date": 1595256883708,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3824686507447717,
            "unit": "iter/sec",
            "range": "stddev: 0.0029681522177338214",
            "extra": "mean: 2.6145933739999996 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 1.242882355577996,
            "unit": "iter/sec",
            "range": "stddev: 0.052509799072824",
            "extra": "mean: 804.5813793333281 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.2846622267033303,
            "unit": "iter/sec",
            "range": "stddev: 0.013556172293187127",
            "extra": "mean: 304.4453070000003 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 26.005814705124532,
            "unit": "iter/sec",
            "range": "stddev: 0.0032154555891742765",
            "extra": "mean: 38.45293874999989 msec\nrounds: 24"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.879291225264264,
            "unit": "iter/sec",
            "range": "stddev: 0.013368420572235692",
            "extra": "mean: 532.1155053333371 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1929282.0957152704,
            "unit": "iter/sec",
            "range": "stddev: 5.639353473862002e-7",
            "extra": "mean: 518.3275178994784 nsec\nrounds: 156251"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2948973.1149135036,
            "unit": "iter/sec",
            "range": "stddev: 2.2372520965806042e-7",
            "extra": "mean: 339.1010907977363 nsec\nrounds: 138889"
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
          "id": "1589096795f049b538222474b724e0d1298a4b49",
          "message": "Complete move to aiidateam organisation\n\nFixes #80",
          "timestamp": "2020-07-20T17:02:04+02:00",
          "tree_id": "e54abe7df4b0f77aefb62e2a5ad6a6b7578e733a",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/1589096795f049b538222474b724e0d1298a4b49"
        },
        "date": 1595257488417,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.39238693541372716,
            "unit": "iter/sec",
            "range": "stddev: 0.06185312968764",
            "extra": "mean: 2.5485048296667023 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.786611693819093,
            "unit": "iter/sec",
            "range": "stddev: 0.1365931059229209",
            "extra": "mean: 1.271275278333178 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.252116580400015,
            "unit": "iter/sec",
            "range": "stddev: 0.009224431329730009",
            "extra": "mean: 307.4920517999999 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 24.075174443309905,
            "unit": "iter/sec",
            "range": "stddev: 0.003839081247817751",
            "extra": "mean: 41.53656299997791 msec\nrounds: 23"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.9383902232365111,
            "unit": "iter/sec",
            "range": "stddev: 0.010184758078945299",
            "extra": "mean: 515.891995333277 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1959777.5547624284,
            "unit": "iter/sec",
            "range": "stddev: 5.679395748444428e-7",
            "extra": "mean: 510.26199252558735 nsec\nrounds: 113637"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2911438.423487024,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015994599268998764",
            "extra": "mean: 343.4728318252462 nsec\nrounds: 138870"
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
          "id": "11cc7cbf88b964e48ac44f5de59ef09bc6bdb745",
          "message": "Adding simple changelog",
          "timestamp": "2020-07-20T17:41:58+02:00",
          "tree_id": "c53c9f1eed85787028f0bcbc6f537bb2915cc518",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/11cc7cbf88b964e48ac44f5de59ef09bc6bdb745"
        },
        "date": 1595259870022,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.30317883692670006,
            "unit": "iter/sec",
            "range": "stddev: 0.053579245154346325",
            "extra": "mean: 3.298383258333336 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 1.1377225192119143,
            "unit": "iter/sec",
            "range": "stddev: 0.07276362980606248",
            "extra": "mean: 878.948938000003 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.0091191270891304,
            "unit": "iter/sec",
            "range": "stddev: 0.006216686360890359",
            "extra": "mean: 332.32316759999776 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 21.714001744774766,
            "unit": "iter/sec",
            "range": "stddev: 0.0029589397709957827",
            "extra": "mean: 46.05323384210554 msec\nrounds: 19"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.7543636198598684,
            "unit": "iter/sec",
            "range": "stddev: 0.01976510840130681",
            "extra": "mean: 570.007259999997 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1745190.2051298504,
            "unit": "iter/sec",
            "range": "stddev: 0.0000032903057115018528",
            "extra": "mean: 573.0034451606354 nsec\nrounds: 151516"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2732666.280205496,
            "unit": "iter/sec",
            "range": "stddev: 5.082158768717026e-7",
            "extra": "mean: 365.94296465821446 nsec\nrounds: 136987"
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
          "id": "1e0ba2e2cec56c81f871ff8d72c15d7688ee8f0a",
          "message": "Change the default value of `compress` for export\n\nFor some reason it was True, but this is unexpected.\nSetting back to False.",
          "timestamp": "2020-07-20T17:51:03+02:00",
          "tree_id": "454bf54a8a996bc894244547a4ebd6dbfa0a7bdb",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/1e0ba2e2cec56c81f871ff8d72c15d7688ee8f0a"
        },
        "date": 1595260628826,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3909260719178936,
            "unit": "iter/sec",
            "range": "stddev: 0.04347898626726598",
            "extra": "mean: 2.558028414666675 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.11770125828204903,
            "unit": "iter/sec",
            "range": "stddev: 0.48839327157336765",
            "extra": "mean: 8.496085892333346 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.493543822367284,
            "unit": "iter/sec",
            "range": "stddev: 0.0069488207164220255",
            "extra": "mean: 286.24229459998105 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 26.711541314086894,
            "unit": "iter/sec",
            "range": "stddev: 0.004060418721268064",
            "extra": "mean: 37.43700104166692 msec\nrounds: 24"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 2.0683040564872037,
            "unit": "iter/sec",
            "range": "stddev: 0.0071881592486474025",
            "extra": "mean: 483.4879073333127 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1876975.35163945,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019681347780139926",
            "extra": "mean: 532.7720468606831 nsec\nrounds: 188644"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2969998.6301159235,
            "unit": "iter/sec",
            "range": "stddev: 4.866199082933234e-7",
            "extra": "mean: 336.700492000035 nsec\nrounds: 133334"
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
          "id": "9dd029d81a791f0fa3324209fa7edfd015796aa8",
          "message": "Removing the 'OS-independent' flag\n\nThis is not really true, it actually is OS dependent,\nand I tested the three most common ones",
          "timestamp": "2020-07-20T18:33:16+02:00",
          "tree_id": "da603cd023341129a9ef4d74d860764b02631c3f",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/9dd029d81a791f0fa3324209fa7edfd015796aa8"
        },
        "date": 1595262956592,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.35957972672490224,
            "unit": "iter/sec",
            "range": "stddev: 0.05661195337263754",
            "extra": "mean: 2.7810244173333323 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.9010685183161007,
            "unit": "iter/sec",
            "range": "stddev: 0.029836913040672108",
            "extra": "mean: 1.1097935169999953 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.3620129534539873,
            "unit": "iter/sec",
            "range": "stddev: 0.01741104428852201",
            "extra": "mean: 297.4408527999998 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 24.13795081529808,
            "unit": "iter/sec",
            "range": "stddev: 0.0031982471694550537",
            "extra": "mean: 41.42853747826112 msec\nrounds: 23"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 2.1402555857549785,
            "unit": "iter/sec",
            "range": "stddev: 0.010797825251563505",
            "extra": "mean: 467.2339166666622 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 3597999.7361469315,
            "unit": "iter/sec",
            "range": "stddev: 3.351778634187125e-7",
            "extra": "mean: 277.93220492878726 nsec\nrounds: 175439"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3412623.146775091,
            "unit": "iter/sec",
            "range": "stddev: 2.3046929967073238e-7",
            "extra": "mean: 293.02971848664356 nsec\nrounds: 163935"
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
          "id": "51e6a578fc55c3c0eca18bb4351cb5ae1dcdb00f",
          "message": "Explicitly specifying the codecov token",
          "timestamp": "2020-07-20T18:59:40+02:00",
          "tree_id": "b5c97bfa36b46639cdf390220798c072fbc6826a",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/51e6a578fc55c3c0eca18bb4351cb5ae1dcdb00f"
        },
        "date": 1595264532957,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3911939149914869,
            "unit": "iter/sec",
            "range": "stddev: 0.012880561212777824",
            "extra": "mean: 2.5562769809999772 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 1.1259191966321591,
            "unit": "iter/sec",
            "range": "stddev: 0.029753587133865517",
            "extra": "mean: 888.1632029999954 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.349612102022457,
            "unit": "iter/sec",
            "range": "stddev: 0.007480156659610367",
            "extra": "mean: 298.54203100001087 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 25.757368458267855,
            "unit": "iter/sec",
            "range": "stddev: 0.0032865367320364784",
            "extra": "mean: 38.823841869568405 msec\nrounds: 23"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.9454830576877868,
            "unit": "iter/sec",
            "range": "stddev: 0.01257078626003894",
            "extra": "mean: 514.0111583333464 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1910119.5145665074,
            "unit": "iter/sec",
            "range": "stddev: 7.867524216509062e-7",
            "extra": "mean: 523.5274507034944 nsec\nrounds: 192308"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2970585.8012589635,
            "unit": "iter/sec",
            "range": "stddev: 3.590264621650184e-7",
            "extra": "mean: 336.6339391972255 nsec\nrounds: 140846"
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
          "id": "48fe289e87e457a1390b6d3dd6942d0b16064a32",
          "message": "Moving the env to the right place",
          "timestamp": "2020-07-20T19:06:51+02:00",
          "tree_id": "a629875f497fff991502bc56fb3979d157cf13b4",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/48fe289e87e457a1390b6d3dd6942d0b16064a32"
        },
        "date": 1595264973344,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.30604511462695133,
            "unit": "iter/sec",
            "range": "stddev: 0.027896514583596405",
            "extra": "mean: 3.2674921186666666 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 1.2267670982614953,
            "unit": "iter/sec",
            "range": "stddev: 0.11469768650557086",
            "extra": "mean: 815.150651999995 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.0364195662735387,
            "unit": "iter/sec",
            "range": "stddev: 0.009359567279677947",
            "extra": "mean: 329.3352509999977 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 22.605360987948426,
            "unit": "iter/sec",
            "range": "stddev: 0.0034253971362175825",
            "extra": "mean: 44.23729399999978 msec\nrounds: 21"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.7702557309127653,
            "unit": "iter/sec",
            "range": "stddev: 0.01763831741477135",
            "extra": "mean: 564.8901356666632 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2754718.0395510173,
            "unit": "iter/sec",
            "range": "stddev: 2.8060669543206526e-7",
            "extra": "mean: 363.01355915276486 nsec\nrounds: 131579"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2764426.3849825556,
            "unit": "iter/sec",
            "range": "stddev: 2.1428229782742814e-7",
            "extra": "mean: 361.7386975583963 nsec\nrounds: 133334"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gio.piz@gmail.com",
            "name": "Giovanni Pizzi",
            "username": "giovannipizzi"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "9aa52ca307119522cbcb110a505b77c6b7562513",
          "message": "Merge pull request #91 from giovannipizzi/test-codecov\n\nTesting Codecov after moving the repo",
          "timestamp": "2020-07-20T19:40:16+02:00",
          "tree_id": "da603cd023341129a9ef4d74d860764b02631c3f",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/9aa52ca307119522cbcb110a505b77c6b7562513"
        },
        "date": 1595266959671,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3122085636152521,
            "unit": "iter/sec",
            "range": "stddev: 0.032886993950833006",
            "extra": "mean: 3.202987094333333 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.8395174685297763,
            "unit": "iter/sec",
            "range": "stddev: 0.10884832637939403",
            "extra": "mean: 1.1911604433333263 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.050168429751699,
            "unit": "iter/sec",
            "range": "stddev: 0.0015675377468291848",
            "extra": "mean: 327.8507475999959 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 21.664997663852958,
            "unit": "iter/sec",
            "range": "stddev: 0.002813703700818629",
            "extra": "mean: 46.15740169999896 msec\nrounds: 20"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.8064157271534111,
            "unit": "iter/sec",
            "range": "stddev: 0.012478294186043085",
            "extra": "mean: 553.5824256666663 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1959646.0711556065,
            "unit": "iter/sec",
            "range": "stddev: 0.000001233626353067529",
            "extra": "mean: 510.29622885437584 nsec\nrounds: 172414"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2786742.976179966,
            "unit": "iter/sec",
            "range": "stddev: 4.09789258239221e-7",
            "extra": "mean: 358.84184818883494 nsec\nrounds: 140846"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gio.piz@gmail.com",
            "name": "Giovanni Pizzi",
            "username": "giovannipizzi"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": false,
          "id": "c718ffdec3881653acb82beaeed69fadf3cd9e3d",
          "message": "Merge pull request #90 from aiidateam/develop\n\nRelease of version 0.4.0",
          "timestamp": "2020-07-20T19:46:14+02:00",
          "tree_id": "da603cd023341129a9ef4d74d860764b02631c3f",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/c718ffdec3881653acb82beaeed69fadf3cd9e3d"
        },
        "date": 1595267621146,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.37436627496913455,
            "unit": "iter/sec",
            "range": "stddev: 0.05591747392657223",
            "extra": "mean: 2.6711807843333304 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.11891719609371995,
            "unit": "iter/sec",
            "range": "stddev: 0.06503253025899901",
            "extra": "mean: 8.409212736666689 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.2327192149573105,
            "unit": "iter/sec",
            "range": "stddev: 0.010285198752526706",
            "extra": "mean: 309.3371039999852 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 24.31082165975014,
            "unit": "iter/sec",
            "range": "stddev: 0.0032302010688651525",
            "extra": "mean: 41.13394495652262 msec\nrounds: 23"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.9158119700491876,
            "unit": "iter/sec",
            "range": "stddev: 0.004825200382311441",
            "extra": "mean: 521.9718926666511 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1913042.8666475813,
            "unit": "iter/sec",
            "range": "stddev: 4.923694460300847e-7",
            "extra": "mean: 522.7274398468662 nsec\nrounds: 140846"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2911999.485225615,
            "unit": "iter/sec",
            "range": "stddev: 1.1567180202573464e-7",
            "extra": "mean: 343.40665411310647 nsec\nrounds: 117634"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gio.piz@gmail.com",
            "name": "Giovanni Pizzi",
            "username": "giovannipizzi"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "e7e3627a67e8de2030b231927a127a9fb06ae474",
          "message": "Merge pull request #95 from giovannipizzi/fix_missing_optional_deps\n\nAdding missing optional dev dependencies",
          "timestamp": "2020-08-26T23:34:55+02:00",
          "tree_id": "397da3027d0c56b27a27da2ce3509320aadc032e",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/e7e3627a67e8de2030b231927a127a9fb06ae474"
        },
        "date": 1598477801387,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.45401810302568507,
            "unit": "iter/sec",
            "range": "stddev: 0.005954265844477211",
            "extra": "mean: 2.202555345999997 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 1.2937085436433728,
            "unit": "iter/sec",
            "range": "stddev: 0.04837953467454012",
            "extra": "mean: 772.9716286666672 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.8888932405603844,
            "unit": "iter/sec",
            "range": "stddev: 0.010948522939552235",
            "extra": "mean: 257.1425694000027 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 30.831203575454328,
            "unit": "iter/sec",
            "range": "stddev: 0.002931028684716154",
            "extra": "mean: 32.43467279999834 msec\nrounds: 25"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 2.199977337153445,
            "unit": "iter/sec",
            "range": "stddev: 0.022920646747715583",
            "extra": "mean: 454.55013700000296 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 3341609.527891311,
            "unit": "iter/sec",
            "range": "stddev: 7.179993723628592e-8",
            "extra": "mean: 299.25698728548775 nsec\nrounds: 166667"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3405203.4892165926,
            "unit": "iter/sec",
            "range": "stddev: 3.6573915241994156e-7",
            "extra": "mean: 293.6682060753844 nsec\nrounds: 153847"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "chrisj_sewell@hotmail.com",
            "name": "Chris Sewell",
            "username": "chrisjsewell"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "64326c7e9778b6af1cc142a1f48a526a5bf7ee2e",
          "message": "🔀👌 Efficiency improvements  (#96)\n\nThis merge collects a number of important efficiency improvements, and a few features that were tightly bound to these efficiency changes, so they are shipped together.\r\n\r\nIn particular:\r\n\r\n- objects are now sorted and returned in the order in which they are on disk, with an important performance benefit. Fixes #92 \r\n- When there are many objects to list (currently set to 9500 objects, 10x the ones we could fit in a single IN SQL statement), performing many queries is slow, so we just resort to listing all objects and doing an efficient intersection (if the hash keys are sorted, both iterators can be looped over only once - fixes #93)\r\n- Since VACUUMing the DB is very important for efficiency, when the DB does not fit fully in the disk cache, `clean_storage` now provides an option to VACUUM the DB. VACUUM is also called after repacking. Fixes #94 \r\n- We implement now a function to perform a full repack of the repository (fixes #12). This is important and needed to reclaim space after deleting an object\r\n- For efficiency, we have moved the logic from an `export` function (still existing but deprecated) to a `import_objects` function\r\n- Still for efficiency, now functions like `pack_all_loose` and `import_objects` provide an option to perform a fsync to disk or not (see also #54 - there are still however calls that always use - or don't use - fsync and full_fsync on Mac). Also, `add_objects_to_pack` allows now to choose if you want to commit the changes to the SQLite DB, or not (delegating the responsibility to the caller, but this is important e.g. in `import_objects`: calling `commit` only once at the very end gives a factor of 2 speedup for very big repos).\r\n- A number of functions, including (but not exclusively) `import_objects` provide a callback to e.g. show a progress bar.\r\n- a `CallbackStreamWrapper` has been implemented, allowing to provide a callback (e.g. for a progress bar) when streaming a big file.\r\n- a new hash algorithm is now supported (`sha1`) in addition to the default `sha256` (fixes #82). This is faster even if a bit less robust. This was also needed to test completely some feature in `import_objects`, where the logic is optimised if both containers use the same algorithm. By default is still better to use everywhere sha256, also because then all export files that will be generated will use this algorithm and importing will be more efficient.\r\n- tests have been added for all new functionality, achieving again 100% coverage\r\n\r\nAs a reference, with these changes, exporting the full large SDB database (6.8M nodes) takes ~ 50 minutes:\r\n```\r\n6714808it [00:24, 274813.02it/s]\r\nAll hashkeys listed in 24.444787740707397s.\r\nListing objects: 100%|████████| 6714808/6714808 [00:06<00:00, 978896.65it/s]\r\nCopy objects: 100%|███████████| 6714808/6714808 [48:15<00:00, 2319.08it/s]\r\nFinal flush: 100%|████████████| 63236/63236 [00:07<00:00, 8582.35it/s]\r\nEverything re-exported in 2960.980943918228s.\r\n```\r\n\r\nThis can be compared to:\r\n\r\n- ~10 minutes to copy the whole 90GB, or ~15 minutes to read all and validate the packs. We will never be able to be faster than just copying the pack files, and we are only 3x slower.\r\n- ~2 days to just list all files in the old legacy AiiDA repo (or all objects if they are loose), and this does not take into account the time to rewrite everything, probably comparable. So we are almost 2 orders of magnitude faster than before.",
          "timestamp": "2020-10-02T05:02:23+01:00",
          "tree_id": "a1e5eacb37c751b57ede7818ed3ea30ccd868aa0",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/64326c7e9778b6af1cc142a1f48a526a5bf7ee2e"
        },
        "date": 1601611428032,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 3.822519717634209,
            "unit": "iter/sec",
            "range": "stddev: 0.010710444634960353",
            "extra": "mean: 261.60754524999777 msec\nrounds: 4"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.8076198267327124,
            "unit": "iter/sec",
            "range": "stddev: 0.09458099688489016",
            "extra": "mean: 1.2382063526666702 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 8.140907568004227,
            "unit": "iter/sec",
            "range": "stddev: 0.007533513574043765",
            "extra": "mean: 122.83642722222352 msec\nrounds: 9"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 25.92046508176401,
            "unit": "iter/sec",
            "range": "stddev: 0.003677563848886081",
            "extra": "mean: 38.57955468181535 msec\nrounds: 22"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 4.588693807199888,
            "unit": "iter/sec",
            "range": "stddev: 0.013275166948977731",
            "extra": "mean: 217.92693999999528 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1967759.1996517286,
            "unit": "iter/sec",
            "range": "stddev: 4.337440371164589e-7",
            "extra": "mean: 508.1922626391424 nsec\nrounds: 181819"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3105001.1831013225,
            "unit": "iter/sec",
            "range": "stddev: 1.1040241489828784e-7",
            "extra": "mean: 322.0610689110473 nsec\nrounds: 138889"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gio.piz@gmail.com",
            "name": "Giovanni Pizzi",
            "username": "giovannipizzi"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "1d7c389c353185c1923c9addb1b107c283d5f561",
          "message": "✨ Add the concept of a (unique) container ID (#97)\n\nAllows for the association of a container with an existing DB, or to uniquely refer to it.\r\n\r\n🐛 This also fixes a bug, whereby config values were cached, but the cache was not cleared when re-initialising the container.\r\nTo reduce the risk of such a problem, now only the whole configuration dictionary is cached, rather than each single config value.",
          "timestamp": "2020-10-02T05:26:39+01:00",
          "tree_id": "cf46e923be5370049e00e368fe2b9cf6f18ef6d3",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/1d7c389c353185c1923c9addb1b107c283d5f561"
        },
        "date": 1601612904794,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.87975330044751,
            "unit": "iter/sec",
            "range": "stddev: 0.02304322040094718",
            "extra": "mean: 1.1366822943333357 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.8996917203621142,
            "unit": "iter/sec",
            "range": "stddev: 0.1531809922697905",
            "extra": "mean: 1.111491833666662 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 9.467770610108342,
            "unit": "iter/sec",
            "range": "stddev: 0.008140071906912648",
            "extra": "mean: 105.62148590000078 msec\nrounds: 10"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 6.480621874994417,
            "unit": "iter/sec",
            "range": "stddev: 0.0034471111401594198",
            "extra": "mean: 154.30617914285602 msec\nrounds: 7"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 0.7065395317925856,
            "unit": "iter/sec",
            "range": "stddev: 0.03119085907244682",
            "extra": "mean: 1.4153489720000039 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2281964.6861013523,
            "unit": "iter/sec",
            "range": "stddev: 4.1473535472676083e-7",
            "extra": "mean: 438.21887608105845 nsec\nrounds: 196079"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3409303.1380530843,
            "unit": "iter/sec",
            "range": "stddev: 1.0535229775015154e-7",
            "extra": "mean: 293.31507334705645 nsec\nrounds: 144928"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "chrisj_sewell@hotmail.com",
            "name": "Chris Sewell",
            "username": "chrisjsewell"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "1b84d6b00ad68bf8e58861c712c3cb9b6394abfd",
          "message": "🐛 Fix performance regression (#102)\n\n`Container.is_initialised` is a costly operation, loading the config JSON every time.\r\nIn 1d7c389, the config is now called on every call to `loose_prefix_len`, leading to a large performance degradation.\r\nThis PR makes sure the `is_initialised` test is called only if the config has not already been loaded into memory.",
          "timestamp": "2020-10-02T18:45:30+01:00",
          "tree_id": "3e63fef3df945593819e81391c96d674c2e19225",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/1b84d6b00ad68bf8e58861c712c3cb9b6394abfd"
        },
        "date": 1601660812154,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 4.059525628070446,
            "unit": "iter/sec",
            "range": "stddev: 0.007460296870933156",
            "extra": "mean: 246.33420050000154 msec\nrounds: 4"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 1.347174144813956,
            "unit": "iter/sec",
            "range": "stddev: 0.07205359971335867",
            "extra": "mean: 742.2945309999989 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 8.52659984282599,
            "unit": "iter/sec",
            "range": "stddev: 0.008656394539269618",
            "extra": "mean: 117.28004344444149 msec\nrounds: 9"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 26.840867648268052,
            "unit": "iter/sec",
            "range": "stddev: 0.0032305308410799476",
            "extra": "mean: 37.256619759999694 msec\nrounds: 25"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 4.464339294329306,
            "unit": "iter/sec",
            "range": "stddev: 0.013012328530117674",
            "extra": "mean: 223.99731159999874 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2089279.6845127218,
            "unit": "iter/sec",
            "range": "stddev: 9.162402949782724e-7",
            "extra": "mean: 478.63385999142946 nsec\nrounds: 185186"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3249136.2856222414,
            "unit": "iter/sec",
            "range": "stddev: 9.708092982684938e-8",
            "extra": "mean: 307.7741012049862 nsec\nrounds: 142858"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gio.piz@gmail.com",
            "name": "Giovanni Pizzi",
            "username": "giovannipizzi"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "d786296bc67219512f4058265ffbd8c9e6f06b0a",
          "message": "✨ Generalize compression algorithm (#99)\n\nThe container configuration now accepts a variable for the compression algorithm to use.\r\nCurrently, the supported values are zlib, with levels from 1 to 9, but this can be expanded in the future.",
          "timestamp": "2020-10-04T11:31:10+01:00",
          "tree_id": "302c95715972bb03a6d7e329dad5995741db8395",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/d786296bc67219512f4058265ffbd8c9e6f06b0a"
        },
        "date": 1601807552492,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 3.1735518423637896,
            "unit": "iter/sec",
            "range": "stddev: 0.01510237694016485",
            "extra": "mean: 315.104353 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.8836012165697237,
            "unit": "iter/sec",
            "range": "stddev: 0.11676242289486118",
            "extra": "mean: 1.1317322579999995 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 7.622376085642099,
            "unit": "iter/sec",
            "range": "stddev: 0.005219327066593961",
            "extra": "mean: 131.1926870000093 msec\nrounds: 8"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 22.959844249891994,
            "unit": "iter/sec",
            "range": "stddev: 0.0015250991806245525",
            "extra": "mean: 43.55430242104992 msec\nrounds: 19"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 3.8352401429815157,
            "unit": "iter/sec",
            "range": "stddev: 0.010024381514081335",
            "extra": "mean: 260.7398657499971 msec\nrounds: 4"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1912741.5186453334,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014384784615108434",
            "extra": "mean: 522.8097943459883 nsec\nrounds: 181819"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2845755.3870736775,
            "unit": "iter/sec",
            "range": "stddev: 4.414585515802322e-7",
            "extra": "mean: 351.40054712432413 nsec\nrounds: 133334"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "mail@sphuber.net",
            "name": "Sebastiaan Huber",
            "username": "sphuber"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "4f4357b4e0a0347ffb6f8a66cb1d5da6de675cc7",
          "message": "Dependencies: set up limit for sqlalchemy dependency (#107)\n\nThe code is incompatible with `sqlalchemy==1.4` so for now we put an\r\nupper limit on the requirement `sqlalchemy<1.4`.",
          "timestamp": "2021-04-23T08:50:13+02:00",
          "tree_id": "b3147e700fe9ef371fe44e913d5b67680a93d08a",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/4f4357b4e0a0347ffb6f8a66cb1d5da6de675cc7"
        },
        "date": 1619160715716,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 3.110737753453293,
            "unit": "iter/sec",
            "range": "stddev: 0.006081654291549682",
            "extra": "mean: 321.4671499999895 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.7068612616512694,
            "unit": "iter/sec",
            "range": "stddev: 0.07522698959636813",
            "extra": "mean: 1.414704772000012 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 7.556229902057653,
            "unit": "iter/sec",
            "range": "stddev: 0.006089939119498206",
            "extra": "mean: 132.3411295000021 msec\nrounds: 8"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 22.63754750796185,
            "unit": "iter/sec",
            "range": "stddev: 0.0012718767616330172",
            "extra": "mean: 44.17439652631497 msec\nrounds: 19"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 3.5702365714440574,
            "unit": "iter/sec",
            "range": "stddev: 0.018421444221210198",
            "extra": "mean: 280.09348400000533 msec\nrounds: 4"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2533586.295796736,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011738966658674193",
            "extra": "mean: 394.69743014441946 nsec\nrounds: 126583"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2581308.588013812,
            "unit": "iter/sec",
            "range": "stddev: 4.5190881894876036e-7",
            "extra": "mean: 387.40040793404114 nsec\nrounds: 128206"
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
          "id": "7a894a4f8befb5de0fe95979183b1cbb03f4ef13",
          "message": "Merge pull request #106 from aiidateam/fix/update-python-support\n\nPython support: remove 3.5 and add 3.9 support",
          "timestamp": "2021-04-23T15:33:19+02:00",
          "tree_id": "f577efcb13f4ee1f11313641f80fbf03890b9d37",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/7a894a4f8befb5de0fe95979183b1cbb03f4ef13"
        },
        "date": 1619184877952,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 3.6665206520648983,
            "unit": "iter/sec",
            "range": "stddev: 0.010301796345693537",
            "extra": "mean: 272.73813374999634 msec\nrounds: 4"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 1.0405565142641988,
            "unit": "iter/sec",
            "range": "stddev: 0.12313696028119797",
            "extra": "mean: 961.0242080000072 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 8.123372559099058,
            "unit": "iter/sec",
            "range": "stddev: 0.005351867598176458",
            "extra": "mean: 123.10158037499974 msec\nrounds: 8"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 24.6966794771186,
            "unit": "iter/sec",
            "range": "stddev: 0.004297786199982911",
            "extra": "mean: 40.49127336840959 msec\nrounds: 19"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 4.1421121567661014,
            "unit": "iter/sec",
            "range": "stddev: 0.00308434579915087",
            "extra": "mean: 241.4227240000031 msec\nrounds: 4"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1872485.1477985224,
            "unit": "iter/sec",
            "range": "stddev: 2.711564371440361e-7",
            "extra": "mean: 534.0496298065159 nsec\nrounds: 128189"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2753054.6296537984,
            "unit": "iter/sec",
            "range": "stddev: 6.381575096710162e-7",
            "extra": "mean: 363.2328938296282 nsec\nrounds: 126583"
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
          "id": "a2561a40cf2e9a4d58325387f913ccf08111f5fd",
          "message": "Merge pull request #104 from giovannipizzi/master_in_dev\n\nMerge v0.5.0 in develop",
          "timestamp": "2021-04-23T16:22:25+02:00",
          "tree_id": "4beb6bcd4bfe656b36e0d022e991951f256753fd",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/a2561a40cf2e9a4d58325387f913ccf08111f5fd"
        },
        "date": 1619187839637,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 3.021310840181747,
            "unit": "iter/sec",
            "range": "stddev: 0.016524510831205787",
            "extra": "mean: 330.98216399999575 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.7864234520685982,
            "unit": "iter/sec",
            "range": "stddev: 0.13055107411439965",
            "extra": "mean: 1.2715795763333517 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 6.552048987390683,
            "unit": "iter/sec",
            "range": "stddev: 0.012252439376262927",
            "extra": "mean: 152.62401149998794 msec\nrounds: 8"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 18.942345549070605,
            "unit": "iter/sec",
            "range": "stddev: 0.007869763538194472",
            "extra": "mean: 52.79177266666769 msec\nrounds: 15"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 3.3672531644685386,
            "unit": "iter/sec",
            "range": "stddev: 0.010122857116211722",
            "extra": "mean: 296.97796725000103 msec\nrounds: 4"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1806370.9374006693,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018334556253608284",
            "extra": "mean: 553.5961519835895 nsec\nrounds: 169492"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2290447.767326605,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028004990930402033",
            "extra": "mean: 436.5958544286526 nsec\nrounds: 125001"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "chrisj_sewell@hotmail.com",
            "name": "Chris Sewell",
            "username": "chrisjsewell"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "2cb284157df3cc9bc5a3ae92da6aebbacbda5623",
          "message": "🔧 MAINTAIN: Improve repo configuration (#112)\n\n- Move config to `setup.cfg` and `pyproject.toml`\r\n- Add `Manifest.in`, `tox.ini`\r\n- Replace `requirements.txt`/`dev-requirements.txt with `requirements.lock`\r\n- Move from yapf to black code formatting\r\n- Add more pre-commit hooks\r\n- Update pylint version and fix new failures\r\n- Drop python 3.6",
          "timestamp": "2021-08-30T16:07:48+02:00",
          "tree_id": "3e95e7e154b9b51de8f0ec0458d0ae1a6a26ba51",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/2cb284157df3cc9bc5a3ae92da6aebbacbda5623"
        },
        "date": 1630332554747,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 3.0995900803484076,
            "unit": "iter/sec",
            "range": "stddev: 0.0158800006050287",
            "extra": "mean: 322.6233063333315 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.6945030463542721,
            "unit": "iter/sec",
            "range": "stddev: 0.09581238490221491",
            "extra": "mean: 1.4398784933333342 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 6.669887097782519,
            "unit": "iter/sec",
            "range": "stddev: 0.009612125424282948",
            "extra": "mean: 149.92757528571386 msec\nrounds: 7"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 21.226056529175292,
            "unit": "iter/sec",
            "range": "stddev: 0.0013007943038136813",
            "extra": "mean: 47.11190694444333 msec\nrounds: 18"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 3.6128368102115345,
            "unit": "iter/sec",
            "range": "stddev: 0.015889706931156062",
            "extra": "mean: 276.79080250000254 msec\nrounds: 4"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2536580.0988827352,
            "unit": "iter/sec",
            "range": "stddev: 3.650667524048866e-7",
            "extra": "mean: 394.2315878140897 nsec\nrounds: 138889"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2509328.9372560787,
            "unit": "iter/sec",
            "range": "stddev: 3.729874710588882e-7",
            "extra": "mean: 398.5129191924635 nsec\nrounds: 126583"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "chrisj_sewell@hotmail.com",
            "name": "Chris Sewell",
            "username": "chrisjsewell"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "2d2d32c14fb4f5a0068fbbe49a16daf3285aeda8",
          "message": "🔧 MAINTAIN: Add contex manager methods",
          "timestamp": "2021-09-01T12:47:38+02:00",
          "tree_id": "8262168f13e44bf574c5f55ebddd2a609ade6203",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/2d2d32c14fb4f5a0068fbbe49a16daf3285aeda8"
        },
        "date": 1630493333933,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 3.453398415953227,
            "unit": "iter/sec",
            "range": "stddev: 0.00871208934557737",
            "extra": "mean: 289.56983225000243 msec\nrounds: 4"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.8180543885854358,
            "unit": "iter/sec",
            "range": "stddev: 0.0764334697799494",
            "extra": "mean: 1.2224126096666765 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 7.409140473967565,
            "unit": "iter/sec",
            "range": "stddev: 0.0062622319251307455",
            "extra": "mean: 134.9684222499974 msec\nrounds: 8"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 23.282805170640245,
            "unit": "iter/sec",
            "range": "stddev: 0.003906636502110669",
            "extra": "mean: 42.95015109523855 msec\nrounds: 21"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 3.852340879702891,
            "unit": "iter/sec",
            "range": "stddev: 0.0017733831569907877",
            "extra": "mean: 259.5824282499955 msec\nrounds: 4"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1671851.1162158677,
            "unit": "iter/sec",
            "range": "stddev: 1.6862554105071818e-7",
            "extra": "mean: 598.1393859181902 nsec\nrounds: 144907"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2615293.321662835,
            "unit": "iter/sec",
            "range": "stddev: 3.556771329350453e-8",
            "extra": "mean: 382.36628821584395 nsec\nrounds: 123442"
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
        "date": 1594399625124,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.2670576307295951,
            "unit": "iter/sec",
            "range": "stddev: 0.20116993756181967",
            "extra": "mean: 3.7445101166666674 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.374189663367292,
            "unit": "iter/sec",
            "range": "stddev: 0.009593851358588696",
            "extra": "mean: 421.1963413999996 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 0.9764185011558881,
            "unit": "iter/sec",
            "range": "stddev: 0.05050397204608055",
            "extra": "mean: 1.024151016 sec\nrounds: 3"
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
          "id": "4d493174c1354603b21ed8d623f487660a050d24",
          "message": "Merge pull request #50 from giovannipizzi/better_debugging_concurrency\n\nSlightly more detailed debugging in case of problems with the concurrent tests",
          "timestamp": "2020-07-10T19:48:46+02:00",
          "tree_id": "36d0accdc00b7f7b1eb3e3b01401bfb7c227471f",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/4d493174c1354603b21ed8d623f487660a050d24"
        },
        "date": 1594403525879,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.18641289007693232,
            "unit": "iter/sec",
            "range": "stddev: 0.21101331445653887",
            "extra": "mean: 5.364435901333334 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 1.714726168059773,
            "unit": "iter/sec",
            "range": "stddev: 0.07547337743437044",
            "extra": "mean: 583.1834951999995 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 0.7518890986156279,
            "unit": "iter/sec",
            "range": "stddev: 0.035622849032763304",
            "extra": "mean: 1.3299833736666642 sec\nrounds: 3"
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
          "id": "91ea646558962736530f212654fd83927f650c87",
          "message": "Merge pull request #53 from giovannipizzi/further_multiprocess_basic_tests\n\nFurther multiprocess basic tests",
          "timestamp": "2020-07-12T09:02:23+02:00",
          "tree_id": "e0d576ca01ebee5c8b61e515d997482d318529fb",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/91ea646558962736530f212654fd83927f650c87"
        },
        "date": 1594537465569,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.28124216237857413,
            "unit": "iter/sec",
            "range": "stddev: 0.18652944042149158",
            "extra": "mean: 3.555654641333333 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.4575564385294855,
            "unit": "iter/sec",
            "range": "stddev: 0.02716535229309906",
            "extra": "mean: 406.90825419999896 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 0.6726741080555227,
            "unit": "iter/sec",
            "range": "stddev: 0.04357975730898271",
            "extra": "mean: 1.4866039706666687 sec\nrounds: 3"
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
          "id": "6fae5f875c73bf4b5f2eb69e28467efa731c2aa3",
          "message": "Merge pull request #58 from sphuber/feature/057/packed-object-reader-mode\n\nAdd the `mode` property to the `PackedObjectReader`",
          "timestamp": "2020-07-12T21:53:29+02:00",
          "tree_id": "f32c32f225344579ea82d4787e2e232ead7dfa2c",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/6fae5f875c73bf4b5f2eb69e28467efa731c2aa3"
        },
        "date": 1594584067920,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.25637096769093004,
            "unit": "iter/sec",
            "range": "stddev: 0.18101048764204516",
            "extra": "mean: 3.9005976729999996 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 1.9572581083069391,
            "unit": "iter/sec",
            "range": "stddev: 0.023496314085722635",
            "extra": "mean: 510.91881839999974 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 0.6366992197621189,
            "unit": "iter/sec",
            "range": "stddev: 0.42621145786798614",
            "extra": "mean: 1.5706003226666685 sec\nrounds: 3"
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
          "id": "6025360bb8a030b1103e7d40da4f7bde7938dd4c",
          "message": "Merge pull request #55 from giovannipizzi/fix_open_files\n\nFix lost open files and implement FULLSYNC for pack files on Mac OS",
          "timestamp": "2020-07-12T22:29:09+02:00",
          "tree_id": "571d031d2c95a14eb9fc9289031f93a62b9693f8",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/6025360bb8a030b1103e7d40da4f7bde7938dd4c"
        },
        "date": 1594585863671,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3083947741165859,
            "unit": "iter/sec",
            "range": "stddev: 0.15956238467904577",
            "extra": "mean: 3.2425970993333335 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 1.3875293779687363,
            "unit": "iter/sec",
            "range": "stddev: 0.052000855552047",
            "extra": "mean: 720.7054609999991 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.857148690624174,
            "unit": "iter/sec",
            "range": "stddev: 0.011963336789995798",
            "extra": "mean: 349.9992853999977 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 0.7465320835614179,
            "unit": "iter/sec",
            "range": "stddev: 0.06630423406040951",
            "extra": "mean: 1.3395271576666659 sec\nrounds: 3"
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
          "id": "09cc7a9539aa68f3417bf4ef2e80b520a1b4ba41",
          "message": "Merge pull request #60 from giovannipizzi/fix_56_seek\n\nAdded seek method to both the PackedObjectReader and the StreamDecompresser",
          "timestamp": "2020-07-13T01:27:47+02:00",
          "tree_id": "cf2de3df905a56e5ca39dbd1155b206012989f9f",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/09cc7a9539aa68f3417bf4ef2e80b520a1b4ba41"
        },
        "date": 1594597043470,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.22859100130799295,
            "unit": "iter/sec",
            "range": "stddev: 0.41362199831320695",
            "extra": "mean: 4.374625397666666 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.11820384108833179,
            "unit": "iter/sec",
            "range": "stddev: 0.24532156376351738",
            "extra": "mean: 8.459961967333333 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.0583851470145333,
            "unit": "iter/sec",
            "range": "stddev: 0.05305504257692827",
            "extra": "mean: 485.817730200003 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 0.6375980103068883,
            "unit": "iter/sec",
            "range": "stddev: 0.0788760964002703",
            "extra": "mean: 1.5683863246666665 sec\nrounds: 3"
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
          "id": "df368df957ecb9cf2a4a308c0b2baccfa7669638",
          "message": "Merge pull request #61 from giovannipizzi/check_concurrency\n\nFix concurrency problems in Mac OS",
          "timestamp": "2020-07-13T10:14:15+02:00",
          "tree_id": "2483876c2ad6de311dce821cd69d08efc5662ed0",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/df368df957ecb9cf2a4a308c0b2baccfa7669638"
        },
        "date": 1594628174810,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3163073672993095,
            "unit": "iter/sec",
            "range": "stddev: 0.025004027532547535",
            "extra": "mean: 3.161481847666667 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.7058886811916807,
            "unit": "iter/sec",
            "range": "stddev: 0.09042342423381623",
            "extra": "mean: 1.4166539663333328 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.7652036088851477,
            "unit": "iter/sec",
            "range": "stddev: 0.00414246411331762",
            "extra": "mean: 361.6370226000001 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 0.9956526314688173,
            "unit": "iter/sec",
            "range": "stddev: 0.06549834233072008",
            "extra": "mean: 1.0043663506666671 sec\nrounds: 3"
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
          "id": "cec284e3680abc6105e80d0098da030a6cc3509e",
          "message": "Merge pull request #62 from giovannipizzi/fix_58_performance_has\n\nAdding methods to just fetch metas without opening streams",
          "timestamp": "2020-07-13T20:34:37+02:00",
          "tree_id": "3318cf4caa826238d95afbbb139840cb292a6f0e",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/cec284e3680abc6105e80d0098da030a6cc3509e"
        },
        "date": 1594665691530,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.303524917639796,
            "unit": "iter/sec",
            "range": "stddev: 0.07457511451689558",
            "extra": "mean: 3.294622424333333 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.16568739061022653,
            "unit": "iter/sec",
            "range": "stddev: 2.3063478960777486",
            "extra": "mean: 6.0354623023333325 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.581518735238749,
            "unit": "iter/sec",
            "range": "stddev: 0.0064269659203062615",
            "extra": "mean: 387.3688718000011 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.127971807680183,
            "unit": "iter/sec",
            "range": "stddev: 0.11498933715114586",
            "extra": "mean: 886.5469803333355 msec\nrounds: 3"
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
          "id": "dab40d1d73c8515a5900560c656d04bdbae5fdf0",
          "message": "Merge pull request #63 from giovannipizzi/fix_10_performance\n\nAdding performance tests for loose read",
          "timestamp": "2020-07-13T22:09:53+02:00",
          "tree_id": "da463ed266c11b51b86ed097afedaa7a018bec82",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/dab40d1d73c8515a5900560c656d04bdbae5fdf0"
        },
        "date": 1594671408363,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3149834403440924,
            "unit": "iter/sec",
            "range": "stddev: 0.011688672079478334",
            "extra": "mean: 3.1747700733333333 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.0630059112410551,
            "unit": "iter/sec",
            "range": "stddev: 0.30794564182151113",
            "extra": "mean: 15.871526660000002 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.8189986974247114,
            "unit": "iter/sec",
            "range": "stddev: 0.01089774824704289",
            "extra": "mean: 354.73588579999955 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 11.148714163163342,
            "unit": "iter/sec",
            "range": "stddev: 0.0007493945786586733",
            "extra": "mean: 89.69644260000109 msec\nrounds: 10"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.420793667779523,
            "unit": "iter/sec",
            "range": "stddev: 0.006852459839201409",
            "extra": "mean: 703.8319656666564 msec\nrounds: 3"
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
          "id": "801df0c0b90f09e910c7f822ae87e548446bce7a",
          "message": "Merge pull request #66 from giovannipizzi/fix_65_list_all\n\nAdding a function to list all objects",
          "timestamp": "2020-07-14T00:46:13+02:00",
          "tree_id": "0587cf74d5f99911d7ac55811765a11dfa23aeab",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/801df0c0b90f09e910c7f822ae87e548446bce7a"
        },
        "date": 1594680488088,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3009759620207616,
            "unit": "iter/sec",
            "range": "stddev: 0.2007963307515031",
            "extra": "mean: 3.3225244743333326 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 1.2425917286898986,
            "unit": "iter/sec",
            "range": "stddev: 0.0891299200817095",
            "extra": "mean: 804.7695609999993 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.7510770951016874,
            "unit": "iter/sec",
            "range": "stddev: 0.019083054736029424",
            "extra": "mean: 363.49399360000024 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 11.286760018004085,
            "unit": "iter/sec",
            "range": "stddev: 0.0014513196537408732",
            "extra": "mean: 88.59938533333296 msec\nrounds: 9"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.3973914413262156,
            "unit": "iter/sec",
            "range": "stddev: 0.01971294596466424",
            "extra": "mean: 715.6190959999975 msec\nrounds: 3"
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
          "id": "5a256e013b16d6a7044f7584114e7261dba5d1f6",
          "message": "Merge pull request #71 from giovannipizzi/fix_69_efficient_list_all\n\nImprove performance of list_all_objects for packed objects",
          "timestamp": "2020-07-16T14:37:20+02:00",
          "tree_id": "4038bcb9cafb4dbb2cf25ee20ef0750f1bbf4912",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/5a256e013b16d6a7044f7584114e7261dba5d1f6"
        },
        "date": 1594903301612,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.2987029221090085,
            "unit": "iter/sec",
            "range": "stddev: 0.1092283337598311",
            "extra": "mean: 3.347807892 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.5053370846036854,
            "unit": "iter/sec",
            "range": "stddev: 0.010148356745714297",
            "extra": "mean: 1.9788771306666675 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.3249799706114285,
            "unit": "iter/sec",
            "range": "stddev: 0.05323003075917984",
            "extra": "mean: 430.11123219999945 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 10.472330276511405,
            "unit": "iter/sec",
            "range": "stddev: 0.007318237771399916",
            "extra": "mean: 95.48973090000032 msec\nrounds: 10"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.280726225731252,
            "unit": "iter/sec",
            "range": "stddev: 0.03442638761247181",
            "extra": "mean: 780.806998333335 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1904478.4400424503,
            "unit": "iter/sec",
            "range": "stddev: 9.687666114060676e-7",
            "extra": "mean: 525.0781415922515 nsec\nrounds: 166723"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2076633.5269556881,
            "unit": "iter/sec",
            "range": "stddev: 5.669641770384444e-7",
            "extra": "mean: 481.54861559323086 nsec\nrounds: 56597"
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
          "id": "32baa140c5860150a0891937b0e4a69aa88b05e7",
          "message": "Do not fail on benchmark test alert",
          "timestamp": "2020-07-16T23:04:29+02:00",
          "tree_id": "f3721560975ad665334615ba90b19359aacbc87d",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/32baa140c5860150a0891937b0e4a69aa88b05e7"
        },
        "date": 1594933732315,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.2661037970083626,
            "unit": "iter/sec",
            "range": "stddev: 0.04435043795173731",
            "extra": "mean: 3.757932097333334 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 1.3765195877496201,
            "unit": "iter/sec",
            "range": "stddev: 0.00743804355632289",
            "extra": "mean: 726.4698656666653 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.296213596683823,
            "unit": "iter/sec",
            "range": "stddev: 0.018693333996654724",
            "extra": "mean: 435.4995552000013 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 8.195900021831573,
            "unit": "iter/sec",
            "range": "stddev: 0.017758514695843552",
            "extra": "mean: 122.01222530000138 msec\nrounds: 10"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 0.9698201640519553,
            "unit": "iter/sec",
            "range": "stddev: 0.04861285142245104",
            "extra": "mean: 1.0311190023333314 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2019888.819315753,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011942843426629838",
            "extra": "mean: 495.0767539466626 nsec\nrounds: 157829"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3188963.4603771023,
            "unit": "iter/sec",
            "range": "stddev: 2.5831137878518007e-7",
            "extra": "mean: 313.5815171371805 nsec\nrounds: 192013"
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
          "id": "2815887c622e923ab8d6eac4370488df9be8166a",
          "message": "Merge pull request #74 from giovannipizzi/fix_hash_computation\n\nFix to the hash calculation when writing to compressed packs.",
          "timestamp": "2020-07-17T15:50:51+02:00",
          "tree_id": "84fff9b9c58f7df075b9377c35ae3974517e74ea",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/2815887c622e923ab8d6eac4370488df9be8166a"
        },
        "date": 1594994111874,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.32044457417199157,
            "unit": "iter/sec",
            "range": "stddev: 0.046848527276737634",
            "extra": "mean: 3.1206644786666664 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.25861635426411633,
            "unit": "iter/sec",
            "range": "stddev: 2.2248446227363368",
            "extra": "mean: 3.866731486666667 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.7100307929633725,
            "unit": "iter/sec",
            "range": "stddev: 0.01432394338022498",
            "extra": "mean: 368.9994971999994 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 10.554319019748116,
            "unit": "iter/sec",
            "range": "stddev: 0.005465780449663768",
            "extra": "mean: 94.7479414 msec\nrounds: 10"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.4269876896816194,
            "unit": "iter/sec",
            "range": "stddev: 0.01820396846360475",
            "extra": "mean: 700.7768933333361 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2269976.1171215037,
            "unit": "iter/sec",
            "range": "stddev: 4.803406253331213e-7",
            "extra": "mean: 440.53326925222166 nsec\nrounds: 171645"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3984768.2450144477,
            "unit": "iter/sec",
            "range": "stddev: 4.150161903802594e-7",
            "extra": "mean: 250.95562364287485 nsec\nrounds: 193051"
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
          "id": "fa85ce1b90b92989c15446fb1125e6c7840ad729",
          "message": "Merge pull request #77 from giovannipizzi/fix_37_concurrency_win\n\nFix concurrency problems on Windows",
          "timestamp": "2020-07-17T16:48:14+02:00",
          "tree_id": "45fabeaefc37015b298754e3beaf07326d2b02f2",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/fa85ce1b90b92989c15446fb1125e6c7840ad729"
        },
        "date": 1594997504739,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.30395784978238904,
            "unit": "iter/sec",
            "range": "stddev: 0.043926858467984824",
            "extra": "mean: 3.289929839666667 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 1.482076644671825,
            "unit": "iter/sec",
            "range": "stddev: 0.007015396081951773",
            "extra": "mean: 674.7289376666679 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 1.9472916073064812,
            "unit": "iter/sec",
            "range": "stddev: 0.09827728488596534",
            "extra": "mean: 513.5337698000008 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 7.9517134708688655,
            "unit": "iter/sec",
            "range": "stddev: 0.029379930615738643",
            "extra": "mean: 125.75905855555585 msec\nrounds: 9"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.0992647964976083,
            "unit": "iter/sec",
            "range": "stddev: 0.028512313709140036",
            "extra": "mean: 909.6989216666648 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1994490.299588943,
            "unit": "iter/sec",
            "range": "stddev: 7.330958229344038e-7",
            "extra": "mean: 501.3812301850234 nsec\nrounds: 172266"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3940152.5606793985,
            "unit": "iter/sec",
            "range": "stddev: 6.41209067269086e-7",
            "extra": "mean: 253.7972793184501 nsec\nrounds: 189934"
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
          "id": "6dea94015bf141e31781e4ea61f169d2b69e6b81",
          "message": "Merge pull request #75 from giovannipizzi/fix_64_export_to_container\n\nAdding a function to export directly a set of hash keys to a new container",
          "timestamp": "2020-07-17T17:16:12+02:00",
          "tree_id": "9d5cf808e9c4e748164afb805c1fb170f183c957",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/6dea94015bf141e31781e4ea61f169d2b69e6b81"
        },
        "date": 1594999261726,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.31633276645317104,
            "unit": "iter/sec",
            "range": "stddev: 0.053873437414981115",
            "extra": "mean: 3.1612280043333327 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.2641629734677538,
            "unit": "iter/sec",
            "range": "stddev: 1.692054100221177",
            "extra": "mean: 3.7855418830000005 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.610266894386695,
            "unit": "iter/sec",
            "range": "stddev: 0.02814479248148882",
            "extra": "mean: 383.1025870000005 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 10.43944142820755,
            "unit": "iter/sec",
            "range": "stddev: 0.007286173219964011",
            "extra": "mean: 95.79056569999835 msec\nrounds: 10"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.3625095521343629,
            "unit": "iter/sec",
            "range": "stddev: 0.01553288587307526",
            "extra": "mean: 733.9398086666667 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1884806.181366991,
            "unit": "iter/sec",
            "range": "stddev: 3.4849378929895864e-7",
            "extra": "mean: 530.5585316335981 nsec\nrounds: 132014"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3496408.4624881167,
            "unit": "iter/sec",
            "range": "stddev: 2.2506547534941204e-7",
            "extra": "mean: 286.0077736136304 nsec\nrounds: 190259"
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
          "id": "38bfa5ed21e99016756308569337be1cdeaeb311",
          "message": "Merge pull request #68 from sphuber/feature/067/packed-object-reader-seek-whence\n\nImplement `whence=1` for the `utils.PackedObjectReader.seek`",
          "timestamp": "2020-07-17T18:20:39+02:00",
          "tree_id": "57f4997cbdc791e0a32f9905fa065586842a7ad8",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/38bfa5ed21e99016756308569337be1cdeaeb311"
        },
        "date": 1595003075982,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.2854989387862171,
            "unit": "iter/sec",
            "range": "stddev: 0.26317012913211",
            "extra": "mean: 3.502639989666667 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 1.2768271128169904,
            "unit": "iter/sec",
            "range": "stddev: 0.09564362558713246",
            "extra": "mean: 783.1913890000012 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.495803629403732,
            "unit": "iter/sec",
            "range": "stddev: 0.02025806426707192",
            "extra": "mean: 400.6725481999993 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 10.08995762258151,
            "unit": "iter/sec",
            "range": "stddev: 0.00804615603345699",
            "extra": "mean: 99.10844400000072 msec\nrounds: 9"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.3044657361776877,
            "unit": "iter/sec",
            "range": "stddev: 0.014100190145361582",
            "extra": "mean: 766.5973680000017 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2208384.7753375396,
            "unit": "iter/sec",
            "range": "stddev: 4.2752793263056895e-7",
            "extra": "mean: 452.81964047553964 nsec\nrounds: 189466"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3566859.5110401055,
            "unit": "iter/sec",
            "range": "stddev: 1.2092035521485646e-7",
            "extra": "mean: 280.3586731983017 nsec\nrounds: 191792"
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
          "id": "dbefa5af8e4b59d8b7e35f67f4597025e7f2b60d",
          "message": "Avoid seeking back to zero for compressed streams when seeking forward\n\nFixes #81",
          "timestamp": "2020-07-17T18:31:03+02:00",
          "tree_id": "01ba21f85aaef7d3d3d31955b500af91455036bd",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/dbefa5af8e4b59d8b7e35f67f4597025e7f2b60d"
        },
        "date": 1595003709801,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.31237191072661186,
            "unit": "iter/sec",
            "range": "stddev: 0.023383692993602108",
            "extra": "mean: 3.201312172 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 1.1825453967460735,
            "unit": "iter/sec",
            "range": "stddev: 0.04180903174411803",
            "extra": "mean: 845.6334976666682 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.631695235055338,
            "unit": "iter/sec",
            "range": "stddev: 0.021666429010139678",
            "extra": "mean: 379.9832088000009 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 9.152882704984385,
            "unit": "iter/sec",
            "range": "stddev: 0.0219725815281887",
            "extra": "mean: 109.25519666666655 msec\nrounds: 9"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.0968604009731597,
            "unit": "iter/sec",
            "range": "stddev: 0.1057317313060235",
            "extra": "mean: 911.6930459999987 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2092301.3229305292,
            "unit": "iter/sec",
            "range": "stddev: 7.031707704255674e-7",
            "extra": "mean: 477.94263141762735 nsec\nrounds: 161395"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3250995.7910992145,
            "unit": "iter/sec",
            "range": "stddev: 2.389340679003734e-7",
            "extra": "mean: 307.598060488994 nsec\nrounds: 108120"
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
          "id": "ddc612b9ceaf7f67711f7079d0f584ead8147507",
          "message": "Merge pull request #84 from giovannipizzi/fix_13_validation\n\nImplement validation routine",
          "timestamp": "2020-07-19T23:21:12+02:00",
          "tree_id": "d7baf41d8de602432d63610a50939df2fde3d94c",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/ddc612b9ceaf7f67711f7079d0f584ead8147507"
        },
        "date": 1595193966028,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3018797930033967,
            "unit": "iter/sec",
            "range": "stddev: 0.05970476292803879",
            "extra": "mean: 3.3125768043333337 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.22791211589385182,
            "unit": "iter/sec",
            "range": "stddev: 4.03883148268026",
            "extra": "mean: 4.387656163333333 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.430051653294592,
            "unit": "iter/sec",
            "range": "stddev: 0.04371850336197779",
            "extra": "mean: 411.5138863999988 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 10.31641471444086,
            "unit": "iter/sec",
            "range": "stddev: 0.007632399868678327",
            "extra": "mean: 96.93290040000093 msec\nrounds: 10"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.321561665526325,
            "unit": "iter/sec",
            "range": "stddev: 0.015578507791108183",
            "extra": "mean: 756.6805439999958 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2172723.9516294203,
            "unit": "iter/sec",
            "range": "stddev: 9.10811330911536e-7",
            "extra": "mean: 460.25174953774336 nsec\nrounds: 185049"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 4060535.889642517,
            "unit": "iter/sec",
            "range": "stddev: 2.502596001275903e-7",
            "extra": "mean: 246.27291253616744 nsec\nrounds: 198099"
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
          "id": "89a6ea1a6c87895d4cbb0c1e2c869225c31fb707",
          "message": "Adding nodes on performance for validation",
          "timestamp": "2020-07-20T14:06:57+02:00",
          "tree_id": "a1c4c31f0e67410babd839471c3349dc89f24c78",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/89a6ea1a6c87895d4cbb0c1e2c869225c31fb707"
        },
        "date": 1595247075267,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3311522277745718,
            "unit": "iter/sec",
            "range": "stddev: 0.006199139454093782",
            "extra": "mean: 3.0197592409999996 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.29555558993917935,
            "unit": "iter/sec",
            "range": "stddev: 0.43232283225321433",
            "extra": "mean: 3.3834582529999992 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.7029814180747493,
            "unit": "iter/sec",
            "range": "stddev: 0.010020524702626142",
            "extra": "mean: 369.9618478000005 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 10.358269033308016,
            "unit": "iter/sec",
            "range": "stddev: 0.0026847528044138032",
            "extra": "mean: 96.54122679999944 msec\nrounds: 10"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.3245678864281307,
            "unit": "iter/sec",
            "range": "stddev: 0.017991244645278508",
            "extra": "mean: 754.9631923333351 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2297233.832719461,
            "unit": "iter/sec",
            "range": "stddev: 2.8350929731417825e-7",
            "extra": "mean: 435.3061433089734 nsec\nrounds: 147689"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 4205266.662517182,
            "unit": "iter/sec",
            "range": "stddev: 3.0077312562060227e-7",
            "extra": "mean: 237.7970483806175 nsec\nrounds: 197434"
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
          "id": "d41ef638da9ca6958401ce010332e42cf4f988e4",
          "message": "Merge pull request #87 from giovannipizzi/fix_5_delete\n\nImplement function `delete_objects` for object deletion",
          "timestamp": "2020-07-20T14:40:53+02:00",
          "tree_id": "909ea5614905a444fc80d603a21b439da060a5a4",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/d41ef638da9ca6958401ce010332e42cf4f988e4"
        },
        "date": 1595249021983,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3144942963258858,
            "unit": "iter/sec",
            "range": "stddev: 0.08833733453726322",
            "extra": "mean: 3.1797079046666665 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.9537844380061834,
            "unit": "iter/sec",
            "range": "stddev: 0.00859628305398457",
            "extra": "mean: 1.0484549339999998 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.6305195097892997,
            "unit": "iter/sec",
            "range": "stddev: 0.009556959749825041",
            "extra": "mean: 380.1530444000008 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 10.374682724824682,
            "unit": "iter/sec",
            "range": "stddev: 0.008831191269334958",
            "extra": "mean: 96.38848979999999 msec\nrounds: 10"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.3114618130586355,
            "unit": "iter/sec",
            "range": "stddev: 0.008005991081098852",
            "extra": "mean: 762.5079053333366 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2261366.354536393,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012403436617743096",
            "extra": "mean: 442.21052373666004 nsec\nrounds: 161787"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 4143949.0178476307,
            "unit": "iter/sec",
            "range": "stddev: 1.819022147170017e-7",
            "extra": "mean: 241.31571013375708 nsec\nrounds: 188929"
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
          "id": "3f3cd07ea6627bbf6d0637e69e409ef4801b4f90",
          "message": "Adding nightly concurrency extensive tests\n\nThis runs only the main branch of the main fork, at 5AM UTC.\nTests are repeated 5 times to increase the change of seeing random errors.\n\nFixes #76",
          "timestamp": "2020-07-20T14:51:14+02:00",
          "tree_id": "01658224411ac3acb670ee1ef1e9d5081979f9ee",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/3f3cd07ea6627bbf6d0637e69e409ef4801b4f90"
        },
        "date": 1595250288318,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3205090683994477,
            "unit": "iter/sec",
            "range": "stddev: 0.14992188406241427",
            "extra": "mean: 3.1200365249999997 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 1.2792789424409095,
            "unit": "iter/sec",
            "range": "stddev: 0.0681536621589124",
            "extra": "mean: 781.6903466666657 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.757163123166226,
            "unit": "iter/sec",
            "range": "stddev: 0.01618033073065509",
            "extra": "mean: 362.69163460000016 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 11.128045894999035,
            "unit": "iter/sec",
            "range": "stddev: 0.0019055506462867622",
            "extra": "mean: 89.86303700000033 msec\nrounds: 11"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.4202018981268167,
            "unit": "iter/sec",
            "range": "stddev: 0.009754030370389973",
            "extra": "mean: 704.1252383333353 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2181832.04885187,
            "unit": "iter/sec",
            "range": "stddev: 4.357846997758716e-7",
            "extra": "mean: 458.3304203117848 nsec\nrounds: 162947"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 4136979.1900180317,
            "unit": "iter/sec",
            "range": "stddev: 1.5404481110491218e-7",
            "extra": "mean: 241.72226981777106 nsec\nrounds: 194932"
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
          "id": "5d977ad3ce8d4eba5ba70dfd0919282c2505e3b1",
          "message": "Merge pull request #88 from giovannipizzi/fix_78_loose_streamed\n\nAdding `add_streamed_object` function",
          "timestamp": "2020-07-20T15:47:49+02:00",
          "tree_id": "4864b702ab018ce6fa9ac195aca677f776b5bbff",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/5d977ad3ce8d4eba5ba70dfd0919282c2505e3b1"
        },
        "date": 1595253148368,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3009431720015124,
            "unit": "iter/sec",
            "range": "stddev: 0.07019418512425264",
            "extra": "mean: 3.3228864883333338 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.8065765648392418,
            "unit": "iter/sec",
            "range": "stddev: 0.5928226056012846",
            "extra": "mean: 1.2398079036666647 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.600559951424497,
            "unit": "iter/sec",
            "range": "stddev: 0.01323996011421978",
            "extra": "mean: 384.5325693999996 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 10.24404827596052,
            "unit": "iter/sec",
            "range": "stddev: 0.004444866278973513",
            "extra": "mean: 97.61765788889123 msec\nrounds: 9"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.2209696044977036,
            "unit": "iter/sec",
            "range": "stddev: 0.04859635388799997",
            "extra": "mean: 819.0212076666654 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2322441.0949071827,
            "unit": "iter/sec",
            "range": "stddev: 4.122731144511924e-7",
            "extra": "mean: 430.58142666906497 nsec\nrounds: 195237"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2086959.7163431766,
            "unit": "iter/sec",
            "range": "stddev: 3.9063989470252764e-7",
            "extra": "mean: 479.16593318448196 nsec\nrounds: 192234"
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
          "id": "1589096795f049b538222474b724e0d1298a4b49",
          "message": "Complete move to aiidateam organisation\n\nFixes #80",
          "timestamp": "2020-07-20T17:02:04+02:00",
          "tree_id": "e54abe7df4b0f77aefb62e2a5ad6a6b7578e733a",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/1589096795f049b538222474b724e0d1298a4b49"
        },
        "date": 1595257696329,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.31450741400645243,
            "unit": "iter/sec",
            "range": "stddev: 0.08076926907081057",
            "extra": "mean: 3.1795752833333335 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.24658235848373294,
            "unit": "iter/sec",
            "range": "stddev: 0.18277960753764133",
            "extra": "mean: 4.055440162666666 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.7182517654668685,
            "unit": "iter/sec",
            "range": "stddev: 0.01154082809237057",
            "extra": "mean: 367.88350980000075 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 10.604638636492863,
            "unit": "iter/sec",
            "range": "stddev: 0.0017793896483055778",
            "extra": "mean: 94.29835700000027 msec\nrounds: 10"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.360838300089584,
            "unit": "iter/sec",
            "range": "stddev: 0.007829908360836751",
            "extra": "mean: 734.8411636666677 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2173559.751023432,
            "unit": "iter/sec",
            "range": "stddev: 7.384947501600906e-7",
            "extra": "mean: 460.0747688344637 nsec\nrounds: 164935"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 4140875.7785321185,
            "unit": "iter/sec",
            "range": "stddev: 1.0263212397863012e-7",
            "extra": "mean: 241.49480773712813 nsec\nrounds: 196735"
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
          "id": "11cc7cbf88b964e48ac44f5de59ef09bc6bdb745",
          "message": "Adding simple changelog",
          "timestamp": "2020-07-20T17:41:58+02:00",
          "tree_id": "c53c9f1eed85787028f0bcbc6f537bb2915cc518",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/11cc7cbf88b964e48ac44f5de59ef09bc6bdb745"
        },
        "date": 1595260190612,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.32364941316461804,
            "unit": "iter/sec",
            "range": "stddev: 0.06936257852725737",
            "extra": "mean: 3.0897630563333336 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.08244706242705191,
            "unit": "iter/sec",
            "range": "stddev: 0.49775177141471866",
            "extra": "mean: 12.128994903666666 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.011486535932645,
            "unit": "iter/sec",
            "range": "stddev: 0.035899706782408426",
            "extra": "mean: 497.1447643999966 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 9.398167304745824,
            "unit": "iter/sec",
            "range": "stddev: 0.009847736692161222",
            "extra": "mean: 106.40372400000014 msec\nrounds: 9"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.2834392250410054,
            "unit": "iter/sec",
            "range": "stddev: 0.010236417628992883",
            "extra": "mean: 779.156488666653 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1652648.1741244192,
            "unit": "iter/sec",
            "range": "stddev: 0.000003026982354180032",
            "extra": "mean: 605.0894652939696 nsec\nrounds: 160308"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3679027.7908399645,
            "unit": "iter/sec",
            "range": "stddev: 1.1051919600240443e-7",
            "extra": "mean: 271.81093942528656 nsec\nrounds: 188360"
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
          "id": "1e0ba2e2cec56c81f871ff8d72c15d7688ee8f0a",
          "message": "Change the default value of `compress` for export\n\nFor some reason it was True, but this is unexpected.\nSetting back to False.",
          "timestamp": "2020-07-20T17:51:03+02:00",
          "tree_id": "454bf54a8a996bc894244547a4ebd6dbfa0a7bdb",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/1e0ba2e2cec56c81f871ff8d72c15d7688ee8f0a"
        },
        "date": 1595260957196,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.31461296743137124,
            "unit": "iter/sec",
            "range": "stddev: 0.08941155394064772",
            "extra": "mean: 3.1785085280000005 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 1.067263420414875,
            "unit": "iter/sec",
            "range": "stddev: 0.08834293201291962",
            "extra": "mean: 936.9758026666672 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.5085872893940993,
            "unit": "iter/sec",
            "range": "stddev: 0.022888031826893022",
            "extra": "mean: 398.63073699999916 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 11.194681072077842,
            "unit": "iter/sec",
            "range": "stddev: 0.001619280828312287",
            "extra": "mean: 89.32813659999965 msec\nrounds: 10"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.2979880587582124,
            "unit": "iter/sec",
            "range": "stddev: 0.022868270888776045",
            "extra": "mean: 770.4231123333306 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1843298.5187936095,
            "unit": "iter/sec",
            "range": "stddev: 7.362532851924884e-7",
            "extra": "mean: 542.5057253637212 nsec\nrounds: 160514"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3898259.640292446,
            "unit": "iter/sec",
            "range": "stddev: 1.0571456852732272e-7",
            "extra": "mean: 256.52472956494495 nsec\nrounds: 195887"
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
          "id": "9dd029d81a791f0fa3324209fa7edfd015796aa8",
          "message": "Removing the 'OS-independent' flag\n\nThis is not really true, it actually is OS dependent,\nand I tested the three most common ones",
          "timestamp": "2020-07-20T18:33:16+02:00",
          "tree_id": "da603cd023341129a9ef4d74d860764b02631c3f",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/9dd029d81a791f0fa3324209fa7edfd015796aa8"
        },
        "date": 1595263126874,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.17657860403683648,
            "unit": "iter/sec",
            "range": "stddev: 0.14664611724631565",
            "extra": "mean: 5.663200280999999 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.9636260594894672,
            "unit": "iter/sec",
            "range": "stddev: 0.29652134217176324",
            "extra": "mean: 1.0377469456666664 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 1.7095565104743151,
            "unit": "iter/sec",
            "range": "stddev: 0.3065385964964499",
            "extra": "mean: 584.9470279999991 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 9.001465926532273,
            "unit": "iter/sec",
            "range": "stddev: 0.009739435621046894",
            "extra": "mean: 111.09301620000025 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 0.8357302536660131,
            "unit": "iter/sec",
            "range": "stddev: 0.24153632540348696",
            "extra": "mean: 1.1965583339999977 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 493428.83096222597,
            "unit": "iter/sec",
            "range": "stddev: 0.000012676840372241037",
            "extra": "mean: 2.02663471862785 usec\nrounds: 98368"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2783224.2868899438,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016647977110268007",
            "extra": "mean: 359.295513735773 nsec\nrounds: 188609"
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
          "id": "51e6a578fc55c3c0eca18bb4351cb5ae1dcdb00f",
          "message": "Explicitly specifying the codecov token",
          "timestamp": "2020-07-20T18:59:40+02:00",
          "tree_id": "b5c97bfa36b46639cdf390220798c072fbc6826a",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/51e6a578fc55c3c0eca18bb4351cb5ae1dcdb00f"
        },
        "date": 1595264630890,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.31899101620624803,
            "unit": "iter/sec",
            "range": "stddev: 0.03592903736012034",
            "extra": "mean: 3.134884524 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 1.3863508636295612,
            "unit": "iter/sec",
            "range": "stddev: 0.04337755079373706",
            "extra": "mean: 721.3181209999983 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.6274072828379453,
            "unit": "iter/sec",
            "range": "stddev: 0.013197827507614437",
            "extra": "mean: 380.6033447999994 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 10.576511313760832,
            "unit": "iter/sec",
            "range": "stddev: 0.0018707502118853942",
            "extra": "mean: 94.54913537500076 msec\nrounds: 8"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.3046715292745819,
            "unit": "iter/sec",
            "range": "stddev: 0.013188490405268297",
            "extra": "mean: 766.4764483333333 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 4040746.5204071193,
            "unit": "iter/sec",
            "range": "stddev: 5.4858460767271986e-8",
            "extra": "mean: 247.47902273742275 nsec\nrounds: 191095"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3754954.401965313,
            "unit": "iter/sec",
            "range": "stddev: 9.875187874546916e-8",
            "extra": "mean: 266.31481849065443 nsec\nrounds: 191315"
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
          "id": "48fe289e87e457a1390b6d3dd6942d0b16064a32",
          "message": "Moving the env to the right place",
          "timestamp": "2020-07-20T19:06:51+02:00",
          "tree_id": "a629875f497fff991502bc56fb3979d157cf13b4",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/48fe289e87e457a1390b6d3dd6942d0b16064a32"
        },
        "date": 1595265103660,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.29701962841739576,
            "unit": "iter/sec",
            "range": "stddev: 0.06107874993325296",
            "extra": "mean: 3.366780859999999 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.42958677003548906,
            "unit": "iter/sec",
            "range": "stddev: 0.09155595756757338",
            "extra": "mean: 2.327818428666665 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.5326576619397865,
            "unit": "iter/sec",
            "range": "stddev: 0.016189826409575583",
            "extra": "mean: 394.8421514000003 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 9.95868821434138,
            "unit": "iter/sec",
            "range": "stddev: 0.0045031989594245935",
            "extra": "mean: 100.41483160000055 msec\nrounds: 10"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.2405698070609177,
            "unit": "iter/sec",
            "range": "stddev: 0.01603835943153407",
            "extra": "mean: 806.0812009999978 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2072603.37585791,
            "unit": "iter/sec",
            "range": "stddev: 4.908003240891821e-7",
            "extra": "mean: 482.48498079671003 nsec\nrounds: 169982"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3591910.3617953067,
            "unit": "iter/sec",
            "range": "stddev: 1.6032965614073199e-7",
            "extra": "mean: 278.40338407001923 nsec\nrounds: 197942"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gio.piz@gmail.com",
            "name": "Giovanni Pizzi",
            "username": "giovannipizzi"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "9aa52ca307119522cbcb110a505b77c6b7562513",
          "message": "Merge pull request #91 from giovannipizzi/test-codecov\n\nTesting Codecov after moving the repo",
          "timestamp": "2020-07-20T19:40:16+02:00",
          "tree_id": "da603cd023341129a9ef4d74d860764b02631c3f",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/9aa52ca307119522cbcb110a505b77c6b7562513"
        },
        "date": 1595266977442,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3119371985522486,
            "unit": "iter/sec",
            "range": "stddev: 0.00841070656361201",
            "extra": "mean: 3.205773484666667 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 1.4070857464939854,
            "unit": "iter/sec",
            "range": "stddev: 0.04458331166522662",
            "extra": "mean: 710.6887426666676 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.6857531382182245,
            "unit": "iter/sec",
            "range": "stddev: 0.017480276455072725",
            "extra": "mean: 372.3350391999979 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 10.402523341751452,
            "unit": "iter/sec",
            "range": "stddev: 0.013140213441354106",
            "extra": "mean: 96.13052209999964 msec\nrounds: 10"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.3556570910883956,
            "unit": "iter/sec",
            "range": "stddev: 0.018980681282411056",
            "extra": "mean: 737.649665666666 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2359968.4117571902,
            "unit": "iter/sec",
            "range": "stddev: 2.351569242364889e-7",
            "extra": "mean: 423.7344851812732 nsec\nrounds: 185323"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 4001441.3809666643,
            "unit": "iter/sec",
            "range": "stddev: 1.040881353911888e-7",
            "extra": "mean: 249.9099461400665 nsec\nrounds: 196619"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gio.piz@gmail.com",
            "name": "Giovanni Pizzi",
            "username": "giovannipizzi"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": false,
          "id": "c718ffdec3881653acb82beaeed69fadf3cd9e3d",
          "message": "Merge pull request #90 from aiidateam/develop\n\nRelease of version 0.4.0",
          "timestamp": "2020-07-20T19:46:14+02:00",
          "tree_id": "da603cd023341129a9ef4d74d860764b02631c3f",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/c718ffdec3881653acb82beaeed69fadf3cd9e3d"
        },
        "date": 1595268289411,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.2933902723423896,
            "unit": "iter/sec",
            "range": "stddev: 0.08886215908766418",
            "extra": "mean: 3.4084292980000006 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 1.1425431132502617,
            "unit": "iter/sec",
            "range": "stddev: 0.0281677011949281",
            "extra": "mean: 875.2404949999999 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.206081368083322,
            "unit": "iter/sec",
            "range": "stddev: 0.04389032937740458",
            "extra": "mean: 453.29243720000034 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 10.214382256457634,
            "unit": "iter/sec",
            "range": "stddev: 0.007923759685980799",
            "extra": "mean: 97.90117257142887 msec\nrounds: 7"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 0.978740999366861,
            "unit": "iter/sec",
            "range": "stddev: 0.07549545966545536",
            "extra": "mean: 1.0217207623333355 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1993570.127933406,
            "unit": "iter/sec",
            "range": "stddev: 4.6054135601775875e-7",
            "extra": "mean: 501.6126525915743 nsec\nrounds: 174004"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 1778739.473984469,
            "unit": "iter/sec",
            "range": "stddev: 7.581084868945942e-7",
            "extra": "mean: 562.1958778257437 nsec\nrounds: 143370"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gio.piz@gmail.com",
            "name": "Giovanni Pizzi",
            "username": "giovannipizzi"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "e7e3627a67e8de2030b231927a127a9fb06ae474",
          "message": "Merge pull request #95 from giovannipizzi/fix_missing_optional_deps\n\nAdding missing optional dev dependencies",
          "timestamp": "2020-08-26T23:34:55+02:00",
          "tree_id": "397da3027d0c56b27a27da2ce3509320aadc032e",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/e7e3627a67e8de2030b231927a127a9fb06ae474"
        },
        "date": 1598477927050,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.28714462303552524,
            "unit": "iter/sec",
            "range": "stddev: 0.17055276303948838",
            "extra": "mean: 3.4825656473333337 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 1.0072675099578978,
            "unit": "iter/sec",
            "range": "stddev: 0.034945295047732444",
            "extra": "mean: 992.7849256666666 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.1134733049055154,
            "unit": "iter/sec",
            "range": "stddev: 0.06513217198238055",
            "extra": "mean: 473.15478160000026 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 7.948679944969446,
            "unit": "iter/sec",
            "range": "stddev: 0.024045345717839624",
            "extra": "mean: 125.80705311111176 msec\nrounds: 9"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.1267729572480092,
            "unit": "iter/sec",
            "range": "stddev: 0.016954657008986487",
            "extra": "mean: 887.4902380000004 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1480110.3392642369,
            "unit": "iter/sec",
            "range": "stddev: 0.000019675598311862305",
            "extra": "mean: 675.6253054060146 nsec\nrounds: 139978"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3128764.1048506605,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029066838718159275",
            "extra": "mean: 319.6150193776881 nsec\nrounds: 197395"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "chrisj_sewell@hotmail.com",
            "name": "Chris Sewell",
            "username": "chrisjsewell"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "64326c7e9778b6af1cc142a1f48a526a5bf7ee2e",
          "message": "🔀👌 Efficiency improvements  (#96)\n\nThis merge collects a number of important efficiency improvements, and a few features that were tightly bound to these efficiency changes, so they are shipped together.\r\n\r\nIn particular:\r\n\r\n- objects are now sorted and returned in the order in which they are on disk, with an important performance benefit. Fixes #92 \r\n- When there are many objects to list (currently set to 9500 objects, 10x the ones we could fit in a single IN SQL statement), performing many queries is slow, so we just resort to listing all objects and doing an efficient intersection (if the hash keys are sorted, both iterators can be looped over only once - fixes #93)\r\n- Since VACUUMing the DB is very important for efficiency, when the DB does not fit fully in the disk cache, `clean_storage` now provides an option to VACUUM the DB. VACUUM is also called after repacking. Fixes #94 \r\n- We implement now a function to perform a full repack of the repository (fixes #12). This is important and needed to reclaim space after deleting an object\r\n- For efficiency, we have moved the logic from an `export` function (still existing but deprecated) to a `import_objects` function\r\n- Still for efficiency, now functions like `pack_all_loose` and `import_objects` provide an option to perform a fsync to disk or not (see also #54 - there are still however calls that always use - or don't use - fsync and full_fsync on Mac). Also, `add_objects_to_pack` allows now to choose if you want to commit the changes to the SQLite DB, or not (delegating the responsibility to the caller, but this is important e.g. in `import_objects`: calling `commit` only once at the very end gives a factor of 2 speedup for very big repos).\r\n- A number of functions, including (but not exclusively) `import_objects` provide a callback to e.g. show a progress bar.\r\n- a `CallbackStreamWrapper` has been implemented, allowing to provide a callback (e.g. for a progress bar) when streaming a big file.\r\n- a new hash algorithm is now supported (`sha1`) in addition to the default `sha256` (fixes #82). This is faster even if a bit less robust. This was also needed to test completely some feature in `import_objects`, where the logic is optimised if both containers use the same algorithm. By default is still better to use everywhere sha256, also because then all export files that will be generated will use this algorithm and importing will be more efficient.\r\n- tests have been added for all new functionality, achieving again 100% coverage\r\n\r\nAs a reference, with these changes, exporting the full large SDB database (6.8M nodes) takes ~ 50 minutes:\r\n```\r\n6714808it [00:24, 274813.02it/s]\r\nAll hashkeys listed in 24.444787740707397s.\r\nListing objects: 100%|████████| 6714808/6714808 [00:06<00:00, 978896.65it/s]\r\nCopy objects: 100%|███████████| 6714808/6714808 [48:15<00:00, 2319.08it/s]\r\nFinal flush: 100%|████████████| 63236/63236 [00:07<00:00, 8582.35it/s]\r\nEverything re-exported in 2960.980943918228s.\r\n```\r\n\r\nThis can be compared to:\r\n\r\n- ~10 minutes to copy the whole 90GB, or ~15 minutes to read all and validate the packs. We will never be able to be faster than just copying the pack files, and we are only 3x slower.\r\n- ~2 days to just list all files in the old legacy AiiDA repo (or all objects if they are loose), and this does not take into account the time to rewrite everything, probably comparable. So we are almost 2 orders of magnitude faster than before.",
          "timestamp": "2020-10-02T05:02:23+01:00",
          "tree_id": "a1e5eacb37c751b57ede7818ed3ea30ccd868aa0",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/64326c7e9778b6af1cc142a1f48a526a5bf7ee2e"
        },
        "date": 1601611460708,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 1.512404081133887,
            "unit": "iter/sec",
            "range": "stddev: 0.02549491783516054",
            "extra": "mean: 661.1989563333333 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 1.3540876495871286,
            "unit": "iter/sec",
            "range": "stddev: 0.09933748808996601",
            "extra": "mean: 738.5046310000002 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 6.137232658744322,
            "unit": "iter/sec",
            "range": "stddev: 0.00447010639160744",
            "extra": "mean: 162.939887666667 msec\nrounds: 6"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 10.183354142678084,
            "unit": "iter/sec",
            "range": "stddev: 0.015937691941777285",
            "extra": "mean: 98.19947199999994 msec\nrounds: 10"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 2.277394369789959,
            "unit": "iter/sec",
            "range": "stddev: 0.0248022110226073",
            "extra": "mean: 439.0983016666669 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2241969.705377868,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022880517228306473",
            "extra": "mean: 446.03635704857 nsec\nrounds: 173914"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 4070204.737165233,
            "unit": "iter/sec",
            "range": "stddev: 0.000002314160899730941",
            "extra": "mean: 245.68788662373345 nsec\nrounds: 198966"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gio.piz@gmail.com",
            "name": "Giovanni Pizzi",
            "username": "giovannipizzi"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "1d7c389c353185c1923c9addb1b107c283d5f561",
          "message": "✨ Add the concept of a (unique) container ID (#97)\n\nAllows for the association of a container with an existing DB, or to uniquely refer to it.\r\n\r\n🐛 This also fixes a bug, whereby config values were cached, but the cache was not cleared when re-initialising the container.\r\nTo reduce the risk of such a problem, now only the whole configuration dictionary is cached, rather than each single config value.",
          "timestamp": "2020-10-02T05:26:39+01:00",
          "tree_id": "cf46e923be5370049e00e368fe2b9cf6f18ef6d3",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/1d7c389c353185c1923c9addb1b107c283d5f561"
        },
        "date": 1601613161055,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.28047039227962817,
            "unit": "iter/sec",
            "range": "stddev: 0.046374240714326935",
            "extra": "mean: 3.5654387326666654 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 1.0417301897821079,
            "unit": "iter/sec",
            "range": "stddev: 0.014345831939742126",
            "extra": "mean: 959.9414606666663 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 6.0728959615616525,
            "unit": "iter/sec",
            "range": "stddev: 0.016181849309259883",
            "extra": "mean: 164.66608457142888 msec\nrounds: 7"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 1.912954627406993,
            "unit": "iter/sec",
            "range": "stddev: 0.009569052110930574",
            "extra": "mean: 522.7515518000018 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 0.21009001345493122,
            "unit": "iter/sec",
            "range": "stddev: 0.0602672347399442",
            "extra": "mean: 4.759864515000001 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2141426.571931177,
            "unit": "iter/sec",
            "range": "stddev: 0.000001903343931825153",
            "extra": "mean: 466.9784213512313 nsec\nrounds: 177305"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 4015990.0877207923,
            "unit": "iter/sec",
            "range": "stddev: 4.515991115904188e-7",
            "extra": "mean: 249.00459865618384 nsec\nrounds: 196851"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "chrisj_sewell@hotmail.com",
            "name": "Chris Sewell",
            "username": "chrisjsewell"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "1b84d6b00ad68bf8e58861c712c3cb9b6394abfd",
          "message": "🐛 Fix performance regression (#102)\n\n`Container.is_initialised` is a costly operation, loading the config JSON every time.\r\nIn 1d7c389, the config is now called on every call to `loose_prefix_len`, leading to a large performance degradation.\r\nThis PR makes sure the `is_initialised` test is called only if the config has not already been loaded into memory.",
          "timestamp": "2020-10-02T18:45:30+01:00",
          "tree_id": "3e63fef3df945593819e81391c96d674c2e19225",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/1b84d6b00ad68bf8e58861c712c3cb9b6394abfd"
        },
        "date": 1601660977125,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 1.4702850264852585,
            "unit": "iter/sec",
            "range": "stddev: 0.054008944249848416",
            "extra": "mean: 680.1402326666666 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.35105874122439196,
            "unit": "iter/sec",
            "range": "stddev: 1.343691361953062",
            "extra": "mean: 2.8485261370000003 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 6.281526668271752,
            "unit": "iter/sec",
            "range": "stddev: 0.0025241769794354645",
            "extra": "mean: 159.19696799999923 msec\nrounds: 6"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 9.37442046453831,
            "unit": "iter/sec",
            "range": "stddev: 0.03531990255982771",
            "extra": "mean: 106.6732609000006 msec\nrounds: 10"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 2.189047813914228,
            "unit": "iter/sec",
            "range": "stddev: 0.019897162088600123",
            "extra": "mean: 456.8196243333323 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2205239.326971461,
            "unit": "iter/sec",
            "range": "stddev: 5.196045071724152e-7",
            "extra": "mean: 453.46552084817847 nsec\nrounds: 186533"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3967031.590200745,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010402571488015606",
            "extra": "mean: 252.07764981510442 nsec\nrounds: 188466"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gio.piz@gmail.com",
            "name": "Giovanni Pizzi",
            "username": "giovannipizzi"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "d786296bc67219512f4058265ffbd8c9e6f06b0a",
          "message": "✨ Generalize compression algorithm (#99)\n\nThe container configuration now accepts a variable for the compression algorithm to use.\r\nCurrently, the supported values are zlib, with levels from 1 to 9, but this can be expanded in the future.",
          "timestamp": "2020-10-04T11:31:10+01:00",
          "tree_id": "302c95715972bb03a6d7e329dad5995741db8395",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/d786296bc67219512f4058265ffbd8c9e6f06b0a"
        },
        "date": 1601807577953,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 1.4348671885017164,
            "unit": "iter/sec",
            "range": "stddev: 0.00519126450802047",
            "extra": "mean: 696.9286133333336 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 1.3881915000401441,
            "unit": "iter/sec",
            "range": "stddev: 0.014199678836680838",
            "extra": "mean: 720.3617079999999 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 5.599974535795809,
            "unit": "iter/sec",
            "range": "stddev: 0.015602399518311324",
            "extra": "mean: 178.572240571428 msec\nrounds: 7"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 10.380897543218532,
            "unit": "iter/sec",
            "range": "stddev: 0.002795179945967988",
            "extra": "mean: 96.33078409999953 msec\nrounds: 10"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 2.259168765270037,
            "unit": "iter/sec",
            "range": "stddev: 0.027865600193569",
            "extra": "mean: 442.6406806666658 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2173600.6680393238,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014121339338479238",
            "extra": "mean: 460.0661081421366 nsec\nrounds: 152069"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 4106077.2499678265,
            "unit": "iter/sec",
            "range": "stddev: 3.1326508754713804e-7",
            "extra": "mean: 243.5414482296474 nsec\nrounds: 194591"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "mail@sphuber.net",
            "name": "Sebastiaan Huber",
            "username": "sphuber"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "4f4357b4e0a0347ffb6f8a66cb1d5da6de675cc7",
          "message": "Dependencies: set up limit for sqlalchemy dependency (#107)\n\nThe code is incompatible with `sqlalchemy==1.4` so for now we put an\r\nupper limit on the requirement `sqlalchemy<1.4`.",
          "timestamp": "2021-04-23T08:50:13+02:00",
          "tree_id": "b3147e700fe9ef371fe44e913d5b67680a93d08a",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/4f4357b4e0a0347ffb6f8a66cb1d5da6de675cc7"
        },
        "date": 1619160727586,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 1.4529740579943098,
            "unit": "iter/sec",
            "range": "stddev: 0.04729099824337318",
            "extra": "mean: 688.2435336666667 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 1.215695179612072,
            "unit": "iter/sec",
            "range": "stddev: 0.09690181897092259",
            "extra": "mean: 822.5746196666664 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 6.119904985047978,
            "unit": "iter/sec",
            "range": "stddev: 0.004617292081824878",
            "extra": "mean: 163.40122966666618 msec\nrounds: 6"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 10.3253249581395,
            "unit": "iter/sec",
            "range": "stddev: 0.00559478366321411",
            "extra": "mean: 96.84925211111108 msec\nrounds: 9"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 2.280026788855554,
            "unit": "iter/sec",
            "range": "stddev: 0.005838092083479731",
            "extra": "mean: 438.59133799999955 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1953059.1534258116,
            "unit": "iter/sec",
            "range": "stddev: 5.140460440633976e-7",
            "extra": "mean: 512.017261866301 nsec\nrounds: 167421"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 4178304.77848948,
            "unit": "iter/sec",
            "range": "stddev: 7.135277363738962e-8",
            "extra": "mean: 239.33151194430138 nsec\nrounds: 195199"
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
          "id": "7a894a4f8befb5de0fe95979183b1cbb03f4ef13",
          "message": "Merge pull request #106 from aiidateam/fix/update-python-support\n\nPython support: remove 3.5 and add 3.9 support",
          "timestamp": "2021-04-23T15:33:19+02:00",
          "tree_id": "f577efcb13f4ee1f11313641f80fbf03890b9d37",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/7a894a4f8befb5de0fe95979183b1cbb03f4ef13"
        },
        "date": 1619185012673,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 1.4087671146420866,
            "unit": "iter/sec",
            "range": "stddev: 0.07496746486130741",
            "extra": "mean: 709.8405333333334 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.19087595264863766,
            "unit": "iter/sec",
            "range": "stddev: 2.205762170911617",
            "extra": "mean: 5.239004631666666 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 5.608891355172454,
            "unit": "iter/sec",
            "range": "stddev: 0.007474632918793218",
            "extra": "mean: 178.28835266666587 msec\nrounds: 6"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 10.00156939070453,
            "unit": "iter/sec",
            "range": "stddev: 0.0026151869990055114",
            "extra": "mean: 99.9843085555554 msec\nrounds: 9"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 2.188666605581953,
            "unit": "iter/sec",
            "range": "stddev: 0.010835003278742433",
            "extra": "mean: 456.89919033333365 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2271625.7689415426,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011547104356649543",
            "extra": "mean: 440.213354537683 nsec\nrounds: 151424"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3874823.9785803133,
            "unit": "iter/sec",
            "range": "stddev: 0.000003633259470869228",
            "extra": "mean: 258.0762392118884 nsec\nrounds: 199522"
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
          "id": "a2561a40cf2e9a4d58325387f913ccf08111f5fd",
          "message": "Merge pull request #104 from giovannipizzi/master_in_dev\n\nMerge v0.5.0 in develop",
          "timestamp": "2021-04-23T16:22:25+02:00",
          "tree_id": "4beb6bcd4bfe656b36e0d022e991951f256753fd",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/a2561a40cf2e9a4d58325387f913ccf08111f5fd"
        },
        "date": 1619187856161,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 1.5078080755570913,
            "unit": "iter/sec",
            "range": "stddev: 0.020469492215575365",
            "extra": "mean: 663.2143813333332 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 1.242527638621194,
            "unit": "iter/sec",
            "range": "stddev: 0.0794438716760416",
            "extra": "mean: 804.8110713333333 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 6.213573022468953,
            "unit": "iter/sec",
            "range": "stddev: 0.007908860628052346",
            "extra": "mean: 160.93799757142818 msec\nrounds: 7"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 9.733500352023212,
            "unit": "iter/sec",
            "range": "stddev: 0.012209304011589574",
            "extra": "mean: 102.73796310000023 msec\nrounds: 10"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 2.0425982781522913,
            "unit": "iter/sec",
            "range": "stddev: 0.0422642467225076",
            "extra": "mean: 489.5725266666666 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2268670.3987707132,
            "unit": "iter/sec",
            "range": "stddev: 2.586221929023684e-7",
            "extra": "mean: 440.78681528257846 nsec\nrounds: 162840"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 4289949.006688217,
            "unit": "iter/sec",
            "range": "stddev: 1.6343968561679802e-7",
            "extra": "mean: 233.10300389139823 nsec\nrounds: 199641"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "chrisj_sewell@hotmail.com",
            "name": "Chris Sewell",
            "username": "chrisjsewell"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "2cb284157df3cc9bc5a3ae92da6aebbacbda5623",
          "message": "🔧 MAINTAIN: Improve repo configuration (#112)\n\n- Move config to `setup.cfg` and `pyproject.toml`\r\n- Add `Manifest.in`, `tox.ini`\r\n- Replace `requirements.txt`/`dev-requirements.txt with `requirements.lock`\r\n- Move from yapf to black code formatting\r\n- Add more pre-commit hooks\r\n- Update pylint version and fix new failures\r\n- Drop python 3.6",
          "timestamp": "2021-08-30T16:07:48+02:00",
          "tree_id": "3e95e7e154b9b51de8f0ec0458d0ae1a6a26ba51",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/2cb284157df3cc9bc5a3ae92da6aebbacbda5623"
        },
        "date": 1630332587949,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 1.6039146003711988,
            "unit": "iter/sec",
            "range": "stddev: 0.008949926538299261",
            "extra": "mean: 623.4745913333334 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.46916064825171605,
            "unit": "iter/sec",
            "range": "stddev: 0.3550621606602441",
            "extra": "mean: 2.1314660633333333 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 6.409446759785378,
            "unit": "iter/sec",
            "range": "stddev: 0.0021586996127789145",
            "extra": "mean: 156.01970614285676 msec\nrounds: 7"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 11.117778529366806,
            "unit": "iter/sec",
            "range": "stddev: 0.0014042056749261134",
            "extra": "mean: 89.94602629999982 msec\nrounds: 10"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 2.479738790002749,
            "unit": "iter/sec",
            "range": "stddev: 0.003078272066467048",
            "extra": "mean: 403.26828133333 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 4294439.06776578,
            "unit": "iter/sec",
            "range": "stddev: 1.0978949843148724e-7",
            "extra": "mean: 232.85928248603832 nsec\nrounds: 191829"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 4263174.368051062,
            "unit": "iter/sec",
            "range": "stddev: 5.8343516934378344e-8",
            "extra": "mean: 234.5669948417554 nsec\nrounds: 190549"
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
          "id": "4d493174c1354603b21ed8d623f487660a050d24",
          "message": "Merge pull request #50 from giovannipizzi/better_debugging_concurrency\n\nSlightly more detailed debugging in case of problems with the concurrent tests",
          "timestamp": "2020-07-10T19:48:46+02:00",
          "tree_id": "36d0accdc00b7f7b1eb3e3b01401bfb7c227471f",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/4d493174c1354603b21ed8d623f487660a050d24"
        },
        "date": 1594403532655,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.22193811348919368,
            "unit": "iter/sec",
            "range": "stddev: 0.07340034947616736",
            "extra": "mean: 4.505760566666665 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.7750278793175984,
            "unit": "iter/sec",
            "range": "stddev: 0.006867972564957476",
            "extra": "mean: 360.35673999999887 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 0.9529941965830053,
            "unit": "iter/sec",
            "range": "stddev: 0.018008616832593055",
            "extra": "mean: 1.0493243333333357 sec\nrounds: 3"
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
          "id": "91ea646558962736530f212654fd83927f650c87",
          "message": "Merge pull request #53 from giovannipizzi/further_multiprocess_basic_tests\n\nFurther multiprocess basic tests",
          "timestamp": "2020-07-12T09:02:23+02:00",
          "tree_id": "e0d576ca01ebee5c8b61e515d997482d318529fb",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/91ea646558962736530f212654fd83927f650c87"
        },
        "date": 1594537520016,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.2179552224218151,
            "unit": "iter/sec",
            "range": "stddev: 0.1935370516350103",
            "extra": "mean: 4.588098366666667 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.435047304689967,
            "unit": "iter/sec",
            "range": "stddev: 0.006447934661812005",
            "extra": "mean: 410.6696400000004 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 0.9348948861841893,
            "unit": "iter/sec",
            "range": "stddev: 0.035769179036896616",
            "extra": "mean: 1.069638966666659 sec\nrounds: 3"
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
          "id": "6fae5f875c73bf4b5f2eb69e28467efa731c2aa3",
          "message": "Merge pull request #58 from sphuber/feature/057/packed-object-reader-mode\n\nAdd the `mode` property to the `PackedObjectReader`",
          "timestamp": "2020-07-12T21:53:29+02:00",
          "tree_id": "f32c32f225344579ea82d4787e2e232ead7dfa2c",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/6fae5f875c73bf4b5f2eb69e28467efa731c2aa3"
        },
        "date": 1594583935626,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.22814713573819176,
            "unit": "iter/sec",
            "range": "stddev: 0.03360645577628413",
            "extra": "mean: 4.383136333333333 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.763966849644962,
            "unit": "iter/sec",
            "range": "stddev: 0.014914493080658",
            "extra": "mean: 361.7988399999995 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 0.8973516460869042,
            "unit": "iter/sec",
            "range": "stddev: 0.044588873551189845",
            "extra": "mean: 1.1143903333333327 sec\nrounds: 3"
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
          "id": "6025360bb8a030b1103e7d40da4f7bde7938dd4c",
          "message": "Merge pull request #55 from giovannipizzi/fix_open_files\n\nFix lost open files and implement FULLSYNC for pack files on Mac OS",
          "timestamp": "2020-07-12T22:29:09+02:00",
          "tree_id": "571d031d2c95a14eb9fc9289031f93a62b9693f8",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/6025360bb8a030b1103e7d40da4f7bde7938dd4c"
        },
        "date": 1594585990191,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.24840519517606055,
            "unit": "iter/sec",
            "range": "stddev: 0.06309042944512261",
            "extra": "mean: 4.0256807 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.1330237055825699,
            "unit": "iter/sec",
            "range": "stddev: 0.06914862014328126",
            "extra": "mean: 7.5174571000000014 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.5293541324289897,
            "unit": "iter/sec",
            "range": "stddev: 0.01084899018701773",
            "extra": "mean: 283.33796000000007 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.0594159298723203,
            "unit": "iter/sec",
            "range": "stddev: 0.006010708672305684",
            "extra": "mean: 943.9163333333292 msec\nrounds: 3"
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
          "id": "09cc7a9539aa68f3417bf4ef2e80b520a1b4ba41",
          "message": "Merge pull request #60 from giovannipizzi/fix_56_seek\n\nAdded seek method to both the PackedObjectReader and the StreamDecompresser",
          "timestamp": "2020-07-13T01:27:47+02:00",
          "tree_id": "cf2de3df905a56e5ca39dbd1155b206012989f9f",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/09cc7a9539aa68f3417bf4ef2e80b520a1b4ba41"
        },
        "date": 1594596910198,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.2764139105927044,
            "unit": "iter/sec",
            "range": "stddev: 0.03513732425702619",
            "extra": "mean: 3.6177629333333328 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.14567610167721848,
            "unit": "iter/sec",
            "range": "stddev: 0.5683789936726585",
            "extra": "mean: 6.864543933333334 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.330319394281483,
            "unit": "iter/sec",
            "range": "stddev: 0.005715752986264874",
            "extra": "mean: 300.27150000000233 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.2257619867673333,
            "unit": "iter/sec",
            "range": "stddev: 0.017234574850089626",
            "extra": "mean: 815.8190666666627 msec\nrounds: 3"
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
          "id": "df368df957ecb9cf2a4a308c0b2baccfa7669638",
          "message": "Merge pull request #61 from giovannipizzi/check_concurrency\n\nFix concurrency problems in Mac OS",
          "timestamp": "2020-07-13T10:14:15+02:00",
          "tree_id": "2483876c2ad6de311dce821cd69d08efc5662ed0",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/df368df957ecb9cf2a4a308c0b2baccfa7669638"
        },
        "date": 1594628258687,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.2143607512666952,
            "unit": "iter/sec",
            "range": "stddev: 0.05432047441591353",
            "extra": "mean: 4.6650331 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.18556104136534773,
            "unit": "iter/sec",
            "range": "stddev: 0.10860015857642057",
            "extra": "mean: 5.389062233333334 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.8420098853061146,
            "unit": "iter/sec",
            "range": "stddev: 0.013786052165613528",
            "extra": "mean: 351.8636600000036 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 0.9175084653918549,
            "unit": "iter/sec",
            "range": "stddev: 0.034969238413356654",
            "extra": "mean: 1.089908200000001 sec\nrounds: 3"
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
          "id": "cec284e3680abc6105e80d0098da030a6cc3509e",
          "message": "Merge pull request #62 from giovannipizzi/fix_58_performance_has\n\nAdding methods to just fetch metas without opening streams",
          "timestamp": "2020-07-13T20:34:37+02:00",
          "tree_id": "3318cf4caa826238d95afbbb139840cb292a6f0e",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/cec284e3680abc6105e80d0098da030a6cc3509e"
        },
        "date": 1594665499455,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.3151538183847542,
            "unit": "iter/sec",
            "range": "stddev: 0.024390539718779258",
            "extra": "mean: 3.1730537333333344 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.14557116825205396,
            "unit": "iter/sec",
            "range": "stddev: 0.2112290070891358",
            "extra": "mean: 6.869492166666666 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.7542086556133825,
            "unit": "iter/sec",
            "range": "stddev: 0.010274225468958958",
            "extra": "mean: 266.3677199999995 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.559570525468692,
            "unit": "iter/sec",
            "range": "stddev: 0.015076867289436302",
            "extra": "mean: 641.2021666666684 msec\nrounds: 3"
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
          "id": "dab40d1d73c8515a5900560c656d04bdbae5fdf0",
          "message": "Merge pull request #63 from giovannipizzi/fix_10_performance\n\nAdding performance tests for loose read",
          "timestamp": "2020-07-13T22:09:53+02:00",
          "tree_id": "da463ed266c11b51b86ed097afedaa7a018bec82",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/dab40d1d73c8515a5900560c656d04bdbae5fdf0"
        },
        "date": 1594671241093,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.2877065108184792,
            "unit": "iter/sec",
            "range": "stddev: 0.052508391337225555",
            "extra": "mean: 3.475764233333334 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.15071001295623845,
            "unit": "iter/sec",
            "range": "stddev: 0.03305972559656238",
            "extra": "mean: 6.6352591999999975 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.3235700140600293,
            "unit": "iter/sec",
            "range": "stddev: 0.01378793649416427",
            "extra": "mean: 300.8812800000001 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 12.65114524492339,
            "unit": "iter/sec",
            "range": "stddev: 0.008319989570557927",
            "extra": "mean: 79.0442272727267 msec\nrounds: 11"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.424740775539588,
            "unit": "iter/sec",
            "range": "stddev: 0.051104846568333154",
            "extra": "mean: 701.8820666666699 msec\nrounds: 3"
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
          "id": "801df0c0b90f09e910c7f822ae87e548446bce7a",
          "message": "Merge pull request #66 from giovannipizzi/fix_65_list_all\n\nAdding a function to list all objects",
          "timestamp": "2020-07-14T00:46:13+02:00",
          "tree_id": "0587cf74d5f99911d7ac55811765a11dfa23aeab",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/801df0c0b90f09e910c7f822ae87e548446bce7a"
        },
        "date": 1594680587709,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.2925971601787554,
            "unit": "iter/sec",
            "range": "stddev: 0.0683886346139719",
            "extra": "mean: 3.417668166666666 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.1606542337354805,
            "unit": "iter/sec",
            "range": "stddev: 0.03049931292362869",
            "extra": "mean: 6.224548066666667 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.607657700819507,
            "unit": "iter/sec",
            "range": "stddev: 0.00899931198720287",
            "extra": "mean: 277.1881600000029 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 12.125694953892173,
            "unit": "iter/sec",
            "range": "stddev: 0.005430917298002992",
            "extra": "mean: 82.46949999999913 msec\nrounds: 10"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.4629776676946602,
            "unit": "iter/sec",
            "range": "stddev: 0.01431458986640771",
            "extra": "mean: 683.5374333333372 msec\nrounds: 3"
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
          "id": "5a256e013b16d6a7044f7584114e7261dba5d1f6",
          "message": "Merge pull request #71 from giovannipizzi/fix_69_efficient_list_all\n\nImprove performance of list_all_objects for packed objects",
          "timestamp": "2020-07-16T14:37:20+02:00",
          "tree_id": "4038bcb9cafb4dbb2cf25ee20ef0750f1bbf4912",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/5a256e013b16d6a7044f7584114e7261dba5d1f6"
        },
        "date": 1594903482045,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.23650757401315325,
            "unit": "iter/sec",
            "range": "stddev: 0.1539634472038429",
            "extra": "mean: 4.2281944 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.12422955058506593,
            "unit": "iter/sec",
            "range": "stddev: 0.2611997400619716",
            "extra": "mean: 8.049614566666664 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.0359281451669022,
            "unit": "iter/sec",
            "range": "stddev: 0.018146148049600387",
            "extra": "mean: 329.388560000001 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 8.530176940393774,
            "unit": "iter/sec",
            "range": "stddev: 0.007900130212115991",
            "extra": "mean: 117.23086250000314 msec\nrounds: 8"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.2035996777722944,
            "unit": "iter/sec",
            "range": "stddev: 0.009726701900103309",
            "extra": "mean: 830.8410333333333 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 3174785.285921935,
            "unit": "iter/sec",
            "range": "stddev: 6.039175731090999e-7",
            "extra": "mean: 314.9819310408545 nsec\nrounds: 175439"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3257555.071848392,
            "unit": "iter/sec",
            "range": "stddev: 2.994646668671088e-7",
            "extra": "mean: 306.9786935121294 nsec\nrounds: 158731"
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
          "id": "32baa140c5860150a0891937b0e4a69aa88b05e7",
          "message": "Do not fail on benchmark test alert",
          "timestamp": "2020-07-16T23:04:29+02:00",
          "tree_id": "f3721560975ad665334615ba90b19359aacbc87d",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/32baa140c5860150a0891937b0e4a69aa88b05e7"
        },
        "date": 1594933827241,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.22533643179940516,
            "unit": "iter/sec",
            "range": "stddev: 0.0551085268916699",
            "extra": "mean: 4.4378088 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.1789242907032572,
            "unit": "iter/sec",
            "range": "stddev: 0.16703559035176724",
            "extra": "mean: 5.588956066666669 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.9684706854614333,
            "unit": "iter/sec",
            "range": "stddev: 0.014869774987703257",
            "extra": "mean: 336.87380000000076 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 8.811530504472318,
            "unit": "iter/sec",
            "range": "stddev: 0.004683711828676767",
            "extra": "mean: 113.48766249999898 msec\nrounds: 8"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.0946020793061135,
            "unit": "iter/sec",
            "range": "stddev: 0.026272675099235563",
            "extra": "mean: 913.573999999997 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 3051224.90517486,
            "unit": "iter/sec",
            "range": "stddev: 5.596392845415392e-7",
            "extra": "mean: 327.7372304820138 nsec\nrounds: 156251"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3058062.5571164875,
            "unit": "iter/sec",
            "range": "stddev: 4.5872185244643646e-7",
            "extra": "mean: 327.0044288899282 nsec\nrounds: 175439"
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
          "id": "2815887c622e923ab8d6eac4370488df9be8166a",
          "message": "Merge pull request #74 from giovannipizzi/fix_hash_computation\n\nFix to the hash calculation when writing to compressed packs.",
          "timestamp": "2020-07-17T15:50:51+02:00",
          "tree_id": "84fff9b9c58f7df075b9377c35ae3974517e74ea",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/2815887c622e923ab8d6eac4370488df9be8166a"
        },
        "date": 1594994203616,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.27121225150358264,
            "unit": "iter/sec",
            "range": "stddev: 0.04832099673809808",
            "extra": "mean: 3.6871490666666666 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.15420144187600232,
            "unit": "iter/sec",
            "range": "stddev: 0.45190855995683693",
            "extra": "mean: 6.48502366666667 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.3980531058613477,
            "unit": "iter/sec",
            "range": "stddev: 0.013827746879478159",
            "extra": "mean: 294.2861599999972 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 12.078764414872749,
            "unit": "iter/sec",
            "range": "stddev: 0.006469250795760168",
            "extra": "mean: 82.78992500000133 msec\nrounds: 12"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.282923176379237,
            "unit": "iter/sec",
            "range": "stddev: 0.004742973732798335",
            "extra": "mean: 779.4698999999952 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 3299688.437684369,
            "unit": "iter/sec",
            "range": "stddev: 7.726345146359184e-7",
            "extra": "mean: 303.05891567808357 nsec\nrounds: 153847"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3383102.3277404504,
            "unit": "iter/sec",
            "range": "stddev: 2.1115328021021875e-7",
            "extra": "mean: 295.5866843873626 nsec\nrounds: 158731"
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
          "id": "fa85ce1b90b92989c15446fb1125e6c7840ad729",
          "message": "Merge pull request #77 from giovannipizzi/fix_37_concurrency_win\n\nFix concurrency problems on Windows",
          "timestamp": "2020-07-17T16:48:14+02:00",
          "tree_id": "45fabeaefc37015b298754e3beaf07326d2b02f2",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/fa85ce1b90b92989c15446fb1125e6c7840ad729"
        },
        "date": 1594997718877,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.25349135759239994,
            "unit": "iter/sec",
            "range": "stddev: 0.01975135043138482",
            "extra": "mean: 3.944907666666666 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.15126051818374536,
            "unit": "iter/sec",
            "range": "stddev: 0.25935645451079326",
            "extra": "mean: 6.6111105000000014 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.480344476143429,
            "unit": "iter/sec",
            "range": "stddev: 0.017798942334083377",
            "extra": "mean: 287.3278799999994 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 9.298467798475956,
            "unit": "iter/sec",
            "range": "stddev: 0.007157536465853204",
            "extra": "mean: 107.54460000000243 msec\nrounds: 8"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.2523288097825225,
            "unit": "iter/sec",
            "range": "stddev: 0.00399264637844847",
            "extra": "mean: 798.5123333333348 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 3310732.454781473,
            "unit": "iter/sec",
            "range": "stddev: 8.729310952352881e-7",
            "extra": "mean: 302.04796481071025 nsec\nrounds: 188680"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3230678.442494244,
            "unit": "iter/sec",
            "range": "stddev: 7.017822297166999e-7",
            "extra": "mean: 309.5325077378457 nsec\nrounds: 58140"
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
          "id": "6dea94015bf141e31781e4ea61f169d2b69e6b81",
          "message": "Merge pull request #75 from giovannipizzi/fix_64_export_to_container\n\nAdding a function to export directly a set of hash keys to a new container",
          "timestamp": "2020-07-17T17:16:12+02:00",
          "tree_id": "9d5cf808e9c4e748164afb805c1fb170f183c957",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/6dea94015bf141e31781e4ea61f169d2b69e6b81"
        },
        "date": 1594999336515,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.27824735367984954,
            "unit": "iter/sec",
            "range": "stddev: 0.05755828558394887",
            "extra": "mean: 3.593924566666667 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.16490464586738293,
            "unit": "iter/sec",
            "range": "stddev: 0.2185194851573727",
            "extra": "mean: 6.064110533333333 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 4.030881063533435,
            "unit": "iter/sec",
            "range": "stddev: 0.013215264747893479",
            "extra": "mean: 248.08472000000137 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 10.456143448993625,
            "unit": "iter/sec",
            "range": "stddev: 0.004884443205249964",
            "extra": "mean: 95.63755555555689 msec\nrounds: 9"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.357739945913072,
            "unit": "iter/sec",
            "range": "stddev: 0.006564129071195798",
            "extra": "mean: 736.5180666666665 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 3985254.5863233935,
            "unit": "iter/sec",
            "range": "stddev: 1.8402361111687316e-7",
            "extra": "mean: 250.92499822507173 nsec\nrounds: 196079"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 4070469.638424939,
            "unit": "iter/sec",
            "range": "stddev: 0.00000139729764297525",
            "extra": "mean: 245.67189755188338 nsec\nrounds: 196079"
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
          "id": "38bfa5ed21e99016756308569337be1cdeaeb311",
          "message": "Merge pull request #68 from sphuber/feature/067/packed-object-reader-seek-whence\n\nImplement `whence=1` for the `utils.PackedObjectReader.seek`",
          "timestamp": "2020-07-17T18:20:39+02:00",
          "tree_id": "57f4997cbdc791e0a32f9905fa065586842a7ad8",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/38bfa5ed21e99016756308569337be1cdeaeb311"
        },
        "date": 1595003273816,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.27035320294198356,
            "unit": "iter/sec",
            "range": "stddev: 0.02458889321482366",
            "extra": "mean: 3.6988649999999996 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.11327974826158727,
            "unit": "iter/sec",
            "range": "stddev: 0.6196784334064309",
            "extra": "mean: 8.827703233333333 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.2430164073929344,
            "unit": "iter/sec",
            "range": "stddev: 0.009846717065353486",
            "extra": "mean: 308.35489999999766 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 11.95029537545074,
            "unit": "iter/sec",
            "range": "stddev: 0.0031882838630742385",
            "extra": "mean: 83.67994000000039 msec\nrounds: 10"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.3373420309304045,
            "unit": "iter/sec",
            "range": "stddev: 0.01253124203752816",
            "extra": "mean: 747.7518666666659 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 3366413.32770417,
            "unit": "iter/sec",
            "range": "stddev: 2.2337903091145484e-7",
            "extra": "mean: 297.0520558989555 nsec\nrounds: 166667"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3323715.298983836,
            "unit": "iter/sec",
            "range": "stddev: 6.221999143679388e-7",
            "extra": "mean: 300.86812799700056 nsec\nrounds: 156250"
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
          "id": "dbefa5af8e4b59d8b7e35f67f4597025e7f2b60d",
          "message": "Avoid seeking back to zero for compressed streams when seeking forward\n\nFixes #81",
          "timestamp": "2020-07-17T18:31:03+02:00",
          "tree_id": "01ba21f85aaef7d3d3d31955b500af91455036bd",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/dbefa5af8e4b59d8b7e35f67f4597025e7f2b60d"
        },
        "date": 1595003862183,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.24675193640432735,
            "unit": "iter/sec",
            "range": "stddev: 0.010301920946599381",
            "extra": "mean: 4.0526531 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.14655887671649023,
            "unit": "iter/sec",
            "range": "stddev: 0.04931564490696668",
            "extra": "mean: 6.8231964000000005 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.2964789187865766,
            "unit": "iter/sec",
            "range": "stddev: 0.014811255540195816",
            "extra": "mean: 303.35397999999856 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 9.149680190084617,
            "unit": "iter/sec",
            "range": "stddev: 0.0041276459299075105",
            "extra": "mean: 109.29343749999987 msec\nrounds: 8"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.1606573375093296,
            "unit": "iter/sec",
            "range": "stddev: 0.020404550937060235",
            "extra": "mean: 861.5807333333313 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 3451658.328169231,
            "unit": "iter/sec",
            "range": "stddev: 2.0660264109258976e-7",
            "extra": "mean: 289.71581336398816 nsec\nrounds: 42736"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3399961.6465860917,
            "unit": "iter/sec",
            "range": "stddev: 4.7144450646644154e-7",
            "extra": "mean: 294.1209648657532 nsec\nrounds: 185186"
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
          "id": "ddc612b9ceaf7f67711f7079d0f584ead8147507",
          "message": "Merge pull request #84 from giovannipizzi/fix_13_validation\n\nImplement validation routine",
          "timestamp": "2020-07-19T23:21:12+02:00",
          "tree_id": "d7baf41d8de602432d63610a50939df2fde3d94c",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/ddc612b9ceaf7f67711f7079d0f584ead8147507"
        },
        "date": 1595194115918,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.2321869194480499,
            "unit": "iter/sec",
            "range": "stddev: 0.05066040939178553",
            "extra": "mean: 4.3068748333333335 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.13294468520406888,
            "unit": "iter/sec",
            "range": "stddev: 0.877942434225952",
            "extra": "mean: 7.521925366666665 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.885805335346148,
            "unit": "iter/sec",
            "range": "stddev: 0.010685990653753757",
            "extra": "mean: 346.52372000000184 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 8.453902717771333,
            "unit": "iter/sec",
            "range": "stddev: 0.007355660480967192",
            "extra": "mean: 118.2885624999983 msec\nrounds: 8"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.0353920470570446,
            "unit": "iter/sec",
            "range": "stddev: 0.01619214279344707",
            "extra": "mean: 965.8177333333384 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2920287.5964954454,
            "unit": "iter/sec",
            "range": "stddev: 9.147619440608881e-7",
            "extra": "mean: 342.4320266266912 nsec\nrounds: 153847"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2926321.7045649514,
            "unit": "iter/sec",
            "range": "stddev: 7.159989387236381e-7",
            "extra": "mean: 341.72592795962953 nsec\nrounds: 163935"
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
          "id": "89a6ea1a6c87895d4cbb0c1e2c869225c31fb707",
          "message": "Adding nodes on performance for validation",
          "timestamp": "2020-07-20T14:06:57+02:00",
          "tree_id": "a1c4c31f0e67410babd839471c3349dc89f24c78",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/89a6ea1a6c87895d4cbb0c1e2c869225c31fb707"
        },
        "date": 1595247215772,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.2430113421169729,
            "unit": "iter/sec",
            "range": "stddev: 0.04838780588974285",
            "extra": "mean: 4.115034266666666 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.15144460357065484,
            "unit": "iter/sec",
            "range": "stddev: 0.12611220552258304",
            "extra": "mean: 6.603074500000001 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.1791437993502507,
            "unit": "iter/sec",
            "range": "stddev: 0.01964324592563476",
            "extra": "mean: 314.5500999999996 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 8.912223069378445,
            "unit": "iter/sec",
            "range": "stddev: 0.004972688907856601",
            "extra": "mean: 112.20545000000115 msec\nrounds: 8"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.1559368434639892,
            "unit": "iter/sec",
            "range": "stddev: 0.00218719107608527",
            "extra": "mean: 865.0991666666717 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 3491768.5985262,
            "unit": "iter/sec",
            "range": "stddev: 7.717337179248842e-7",
            "extra": "mean: 286.38782089434216 nsec\nrounds: 185186"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3566420.566397539,
            "unit": "iter/sec",
            "range": "stddev: 8.574137179234145e-7",
            "extra": "mean: 280.3931789263142 nsec\nrounds: 188680"
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
          "id": "d41ef638da9ca6958401ce010332e42cf4f988e4",
          "message": "Merge pull request #87 from giovannipizzi/fix_5_delete\n\nImplement function `delete_objects` for object deletion",
          "timestamp": "2020-07-20T14:40:53+02:00",
          "tree_id": "909ea5614905a444fc80d603a21b439da060a5a4",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/d41ef638da9ca6958401ce010332e42cf4f988e4"
        },
        "date": 1595249213562,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.2541795096865397,
            "unit": "iter/sec",
            "range": "stddev: 0.0770196950404459",
            "extra": "mean: 3.9342274333333327 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.16921944159456973,
            "unit": "iter/sec",
            "range": "stddev: 0.08368936230396185",
            "extra": "mean: 5.909486466666665 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.057297484767473,
            "unit": "iter/sec",
            "range": "stddev: 0.008419230545185157",
            "extra": "mean: 327.0862600000001 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 8.858388473110631,
            "unit": "iter/sec",
            "range": "stddev: 0.004402470283506392",
            "extra": "mean: 112.88734999999939 msec\nrounds: 8"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.17093431893737,
            "unit": "iter/sec",
            "range": "stddev: 0.004479320870773085",
            "extra": "mean: 854.0188666666685 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 3507684.745768682,
            "unit": "iter/sec",
            "range": "stddev: 2.7701174928292844e-7",
            "extra": "mean: 285.0883338948699 nsec\nrounds: 172414"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3413328.498228248,
            "unit": "iter/sec",
            "range": "stddev: 3.533597910401256e-7",
            "extra": "mean: 292.9691650006931 nsec\nrounds: 156251"
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
          "id": "3f3cd07ea6627bbf6d0637e69e409ef4801b4f90",
          "message": "Adding nightly concurrency extensive tests\n\nThis runs only the main branch of the main fork, at 5AM UTC.\nTests are repeated 5 times to increase the change of seeing random errors.\n\nFixes #76",
          "timestamp": "2020-07-20T14:51:14+02:00",
          "tree_id": "01658224411ac3acb670ee1ef1e9d5081979f9ee",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/3f3cd07ea6627bbf6d0637e69e409ef4801b4f90"
        },
        "date": 1595249962430,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.26236016334473805,
            "unit": "iter/sec",
            "range": "stddev: 0.015214992708619021",
            "extra": "mean: 3.811554266666667 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.12245047998506495,
            "unit": "iter/sec",
            "range": "stddev: 2.1062737060495547",
            "extra": "mean: 8.166566600000001 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.1508809421991537,
            "unit": "iter/sec",
            "range": "stddev: 0.008894274578793231",
            "extra": "mean: 317.37155999999516 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 11.005342971731432,
            "unit": "iter/sec",
            "range": "stddev: 0.003602992885821137",
            "extra": "mean: 90.86495555555354 msec\nrounds: 9"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.288737848813014,
            "unit": "iter/sec",
            "range": "stddev: 0.016016180518770486",
            "extra": "mean: 775.9529999999965 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2005744.1118593512,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011899466121932702",
            "extra": "mean: 498.5680845763455 nsec\nrounds: 178572"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3284171.268013898,
            "unit": "iter/sec",
            "range": "stddev: 8.710337049285508e-7",
            "extra": "mean: 304.49081926352255 nsec\nrounds: 156251"
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
          "id": "5d977ad3ce8d4eba5ba70dfd0919282c2505e3b1",
          "message": "Merge pull request #88 from giovannipizzi/fix_78_loose_streamed\n\nAdding `add_streamed_object` function",
          "timestamp": "2020-07-20T15:47:49+02:00",
          "tree_id": "4864b702ab018ce6fa9ac195aca677f776b5bbff",
          "url": "https://github.com/giovannipizzi/disk-objectstore/commit/5d977ad3ce8d4eba5ba70dfd0919282c2505e3b1"
        },
        "date": 1595253394386,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.27257584445586647,
            "unit": "iter/sec",
            "range": "stddev: 0.010843486243978124",
            "extra": "mean: 3.668703666666666 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.06420825665529815,
            "unit": "iter/sec",
            "range": "stddev: 8.27453224706836",
            "extra": "mean: 15.574321000000003 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.078635366550364,
            "unit": "iter/sec",
            "range": "stddev: 0.008790803537955826",
            "extra": "mean: 324.8192399999965 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 11.005234639856775,
            "unit": "iter/sec",
            "range": "stddev: 0.003335631275673855",
            "extra": "mean: 90.8658499999973 msec\nrounds: 10"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.2887140438042526,
            "unit": "iter/sec",
            "range": "stddev: 0.0011969267577212762",
            "extra": "mean: 775.9673333333316 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 3237478.0073088994,
            "unit": "iter/sec",
            "range": "stddev: 3.3455117602453353e-7",
            "extra": "mean: 308.8824071521331 nsec\nrounds: 156251"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 1959702.6345570963,
            "unit": "iter/sec",
            "range": "stddev: 0.000001970804800381522",
            "extra": "mean: 510.2815000429928 nsec\nrounds: 200000"
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
          "id": "1589096795f049b538222474b724e0d1298a4b49",
          "message": "Complete move to aiidateam organisation\n\nFixes #80",
          "timestamp": "2020-07-20T17:02:04+02:00",
          "tree_id": "e54abe7df4b0f77aefb62e2a5ad6a6b7578e733a",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/1589096795f049b538222474b724e0d1298a4b49"
        },
        "date": 1595257749296,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.2629264687041867,
            "unit": "iter/sec",
            "range": "stddev: 0.017950015157190115",
            "extra": "mean: 3.8033447333333337 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.15033671063417445,
            "unit": "iter/sec",
            "range": "stddev: 0.6143148031497718",
            "extra": "mean: 6.651735266666667 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.988124833337356,
            "unit": "iter/sec",
            "range": "stddev: 0.024224097714220755",
            "extra": "mean: 334.6580399999979 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 11.171092984702819,
            "unit": "iter/sec",
            "range": "stddev: 0.0023490445254988686",
            "extra": "mean: 89.51675555555344 msec\nrounds: 9"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.283834385364275,
            "unit": "iter/sec",
            "range": "stddev: 0.019267300657159973",
            "extra": "mean: 778.9166666666745 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 3214505.1981661976,
            "unit": "iter/sec",
            "range": "stddev: 2.973755896738437e-7",
            "extra": "mean: 311.08986868962256 nsec\nrounds: 147059"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3191673.961511389,
            "unit": "iter/sec",
            "range": "stddev: 2.6017325955302145e-7",
            "extra": "mean: 313.31521078240127 nsec\nrounds: 156251"
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
          "id": "11cc7cbf88b964e48ac44f5de59ef09bc6bdb745",
          "message": "Adding simple changelog",
          "timestamp": "2020-07-20T17:41:58+02:00",
          "tree_id": "c53c9f1eed85787028f0bcbc6f537bb2915cc518",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/11cc7cbf88b964e48ac44f5de59ef09bc6bdb745"
        },
        "date": 1595260120398,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.2694764775375052,
            "unit": "iter/sec",
            "range": "stddev: 0.016824151694018217",
            "extra": "mean: 3.7108990333333343 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.1541563733886882,
            "unit": "iter/sec",
            "range": "stddev: 0.21026475008372209",
            "extra": "mean: 6.4869196 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.0172099847202345,
            "unit": "iter/sec",
            "range": "stddev: 0.009271591526647735",
            "extra": "mean: 331.43202000000116 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 11.050991262865336,
            "unit": "iter/sec",
            "range": "stddev: 0.00489174989385169",
            "extra": "mean: 90.4896199999996 msec\nrounds: 10"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.2873284484654175,
            "unit": "iter/sec",
            "range": "stddev: 0.015334894740540759",
            "extra": "mean: 776.8025333333289 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1975614.4656019493,
            "unit": "iter/sec",
            "range": "stddev: 0.000002232566830587144",
            "extra": "mean: 506.17163288248673 nsec\nrounds: 185186"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3221907.942839907,
            "unit": "iter/sec",
            "range": "stddev: 1.8639822753570729e-7",
            "extra": "mean: 310.37510001561185 nsec\nrounds: 158731"
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
          "id": "1e0ba2e2cec56c81f871ff8d72c15d7688ee8f0a",
          "message": "Change the default value of `compress` for export\n\nFor some reason it was True, but this is unexpected.\nSetting back to False.",
          "timestamp": "2020-07-20T17:51:03+02:00",
          "tree_id": "454bf54a8a996bc894244547a4ebd6dbfa0a7bdb",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/1e0ba2e2cec56c81f871ff8d72c15d7688ee8f0a"
        },
        "date": 1595260707288,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.2275064470587379,
            "unit": "iter/sec",
            "range": "stddev: 0.06963995566270392",
            "extra": "mean: 4.395479833333333 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.17497474458280374,
            "unit": "iter/sec",
            "range": "stddev: 0.24647119155676156",
            "extra": "mean: 5.7151105000000015 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.8868495285688045,
            "unit": "iter/sec",
            "range": "stddev: 0.013223110291155015",
            "extra": "mean: 346.3983800000008 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 8.268639839753623,
            "unit": "iter/sec",
            "range": "stddev: 0.0060562819255827365",
            "extra": "mean: 120.938875000002 msec\nrounds: 8"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.09223979644146,
            "unit": "iter/sec",
            "range": "stddev: 0.01340348925366441",
            "extra": "mean: 915.5498666666612 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1850549.8108013223,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014308587590534244",
            "extra": "mean: 540.3799423085951 nsec\nrounds: 185186"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3276520.7355289217,
            "unit": "iter/sec",
            "range": "stddev: 8.585257540847171e-7",
            "extra": "mean: 305.20179199727863 nsec\nrounds: 156250"
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
          "id": "9dd029d81a791f0fa3324209fa7edfd015796aa8",
          "message": "Removing the 'OS-independent' flag\n\nThis is not really true, it actually is OS dependent,\nand I tested the three most common ones",
          "timestamp": "2020-07-20T18:33:16+02:00",
          "tree_id": "da603cd023341129a9ef4d74d860764b02631c3f",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/9dd029d81a791f0fa3324209fa7edfd015796aa8"
        },
        "date": 1595263264865,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.21699777573663234,
            "unit": "iter/sec",
            "range": "stddev: 0.46555264066412905",
            "extra": "mean: 4.6083421666666675 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.13108908986273782,
            "unit": "iter/sec",
            "range": "stddev: 1.4694158377960351",
            "extra": "mean: 7.628399899999998 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.1080958437298984,
            "unit": "iter/sec",
            "range": "stddev: 0.00901436713446768",
            "extra": "mean: 321.7404000000016 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 8.540011394510248,
            "unit": "iter/sec",
            "range": "stddev: 0.004897669049639919",
            "extra": "mean: 117.09586249999937 msec\nrounds: 8"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.093435802361177,
            "unit": "iter/sec",
            "range": "stddev: 0.02036881786316669",
            "extra": "mean: 914.5484333333419 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 3244728.4788469253,
            "unit": "iter/sec",
            "range": "stddev: 6.311317304848863e-7",
            "extra": "mean: 308.19219744242264 nsec\nrounds: 153847"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3504962.483172947,
            "unit": "iter/sec",
            "range": "stddev: 2.924390807867104e-7",
            "extra": "mean: 285.3097586067027 nsec\nrounds: 181819"
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
          "id": "51e6a578fc55c3c0eca18bb4351cb5ae1dcdb00f",
          "message": "Explicitly specifying the codecov token",
          "timestamp": "2020-07-20T18:59:40+02:00",
          "tree_id": "b5c97bfa36b46639cdf390220798c072fbc6826a",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/51e6a578fc55c3c0eca18bb4351cb5ae1dcdb00f"
        },
        "date": 1595264818279,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.22617482498233932,
            "unit": "iter/sec",
            "range": "stddev: 0.02143558583858539",
            "extra": "mean: 4.421358566666667 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.0827656878519616,
            "unit": "iter/sec",
            "range": "stddev: 7.892825477577552",
            "extra": "mean: 12.082301566666667 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.947732400843747,
            "unit": "iter/sec",
            "range": "stddev: 0.016473669968685618",
            "extra": "mean: 339.24381999999866 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 8.54791173981969,
            "unit": "iter/sec",
            "range": "stddev: 0.001988129635715914",
            "extra": "mean: 116.98763749999763 msec\nrounds: 8"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.0781861028280428,
            "unit": "iter/sec",
            "range": "stddev: 0.005320569670943392",
            "extra": "mean: 927.4836666666696 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 3038307.70932304,
            "unit": "iter/sec",
            "range": "stddev: 2.4671705676380486e-7",
            "extra": "mean: 329.1305870474523 nsec\nrounds: 147059"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3011642.766221027,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011061345782231247",
            "extra": "mean: 332.0446937520855 nsec\nrounds: 153847"
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
          "id": "48fe289e87e457a1390b6d3dd6942d0b16064a32",
          "message": "Moving the env to the right place",
          "timestamp": "2020-07-20T19:06:51+02:00",
          "tree_id": "a629875f497fff991502bc56fb3979d157cf13b4",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/48fe289e87e457a1390b6d3dd6942d0b16064a32"
        },
        "date": 1595265267689,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.27113375065878725,
            "unit": "iter/sec",
            "range": "stddev: 0.0267530111503356",
            "extra": "mean: 3.6882166 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.11084531185351205,
            "unit": "iter/sec",
            "range": "stddev: 0.22244694916663493",
            "extra": "mean: 9.021581366666664 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.119239738964527,
            "unit": "iter/sec",
            "range": "stddev: 0.012460276953507314",
            "extra": "mean: 320.59094000000243 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 11.516521089309117,
            "unit": "iter/sec",
            "range": "stddev: 0.003319342350817973",
            "extra": "mean: 86.83177777777946 msec\nrounds: 9"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.3037312745620195,
            "unit": "iter/sec",
            "range": "stddev: 0.008680356380540264",
            "extra": "mean: 767.029233333337 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 3185321.569969749,
            "unit": "iter/sec",
            "range": "stddev: 7.979842041227921e-7",
            "extra": "mean: 313.94004593698145 nsec\nrounds: 151516"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3050371.6178298513,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014562039908364605",
            "extra": "mean: 327.8289091580143 nsec\nrounds: 151516"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gio.piz@gmail.com",
            "name": "Giovanni Pizzi",
            "username": "giovannipizzi"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "9aa52ca307119522cbcb110a505b77c6b7562513",
          "message": "Merge pull request #91 from giovannipizzi/test-codecov\n\nTesting Codecov after moving the repo",
          "timestamp": "2020-07-20T19:40:16+02:00",
          "tree_id": "da603cd023341129a9ef4d74d860764b02631c3f",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/9aa52ca307119522cbcb110a505b77c6b7562513"
        },
        "date": 1595267221111,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.28324662225806535,
            "unit": "iter/sec",
            "range": "stddev: 0.016253309212691098",
            "extra": "mean: 3.5304922333333324 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.10892668804723271,
            "unit": "iter/sec",
            "range": "stddev: 0.2473009742963626",
            "extra": "mean: 9.1804866 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.2619952372260523,
            "unit": "iter/sec",
            "range": "stddev: 0.008851564401450983",
            "extra": "mean: 306.5608399999945 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 11.89545229721349,
            "unit": "iter/sec",
            "range": "stddev: 0.003851142659061087",
            "extra": "mean: 84.06574000000404 msec\nrounds: 10"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.34279574639904,
            "unit": "iter/sec",
            "range": "stddev: 0.011365657899121707",
            "extra": "mean: 744.7149000000101 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 3230558.57673033,
            "unit": "iter/sec",
            "range": "stddev: 6.948993874739497e-7",
            "extra": "mean: 309.54399254745016 nsec\nrounds: 147059"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2986697.023272517,
            "unit": "iter/sec",
            "range": "stddev: 0.000004162817008072879",
            "extra": "mean: 334.81802546672736 nsec\nrounds: 158731"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gio.piz@gmail.com",
            "name": "Giovanni Pizzi",
            "username": "giovannipizzi"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": false,
          "id": "c718ffdec3881653acb82beaeed69fadf3cd9e3d",
          "message": "Merge pull request #90 from aiidateam/develop\n\nRelease of version 0.4.0",
          "timestamp": "2020-07-20T19:46:14+02:00",
          "tree_id": "da603cd023341129a9ef4d74d860764b02631c3f",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/c718ffdec3881653acb82beaeed69fadf3cd9e3d"
        },
        "date": 1595267661335,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.2866759689196235,
            "unit": "iter/sec",
            "range": "stddev: 0.0297901905418546",
            "extra": "mean: 3.4882589 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.15622372756281633,
            "unit": "iter/sec",
            "range": "stddev: 0.11093508379755729",
            "extra": "mean: 6.401076299999997 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 3.3663745237085143,
            "unit": "iter/sec",
            "range": "stddev: 0.015179690088140144",
            "extra": "mean: 297.0554799999988 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 11.808685130464019,
            "unit": "iter/sec",
            "range": "stddev: 0.0049940728440355355",
            "extra": "mean: 84.6834333333355 msec\nrounds: 12"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.3298744775809734,
            "unit": "iter/sec",
            "range": "stddev: 0.015599704359487706",
            "extra": "mean: 751.9506666666681 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 3306579.140169693,
            "unit": "iter/sec",
            "range": "stddev: 6.882692770805267e-7",
            "extra": "mean: 302.42736000206605 nsec\nrounds: 156250"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3364441.444432534,
            "unit": "iter/sec",
            "range": "stddev: 6.91872185919897e-7",
            "extra": "mean: 297.22615670848666 nsec\nrounds: 163935"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gio.piz@gmail.com",
            "name": "Giovanni Pizzi",
            "username": "giovannipizzi"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "e7e3627a67e8de2030b231927a127a9fb06ae474",
          "message": "Merge pull request #95 from giovannipizzi/fix_missing_optional_deps\n\nAdding missing optional dev dependencies",
          "timestamp": "2020-08-26T23:34:55+02:00",
          "tree_id": "397da3027d0c56b27a27da2ce3509320aadc032e",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/e7e3627a67e8de2030b231927a127a9fb06ae474"
        },
        "date": 1598478087395,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.22952341650685584,
            "unit": "iter/sec",
            "range": "stddev: 0.029430953074329143",
            "extra": "mean: 4.356853933333334 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.13826753443309825,
            "unit": "iter/sec",
            "range": "stddev: 0.1946169942027011",
            "extra": "mean: 7.232355766666667 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 2.9295310676183965,
            "unit": "iter/sec",
            "range": "stddev: 0.0201026605664022",
            "extra": "mean: 341.35155999999824 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 8.710808981541097,
            "unit": "iter/sec",
            "range": "stddev: 0.003914249332883107",
            "extra": "mean: 114.79989999999773 msec\nrounds: 8"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.1270875351782779,
            "unit": "iter/sec",
            "range": "stddev: 0.012331810091923882",
            "extra": "mean: 887.2425333333354 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 3009310.5063548596,
            "unit": "iter/sec",
            "range": "stddev: 4.3523176534932423e-7",
            "extra": "mean: 332.3020332689822 nsec\nrounds: 156251"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3006159.7936800066,
            "unit": "iter/sec",
            "range": "stddev: 3.4026649937399424e-7",
            "extra": "mean: 332.6503142320557 nsec\nrounds: 149254"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "chrisj_sewell@hotmail.com",
            "name": "Chris Sewell",
            "username": "chrisjsewell"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "64326c7e9778b6af1cc142a1f48a526a5bf7ee2e",
          "message": "🔀👌 Efficiency improvements  (#96)\n\nThis merge collects a number of important efficiency improvements, and a few features that were tightly bound to these efficiency changes, so they are shipped together.\r\n\r\nIn particular:\r\n\r\n- objects are now sorted and returned in the order in which they are on disk, with an important performance benefit. Fixes #92 \r\n- When there are many objects to list (currently set to 9500 objects, 10x the ones we could fit in a single IN SQL statement), performing many queries is slow, so we just resort to listing all objects and doing an efficient intersection (if the hash keys are sorted, both iterators can be looped over only once - fixes #93)\r\n- Since VACUUMing the DB is very important for efficiency, when the DB does not fit fully in the disk cache, `clean_storage` now provides an option to VACUUM the DB. VACUUM is also called after repacking. Fixes #94 \r\n- We implement now a function to perform a full repack of the repository (fixes #12). This is important and needed to reclaim space after deleting an object\r\n- For efficiency, we have moved the logic from an `export` function (still existing but deprecated) to a `import_objects` function\r\n- Still for efficiency, now functions like `pack_all_loose` and `import_objects` provide an option to perform a fsync to disk or not (see also #54 - there are still however calls that always use - or don't use - fsync and full_fsync on Mac). Also, `add_objects_to_pack` allows now to choose if you want to commit the changes to the SQLite DB, or not (delegating the responsibility to the caller, but this is important e.g. in `import_objects`: calling `commit` only once at the very end gives a factor of 2 speedup for very big repos).\r\n- A number of functions, including (but not exclusively) `import_objects` provide a callback to e.g. show a progress bar.\r\n- a `CallbackStreamWrapper` has been implemented, allowing to provide a callback (e.g. for a progress bar) when streaming a big file.\r\n- a new hash algorithm is now supported (`sha1`) in addition to the default `sha256` (fixes #82). This is faster even if a bit less robust. This was also needed to test completely some feature in `import_objects`, where the logic is optimised if both containers use the same algorithm. By default is still better to use everywhere sha256, also because then all export files that will be generated will use this algorithm and importing will be more efficient.\r\n- tests have been added for all new functionality, achieving again 100% coverage\r\n\r\nAs a reference, with these changes, exporting the full large SDB database (6.8M nodes) takes ~ 50 minutes:\r\n```\r\n6714808it [00:24, 274813.02it/s]\r\nAll hashkeys listed in 24.444787740707397s.\r\nListing objects: 100%|████████| 6714808/6714808 [00:06<00:00, 978896.65it/s]\r\nCopy objects: 100%|███████████| 6714808/6714808 [48:15<00:00, 2319.08it/s]\r\nFinal flush: 100%|████████████| 63236/63236 [00:07<00:00, 8582.35it/s]\r\nEverything re-exported in 2960.980943918228s.\r\n```\r\n\r\nThis can be compared to:\r\n\r\n- ~10 minutes to copy the whole 90GB, or ~15 minutes to read all and validate the packs. We will never be able to be faster than just copying the pack files, and we are only 3x slower.\r\n- ~2 days to just list all files in the old legacy AiiDA repo (or all objects if they are loose), and this does not take into account the time to rewrite everything, probably comparable. So we are almost 2 orders of magnitude faster than before.",
          "timestamp": "2020-10-02T05:02:23+01:00",
          "tree_id": "a1e5eacb37c751b57ede7818ed3ea30ccd868aa0",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/64326c7e9778b6af1cc142a1f48a526a5bf7ee2e"
        },
        "date": 1601611679662,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 1.3490521289931268,
            "unit": "iter/sec",
            "range": "stddev: 0.05475541885083089",
            "extra": "mean: 741.2611999999999 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.11850782999008924,
            "unit": "iter/sec",
            "range": "stddev: 0.7265856449270872",
            "extra": "mean: 8.438260999999995 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 8.310240387207243,
            "unit": "iter/sec",
            "range": "stddev: 0.008169291224180832",
            "extra": "mean: 120.33346250000143 msec\nrounds: 8"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 13.709983984245751,
            "unit": "iter/sec",
            "range": "stddev: 0.005071823164774853",
            "extra": "mean: 72.93954545454669 msec\nrounds: 11"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 2.352573990412502,
            "unit": "iter/sec",
            "range": "stddev: 0.014945327397664207",
            "extra": "mean: 425.0663333333288 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 3685640.4593223464,
            "unit": "iter/sec",
            "range": "stddev: 1.4006334671080455e-7",
            "extra": "mean: 271.3232641755691 nsec\nrounds: 185186"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3571243.358787849,
            "unit": "iter/sec",
            "range": "stddev: 1.422503370532878e-7",
            "extra": "mean: 280.01452142413143 nsec\nrounds: 158731"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gio.piz@gmail.com",
            "name": "Giovanni Pizzi",
            "username": "giovannipizzi"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "1d7c389c353185c1923c9addb1b107c283d5f561",
          "message": "✨ Add the concept of a (unique) container ID (#97)\n\nAllows for the association of a container with an existing DB, or to uniquely refer to it.\r\n\r\n🐛 This also fixes a bug, whereby config values were cached, but the cache was not cleared when re-initialising the container.\r\nTo reduce the risk of such a problem, now only the whole configuration dictionary is cached, rather than each single config value.",
          "timestamp": "2020-10-02T05:26:39+01:00",
          "tree_id": "cf46e923be5370049e00e368fe2b9cf6f18ef6d3",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/1d7c389c353185c1923c9addb1b107c283d5f561"
        },
        "date": 1601613265915,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.15813210478322423,
            "unit": "iter/sec",
            "range": "stddev: 0.05826465848362362",
            "extra": "mean: 6.3238265333333326 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.142047397608578,
            "unit": "iter/sec",
            "range": "stddev: 0.00874524408979022",
            "extra": "mean: 7.0399037000000035 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 8.08036406888356,
            "unit": "iter/sec",
            "range": "stddev: 0.00888086926231448",
            "extra": "mean: 123.75679999999889 msec\nrounds: 8"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 1.0896656674723078,
            "unit": "iter/sec",
            "range": "stddev: 0.00566485253973726",
            "extra": "mean: 917.7126799999996 msec\nrounds: 5"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 0.12159347519684624,
            "unit": "iter/sec",
            "range": "stddev: 0.08396803952273874",
            "extra": "mean: 8.224125499999994 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 3365052.5485358736,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011797341456384678",
            "extra": "mean: 297.17217950586013 nsec\nrounds: 175439"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2656425.02047959,
            "unit": "iter/sec",
            "range": "stddev: 9.754785788472534e-7",
            "extra": "mean: 376.44578419889314 nsec\nrounds: 59881"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "chrisj_sewell@hotmail.com",
            "name": "Chris Sewell",
            "username": "chrisjsewell"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "1b84d6b00ad68bf8e58861c712c3cb9b6394abfd",
          "message": "🐛 Fix performance regression (#102)\n\n`Container.is_initialised` is a costly operation, loading the config JSON every time.\r\nIn 1d7c389, the config is now called on every call to `loose_prefix_len`, leading to a large performance degradation.\r\nThis PR makes sure the `is_initialised` test is called only if the config has not already been loaded into memory.",
          "timestamp": "2020-10-02T18:45:30+01:00",
          "tree_id": "3e63fef3df945593819e81391c96d674c2e19225",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/1b84d6b00ad68bf8e58861c712c3cb9b6394abfd"
        },
        "date": 1601661143170,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.860640722346086,
            "unit": "iter/sec",
            "range": "stddev: 0.04687555787959597",
            "extra": "mean: 1.1619250333333333 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.11374599970011248,
            "unit": "iter/sec",
            "range": "stddev: 0.2922286089153543",
            "extra": "mean: 8.791517966666666 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 6.8148109206371394,
            "unit": "iter/sec",
            "range": "stddev: 0.007764975348196765",
            "extra": "mean: 146.73921428571444 msec\nrounds: 7"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 7.286078017137512,
            "unit": "iter/sec",
            "range": "stddev: 0.010808983514786302",
            "extra": "mean: 137.24805000000137 msec\nrounds: 6"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.5009346319953556,
            "unit": "iter/sec",
            "range": "stddev: 0.013042113157113646",
            "extra": "mean: 666.251533333328 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1801464.0572092365,
            "unit": "iter/sec",
            "range": "stddev: 0.000002572829534308776",
            "extra": "mean: 555.1040532827304 nsec\nrounds: 175439"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2066525.7138530237,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011011192682512924",
            "extra": "mean: 483.9039714320837 nsec\nrounds: 178572"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gio.piz@gmail.com",
            "name": "Giovanni Pizzi",
            "username": "giovannipizzi"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "d786296bc67219512f4058265ffbd8c9e6f06b0a",
          "message": "✨ Generalize compression algorithm (#99)\n\nThe container configuration now accepts a variable for the compression algorithm to use.\r\nCurrently, the supported values are zlib, with levels from 1 to 9, but this can be expanded in the future.",
          "timestamp": "2020-10-04T11:31:10+01:00",
          "tree_id": "302c95715972bb03a6d7e329dad5995741db8395",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/d786296bc67219512f4058265ffbd8c9e6f06b0a"
        },
        "date": 1601807855565,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 1.1520147162967918,
            "unit": "iter/sec",
            "range": "stddev: 0.019804200525730033",
            "extra": "mean: 868.0444666666668 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.10547294172542625,
            "unit": "iter/sec",
            "range": "stddev: 0.12138301980616126",
            "extra": "mean: 9.481104666666665 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 6.897518735877944,
            "unit": "iter/sec",
            "range": "stddev: 0.011034289827127427",
            "extra": "mean: 144.97967142857146 msec\nrounds: 7"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 9.860361261450842,
            "unit": "iter/sec",
            "range": "stddev: 0.004797606336180165",
            "extra": "mean: 101.41616249999963 msec\nrounds: 8"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.8229005896961874,
            "unit": "iter/sec",
            "range": "stddev: 0.003117950070682194",
            "extra": "mean: 548.5762666666668 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 3094997.280936908,
            "unit": "iter/sec",
            "range": "stddev: 1.9494930098499138e-7",
            "extra": "mean: 323.10206091580307 nsec\nrounds: 149254"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 1911951.429243788,
            "unit": "iter/sec",
            "range": "stddev: 7.36897536691017e-7",
            "extra": "mean: 523.0258387868768 nsec\nrounds: 68966"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "mail@sphuber.net",
            "name": "Sebastiaan Huber",
            "username": "sphuber"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "4f4357b4e0a0347ffb6f8a66cb1d5da6de675cc7",
          "message": "Dependencies: set up limit for sqlalchemy dependency (#107)\n\nThe code is incompatible with `sqlalchemy==1.4` so for now we put an\r\nupper limit on the requirement `sqlalchemy<1.4`.",
          "timestamp": "2021-04-23T08:50:13+02:00",
          "tree_id": "b3147e700fe9ef371fe44e913d5b67680a93d08a",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/4f4357b4e0a0347ffb6f8a66cb1d5da6de675cc7"
        },
        "date": 1619160877081,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.8855895887962528,
            "unit": "iter/sec",
            "range": "stddev: 0.0202285672298691",
            "extra": "mean: 1.129191233333333 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.19358678722167685,
            "unit": "iter/sec",
            "range": "stddev: 0.15647343898058327",
            "extra": "mean: 5.165641800000001 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 6.653762170206331,
            "unit": "iter/sec",
            "range": "stddev: 0.0135319598654983",
            "extra": "mean: 150.2909142857131 msec\nrounds: 7"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 8.285607371787755,
            "unit": "iter/sec",
            "range": "stddev: 0.0031228570254256903",
            "extra": "mean: 120.6912124999997 msec\nrounds: 8"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.4150483505512534,
            "unit": "iter/sec",
            "range": "stddev: 0.020173152892233842",
            "extra": "mean: 706.6896333333309 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2015706.6131355523,
            "unit": "iter/sec",
            "range": "stddev: 0.00000212521909099602",
            "extra": "mean: 496.1039436411037 nsec\nrounds: 163935"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3182532.780429039,
            "unit": "iter/sec",
            "range": "stddev: 7.179534674635456e-7",
            "extra": "mean: 314.2151452924051 nsec\nrounds: 161291"
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
          "id": "7a894a4f8befb5de0fe95979183b1cbb03f4ef13",
          "message": "Merge pull request #106 from aiidateam/fix/update-python-support\n\nPython support: remove 3.5 and add 3.9 support",
          "timestamp": "2021-04-23T15:33:19+02:00",
          "tree_id": "f577efcb13f4ee1f11313641f80fbf03890b9d37",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/7a894a4f8befb5de0fe95979183b1cbb03f4ef13"
        },
        "date": 1619185116222,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 1.138265790601666,
            "unit": "iter/sec",
            "range": "stddev: 0.008915103375919197",
            "extra": "mean: 878.5294333333331 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.19373665287655625,
            "unit": "iter/sec",
            "range": "stddev: 0.08970776729754142",
            "extra": "mean: 5.161645900000001 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 7.12935973715481,
            "unit": "iter/sec",
            "range": "stddev: 0.0087791078622575",
            "extra": "mean: 140.26504999999912 msec\nrounds: 8"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 10.049388276986738,
            "unit": "iter/sec",
            "range": "stddev: 0.0036068558593713414",
            "extra": "mean: 99.50854444444307 msec\nrounds: 9"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.8516130852015504,
            "unit": "iter/sec",
            "range": "stddev: 0.02072844550667635",
            "extra": "mean: 540.0696333333315 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 1916680.025899422,
            "unit": "iter/sec",
            "range": "stddev: 5.606063072563075e-7",
            "extra": "mean: 521.7354939204 nsec\nrounds: 147059"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 1885488.7516722006,
            "unit": "iter/sec",
            "range": "stddev: 0.000005667488155037836",
            "extra": "mean: 530.3664628670529 nsec\nrounds: 178572"
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
          "id": "a2561a40cf2e9a4d58325387f913ccf08111f5fd",
          "message": "Merge pull request #104 from giovannipizzi/master_in_dev\n\nMerge v0.5.0 in develop",
          "timestamp": "2021-04-23T16:22:25+02:00",
          "tree_id": "4beb6bcd4bfe656b36e0d022e991951f256753fd",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/a2561a40cf2e9a4d58325387f913ccf08111f5fd"
        },
        "date": 1619188037787,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 0.8404443092885482,
            "unit": "iter/sec",
            "range": "stddev: 0.018453769124310123",
            "extra": "mean: 1.1898468333333339 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.15783860611085418,
            "unit": "iter/sec",
            "range": "stddev: 0.12957922202378683",
            "extra": "mean: 6.335585600000002 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 6.8860347477182815,
            "unit": "iter/sec",
            "range": "stddev: 0.009769413198663144",
            "extra": "mean: 145.22145714285782 msec\nrounds: 7"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 7.859965948381809,
            "unit": "iter/sec",
            "range": "stddev: 0.00726974383900434",
            "extra": "mean: 127.22701428571423 msec\nrounds: 7"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.4773262187929028,
            "unit": "iter/sec",
            "range": "stddev: 0.020323205017014682",
            "extra": "mean: 676.8985666666651 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 2094334.7980066123,
            "unit": "iter/sec",
            "range": "stddev: 0.000001103722618665446",
            "extra": "mean: 477.4785774231512 nsec\nrounds: 45046"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 2004380.4481194394,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014423394522687615",
            "extra": "mean: 498.9072812689953 nsec\nrounds: 172414"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "chrisj_sewell@hotmail.com",
            "name": "Chris Sewell",
            "username": "chrisjsewell"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "2cb284157df3cc9bc5a3ae92da6aebbacbda5623",
          "message": "🔧 MAINTAIN: Improve repo configuration (#112)\n\n- Move config to `setup.cfg` and `pyproject.toml`\r\n- Add `Manifest.in`, `tox.ini`\r\n- Replace `requirements.txt`/`dev-requirements.txt with `requirements.lock`\r\n- Move from yapf to black code formatting\r\n- Add more pre-commit hooks\r\n- Update pylint version and fix new failures\r\n- Drop python 3.6",
          "timestamp": "2021-08-30T16:07:48+02:00",
          "tree_id": "3e95e7e154b9b51de8f0ec0458d0ae1a6a26ba51",
          "url": "https://github.com/aiidateam/disk-objectstore/commit/2cb284157df3cc9bc5a3ae92da6aebbacbda5623"
        },
        "date": 1630332772105,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmark.py::test_pack_write",
            "value": 1.1139734038849822,
            "unit": "iter/sec",
            "range": "stddev: 0.00840065488697127",
            "extra": "mean: 897.6875 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_write",
            "value": 0.156828525728739,
            "unit": "iter/sec",
            "range": "stddev: 0.13021993414178143",
            "extra": "mean: 6.376391000000001 sec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_pack_read",
            "value": 7.288896126878425,
            "unit": "iter/sec",
            "range": "stddev: 0.00903775994710011",
            "extra": "mean: 137.194985714286 msec\nrounds: 7"
          },
          {
            "name": "tests/test_benchmark.py::test_loose_read",
            "value": 10.048331357347486,
            "unit": "iter/sec",
            "range": "stddev: 0.005279700985956113",
            "extra": "mean: 99.51901111111204 msec\nrounds: 9"
          },
          {
            "name": "tests/test_benchmark.py::test_has_objects",
            "value": 1.8507088677640986,
            "unit": "iter/sec",
            "range": "stddev: 0.011789407619129428",
            "extra": "mean: 540.3334999999933 msec\nrounds: 3"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_packed",
            "value": 3066204.095693729,
            "unit": "iter/sec",
            "range": "stddev: 1.658654076057694e-7",
            "extra": "mean: 326.1361503642205 nsec\nrounds: 144928"
          },
          {
            "name": "tests/test_benchmark.py::test_list_all_loose",
            "value": 3085296.552789979,
            "unit": "iter/sec",
            "range": "stddev: 3.0645837741369406e-7",
            "extra": "mean: 324.11795199912376 nsec\nrounds: 78125"
          }
        ]
      }
    ]
  }
}