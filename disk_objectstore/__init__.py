"""An implementation of an efficient object store that writes directly on disk.

It does not require a server running.
"""

import logging

from .container import CompressMode, Container, ObjectType

LOGGER = logging.getLogger(__name__)

__all__ = ('CompressMode', 'Container', 'ObjectType')

__version__ = '1.3.0'
