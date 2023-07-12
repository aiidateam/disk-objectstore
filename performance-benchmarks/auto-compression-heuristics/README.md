# Benchmarking of the AUTO compression mode

This folder contains performance benchmarks of the CompressMode.AUTO
compression mode, in particular to check the accuracy of the
heuristics, as well as the performance.
This was tested on top of the code implemented in #148 (as of July 2023).

## Test sets

We test this on two different real datasets generated with AiiDA:
- a "small-objects" case, from a database by Giovanni Pizzi
  - 1,055,219 objects
  - 40,344,256,249 total size (~40GB)
  - largest object size ~6MB

- a "large-objects" case, from a database by Bonan Zhu, that contains
  - 147,454 objects
  - 98,801,766,777 total size (~98GB)
  - largest object size ~2GB


## Results
### small-objects case
The small-objects case results were performed on a 2019 MacBook Pro with 2.6GHz Intel Core i7 and 32GB of RAM.

Timing:
- 325s to fully recompress everything from fully decompressed objects
- 360s (6 minutes) to decompress everything, from fully compressed objects
- 523s to repack everything, while evaluating whether to compress or not (i.e., starting from **fully decompressed** objects, since if the objects are already compressed, it will check whether to compress or not based on the information on full size and compressed length, and when compressing it will just stream the data and not recompress, so it would be much faster)
- 322s to decompress everything from the automatically compressed version

Note that the time to repack everything while also evaluating the compressibility is a bit less than twice the time to compress everything.
It makes sense since even the largest files are up to a few MB so even the heuristics has to almost try to compress everything before deciding.

In terms of sizes, this is the output of the script (see script below):
```
sizes.sum()=40344256249.0, compressed_lengths.sum()=7564127548.0 (18.7%), auto_compressed_lengths.sum()=7564886295.0 (18.8%)
Size of auto-uncompressed: 10230341.0 (smallest = 85.0, largest = 8576.0)
Size of auto-compressed:   40334025908.0 (smallest = 136.0, largest = 6314959.0)
Total number of objects: 1055219
Number of objects with compressed size > uncompressed: 183 (max (in %): 107.05882352941177
```

### large-objects case
The small-objects case results were performed on a 2022 Ubuntu machine with 3.30GHz Intel Core i9 CPU and 256GB of RAM.

Timing:
- 489s (~8min) for the first validation (might be slower because files might not have been all cached)
- 1054s (~17.5 minutes) to decompress everything
- 2658s (~44 minutes) to fully recompress everything from fully decompressed objects
- 1069s (~17.5 minutes) to decompress everything again from fully compressed objects
- 820s (~13.5m) to repack everything, while evaluating whether to compress or not (i.e., starting from **fully decompressed** objects, since if the objects are already compressed, it will check whether to compress or not based on the information on full size and compressed length, and when compressing it will just stream the data and not recompress, so it would be much faster)
- 210s (~3.5min) for a final validation (this could be a combination of object being cached in memory and smaller file size)

Here, since the objects are often big, the heuristics helps in significantly reducing the compression time for the AUTO mode (since most objects are left uncompressed and only copied).

In terms of sizes, this is the output of the script (see script below):
```
sizes.sum()=98801697641.0, compressed_lengths.sum()=83632942670.0 (84.6%), auto_compressed_lengths.sum()=87045040360.0 (88.1%)
Size of auto-uncompressed: 83202739363.0 (smallest = 1.0, largest = 2662690408.0)
Size of auto-compressed:   15598958278.0 (smallest = 64.0, largest = 204356253.0)
Total number of objects: 147452
Number of objects with compressed size > uncompressed: 616 (max (in %): 900.0
ABOVE MAX=130
- Not compressed: [900.], compr_len=[9.], size=[1.]
- Compressed: [], compr_len=[], size=[]
```
The last two lines indicate that only one object will be out of scale in the plots below because it was a 1-byte object that, if compressed, would take 9 bytes (so compression factor of 900%, and indeed it was not auto-compressed).

## Scripts and plots

To compress or decompress everything, I used these scripts from ipython
```python
import time
import disk_objectstore as dostore

c = dostore.Container(".")
t = time.monotonic()
c.repack(compress_mode=dostore.container.CompressMode.AUTO)
print(time.monotonic() - t)
```
(replacing `CompressMode.AUTO` with `CompressMode.YES` or `CompressMode.NO` where appropriate).

I then dumped the relevant sizes using the following code
```python
### Dump relevant data to csv
import sqlite3
import pandas as pd
conn = sqlite3.connect('packs.idx')
cursor = conn.cursor()
clients = pd.read_sql('SELECT length,size,compressed FROM db_object ORDER BY id' ,conn)
clients.to_csv('auto-compressed.csv', index=False)
```
where I changed the last filename to `auto-compressed.csv` for the result of `CompressMode.AUTO` and `all-compressed.csv` for the result of `CompressMode.YES`.

Data from the two cases is found in the two subfolders `small-objects` an `large-objects.

I then used the script in this folder called `plot_results.py` to obtain plots.
The attached figures `large-objects.png` and `small-objects.png` show the plotted results.

## Final comments

From the plots, we can see that in general the heuristics works quite well, trying to compress only objects where you can compress them by to at least 90% or less or the original size.
Numbers and plots also show the nature of the different datasets (e.g. the large number of large, uncompressible files in teh `large-objects` dataset) and that time for the heuristics is reasonable compared with the typical times to fully repack objects.
