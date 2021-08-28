Here we benchmark removal of objects from a set

At the beginning, `data` is a set of 1'000'000 UUIDs.
`data2` has a random half of them.

We also store in `data_bk` a copy of data.

# Results
- Subtracting the two sets is very fast (0.08s)
- Subtracting elements one by one is slower (0.31s) (~4x slower)
- Subtracting in batches has an optimal for batches of 100-1000 elements (minimum ~0.25s),
  and goes up to 0.31-0.35s for batches that are either very small (1) or very large (100000).

Therefore: we just remove elements one by one, it's a bit faster,
but if we don't want to put all in memory it's OK, and anyway we are speaking of less than 0.5s
for 1'000'000 objects, that is anyway faster than any disk access.
