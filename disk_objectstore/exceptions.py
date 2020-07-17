"""Custom exceptions raised by the objesctore implementation."""


class NotExistent(Exception):
    """Raised if the request object does not exist."""


class NotInitialised(Exception):
    """Raised if you are trying to perform an operation on a container that is not yet initialised."""


class ModificationNotAllowed(Exception):
    """Raised if you are trying to modify an object but you are not allowed to do so."""


class ClosingNotAllowed(Exception):
    """Raised if you manually close a ObjectWriter instead of letting it be closed by the context manager."""


class InconsistentContent(Exception):
    """Raised if the content of the repository is inconsistent and there is no way to automatically recover from it.

    This should really never happen, if it happens it might either be a bug in the implementation, some serious
    problem e.g. with your disk, or someone accessing the directory manually and modifying the files.
    """
