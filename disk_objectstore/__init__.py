"""An implementation of an efficient object store that writes directly on disk.

It does not require a server running.
"""
from .container import CompressMode, Container, ObjectType

__all__ = ("Container", "ObjectType", "CompressMode")

__version__ = "0.6.0"
