"""
Definition of the dataclasses used as return values of
a number of methods.
"""
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING, List, Optional, Union

if TYPE_CHECKING:
    from container import ObjectType


@dataclass(frozen=True)
class ObjectCount:
    """Return the count of objects in a Container.

    :param loose: number of loose objects.
    :param packed: number of objects in pack files.
    :param pack_files: number of pack files in the container.
    """

    packed: int
    loose: int
    pack_files: int

    def __getitem__(self, item: str) -> int:
        """Return members using dictionary access.

        I.e., (self['key']) rather than self.key.
        """
        return asdict(self)[item]


@dataclass(frozen=True)
class ObjectMeta:
    """Metadata on a given object.

    :param type: always present. It is an ObjectType Enum whose values can be only one of the following strings:
        `loose`, `packed`, `missing`, where
         `missing` is returned for missing objects if `skip_if_missing` is False.
    :param size: the size of the object in bytes (i.e., `len(stream.read())`).
        Always present, set to None if `type` is `missing`.
    :param pack_id: the ID of the pack in which this object is stored.
        Set to `None` if `type` is not `packed`.
    :param pack_compressed: a boolean indicating if the object has been stored as compressed
        on disk or not
    :param pack_offset: the offset in the pack file. Set to `None` if `type` is not `packed`.
    :param pack_length: the size *on disk* of the object within the pack, in bytes.
        It is equal to `size` if `pack_compressed` is False, otherwise it can be different
        (in general smaller, but for small or uncompressible objects, even larger).
        Set to `None` if `type` is not `packed`.
    """

    type: "ObjectType"
    size: Optional[int]
    pack_id: Optional[str]
    pack_compressed: Optional[bool]
    pack_offset: Optional[int]
    pack_length: Optional[int]

    def __getitem__(self, item: str) -> Union[str, int, bool, None]:
        """Return members using dictionary access.

        I.e., (self['key']) rather than self.key.
        """
        return asdict(self)[item]


@dataclass(frozen=True)
class TotalSize:
    """Information on the total size of objects in a container.

    :param total_size_packed: size of the objects (before compressing)
        in the packs.
    :param total_size_packed_on_disk: size actually occupied on disk by
        the objects (including optional compression).
    :param total_size_packfiles_on_disk: size of the packs on disk
        (can be larger if objects are still in the packs but are not
        referenced anymore).
    :param total_size_packindexes_on_disk: size of the pack indexes on disk.
    :param total_size_loose: size of the loose objects in the packs
        (always uncompressed).
    """

    total_size_packed: int
    total_size_packed_on_disk: int
    total_size_packfiles_on_disk: int
    total_size_packindexes_on_disk: int
    total_size_loose: int

    def __getitem__(self, item: str) -> Union[str, int, bool, None]:
        """Return members using dictionary access.

        I.e., (self['key']) rather than self.key.
        """
        return asdict(self)[item]


@dataclass(frozen=True)
class ValidationIssues:
    """A class with issues found when validating a container.

    Every member is a list of hashes with the given error.

    :param invalid_hashes_loose: list of hashkeys for which the (re)computed
        hash does not match the hashkey (for loose objects)
    :param invalid_hashes_packed: list of hashkeys for which the (re)computed
        hash does not match the hashkey (for packed objects)
    :param invalid_sizes_packed: list of hashkeys for which the (re)computed
        size does not match the object size (this can happen for compressed
        objects)
    :param overlapping_packed: list of hashkeys for which the packed object
        have some overlap
    """

    invalid_hashes_loose: List[str]
    invalid_hashes_packed: List[str]
    invalid_sizes_packed: List[str]
    overlapping_packed: List[str]

    def __getitem__(self, item: str) -> Union[str, int, bool, None]:
        """Return members using dictionary access.

        I.e., (self['key']) rather than self.key.
        """
        return asdict(self)[item]

    def is_valid(self) -> bool:
        """Return True if this result of a validation has no issues.

        This happens if all lists are empty.
        If instead at least one list (of the fields if this dataclass)
        has at least one element, return False, as this means that there
        is at least one issue.
        """
        has_error = any(asdict(self).values())
        return not has_error
