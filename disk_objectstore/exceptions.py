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


class DynamicInconsistentContent(InconsistentContent):
    """Raised if the content of the repository is inconsistent and this happens while generating the content.

    This should really never happen, and the same notes hold as the for the parent class ``InconsistentContent``.
    However, this exception is raised specifically when the content was being operated on, e.g. when
    trying to replace an object and failing to do so (while the base class can be raised also when the static
    content is corrupt). So this exception is transient and might be solved by just retrying the operation.
    However, since this exception should not really happen, it's better not to ignore it, but to investigate
    why it has been raised.
    """
