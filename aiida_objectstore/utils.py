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
            raise IOError("File {} already open".format(self.path))
        self._fhandle = open(self.path, mode=self.mode)
        return self._fhandle
    
    def __exit__(self, exc_type, value, traceback):
        """Close the file when exiting the with context manager."""
        if self._fhandle is not None:
            if not self._fhandle.closed:
                self._fhandle.close()
        self._fhandle = None

