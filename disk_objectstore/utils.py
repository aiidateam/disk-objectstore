"""Useful utilities to be used by the ``Container`` class.

Some might be useful also for end users, like the wrappers to get streams,
like the ``LazyOpener``.
"""
import os
import shutil
import uuid
import zlib

from contextlib import contextmanager

from .exceptions import ModificationNotAllowed


def get_new_uuid():
    """Utility function to generate a new UUID.

    In this way all parts of the code that need to do it, will do it in the same
    way. Note that this returns the UUID without dashes,
    so we reduce storage space.
    """
    return uuid.uuid4().hex


class LazyOpener:
    """A class to return a stream to a given file, that however is opened lazily.

    This means that upon instance creation no file is opened, while the file is opened
    when opening the stream.
    """

    def __init__(self, path, mode='rb'):
        """Lazily store file path and mode, but do not open now.

        File will be opened only when entering the context manager.
        """
        self._path = path
        self._mode = mode
        self._fhandle = None

    @property
    def path(self):
        """The file path."""
        return self._path

    @property
    def mode(self):
        """The file open mode."""
        return self._mode

    def __enter__(self):
        """Open the file when entering the with context manager.

        Note: you cannot open it twice with two with statements.
        """
        if self._fhandle is not None:
            raise IOError('File {} already open'.format(self.path))
        self._fhandle = open(self.path, mode=self.mode)
        return self._fhandle

    def __exit__(self, exc_type, value, traceback):
        """Close the file when exiting the with context manager."""
        if self._fhandle is not None:
            if not self._fhandle.closed:
                self._fhandle.close()
        self._fhandle = None


@contextmanager
def nullcontext(enter_result):
    """Return a context manager that returns enter_result from __enter__, but otherwise does nothing.

    This can be replaced by ``contextlib.nullcontext`` if we want to support only py>=3.7.
    """
    yield enter_result


class ObjectWriter:
    """A class to get direct write access for a new object."""

    def __init__(self, sandbox_folder, loose_folder, loose_prefix_len):
        """Initialise an object to store a new loose object.

        :param sandbox_folder: the folder to store objects while still giving
          access to users to write them
        :param loose_folder: the folder to store the loose objects once finished
        :param loose_prefix_len: the length of the prefix to group loose objects
          in subfolders. E.g., 2 means store in folders aa/..., ab/...
          0 means store objects flat. Note that objects are always stored flat
          in the sandbox (there shouldn't be too many sandbox objects at the
          same time).
        """
        self._sandbox_folder = sandbox_folder
        self._loose_folder = loose_folder
        self._uuid = get_new_uuid()
        self._loose_prefix_len = loose_prefix_len
        self._stored = False
        self._obj_path = None
        self._filehandle = None

    def get_uuid(self):
        """Return the object ID (it's actually a uuid)."""
        return self._uuid

    def __enter__(self):
        """Start creating a new object in a context manager.

        You will get access access to a file-like object.

        :note: Do not close the file, it will be closed automatically.
        """
        if self._stored:
            raise ModificationNotAllowed("You have already stored this object '{}'".format(self.get_uuid()))
        self._obj_path = os.path.join(self._sandbox_folder, self._uuid)
        self._filehandle = open(self._obj_path, 'wb')
        return self._filehandle

    def __exit__(self, exc_type, value, traceback):
        """
        Close the file object, and move it from the sandbox to the loose
        object folder, possibly using sharding if loose_prexix_len is not 0.
        """
        if not self._filehandle.closed:
            self._filehandle.close()

        if exc_type is None:
            if self._loose_prefix_len:
                parent_folder = os.path.join(self._loose_folder, self._uuid[:self._loose_prefix_len])
                # Create parent folder the first time
                if not os.path.exists(parent_folder):
                    os.mkdir(parent_folder)

                dest_loose_object = os.path.join(
                    self._loose_folder, self._uuid[:self._loose_prefix_len], self._uuid[self._loose_prefix_len:]
                )
            else:  # prefix_len == 0
                dest_loose_object = os.path.join(self._loose_folder, self._uuid)

            if os.path.exists(dest_loose_object):
                raise ModificationNotAllowed("Destination object '{}' already exists!".format(self._uuid))
            # Hopefully this is a fast, atomic operation on most filesystems
            shutil.move(self._obj_path, dest_loose_object)
            self._stored = True
        else:
            if os.path.exists(self._obj_path):
                os.remove(self._obj_path)


class PackedObjectReader:
    """A class to read from a pack file.

    This ensures that the .read() method works and does not go beyond the
    length of the given object."""

    @property
    def seekable(self):
        """Return whether object supports random access."""
        return False

    def seek(self, target, whence=0):  # pylint: disable=no-self-use
        """Change stream position."""
        raise OSError('Object not seekable')

    def tell(self):  # pylint: disable=no-self-use
        """Return current stream position."""
        raise OSError('Object not seekable')

    def __init__(self, fhandle, offset, length):
        """
        Initialises the reader to a pack file.

        :param fhandle: an open handle to the pack file, must be opened in read and binary mode.
        :param offset: the integer offset where in the fhandle where the object starts.
        :param length: the integer length of the byte stream.
          The read() method will ensure that you never go beyond the given length.
        """
        assert 'b' in fhandle.mode
        assert 'r' in fhandle.mode

        self._fhandle = fhandle
        self._offset = offset
        self._length = length

        # Move to the offset position, and keep track of the internal position
        self._fhandle.seek(self._offset)
        self._update_pos()

    def _update_pos(self):
        """Update the internal position variable with the correct value.

        This function must be called (internally) after any operation that
        moves into the file.
        """
        self._pos = self._fhandle.tell() - self._offset
        assert self._pos <= self._length, RuntimeError(
            "PackedObjectReader didn't manage to prevent to go beyond the length!"
        )

        assert self._pos >= 0, RuntimeError(
            "PackedObjectReader didn't manage to prevent to go beyond the length (in the negative direction)!"
        )

    def read(self, size=-1):
        """
        Read and return up to n bytes.

        If the argument is omitted, None, or negative, reads and
        returns all data until EOF (that corresponds to the length specified
        in the __init__ method).

        Returns an empty bytes object on EOF.
        """
        # Check how many bytes are left on this portion of the pack
        # (avoid to go beyond)
        remaining_bytes = self._length - self._pos

        if size is None or size < 0:
            stream = self._fhandle.read(remaining_bytes)
            self._update_pos()
            return stream

        # Get the requested bytes, but at most the remaining_bytes
        bytes_to_fetch = min(remaining_bytes, size)
        stream = self._fhandle.read(bytes_to_fetch)
        self._update_pos()
        return stream


class StreamDecompresser:
    """A class that gets a stream of compressed zlib bytes, and returns the corresponding
    uncompressed bytes when being read via the .read() method.
    """

    _CHUNKSIZE = 65536

    def __init__(self, compressed_stream):
        """Create the class from a given compressed bytestream.

        :param compressed_stream: an open bytes stream that supports the .read() method,
          returning a valid compressed stream.
        """
        self._compressed_stream = compressed_stream
        self._decompressor = zlib.decompressobj()
        self._internal_buffer = b''

    def read(self, size=-1):
        """
        Read and return up to n bytes.

        If the argument is omitted, None, or negative, reads and
        returns all data until EOF (that corresponds to the length specified
        in the __init__ method).

        Returns an empty bytes object on EOF.
        """
        if size is None or size < 0:
            # Read all the rest: we call ourselves but with a length,
            # and return the joined result
            data = []
            while True:
                next_chunk = self.read(size=self._CHUNKSIZE)
                if not next_chunk:
                    # Empty returned value: EOF
                    break
                data.append(next_chunk)
            # Making a list and joining does many less mallocs, so should be faster
            return b''.join(data)

        if size == 0:
            return b''

        while len(self._internal_buffer) < size:
            next_chunk = self._compressed_stream.read(self._CHUNKSIZE)

            old_unconsumed = self._decompressor.unconsumed_tail

            # In the previous step, I might have some leftover data
            # since I am using the max_size parameter of .decompress()
            compressed_chunk = old_unconsumed + next_chunk
            # The second parameter is max_size. We know that in any case we do
            # not need more than `size` bytes. Leftovers will be left in
            # .unconsumed_tail and reused a the next loop
            decompressed_chunk = self._decompressor.decompress(compressed_chunk, size)
            self._internal_buffer += decompressed_chunk

            if not next_chunk and not self._decompressor.unconsumed_tail:
                # Nothing to do: no data read, and the unconsumed tail is over.
                # We break.
                break

            if not next_chunk and len(self._decompressor.unconsumed_tail) == len(old_unconsumed):
                raise ValueError(
                    'There is no data in the reading buffer, and we are not consuming the '
                    'remaining decompressed chunk: there must be a problem in the incoming buffer'
                )

        # Note that we could be here also with len(self._internal_buffer) < size,
        # if we used 'break' because the internal buffer reached EOF.
        to_return, self._internal_buffer = self._internal_buffer[:size], self._internal_buffer[size:]

        return to_return
