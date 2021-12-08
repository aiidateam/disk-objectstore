# CLI usage

The package comes with a CLI tool that can be used to interact with a container.

```console
$ dostore
Usage: dostore [OPTIONS] COMMAND [ARGS]...

  Manage a disk objectstore

Options:
  --version        Show the version and exit.
  -p, --path TEXT  Path to the container (or set env DOSTORE_PATH)
                   [default: /path/to/dostore]
  --help           Show this message and exit.

Commands:
  add-files  Add file(s) to the container
  create     Create a container
  optimize   Optimize the container's memory use
  status     Print details about the container
```

Create a container:

```console
$ dostore create
Created container: /path/to/dostore
```

Inspect the container:

```console
$ dostore status
{
  "path": "/path/to/dostore",
  "id": "da81094c07ac4ae9aa730d6b59fe353a",
  "compression": "zlib+1",
  "count": {
    "packed": 0,
    "loose": 0,
    "pack_files": 0
  },
  "size": {
    "total_size_packed": 0,
    "total_size_packed_on_disk": 0,
    "total_size_packfiles_on_disk": 0,
    "total_size_packindexes_on_disk": 12288,
    "total_size_loose": 0
  }
}
```

Add files to the container:

```console
$ dostore add-files README.md CHANGELOG.md
Adding 2 file(s) to container: /path/to/dostore
4911fc17759f2260e7674094eadb71b882ec50de2b771fda0410b19501862071: README.md
c19f337aff836a2a894333a55713ce29e31ab8091b4c55c6654e7e8e5c8e0fa7: CHANGELOG.md
```

Optimize memory usage of the container (i.e. pack objects):

```console
$ dostore optimize
Is this the only process accessing the container? [y/N]: y
Initial container size: 39.33 Mb
Final container size: 23.91 Mb
```
