#!/usr/bin/env python

# In[1]:


import time
import zlib

import numpy

import disk_objectstore as dos

# In[2]:


def get_bytes(size):
    return b''.join(numpy.random.choice([str(_).encode() for _ in range(10)], size))


# In[3]:


content = get_bytes(100_000_000)

with open('test.binary.gz', 'wb') as fh:
    fh.write(zlib.compress(content))


# In[4]:


def readline_SLOW(self, size=-1):
    res = bytearray()
    while size < 0 or len(res) < size:
        b = self.read(1)
        if not b:
            break
        res += b
        if res.endswith(b'\n'):
            break
    return bytes(res)


# In[33]:


def readline_WITH_PEEK(self, size=-1):
    r"""Read and return a line of bytes from the stream.

    If size is specified, at most size bytes will be read.
    Size should be an int.

    The line terminator is always b'\n' for binary files; for text
    files, the newlines argument to open can be used to select the line
    terminator(s) recognized.
    """
    # For backwards compatibility, a (slowish) readline().
    if hasattr(self, 'peek'):

        def nreadahead():
            readahead = self.peek(1)
            if not readahead:
                # print('peek 1')
                return 1
            n = (readahead.find(b'\n') + 1) or len(readahead)
            if size >= 0:
                n = min(n, size)
            # print(f'peek {n}')
            return n
    else:

        def nreadahead():
            # print(f'nopeek 1')
            return 1

    res = bytearray()
    while size < 0 or len(res) < size:
        b = self.read(nreadahead())
        if not b:
            break
        res += b
        if res.endswith(b'\n'):
            break
    return bytes(res)


# In[34]:


def readline(self, size=-1):
    r"""Read and return a line of bytes from the stream.

    If size is specified, at most size bytes will be read.
    Size should be an int.

    The line terminator is always b'\n' for binary files; for text
    files, the newlines argument to open can be used to select the line
    terminator(s) recognized.
    """

    res = bytearray()
    while size < 0 or len(res) < size:
        # Read for a number of bytes equal to the size of the internal buffer
        # (so no read on disk are needed). However, if it the buffer is empty
        # read at least 1 byte. This will in pracice read another chunk,
        # so at the next iteration, we have a much bigger read ahead)
        bytes_to_read = max(1, len(self._internal_buffer))
        b = self.read(bytes_to_read)
        if not b:
            break
        res += b
        if res.endswith(b'\n'):
            break
    return bytes(res)


# In[35]:


with open('test.binary.gz', 'rb') as fh:
    t = time.monotonic()
    # data = zlib.decompress(fh.read())
    stream = dos.utils.ZlibStreamDecompresser(fh)
    data = stream.read()
    print(time.monotonic() - t)

assert data == content


# In[36]:


class Peekable(dos.utils.ZlibStreamDecompresser):
    # def peek(self, size):
    #    want = min(size, len(self._internal_buffer))
    #    #return self._internal_buffer[:want]
    #    return self._internal_buffer

    def _read_compressed(self, size: int = -1) -> bytes:
        """
        Read and return up to n bytes.

        If the argument is omitted, None, or negative, reads and
        returns all data until EOF (that corresponds to the length specified
        in the __init__ method).

        Returns an empty bytes object on EOF.

        Note that this should be used only internally, as this function
        always reads from the compressed stream, but the position
        (seek) in the compressed stream will be wrong/outdated once
        an uncompressed stream is set!

        TODO: add method to reset the uncompressed stream (close it if not
        closed, set internally variable to False, seek back to zero)
        """
        if size is None or size < 0:
            # Read all the rest: we call ourselves but with a length,
            # and return the joined result
            data = []
            while True:
                next_chunk = self.read(self._CHUNKSIZE)
                if not next_chunk:
                    # Empty returned value: EOF
                    break
                data.append(next_chunk)
            # Making a list and joining does many less mallocs, so should be faster
            return b''.join(data)

        if size == 0:
            return b''

        while len(self._internal_buffer) < size:
            old_unconsumed = self._decompressor.unconsumed_tail
            next_chunk = self._compressed_stream.read(max(0, self._CHUNKSIZE - len(old_unconsumed)))

            # In the previous step, I might have some leftover data
            # since I am using the max_size parameter of .decompress()
            compressed_chunk = old_unconsumed + next_chunk
            # The second parameter is max_size. We know that in any case we do
            # not need more than `size` bytes. Leftovers will be left in
            # .unconsumed_tail and reused a the next loop
            while len(self._internal_buffer) < size:
                # I do another while loop, as I want also to decompress in chunks
                # (this time, of uncompressed data).
                # I continue either until I get to the required size,
                # or if there is no more data to decompress: then I break from
                # this internal loop, so I can read another chunk of *compressed*
                # data in the outer loop.
                try:
                    decompressed_chunk = self._decompressor.decompress(
                        # Here I still limit what I decompress.
                        # I want to possibly still decompress a bit more than I need, because
                        # e.g. this will allow the `peek()` method to return more bytes, making
                        # the implementation of `readline()` efficient (otherwise, it would
                        # iterate one byte at a time, and would be impossibly slow for large
                        # objects).
                        # However, I still put a limit to self._CHUNKSIZE to still have a hard
                        # limit on the amount of bytes I put in memory.
                        # This is e.g. to protect from a very huge (say 1TB) compressed file
                        # of the same byte character: this would compress down to a very small
                        # compressed size of a few bytes, but when decompressing, would
                        # fill up the memory. In this way, instead, I can only decompress
                        # up to self._CHUNKSIZE *decompressed* bytes: I avoid memory issues,
                        # and the implementation of `readline` is still quite efficient.
                        compressed_chunk,
                        self._CHUNKSIZE,
                    )
                except self.decompress_error as exc:
                    raise ValueError('Error while uncompressing data') from exc
                if not decompressed_chunk:
                    break
                self._internal_buffer += decompressed_chunk

            if not next_chunk and not self._decompressor.unconsumed_tail:
                # Nothing to do: no data read, and the unconsumed tail is over.
                if self._decompressor.eof:
                    # Compressed file is over. We break
                    break
                raise ValueError(
                    "There is no data in the reading buffer, but we didn't reach the end of "
                    'the compressed stream: there must be a problem in the incoming buffer'
                )

        # Note that we could be here also with len(self._internal_buffer) < size,
        # if we used 'break' because the internal buffer reached EOF.
        to_return, self._internal_buffer = (
            self._internal_buffer[:size],
            self._internal_buffer[size:],
        )
        self._pos += len(to_return)

        return to_return


# In[37]:


with open('test.binary.gz', 'rb') as fh:
    t = time.monotonic()
    # data = zlib.decompress(fh.read())
    stream = Peekable(fh)
    data = stream.read()
    print(time.monotonic() - t)

assert data == content


# In[38]:


with open('test.binary.gz', 'rb') as fh:
    t = time.monotonic()
    stream = Peekable(fh)
    data = readline(stream)
    print(time.monotonic() - t)

print(len(stream._internal_buffer))
print(len(stream._decompressor.unconsumed_tail))

assert data == content


# In[32]:


stream.peek(1)


# In[ ]:
