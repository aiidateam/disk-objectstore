"""An implementation of an efficient object store that writes directly on disk.

It does not require a server running.
"""
from .container import Container, ObjectType, CompressMode

__all__ = ('Container', 'ObjectType', 'CompressMode')

__version__ = '0.5.0'
