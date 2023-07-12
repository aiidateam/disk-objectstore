"""
Plot the results of compression in particular comparing 
full compression vs. auto compression.
"""
import numpy as np
import pylab as pl


for fignum, what in [[1, 'small-objects'], [2, 'large-objects']]:
    all_compressed = np.loadtxt(f'{what}/all-compressed.csv', delimiter=',')
    auto_compressed = np.loadtxt(f'{what}/auto-compressed.csv', delimiter=',')
    # I know the first one is the zero-length byte string, I remove it in the future to avoid

    heuristics = auto_compressed[:, 2] # 0 = was not compressed
    # Check that they are sorted in the same way
    assert np.allclose(all_compressed[:, 1], auto_compressed[:, 1])
    assert np.allclose((all_compressed[:, 0])[heuristics == 1], (auto_compressed[:, 0])[heuristics == 1])

    # Avoid zero-division errors: drop the zero-byte object
    non_zero_mask = np.where(auto_compressed[:,1] != 0)
    all_compressed = all_compressed[non_zero_mask]
    auto_compressed = auto_compressed[non_zero_mask]
    heuristics = heuristics[non_zero_mask]

    ## Analyze

    sizes = all_compressed[1:, 1]
    compressed_lengths = all_compressed[1:, 0]
    auto_compressed_lengths = auto_compressed[1:,0]
    heuristics = heuristics[1:]

    print(f"{sizes.sum()=}, {compressed_lengths.sum()=} ({100 * compressed_lengths.sum() / sizes.sum():.1f}%), {auto_compressed_lengths.sum()=} ({100 * auto_compressed_lengths.sum() / sizes.sum():.1f}%)")

    print(f"Size of auto-uncompressed: {sizes[heuristics==0].sum()} (smallest = {sizes[heuristics==0].min()}, largest = {sizes[heuristics==0].max()})")
    print(f"Size of auto-compressed:   {sizes[heuristics==1].sum()} (smallest = {sizes[heuristics==1].min()}, largest = {sizes[heuristics==1].max()})")

    print(f"Total number of objects: {len(sizes)}")
    print(f"Number of objects with compressed size > uncompressed: {sum((compressed_lengths / sizes) > 1)} (max (in %): {(100 * compressed_lengths / sizes).max()}")

    # Compression factor (percentage) for the two heuristics cases
    was_not_compressed = (100 * (compressed_lengths / sizes))[heuristics == 0]
    was_compressed = (100 * (compressed_lengths / sizes))[heuristics == 1]

    MAX = 130
    pl.figure(fignum, figsize=(12,8))
    pl.subplot(121)
    res = pl.hist(was_compressed, bins=MAX, range=(0, MAX), color='green', alpha=0.5, label='compressed')
    res2 = pl.hist(was_not_compressed, bins=MAX, range=(0, MAX), color='red', alpha=0.5, label='not compressed')
    pl.axvline(90, color='gray', alpha=0.5)
    pl.xlabel("compression factor (%)")
    pl.ylabel("# objects")
    pl.legend(loc='best')
    print(f'Check on histogram: # objects compressed: {res[0].sum()}, uncompressed: {res2[0].sum()}; total = {res[0].sum() + res2[0].sum()}, should be {len(was_compressed) + len(was_not_compressed)}') # Might need to increase MAX if this is not true!

    pl.subplot(122)
    res = pl.hist(was_compressed, bins=MAX, range=(0, MAX), weights=sizes[heuristics==1] / 1024 / 1024, color='green', alpha=0.5, label='compressed')
    res2 = pl.hist(was_not_compressed, bins=MAX, range=(0, MAX), weights=sizes[heuristics==0] / 1024 / 1024, color='red', alpha=0.5, label='not compressed')
    pl.axvline(90, color='gray', alpha=0.5)
    pl.xlabel("compression factor (%)")
    pl.ylabel("total MB")
    pl.legend(loc='best')
    print(f'Check on histogram: amount compressed: {res[0].sum() * 1024 * 1024} bytes, uncompressed: {res2[0].sum() * 1024 * 1024} bytes; total = {(res[0].sum() + res2[0].sum()) * 1024 * 1024} bytes, should be {sizes.sum()}') # Might need to increase MAX if this is not true!

    print(f"ABOVE {MAX=}")
    print(f"- Not compressed: {was_not_compressed[was_not_compressed > MAX]}, compr_len={(compressed_lengths[heuristics == 0])[was_not_compressed > MAX]}, size={(sizes[heuristics == 0])[was_not_compressed > MAX]}")
    print(f"- Compressed: {was_compressed[was_compressed > MAX]}, compr_len={(compressed_lengths[heuristics == 1])[was_compressed > MAX]}, size={(sizes[heuristics == 1])[was_compressed > MAX]}")

    pl.show()
