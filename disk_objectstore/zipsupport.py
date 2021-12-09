import struct
import sys
import zipfile
from zipfile import (
    ZIP64_LIMIT,
    ZIP64_VERSION,
    ZIP_DEFLATED,
    ZIP_FILECOUNT_LIMIT,
    ZIP_STORED,
    ZipInfo,
)

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

            min_version = ZIP64_VERSION

        # if zinfo.compress_type == ZIP_BZIP2:
        #     min_version = max(BZIP2_VERSION, min_version)
        # elif zinfo.compress_type == ZIP_LZMA:
        #     min_version = max(LZMA_VERSION, min_version)

        extract_version = max(min_version, zinfo.extract_version)
        create_version = max(min_version, zinfo.create_version)
        try:
            filename, flag_bits = zinfo._encodeFilenameFlags()
            centdir = struct.pack(
                zipfile.structCentralDir,
                zipfile.stringCentralDir,
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
                    zipfile.structCentralDir,
                    zipfile.stringCentralDir,
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
            zipfile.structEndArchive64,
            zipfile.stringEndArchive64,
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
            zipfile.structEndArchive64Locator,
            zipfile.stringEndArchive64Locator,
            0,
            pos2,
            1,
        )
        fhandle.write(zip64locrec)
        centDirCount = min(centDirCount, 0xFFFF)
        centDirSize = min(centDirSize, 0xFFFFFFFF)
        centDirOffset = min(centDirOffset, 0xFFFFFFFF)

    endrec = struct.pack(
        zipfile.structEndArchive,
        zipfile.stringEndArchive,
        0,
        0,
        centDirCount,
        centDirCount,
        centDirSize,
        centDirOffset,
        len(COMMENT),
    )
    fhandle.write(endrec)
    fhandle.write(COMMENT)
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
