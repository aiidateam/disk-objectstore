"""I check the minimum file size after which I get at least a 10% compression,
when the file is a randomly shuffled string of 94 ASCII characters.

Result: around 450-500 bytes I start having some advantage in compressing.

Note, however, that real files compress more than a random sequence of
characters!
"""
import zlib
import string
import numpy
import pylab as pl
from scipy.stats import linregress


ref_string = string.ascii_letters + string.digits + string.punctuation
print(len(ref_string), len(ref_string) / 256)

ref_string = ref_string * 10

print(len(ref_string))

ref_array = numpy.array(list(ref_string))
numpy.random.shuffle(ref_array)
ref_string = "".join(ref_array).encode()

x = []; y = []
for i in range(len(ref_string)):
    x.append(i)
    y.append(len(zlib.compress(ref_string[:i], level=1)))

x = numpy.array(x)
y = numpy.array(y)
fit = linregress(x, y)
print(f"{fit.slope=}, {fit.intercept=}")

pl.plot(x, y, '-b', label='compressed_size')
pl.plot(x, fit.slope * x + fit.intercept, '--g', label='fit')
pl.plot(x, x, '-k', label='no compression')
pl.plot(x, 0.9 * x, '-r', label='10% compression') 
pl.xlabel("Initial size")
pl.ylabel("Compressed size")
pl.legend(loc='upper left')
pl.show()
