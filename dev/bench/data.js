window.BENCHMARK_DATA = {
  "lastUpdate": 1595247217885,
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
      }
    ]
  }
}