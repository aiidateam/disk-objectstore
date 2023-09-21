"""Useful utilities to be used by the ``Container`` class.

Some might be useful also for end users, like the wrappers to get streams,
like the ``LazyOpener``.
"""
#  pylint: disable= too-many-lines
from __future__ import annotations

import abc
import hashlib
import itertools
import os
import uuid
import zlib
from contextlib import contextmanager
from enum import Enum
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    Callable,
    Iterable,
    Iterator,
    Literal,
    Sequence,
    Union,
)
from zlib import error

from .exceptions import ClosingNotAllowed, ModificationNotAllowed

if TYPE_CHECKING:
    from .container import Container

F_FULLFSYNC: int

try:
    import fcntl

    # Next line exists only on Mac, will be 0 otherwise
    # (Just to have an int, will never be used not on Mac)
    F_FULLFSYNC = getattr(fcntl, "F_FULLFSYNC", 0)
except ImportError:
    # Not available on Windows
    fcntl = None  # type: ignore
    F_FULLFSYNC = 0


# requires read method only
StreamReadBytesType = Union[
    BinaryIO,
    "PackedObjectReader",
    "CallbackStreamWrapper",
    "ZlibLikeBaseStreamDecompresser",
    "ZeroStream",
]
# requires read and seek capability
StreamSeekBytesType = Union[
    BinaryIO,
    "PackedObjectReader",
    "CallbackStreamWrapper",
    "ZlibLikeBaseStreamDecompresser",
]
StreamWriteBytesType = BinaryIO

# For now I I don't always activate it as I need to think at the right balance between
# safety and performance/disk wearing
# I use it only when storing packs
_MACOS_ALWAYS_USE_FULLSYNC = False


class CompressMode(Enum):
    """Various possible behaviors when compressing.

    For now used only in the `repack` function, should probably be applied to all functions
    that have a `compress` kwarg.
    """

    # Never compress
    NO = "no"  # pylint: disable=invalid-name
    # Always recompress
    YES = "yes"
    # Keep the current compression when repacking.
    KEEP = "keep"
    # Automatically determine if it's worth compressing this object or not, ideally in a relatively efficient way.
    AUTO = "auto"


class Location(Enum):
    """Enum that describes if an element is only on the left or right iterator, or on both."""

    LEFTONLY = -1
    BOTH = 0
    RIGHTONLY = 1


class LazyOpener:
    """A class to return a stream to a given file, that however is opened lazily.

    This means that upon instance creation no file is opened, while the file is opened
    when opening the stream.
    """

    def __init__(self, path: Path) -> None:
        """Lazily store file path and mode, but do not open now.

        File will be opened only when entering the context manager.
        """
        self._path = path
        self._fhandle: BinaryIO | None = None

    @property
    def path(self) -> Path:
        """The file path."""
        return self._path

    @property
    def mode(self) -> Literal["rb"]:
        """The file open mode."""
        return "rb"

    def tell(self) -> int:
        """Return the position in the underlying file object.

        :return: an integer with the position.
        :raises ValueError: if the file is not open.
        """
        if self._fhandle is None:
            raise ValueError("I/O operation on closed file.")
        return self._fhandle.tell()

    def __enter__(self) -> BinaryIO:
        """Open the file when entering the with context manager.

        Note: you cannot open it twice with two with statements.
        """
        if self._fhandle is not None:
            raise OSError(f"File {self.path} already open")
        self._fhandle = open(self.path, mode=self.mode)
        return self._fhandle

    def __exit__(self, exc_type, value, traceback) -> None:
        """Close the file when exiting the with context manager."""
        if self._fhandle is not None:
            if not self._fhandle.closed:
                self._fhandle.close()
        self._fhandle = None


class LazyLooseStream:
    """A class to point to a loose stream that is created lazily.

    The main usage is to pass to a decompresser, to allow for fully decompressing a packed
    object back as a loose object, and getting an open stream to it.

    The idea is that when the class is instantiated, nothing actually happens.
    The difference with the `utils.LazyOpener` is that this class knows about the container
    and will take care of uncompressing the object to a loose object automatically
    (and doing it "correctly", e.g. with respect to race conditions and not creating
    partial objects in the loose folder), automatically creating the object from the
    corresponding packed object.
    """

    def __init__(self, container, hashkey):
        self._container: Container = container
        self._hashkey = hashkey
        self._stream = None

    @property
    def mode(self) -> str:
        return "rb"

    @staticmethod
    def seekable() -> bool:
        """Return whether object supports random access."""
        return True

    def seek(self, target: int, whence: int = 0) -> int:
        """Change stream position.

        Note that contrary to a standard file, also seeking beyond the borders will raise a ValueError.
        """
        if self.closed:
            raise ValueError("I/O operation on closed file.")
        assert self._stream is not None, (
            "LazyLooseStream has an open stream, but the stream is None! "
            "This should not happen"
        )

        return self._stream.seek(target, whence)

    def tell(self) -> int:
        """Return current stream position, relative to the internal offset."""
        if self.closed:
            raise ValueError("I/O operation on closed file.")
        assert self._stream is not None, (
            "LazyLooseStream has an open stream, but the stream is None! "
            "This should not happen"
        )
        return self._stream.tell()

    def read(self, size: int = -1) -> bytes:
        """
        Read and return up to n bytes.

        If the argument is omitted, None, or negative, reads and
        returns all data until EOF (that corresponds to the length specified
        in the __init__ method).

        Returns an empty bytes object on EOF.
        """
        if self.closed:
            raise ValueError("I/O operation on closed file.")
        assert self._stream is not None, (
            "LazyLooseStream has an open stream, but the stream is None! "
            "This should not happen"
        )
        return self._stream.read(size)

    def __enter__(self) -> LazyLooseStream:
        """Use as context manager. Opens the underlying stream, possibly uncompressing to a loose object."""
        self.open_stream()
        return self

    def __exit__(self, exc_type, value, traceback) -> None:
        """Close context manager."""
        self.close_stream()

    def open_stream(self) -> None:
        """Open the underlying stream, uncompressing the file if needed.

        Note that when called this might uncompress the whole file, if not already done.
        """
        MAX_RETRIES = 3  # pylint: disable=invalid-name
        if not self.closed:
            # Already open, just return
            return

        counter: int = 0
        while True:
            loose_path = self._container.loosen_object(self._hashkey)
            try:
                self._stream = open(  # pylint: disable=consider-using-with
                    loose_path, mode="rb"
                )
                # I could open the stream, exit the infinite loop
                break
            except FileNotFoundError as exc:
                # Probably a concurrent packing was called and
                # it removed the loose object! Retry. I pass and
                # stay in the while True loop.
                counter += 1
                if counter > MAX_RETRIES:
                    raise RuntimeError(
                        "Unable to open the loose object! I tried multiple "
                        "times but I never find the file. Ensure that you are "
                        "not running many concurrent cleaning of the container "
                        "storage."
                    ) from exc

    def close_stream(self) -> None:
        """Close the underlying stream (if open)."""
        if self._stream is not None and not self.closed:
            self._stream.close()
            self._stream = None

    @property
    def closed(self) -> bool:
        """Return True if the underlying stream is closed, False otherwise."""
        return self._stream is None or self._stream.closed


@contextmanager
def nullcontext(enter_result: Any) -> Iterator[Any]:
    """Return a context manager that returns enter_result from __enter__, but otherwise does nothing.

    This can be replaced by ``contextlib.nullcontext`` if we want to support only py>=3.7.
    """
    yield enter_result


class ObjectWriter:  # pylint: disable=too-many-instance-attributes
    """A class to get direct write access for a new object."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        sandbox_folder: Path,
        loose_folder: Path,
        loose_prefix_len: int,
        duplicates_folder: Path,
        hash_type: str,
        trust_existing: bool = False,
    ) -> None:
        """Initialise an object to store a new loose object.

        :param sandbox_folder: the folder to store objects while still giving
          access to users to write them
        :param loose_folder: the folder to store the loose objects once finished
        :param loose_prefix_len: the length of the prefix to group loose objects
          in subfolders. E.g., 2 means store in folders aa/..., ab/...
          0 means store objects flat. Note that objects are always stored flat
          in the sandbox (there shouldn't be too many sandbox objects at the
          same time).
        :param duplicates_folder: the folder to store the duplicates objects (for concurrent writes
          on Windows where I cannot replace).
        :param trust_existing: if True, just continues if a file with the same hashkey is found.
          Otherwise, check the existing file content and overwrite if wrong.
        """
        self._sandbox_folder = sandbox_folder
        self._loose_folder = loose_folder
        self._duplicates_folder = duplicates_folder
        self._hash_type = hash_type
        self._hashkey: str | None = None
        self._loose_prefix_len = loose_prefix_len
        self._stored = False
        self._obj_path: Path | None = None
        self._filehandle: HashWriterWrapper | None = None
        self._trust_existing = trust_existing

    @property
    def hash_type(self) -> str:
        """Return the currently used hash type."""
        return self._hash_type

    def get_hashkey(self) -> str | None:
        """Return the object hash key. Return None if the stream wasn't opened yet."""
        return self._hashkey

    def __enter__(self) -> HashWriterWrapper:
        """Start creating a new object in a context manager.

        You will get access access to a file-like object.

        :note: Do not close the file, it will be closed automatically.
        """
        if self._filehandle is not None:
            raise OSError("You have already opened this ObjectWriter instance")
        if self._stored:
            raise ModificationNotAllowed(
                f"You have already tried to store this object '{self.get_hashkey()}'"
            )
        # Create a new uniquely-named file in the sandbox.
        # It seems faster than using a NamedTemporaryFile, see benchmarks.
        self._obj_path = self._sandbox_folder / uuid.uuid4().hex
        self._filehandle = HashWriterWrapper(
            open(self._obj_path, "wb"), hash_type=self.hash_type
        )
        return self._filehandle

    def __exit__(  # pylint: disable=too-many-branches, too-many-statements
        self, exc_type: Any, value: Any, traceback: Any
    ) -> None:
        """
        Close the file object, and move it from the sandbox to the loose
        object folder, possibly using sharding if loose_prexix_len is not 0.
        """
        try:
            if exc_type is None:
                assert self._filehandle is not None and self._obj_path is not None
                if self._filehandle.closed:
                    raise ClosingNotAllowed(
                        "You cannot close the file handle yourself!"
                    )
                # Flush out of the buffer and sync to disk so data is preserved even for power failures
                # NOTE: For now I don't use `fullsync` on Mac for performance reasons, for loose objects - to decide
                # if we want to change this!
                safe_flush_to_disk(self._filehandle, self._obj_path)
                self._filehandle.close()
                self._hashkey = str(self._filehandle.hexdigest())
                self._filehandle = None

                if self._loose_prefix_len:
                    parent_folder = (
                        self._loose_folder / self._hashkey[: self._loose_prefix_len]
                    )
                    # Create parent folder the first time; done with try/except
                    # rather than with if/else to avoid problems at the beginning, for concurrent writing
                    try:
                        os.mkdir(parent_folder)
                    except FileExistsError:
                        # The folder already exists, great! No work to do
                        pass

                    dest_loose_object = (
                        self._loose_folder
                        / self._hashkey[: self._loose_prefix_len]
                        / self._hashkey[self._loose_prefix_len :]
                    )
                else:  # prefix_len == 0
                    dest_loose_object = self._loose_folder / self._hashkey

                dest_parent_folder = dest_loose_object.parent
                exists_wrong_checksum = False
                # At this point, if the destination exists, it means someone already put an object
                # with the same content/hash key
                if dest_loose_object.exists():
                    if self._trust_existing:
                        # I trust that the object is correct: I just return
                        # Note: if another process is deleting the file at the same time (right after),
                        # it will be deleted. But this is OK - the deletion is in an independent process,
                        # an if it happens only microseconds or seconds after the write, the effect is the same:
                        # the object is deleted and the caller of this function will not find it anymore.
                        return
                    # I do not trust the object is correct.
                    # This might still not be perfect: while I check, another
                    # process might in the meantime rewrite it again, and this might
                    # be wrong. But this is very difficult to catch, and in general
                    # the situation in which a process writes a corrupt node is really an error
                    try:
                        existing_checksum = _compute_hash_for_file(
                            filepath=dest_loose_object, hash_type=self.hash_type
                        )
                    except PermissionError:
                        # On Windows I might get a PermissionError. I store a copy and return.
                        # This would happen if e.g. the file exists but is being moved in place and
                        # I cannot open for reading.
                        self._store_duplicate_copy(self._obj_path, self._hashkey)
                        return
                    if existing_checksum == self._hashkey:
                        # The existing object has the correct hash, I just return.
                        return
                    # If existing_checksum is None, the file has been removed in the meantime.
                    # It could be a delete of the object: then, for consistency with the logic above,
                    # I decide that the two operations that happened almost at the same time could
                    # have happened in swapped order, and I don't write it back.
                    # Or it's a packing operation (and then it's OK to not put the file back).
                    # I therefore just return
                    if existing_checksum is None:
                        return
                    # If we are here, the file exists and has the wrong checksum. I mark this condition
                    exists_wrong_checksum = True

                # If I am here, there are two options:
                # 1. The object did not exist
                # 2. The file is there but its content is wrong. In this case I want to overwrite the object.

                # I therefore call a 'replace' call, that should be an atomic operation
                # Notes (on os.replace vs os.rename):
                # - os.rename() on Linux is atomic (see e.g. also
                #   https://alexwlchan.net/2019/03/atomic-cross-filesystem-moves-in-python/
                #   but needs to be on the same filesystem (this should always be the case for us)
                # - Remember that instead shutil.move is not guaranteed to be atomic!
                # - os.rename performs a silent overwrite if the file exists on Posix, so would be enough
                #   on Linux/Mac; instead, it raises OSError on Windows if the file exists.
                # - we use os.rename: we make sure in this way, on Windows, that only one process writes
                #   to the destination, avoiding race conditions with two processes trying to write the
                #   same file.
                if exists_wrong_checksum:
                    # In this case I try a replace of the file
                    try:
                        os.replace(self._obj_path, dest_loose_object)
                    except PermissionError:
                        # NOTE! This branch only happens on Windows, when the
                        # file with the same name is open by someone else...
                        # I just store a duplicate copy. This happens if I find a file, it has a wrong
                        # hash key, but then I cannot replace it (e.g. it's open, or two processes are writing
                        # at the same time).
                        self._store_duplicate_copy(self._obj_path, self._hashkey)
                else:
                    # In this case the file does not exist. I try just a rename of the file,
                    # to put it in place and reduce the risk of multiple processes trying to overwrite
                    # the same file
                    try:
                        os.rename(self._obj_path, dest_loose_object)
                    except FileExistsError:
                        # NOTE! This branch only happens on Windows, when the
                        # file with the same name was opened in the meantime by someone else...
                        if self._trust_existing:
                            # If I trust existing files, I just return - someone put the file in place
                            return
                        # I'm here: the file did not exist, but appeared exactly at the same time: someone
                        # else is writing it.
                        # I do a final attempt to check the checksum! However, there is a high chance
                        # that the file is being still locked for reading, so I need to take care of checking for those
                        # error
                        try:
                            existing_checksum = _compute_hash_for_file(
                                filepath=dest_loose_object, hash_type=self.hash_type
                            )
                            if existing_checksum == self._hashkey:
                                # The existing object has the correct hash, I just return.
                                return
                        except PermissionError:
                            # The file is probably being moved and I cannot open for reading.
                            # I just pass, so in the lines below I will store a duplicate copy.
                            pass

                        # I'm here. Either I got a permission error, or the checksum is different (
                        # and the file was created exactly in a concurrent process, it wasn't existing at the
                        # beginning of this function): I just store a duplicate
                        self._store_duplicate_copy(self._obj_path, self._hashkey)

                # Flush also the parent directory, see e.g.
                # https://blog.gocept.com/2013/07/15/reliable-file-updates-with-python/
                # I do not call safe_flush_to_disk as I need to flush only the folder metadata (I think)
                # Otherwise I should open again the file
                if os.name == "posix":
                    dirfd = os.open(dest_parent_folder.parent, os.O_DIRECTORY)
                    os.fsync(dirfd)
                    os.close(dirfd)
        finally:
            # I set the stored flag, even if there was a problem, to avoid reuse of the same object.
            self._stored = True

            if self._filehandle is not None and not self._filehandle.closed:
                self._filehandle.close()
            if self._obj_path is not None and self._obj_path.exists():
                os.remove(self._obj_path)

    def _store_duplicate_copy(self, source_file: Path, hashkey: str) -> None:
        """This function is called (on Windows) when trying to store a file that already exists.

        In the `clean_storage` I will clean up old copies if the hash matches.
        """
        # Destination file starts with the hashkey, then has an dot as a separator, and is
        # followed by un UUID to make sure there is never a collision
        dest_file = self._duplicates_folder / f"{hashkey}.{uuid.uuid4().hex}"
        os.rename(source_file, dest_file)


class PackedObjectReader:
    """A class to read from a pack file.

    This ensures that the .read() method works and does not go beyond the
    length of the given object.
    """

    def __init__(self, fhandle: StreamSeekBytesType, offset: int, length: int) -> None:
        """
        Initialises the reader to a pack file.

        :param fhandle: an open handle to the pack file, must be opened in read and binary mode.
        :param offset: the integer offset where in the fhandle where the object starts.
        :param length: the integer length of the byte stream.
          The read() method will ensure that you never go beyond the given length.
        """
        assert "b" in fhandle.mode
        assert "r" in fhandle.mode

        self._fhandle = fhandle
        self._offset = offset
        self._length = length

        # Move to the offset position, and keep track of the internal position
        self._fhandle.seek(self._offset)
        self._update_pos()

    @property
    def mode(self) -> str:
        return self._fhandle.mode

    @staticmethod
    def seekable() -> bool:
        """Return whether object supports random access."""
        return True

    def seek(self, target: int, whence: int = 0) -> int:
        """Change stream position.

        Note that contrary to a standard file, also seeking beyond the borders will raise a ValueError.
        """
        if whence not in [0, 1, 2]:
            raise ValueError(
                "Invalid value for `whence`: only 0, 1 and 2 are currently implemented."
            )

        if whence in [0, 1]:
            if whence == 1:
                target = self.tell() + target

            if target < 0:
                raise ValueError(
                    "specified target would exceed the lower boundary of bytes that are accessible."
                )
            if target > self._length:
                raise ValueError(
                    "specified target would exceed the upper boundary of bytes that are accessible."
                )
            new_pos = self._offset + target
        else:
            # Seek relative to the end
            new_pos = self._offset + self._length + target

        self._fhandle.seek(new_pos)
        # Next function MUST be called every time we move into the _fhandle file, to update the position
        self._update_pos()

        # seek returns the new absolute position
        return target

    def tell(self) -> int:
        """Return current stream position, relative to the internal offset."""
        return self._fhandle.tell() - self._offset

    def _update_pos(self) -> None:
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

    def read(self, size: int = -1) -> bytes:
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

    def __enter__(self) -> PackedObjectReader:
        """Use as context manager."""
        return self

    def __exit__(self, exc_type, value, traceback) -> None:
        """Close context manager."""


class CallbackStreamWrapper:
    """A class to just wrap a read stream, but perform a callback every few bytes.

    Should be used only for streams open in read mode.
    """

    def __init__(
        self,
        stream: StreamSeekBytesType,
        callback: Callable | None,
        total_length: int = 0,
        description: str = "Streamed object",
    ) -> None:
        """
        Initialises the reader to a given stream.

        :param stream: an open stream
        :param callback: a callback to call to update the status (or None if not needed)
        :param total_length: the expected length
        """
        self._stream = stream
        self._callback = callback
        self._total_length = total_length
        self._description = description

        # Update at most 400 times, avoiding to increase CPU usage; if the list is small: every object.
        self._update_every: int = max(int(total_length / 400), 1) if total_length else 1
        # Counter of how many objects have been since since the last update.
        # A new callback will be performed when this value is > update_every.
        self._since_last_update: int = 0
        if self._callback:
            # If we have a callback, compute the total count of objects in this pack
            self._callback(
                action="init", value={"total": total_length, "description": description}
            )

    @property
    def mode(self) -> str:
        return self._stream.mode

    def seekable(self) -> bool:
        """Return whether object supports random access."""
        return self._stream.seekable()

    def seek(self, target: int, whence: int = 0) -> int:
        """Change stream position."""
        if target > self.tell():
            if self._callback:
                self._since_last_update = self._since_last_update + target - self.tell()
                if self._since_last_update >= self._update_every:
                    self._callback(action="update", value=self._since_last_update)
                    self._since_last_update = 0
        else:
            self.close_callback()
            if self._callback:
                # If we have a callback, compute the total count of objects in this pack
                self._callback(
                    action="init",
                    value={
                        "total": self._total_length,
                        "description": f"{self._description} [rewind]",
                    },
                )
                # Counter of how many objects have been since since the last update.
                # A new callback will be performed when this value is > update_every.
                self._since_last_update = target
                self._callback(action="update", value=self._since_last_update)

        return self._stream.seek(target, whence)

    def tell(self) -> int:
        """Return current stream position."""
        return self._stream.tell()

    def read(self, size: int = -1) -> bytes:
        """
        Read and return up to n bytes.

        If the argument is omitted, None, or negative, reads and
        returns all data until EOF (that corresponds to the length specified
        in the __init__ method).

        Returns an empty bytes object on EOF.
        """
        data = self._stream.read(size)

        if self._callback:
            self._since_last_update += len(data)
            if self._since_last_update >= self._update_every:
                self._callback(action="update", value=self._since_last_update)
                self._since_last_update = 0

        return data

    def __enter__(self) -> CallbackStreamWrapper:
        """Use as context manager."""
        return self

    def __exit__(self, exc_type, value, traceback) -> None:
        """Close context manager."""

    def close_callback(self) -> None:
        """
        Call the wrap up closing calls for the callback.

        .. note:: it DOES NOT close the stream.
        """
        if self._callback:
            # Final call to complete the bar
            if self._since_last_update:
                self._callback(action="update", value=self._since_last_update)
            # Perform any wrap-up, if needed
            self._callback(action="close", value=None)


def rename_callback(callback: Callable | None, new_description: str) -> Callable | None:
    """Given a callback, return a new one where the description will be changed to `new_name`.

    Works even if `callback` is None (in this case, it returns None).
    :param callback: a callback function.
    :param new_description: a string with a modified description for the callback.
        This will be replaced during the `init` call to the callback.
    """
    if callback is None:
        return None

    def wrapper_callback(action, value):
        """A wrapper callback with changed description."""
        if action == "init":
            new_value = value.copy()
            new_value["description"] = new_description
            return callback(action, new_value)  # type: ignore
        return callback(action, value)  # type: ignore

    return wrapper_callback


class ZlibLikeBaseStreamDecompresser(abc.ABC):
    """A class that gets a stream of compressed bytes, and returns the corresponding
    uncompressed bytes when being read via the .read() method.

    This is the base class. Define the `decompressobj_class` and `decompress_error` properties to implement concrete
    decompresser classes using specific algorithms that follow the zlib API.
    """

    _CHUNKSIZE = 524288

    def __init__(
        self,
        compressed_stream: StreamSeekBytesType,
        lazy_uncompressed_stream: LazyLooseStream | None = None,
    ) -> None:
        """Create the class from a given compressed bytestream.

        :param compressed_stream: an open bytes stream that supports the
            .read() method,
            returning a valid compressed stream.
        :param lazy_uncompressed_stream: A LazyLooseStream object, that points
            to the same data, but uncompressed.
            If not passed, some functionality will not be avaiable (e.g.
            seeking backward from the bottom of a file with `whence=2`).
            It is the responsibility of the caller to create and
            pass it, and to close it if it was ever opened by this class.
        """
        self._compressed_stream = compressed_stream
        self._decompressor = self.decompressobj_class()
        self._internal_buffer = b""
        self._pos = 0
        self._lazy_uncompressed_stream: None | (
            LazyLooseStream
        ) = lazy_uncompressed_stream
        # If True, this class just proxies request to the underlying
        # uncompressed stream
        self._use_uncompressed_stream: bool = False

    @property
    def mode(self) -> str:
        return getattr(self._compressed_stream, "mode", "rb")

    def read(self, size: int = -1) -> bytes:
        """
        Read and return up to n bytes.
        """
        # Once an uncompressed_stream is set, this is used and we
        # don't use anymore the compressed one.
        if self._use_uncompressed_stream:
            assert self._lazy_uncompressed_stream is not None, (
                "Using internally an uncompressed stream, but it is None! "
                "This should not happen"
            )
            return self._lazy_uncompressed_stream.read(size)
        return self._read_compressed(size)

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
            return b"".join(data)

        if size == 0:
            return b""

        while len(self._internal_buffer) < size:
            old_unconsumed = self._decompressor.unconsumed_tail
            next_chunk = self._compressed_stream.read(
                max(0, self._CHUNKSIZE - len(old_unconsumed))
            )

            # In the previous step, I might have some leftover data
            # since I am using the max_size parameter of .decompress()
            compressed_chunk = old_unconsumed + next_chunk
            # The second parameter is max_size. We know that in any case we do
            # not need more than `size` bytes. Leftovers will be left in
            # .unconsumed_tail and reused a the next loop
            try:
                decompressed_chunk = self._decompressor.decompress(
                    compressed_chunk, size
                )
            except self.decompress_error as exc:
                raise ValueError("Error while uncompressing data") from exc
            self._internal_buffer += decompressed_chunk

            if not next_chunk and not self._decompressor.unconsumed_tail:
                # Nothing to do: no data read, and the unconsumed tail is over.
                if self._decompressor.eof:
                    # Compressed file is over. We break
                    break
                raise ValueError(
                    "There is no data in the reading buffer, but we didn't reach the end of "
                    "the compressed stream: there must be a problem in the incoming buffer"
                )

        # Note that we could be here also with len(self._internal_buffer) < size,
        # if we used 'break' because the internal buffer reached EOF.
        to_return, self._internal_buffer = (
            self._internal_buffer[:size],
            self._internal_buffer[size:],
        )
        self._pos += len(to_return)

        return to_return

    def __enter__(self) -> ZlibLikeBaseStreamDecompresser:
        """Use as context manager."""
        return self

    def __exit__(self, exc_type, value, traceback) -> None:
        """Close context manager."""

    @property
    @abc.abstractmethod
    def decompressobj_class(self):
        """Return here the `decompressobj` class of the given compression type.

        Needs to be implemented by subclasses.
        """

    @property
    @abc.abstractmethod
    def decompress_error(self):
        """Return here the Exception (or tuple of exceptions) that need to be caught if there is a compression error.

        Needs to be implemented by subclasses.
        """

    @staticmethod
    def seekable() -> bool:
        """Return whether object supports random access."""
        return True

    def tell(self) -> int:
        """Return current position in file."""
        if self._use_uncompressed_stream:
            assert self._lazy_uncompressed_stream is not None, (
                "Using internally an uncompressed stream, but it is None! "
                "This should not happen"
            )
            return self._lazy_uncompressed_stream.tell()
        return self._pos

    def seek(self, target: int, whence: int = 0) -> int:
        """Change stream position.

        This will internally try to uncompress the whole file if certain conditions are met,
        typically when you are not accessing a file in a sequential order (e.g. with whence=1 or whence=2).
        """
        # First, assess if it's worth uncompressing.
        # Note that this is only possible when there is a container
        # attached to this decompresser. Otherwise, always resort
        # to the slow option or re-decompressing everything from
        # the very start.
        if whence not in [0, 1, 2]:
            raise ValueError(
                "Invalid value for `whence`: only 0, 1 and 2 are valid values."
            )
        # If we didn't switch to the uncompressed stream
        # but we are asking for a potential random-access position
        # we ask to materialize/open the uncompressed stream, and switch to it.
        # The conditions are:
        # - whence = 0 (seek from start of file) and looking for a previous position
        # - whence = 1 (seek relative to current position) and looking for a previous
        #   position (target < 0)
        # - whence = 2 (seek from the end of the file - in this case most probably we
        #   would have anyway to uncompress it all, so I trigger the creation of
        #   the loose uncompressed version)
        # Note that if there is no _lazy_uncompressed_stream specified, I just
        # do nothing; the _seek_internal method will decide if there are situations
        # it cannot deal with (e.g. whence = 2) and raise, or accept that in this
        # case some operations will be (much) slower, potentially requiring to
        # re-decompress the file when seeking backwards.
        should_uncompress = (
            whence == 2
            or (whence == 1 and target < 0)
            or (whence == 1 and target < self._pos)
        )
        if (
            not self._use_uncompressed_stream
            and self._lazy_uncompressed_stream is not None
            and should_uncompress
        ):
            # Request to open the uncompressed stream.
            # From now on, this class will directly proxy
            # tell/seek requests to the uncompressed stream
            self._lazy_uncompressed_stream.open_stream()
            # I move to the current position in the uncompressed stream
            self._lazy_uncompressed_stream.seek(self._pos, 0)
            self._use_uncompressed_stream = True

        return self._seek_internal(target, whence)

    def _seek_internal(self, target: int, whence: int = 0) -> int:
        """Change stream position.

        This should only be called internally.
        This uses the uncompressed stream if available, otherwise
        resorts to the compressed one that might be very slow
        when seeking backwards! Moreover, without uncompressed stream,
        it will not be possible to search from the end (whence=2).
        """
        read_chunk_size = 256 * 1024

        # NOTE: once the uncompressed stream has been materialized,
        # this will always be used and the seek position refers only
        # to it. So do NOT set back self._lazy_uncompressed_stream to None
        # as the underlying compressed stream might not be pointing
        # anymore to the correct position!

        # Seek to the desired location as requested
        # If we are using the uncompressed stream, I just proxy the request
        if self._use_uncompressed_stream:
            assert self._lazy_uncompressed_stream is not None, (
                "Using internally an uncompressed stream, but it is None! "
                "This should not happen"
            )
            return self._lazy_uncompressed_stream.seek(target, whence)

        # Here I implement the slow version without uncompressed stream
        if whence == 1:
            target = self.tell() + target
        if whence == 2:
            raise NotImplementedError(
                "Cannot seek backwards for a compressed stream without container support"
            )

        if target < 0:
            raise ValueError(f"negative seek position {target}")
        if target == 0:
            # Going back to zero it's efficient. I need to reset all internal variables, as in the init.
            self._compressed_stream.seek(0)
            self._decompressor = self.decompressobj_class()
            self._internal_buffer = b""
            self._pos = 0
            return 0

        if target < self.tell():
            # I cannot go backwards. In this case, I am forced to go back to zero and restart
            # (I always know how to go back to zero). Otherwise, I just continue from where I am.
            self.seek(0)

        # Read target bytes, but at most `read_chunk_size` at a time to avoid memory overflow
        while self.tell() < target:
            content = self.read(min(read_chunk_size, target - self.tell()))
            if not content:
                # If I am asking a position beyond the end, I stop to avoid infinite loops
                break
        # Differently than files, I return here the actual position
        return self._pos


class ZlibStreamDecompresser(ZlibLikeBaseStreamDecompresser):
    """A class that gets a stream of compressed bytes using ZLIB, and returns the corresponding
    uncompressed bytes when being read via the .read() method."""

    @property
    def decompressobj_class(self) -> Callable:
        """Return the `decompressobj` class of zlib."""
        return zlib.decompressobj

    @property
    def decompress_error(self) -> type[error]:
        """Return the zlib error raised when there is an error."""
        return zlib.error


def _get_compression_algorithm_info(algorithm: str):
    """Return a compresser and a decompresser for the given algorithm."""
    known_algorithms = {
        "zlib": {
            "compressobj": zlib.compressobj,
            "variant_name": "level",
            "variant_mapper": {str(i): i for i in range(1, 10)},  # from 1 to 9
            "decompresser": ZlibStreamDecompresser,
        }
    }

    algorithm_name, _, variant = algorithm.partition("+")
    try:
        algorithm_info = known_algorithms[algorithm_name]
    except KeyError:
        # pylint: disable=raise-missing-from)
        raise ValueError(
            f"Unknown or unsupported compression algorithm '{algorithm_name}'"
        )
    try:
        kwargs = {
            algorithm_info["variant_name"]: algorithm_info["variant_mapper"][variant]  # type: ignore
        }
        compresser = algorithm_info["compressobj"](**kwargs)  # type: ignore
    except KeyError:
        # pylint: disable=raise-missing-from
        raise ValueError(
            f"Invalid variant '{variant}' for compression algorithm '{algorithm_name}'"
        )

    decompresser = algorithm_info["decompresser"]

    return compresser, decompresser


def get_compressobj_instance(algorithm: str):
    """Return a compressobj class with a given algorithm.

    :param algorithm: A string defining the algorithm and its variant.
        The algorithm is split by a + sign from the variant.
        E.g. 'zlib+1' means using a level 1, while 'zlib+9' indicates a zlib compression with level 9
        (slower but compressing more).
    """
    return _get_compression_algorithm_info(algorithm)[0]


def get_stream_decompresser(algorithm: str) -> type[ZlibStreamDecompresser]:
    """Return a StreamDecompresser class with a given algorithm.

    :param algorithm: a compression algorithm (see `get_compressionobj_instance` for a description).
    """
    return _get_compression_algorithm_info(algorithm)[1]


class ZeroStream:
    """A class to return an (unseekable) stream returning only zeros, with length length."""

    def __init__(self, length: int) -> None:
        """
        Initialises the object and specifies the expected length.

        :param length: the integer length of the byte stream.
          The read() method will return this number of bytes.
        """
        self._length = length
        self._pos = 0

    @property
    def mode(self) -> str:
        return "rb"

    def read(self, size: int = -1) -> bytes:
        """
        Read and return up to n bytes (composed only of zeros).

        If the argument is omitted, None, or negative, reads and
        returns all data until EOF (that corresponds to the length specified
        in the __init__ method).

        Returns an empty bytes object on EOF.
        """
        # Check how many bytes are left on this portion of the pack
        # (avoid to go beyond)
        remaining_bytes = self._length - self._pos

        if size is None or size < 0:
            stream = b"\x00" * remaining_bytes
            self._pos += remaining_bytes
            return stream

        # Get the requested bytes, but at most the remaining_bytes
        bytes_to_fetch = min(remaining_bytes, size)
        stream = b"\x00" * bytes_to_fetch
        self._pos += bytes_to_fetch
        return stream


def is_known_hash(hash_type: str) -> bool:
    """Return True if the hash_type is known, False otherwise."""
    try:
        get_hash_cls(hash_type)
        return True
    except ValueError:
        return False


def get_hash_cls(hash_type: str) -> Callable:
    """Return a hash class with an update method and a hexdigest method."""
    known_hashes = {"sha1": hashlib.sha1, "sha256": hashlib.sha256}

    try:
        return known_hashes[hash_type]
    except KeyError:
        # pylint: disable=raise-missing-from
        raise ValueError(f"Unknown or unsupported hash type '{hash_type}'")


def _compute_hash_for_file(filepath: Path, hash_type: str) -> str | None:
    """Return the hash for the given file.

    Will read the file in chunks.

    :param filename: a filename to a file to check.
    :param hash_type: a valid string as recognised by the get_hash function
    :return: the hash hexdigest (the hash key), or `None` if the file does not exist
    """
    _chunksize = 524288

    hasher = get_hash_cls(hash_type)()
    try:
        with open(filepath, "rb") as fhandle:
            while True:
                chunk = fhandle.read(_chunksize)
                hasher.update(chunk)

                if not chunk:
                    # Empty returned value: EOF
                    break
    except FileNotFoundError:
        return None

    return hasher.hexdigest()


class HashWriterWrapper:
    """A class that gets a stream open in write mode and wraps it in a new class that computes a hash while writing."""

    def __init__(self, write_stream: BinaryIO, hash_type: str) -> None:
        """Create the class from a given compressed bytestream.

        :param write_stream: an open bytes stream that supports the .write() method.
           Must be a ``bytes`` stream (e.g., a file opened with ``b`` in the mode).
           Writes to this class will be forwarded to the write_stream, but will first
           be also passed to a hashlib implementation to compute the hash.
        """
        self._write_stream = write_stream
        assert "b" in self._write_stream.mode
        self._hash_type = hash_type

        self._hash = get_hash_cls(self._hash_type)()
        self._position = self._write_stream.tell()

    @property
    def hash_type(self) -> str:
        """Return the currently used hash type."""
        return self._hash_type

    def flush(self) -> None:
        """Flush the internal I/O buffer."""
        self._write_stream.flush()

    def write(self, data: bytes) -> int:
        """
        Write binary data to the underlying write_stream object, and compute a hash at the same time.
        """
        # This assert is important to avoid that there is an exception while writing.
        # In this case, the hash function does not get the data, but part of it might have already been
        # written to disk (e.g. a first chunk of bytes, and then the disk became full).
        # We want to make sure we are computing the correct hash.
        assert self._position == self._write_stream.tell(), (
            f"Error in the position ({self._position} vs {self._write_stream.tell()}), "
            "possibly an error occurred in a previous `write` call. "
            "This HashWriterMapper object is invalid and should not be used anymore"
        )

        self._write_stream.write(data)
        # Update the length after a successful write. Otherwise we will stay at the previous position.
        # If nothing was written, then the next call will succeed (the position remained the same).
        # If the call wrote something, the next call will correctly assert (there would be a mismatch
        # between the data on the write_stream and the one that was hashed).
        self._position += len(data)

        # Update the hash information
        self._hash.update(data)
        return self._position

    def hexdigest(self) -> str:
        """Return the hexdigest of the hash computed until now."""
        return self._hash.hexdigest()

    @property
    def closed(self) -> bool:
        """Return True if the underlying file is closed."""
        return self._write_stream.closed

    def close(self) -> None:
        """Close the underlying file."""
        self._write_stream.close()

    @property
    def mode(self) -> str:
        """Return a string with the mode the file was open with."""
        return self._write_stream.mode

    def fileno(self) -> int:
        """Return the integer file descriptor of the underlying file object."""
        return self._write_stream.fileno()


def chunk_iterator(iterator, size):
    """Given an iterator, split it in chunks of size `size` (except the last one, that can be shorter).

    Examples:

    - `list(chunk_iterator(range(10), 3))` returns `[(0, 1, 2), (3, 4, 5), (6, 7, 8), (9,)]`
    - `list(chunk_iterator(range(9), 3))` returns `[(0, 1, 2), (3, 4, 5), (6, 7, 8)]`

    :param iterator: an iterator to divide in chunks
    :param size: the size of each chunk
    """
    iterator = iter(iterator)
    return iter(lambda: tuple(itertools.islice(iterator, size)), ())


def safe_flush_to_disk(
    fhandle: StreamWriteBytesType | HashWriterWrapper,
    real_path: Path,
    use_fullsync: bool = False,
) -> None:
    """Tries to to its best to safely commit to disk.

    Note that calling this is needed to reduce the risk of data loss due to, e.g., a power failure.
    However, this call is typically expensive so should be called only if the guarantees are really needed, and
    as few times as possible.

    :param fhandle: an open file handle. Must support the `.fileno()` method and the `.flush()` method.
    :param real_path: the real path of the file. It must be ideally the absolute path. It is used (on POSIX) to find
        the parent folder and flush it too.
    :param use_fullsync: on Mac OS, runs a FULLSYNC to really push data to disk.
    """
    fileno = fhandle.fileno()

    # Flush buffers
    fhandle.flush()

    # Default fsync function, replaced on Mac OS X
    _fsync_function: Callable[
        [Any], Any
    ] = lambda fileno: os.fsync(  # pylint: disable=unnecessary-lambda
        fileno
    )

    # Flush to disk
    if hasattr(fcntl, "F_FULLFSYNC") is not None and (
        _MACOS_ALWAYS_USE_FULLSYNC or use_fullsync
    ):
        # This exists only on Mac OS X; See e.g. (link split on two lines, put them together):
        # https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/
        #          man2/fsync.2.html
        # that says:
        # > For applications that require tighter guarantees about the integrity of
        # > their data, Mac OS X provides the F_FULLFSYNC fcntl.  The F_FULLFSYNC
        # > fcntl asks the drive to flush all buffered data to permanent storage.
        # > Applications, such as databases, that require a strict ordering of writes
        # > should use F_FULLFSYNC to ensure that their data is written in the order
        # > they expect.  Please see fcntl(2) for more detail.
        # Replace the _fsync_function
        _fsync_function = (
            lambda fileno: fcntl.fcntl(  # pylint: disable=unnecessary-lambda-assignment
                fileno,
                F_FULLFSYNC,
            )
        )
    else:
        # In general this is the function to call
        _fsync_function(fileno)

    # Flush also the parent directory on posix, see e.g.
    # https://blog.gocept.com/2013/07/15/reliable-file-updates-with-python/
    if os.name == "posix":
        dirfd = os.open(real_path.parent, os.O_DIRECTORY)
        # Also here call the correct fsync function
        _fsync_function(dirfd)
        os.close(dirfd)


def compute_hash_and_size(
    stream: StreamReadBytesType,
    hash_type: str,
) -> tuple[str, int]:
    """Given a stream and a hash type, return the hash key (hexdigest) and the total size.

    :param stream: an open stream
    :param hash_type: the string with a name of a valid hash type
    :return: a tuple with ``(hash, size)`` where ``hash`` is the hexdigest and ``size`` is the size in bytes
    """
    _hash_chunksize = 524288
    hasher = get_hash_cls(hash_type)()

    # Read and hash all content
    size = 0
    while True:
        next_chunk = stream.read(_hash_chunksize)
        if not next_chunk:
            # Empty returned value: EOF
            break
        hasher.update(next_chunk)
        size += len(next_chunk)

    return hasher.hexdigest(), size


def detect_where_sorted(  # pylint: disable=too-many-branches, too-many-statements
    left_iterator: Iterable[Any],
    right_iterator: Iterable[Any],
    left_key: Callable | None = None,
) -> Iterator[tuple[Any, Location]]:
    """Generator that loops in alternation (but only once each) the two iterators and yields an element, specifying if
    it's only on the left, only on the right, or in both.

    .. note:: IMPORTANT! The two iterators MUST return unique and sorted results.

    .. note:: if it's on both, the one on the left is returned.

    This function will check and raise a ValueError if it detects non-unique or non-sorted elements.
    HOWEVER, this exception is raised only at the first occurrence of the issue, that can be very late in the execution,
    so if you process results in a streamed way, please ensure that you pass sorted iterators.

    :param left_iterator: a left iterator
    :param right_iterator: a right iterator
    :param left_key: if specified, it's a lambda that determines how to process each element
        of the left iterator when comparing with the right iterator. For instance, the left
        iterator might be a tuple, whose first element is a hash key, while the right iterator
        just a list of hash keys. In this case, left_key could be defined as a lambda returning
        the first element of the tuple.
        Note that when the element is in both iterators, the left one is returned (i.e. the
        full tuple, in this example).
    """
    left_exhausted = False
    right_exhausted = False

    if left_key is None:
        left_key = lambda x: x  # pylint: disable=unnecessary-lambda-assignment

    # Convert first in iterators (in case they are, e.g., lists)
    left_iterator = iter(left_iterator)
    right_iterator = iter(right_iterator)

    try:
        last_left = next(left_iterator)
    except StopIteration:
        left_exhausted = True

    try:
        last_right = next(right_iterator)
    except StopIteration:
        right_exhausted = True

    if left_exhausted and right_exhausted:
        # Nothing to be done, both iterators are empty
        return

    now_left = True
    if left_exhausted or (not right_exhausted and left_key(last_left) > last_right):
        now_left = False  # I want the 'current' (now) to be behind or at the same position of the other at any time

    while not (left_exhausted and right_exhausted):
        advance_both = False
        if now_left:
            if right_exhausted:
                yield last_left, Location.LEFTONLY
            else:
                if left_key(last_left) == last_right:
                    # They are equal: add to intersection and continue
                    yield last_left, Location.BOTH
                    # I need to consume and advance on both iterators at the next iteration
                    advance_both = True
                elif left_key(last_left) < last_right:
                    # the new entry (last_left) is still smaller: it's on the left only
                    yield last_left, Location.LEFTONLY
                else:
                    # the new entry (last_left) is now larger: then, last_right is only on the right
                    # and I switch to now_right
                    yield last_right, Location.RIGHTONLY
                    now_left = False
        else:
            if left_exhausted:
                yield last_right, Location.RIGHTONLY
            else:
                if left_key(last_left) == last_right:
                    # They are equal: add to intersection and continue
                    yield last_left, Location.BOTH
                    # I need to consume and advance on both iterators at the next iteration
                    advance_both = True
                elif left_key(last_left) > last_right:
                    # the new entry (last_right) is still smaller: it's on the right only
                    yield last_right, Location.RIGHTONLY
                else:
                    # the new entry (last_right) is now larger: then, last_left is only on the left
                    # and I switch to now_left
                    yield last_left, Location.LEFTONLY
                    now_left = True

        # When we are here: if now_left, then last_left has been inserted in one of the lists;
        # if not now_left, then last_right has been insterted in one of the lists.
        # If advance both, they both can be discarded. So if I exhausted an iterator, I am not losing
        # any entry.

        # I will need to cache the old value, see comments below in the `except StopIteration` block
        new_now_left = now_left
        if now_left or advance_both:
            try:
                new = next(left_iterator)
                if left_key(new) <= left_key(last_left):
                    raise ValueError(
                        "The left iterator does not return sorted unique entries, "
                        f"I got '{left_key(new)}' after '{left_key(last_left)}'"
                    )
                last_left = new
            except StopIteration:
                left_exhausted = True
                # I need to store in a different variable, otherwise in this case
                # I would also enter the next iteration even if advance_both is False!
                new_now_left = False

        if not now_left or advance_both:
            try:
                new = next(right_iterator)
                if new <= last_right:
                    raise ValueError(
                        f"The right iterator does not return sorted unique entries, I got '{new}' after '{last_right}'"
                    )
                last_right = new
            except StopIteration:
                right_exhausted = True
                # For consistency, also here I set new_now_left
                new_now_left = True

        # Set the new now_left value
        now_left = new_now_left


def yield_first_element(iterator: Iterable[Sequence]) -> Iterator[Any]:
    """Given an iterator that returns a tuple, return an iterator that yields only the first element of the tuple."""
    for elem in iterator:
        yield elem[0]


def merge_sorted(iterator1: Iterable[Any], iterator2: Iterable[Any]) -> Iterator[Any]:
    """Given two sorted iterators, return another sorted iterator being the union of the two."""
    for item, _ in detect_where_sorted(iterator1, iterator2):
        # Whereever it is (only left, only right, on both) I return the object.
        yield item


def should_compress(
    source_stream: StreamSeekBytesType,
    compress_mode: CompressMode,
    source_compressed: bool,
    source_length: int,
    source_size: int,
) -> bool:
    """Return a boolean determining if the source_stream should be compressed or not.

    :param source_stream: a seekable stream for which we should decide if we need to compress or not.
    :param compress_mode: the compress mode that should be honoured by should_compress (i.e., what
       the user asked for). E.g.:

       - If `compress_mode` is `CompressMode.YES`, the answer is always True.
       - If `compress_mode` is `CompressMode.NO`, the answer is always False.
       - If `compress_mode` is ``CompressMode.KEEP`, the answer is equal to the input value of `source_compressed`
         (i.e., the compression is unchanged)
       - If `compress_mode` is `CompressMode.AUTO`, the stream is analyzed in a not-too-expensive way to determine
         whether compression should be applied or not (i.e., if compressing will give a benefit or not).
    :param source_compressed: whether the source stream was already compressed
    :param source_length: the length (on disk, i.e. the compressed size if source_compressed is True) of
        the source_stream - can be used to quickly decide if compression is already efficient on this object.
    :param source_size: the uncompressed size of the source_stream - togetehr with source_length, can be used to
        quickly decide if compression is already efficient on this object.

    Note that in some cases this function will have to read parts of the stream to do some heuristics, so the stream
    needs to be readable and seekable (because at the end the stream will be put back in the same position as when
    we entered this method).
    """
    # It shoudl at least reduce by 10% to be worth compressing
    compression_threshold = 0.9

    if compress_mode == CompressMode.NO:
        return False
    if compress_mode == CompressMode.YES:
        return True
    if compress_mode == CompressMode.KEEP:
        # Use the same compression type
        return source_compressed
    if compress_mode == CompressMode.AUTO:
        if source_compressed:
            if source_size == 0:
                # Zero-length: I don't compress, useless and it
                # actually would occupy more space
                return False
            # Only compress if it's worth it
            return source_length / source_size < compression_threshold

        # As noted by @dev-zero in #14:
        #  > modern compression algorithms already automatically store uncompressed data if data is uncompressible
        #  > (see the various tuning knobs of LZMA/LZ4/XZ), if possible use one of those as they usually
        #  > already provide multithreaded implementations.
        # Therefore, in the future if we support those clever algorithms we can just skip this and let the algorithm
        # do its job.

        # Estimate the amount of compression we can get and decide whether to compress based on how much we can save.
        compression_ratio = estimate_compression(source_stream, source_size)
        return compression_ratio < compression_threshold
    raise NotImplementedError(f"Unknown {compress_mode=}")


def estimate_compression(stream: StreamSeekBytesType, size: int) -> float:
    """Tries to quickly estimate the compression ratio of the file.

    At the end the stream, put back at the same position as when we entered this method (i.e. we will seek back
    at the stream.tell() position that was set at the function enter).

    :param stream: a seekable stream.
    :param size: the total size of the stream (this is used to try to get small chunks of data from small
        random parts of the stream.
    :return: the ratio between the expected compressed size and the total file size. E.g. 1. means compressing
        does not provide any feedback, 0.5 means compression halves the files size, 0.1 means the compressed version
        only occupies 10% of the space, a value larger than 1 means that compressing actually increases the file size,
        etc. Note that this is only a quick estimate; actual compression levels might vary, but it is meant as a
        quick heuristics to decide whether we should compress or not, when CompressMode.AUTO is requested.
    """
    if size == 0:
        # Return a large value for zero-length files, so they are not even attempted to be compressed.
        return 1.0

    # Set some internal parameters
    sample_size = 1 * 1024  # Get this amount of consecutive bytes...
    # Only check a sampled_data of at most `max_sample_data_size` bytes (approximately)
    max_sampled_data_size = 131072  # 128kB
    # Approximately, except for rounding errors, get a small sample of size `sample_size` every so many bytes
    sample_interval = size // (max_sampled_data_size // sample_size)

    # Get the current pos (to go back to the same position at the end)
    initial_pos = stream.tell()
    # Go back to the beginning
    stream.seek(0)

    sampled_data = []
    total_length = 0
    # Only check the first part of the file
    while total_length < max_sampled_data_size:
        chunk = stream.read(sample_size)
        if not chunk:
            # EOF, stop
            break
        sampled_data.append(chunk)
        total_length += len(chunk)
        # Advance to the next sample of length SAMPLE_INTERVAL
        max_seek = size - stream.tell()
        # Never go back, and never go past the end of the file
        stream.seek(min(max_seek, max(0, sample_interval - len(chunk))), 1)
    # I now have the sample, I compress it and compare the size

    # I just want to know if it's compressible, I compress with some cheap ZLIB version,
    # Ideally this gives me a good estimate. Probably I could even do better, e.g. like BTRFS I
    # could estimate Shannon's entropy
    compresser = get_compressobj_instance("zlib+1")
    compressed = compresser.compress(b"".join(sampled_data))
    compressed += compresser.flush()

    # Since I have a guard above for small-size files, I never get here for
    # a sample of 0 bytes
    estimated = len(compressed) / total_length
    # Restore the stream to the initial position
    stream.seek(initial_pos)

    return estimated
