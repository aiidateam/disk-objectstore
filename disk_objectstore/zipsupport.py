"""
Utility module providing ZIP format support

Many of the functions are adapted from the zipfile stdlib
"""
import struct
import sys
import zipfile
from zipfile import ZIP64_LIMIT, ZIP_DEFLATED, ZIP_FILECOUNT_LIMIT, ZIP_STORED, ZipInfo

# pylint: disable=too-many-locals, invalid-name, protected-access, too-many-statements
_DD_SIGNATURE = 0x08074B50
_EXTRA_FIELD_STRUCT = struct.Struct("<HH")


def write_zip_header(fhandle, fname, compress_type=None):
    """Write a zip header to the handle"""
    zinfo = ZipInfo(fname)
    zinfo.flag_bits = 0x08
    compress_type_map = {"zlib": ZIP_DEFLATED, None: ZIP_STORED}
    zinfo.compress_type = compress_type_map[compress_type]
    header = zinfo.FileHeader(zip64=True)
    fhandle.write(header)


def write_file_describer(fhandle, crc, compressed_size, file_size):
    """Write the tailing descriptor"""
    fmt = "<LLQQ"  # ZIP64
    fhandle.write(struct.pack(fmt, _DD_SIGNATURE, crc, compressed_size, file_size))


def write_end_record(fhandle, zinfos):
    """
    Write the tailing central directory of contents and the end of zip-archive record
    """
    start_dir = fhandle.tell()
    COMMENT = "ZIP-compatible pack file by disk-objectstore"
    for zinfo in zinfos:  # write central directory
        dt = zinfo.date_time
        dosdate = (dt[0] - 1980) << 9 | dt[1] << 5 | dt[2]
        dostime = dt[3] << 11 | dt[4] << 5 | (dt[5] // 2)
        extra = []
        if zinfo.file_size > ZIP64_LIMIT or zinfo.compress_size > ZIP64_LIMIT:
            extra.append(zinfo.file_size)
            extra.append(zinfo.compress_size)
            file_size = 0xFFFFFFFF
            compress_size = 0xFFFFFFFF
        else:
            file_size = zinfo.file_size
            compress_size = zinfo.compress_size

        if zinfo.header_offset > ZIP64_LIMIT:
            extra.append(zinfo.header_offset)
            header_offset = 0xFFFFFFFF
        else:
            header_offset = zinfo.header_offset

        extra_data = zinfo.extra
        min_version = 0
        if extra:
            # Append a ZIP64 field to the extra's
            extra_data = _strip_extra(extra_data, (1,))
            extra_data = (
                struct.pack("<HH" + "Q" * len(extra), 1, 8 * len(extra), *extra)
                + extra_data
            )

            min_version = zipfile.ZIP64_VERSION  # type: ignore

        # if zinfo.compress_type == ZIP_BZIP2:
        #     min_version = max(BZIP2_VERSION, min_version)
        # elif zinfo.compress_type == ZIP_LZMA:
        #     min_version = max(LZMA_VERSION, min_version)

        extract_version = max(min_version, zinfo.extract_version)
        create_version = max(min_version, zinfo.create_version)
        try:
            filename, flag_bits = zinfo._encodeFilenameFlags()
            centdir = struct.pack(
                zipfile.structCentralDir,  # type: ignore
                zipfile.stringCentralDir,  # type: ignore
                create_version,
                zinfo.create_system,
                extract_version,
                zinfo.reserved,
                flag_bits,
                zinfo.compress_type,
                dostime,
                dosdate,
                zinfo.CRC,
                compress_size,
                file_size,
                len(filename),
                len(extra_data),
                len(zinfo.comment),
                0,
                zinfo.internal_attr,
                zinfo.external_attr,
                header_offset,
            )
        except DeprecationWarning:
            print(
                (
                    zipfile.structCentralDir,  # type: ignore
                    zipfile.stringCentralDir,  # type: ignore
                    create_version,
                    zinfo.create_system,
                    extract_version,
                    zinfo.reserved,
                    zinfo.flag_bits,
                    zinfo.compress_type,
                    dostime,
                    dosdate,
                    zinfo.CRC,
                    compress_size,
                    file_size,
                    len(zinfo.filename),
                    len(extra_data),
                    len(zinfo.comment),
                    0,
                    zinfo.internal_attr,
                    zinfo.external_attr,
                    header_offset,
                ),
                file=sys.stderr,
            )
            raise
        fhandle.write(centdir)
        fhandle.write(filename)
        fhandle.write(extra_data)
        fhandle.write(zinfo.comment)

    pos2 = fhandle.tell()

    # Write end-of-zip-archive record
    centDirCount = len(zinfos)
    centDirSize = pos2 - start_dir
    centDirOffset = start_dir

    requires_zip64 = None
    if centDirCount > ZIP_FILECOUNT_LIMIT:
        requires_zip64 = "Files count"
    elif centDirOffset > ZIP64_LIMIT:
        requires_zip64 = "Central directory offset"
    elif centDirSize > ZIP64_LIMIT:
        requires_zip64 = "Central directory size"
    if requires_zip64:
        # Need to write the ZIP64 end-of-archive records
        zip64endrec = struct.pack(
            zipfile.structEndArchive64,  # type: ignore
            zipfile.stringEndArchive64,  # type: ignore
            44,
            45,
            45,
            0,
            0,
            centDirCount,
            centDirCount,
            centDirSize,
            centDirOffset,
        )
        fhandle.write(zip64endrec)

        zip64locrec = struct.pack(
            zipfile.structEndArchive64Locator,  # type: ignore
            zipfile.stringEndArchive64Locator,  # type: ignore
            0,
            pos2,
            1,
        )
        fhandle.write(zip64locrec)
        centDirCount = min(centDirCount, 0xFFFF)
        centDirSize = min(centDirSize, 0xFFFFFFFF)
        centDirOffset = min(centDirOffset, 0xFFFFFFFF)

    endrec = struct.pack(
        zipfile.structEndArchive,  # type: ignore
        zipfile.stringEndArchive,  # type: ignore
        0,
        0,
        centDirCount,
        centDirCount,
        centDirSize,
        centDirOffset,
        len(COMMENT),
    )
    fhandle.write(endrec)
    fhandle.write(COMMENT.encode())
    fhandle.flush()


def _strip_extra(extra, xids):
    # Remove Extra Fields with specified IDs.
    unpack = _EXTRA_FIELD_STRUCT.unpack
    modified = False
    buffer = []
    start = i = 0
    while i + 4 <= len(extra):
        xid, xlen = unpack(extra[i : i + 4])
        j = i + 4 + xlen
        if xid in xids:
            if i != start:
                buffer.append(extra[start:i])
            start = j
            modified = True
        i = j
    if not modified:
        return extra
    return b"".join(buffer)


# Copied from zipfile.py
def is_zip(fpin):
    """This if a file is a ZIP archive"""
    # Determine file size
    fpin.seek(0, 2)
    filesize = fpin.tell()

    # Check to see if this is ZIP file with no archive comment (the
    # "end of central directory" structure should be the last item in the
    # file if this is the case).
    try:
        fpin.seek(-zipfile.sizeEndCentDir, 2)  # type: ignore
    except OSError:
        return False
    data = fpin.read()
    if (
        len(data) == zipfile.sizeEndCentDir  # type: ignore
        and data[0:4] == zipfile.stringEndArchive  # type: ignore
        and data[-2:] == b"\000\000"
    ):
        # the signature is correct and there's no comment, unpack structure
        return True

    # Either this is not a ZIP file, or it is a ZIP file with an archive
    # comment.  Search the end of the file for the "end of central directory"
    # record signature. The comment is the last item in the ZIP file and may be
    # up to 64K long.  It is assumed that the "end of central directory" magic
    # number does not appear in the comment.
    maxCommentStart = max(filesize - (1 << 16) - zipfile.sizeEndCentDir, 0)  # type: ignore
    fpin.seek(maxCommentStart, 0)
    data = fpin.read()
    start = data.rfind(zipfile.stringEndArchive)  # type: ignore
    if start >= 0:
        # found the magic number; attempt to unpack and interpret
        recData = data[start : start + zipfile.sizeEndCentDir]  # type: ignore
        if len(recData) != zipfile.sizeEndCentDir:  # type: ignore
            # Zip file is corrupted.
            return False
        return True

    # Unable to find a valid end of central directory structure
    return False
