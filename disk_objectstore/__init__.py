"""An implementation of an efficient object store that writes directly on disk.

It does not require a server running.
"""
from .container import Container, ObjectType

__all__ = ('Container', 'ObjectType')

__version__ = '0.4.0'
