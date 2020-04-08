"""Custom exceptions raised by the objesctore implementation."""


class NotExistent(Exception):
    """Raised if the request object does not exist."""


class NotInitialised(Exception):
    """Raised if you are trying to perform an operation on a container that is not yet initialised."""


class ModificationNotAllowed(Exception):
    """Raised if you are trying to modify an object but you are not allowed to do so."""
