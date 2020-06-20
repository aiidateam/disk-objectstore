"""An implementation of an efficient object store that writes directly on disk.

It does not require a server running.
"""
from .container import Container

__all__ = ('Container',)

__version__ = '0.3.0'
