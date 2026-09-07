#!/usr/bin/env python3
"""Remove GPS/location EXIF and XMP from JPEG files. Keeps time and camera tags."""

from __future__ import annotations

import re
import struct
import sys
from pathlib import Path

GPS_IFD_TAG = 0x8825


def _u16(data: bytes, off: int, endian: str) -> int:
    return struct.unpack_from(endian + "H", data, off)[0]


def _u32(data: bytes, off: int, endian: str) -> int:
    return struct.unpack_from(endian + "I", data, off)[0]


def _type_size(typ: int) -> int:
    return {1: 1, 2: 1, 3: 2, 4: 4, 5: 8, 6: 1, 7: 1, 8: 2, 9: 4, 10: 8, 11: 4, 12: 8}.get(typ, 1)


def _zero_ifd_values(buf: bytearray, ifd_off: int, endian: str) -> None:
    if ifd_off <= 0 or ifd_off + 2 > len(buf):
        return
    count = _u16(buf, ifd_off, endian)
    for i in range(count):
        eoff = ifd_off + 2 + i * 12
        if eoff + 12 > len(buf):
            return
        typ = _u16(buf, eoff + 2, endian)
        cnt = _u32(buf, eoff + 4, endian)
        size = _type_size(typ) * cnt
        if size <= 4:
            buf[eoff + 8 : eoff + 12] = b"\x00\x00\x00\x00"
        else:
            val_off = _u32(buf, eoff + 8, endian)
            end = min(len(buf), val_off + size)
            if 0 <= val_off < len(buf):
                buf[val_off:end] = b"\x00" * (end - val_off)
            buf[eoff + 8 : eoff + 12] = b"\x00\x00\x00\x00"


def _remove_tag_from_ifd(buf: bytearray, ifd_off: int, tag: int, endian: str) -> None:
    if ifd_off <= 0 or ifd_off + 2 > len(buf):
        return
    count = _u16(buf, ifd_off, endian)
    for i in range(count):
        eoff = ifd_off + 2 + i * 12
        if eoff + 12 > len(buf):
            return
        if _u16(buf, eoff, endian) != tag:
            continue
        next_ifd_off = ifd_off + 2 + count * 12
        next_ifd = buf[next_ifd_off : next_ifd_off + 4]
        tail = buf[eoff + 12 : next_ifd_off]
        buf[eoff : eoff + len(tail)] = tail
        new_count = count - 1
        struct.pack_into(endian + "H", buf, ifd_off, new_count)
        new_next = ifd_off + 2 + new_count * 12
        buf[new_next : new_next + 4] = next_ifd
        return


def strip_gps_from_tiff(tiff: bytes) -> bytes:
    if len(tiff) < 8 or tiff[:2] not in (b"II", b"MM"):
        return tiff
    endian = "<" if tiff[:2] == b"II" else ">"
    if _u16(tiff, 2, endian) != 42:
        return tiff
    buf = bytearray(tiff)
    ifd0 = _u32(buf, 4, endian)
    if ifd0 + 2 > len(buf):
        return tiff

    count = _u16(buf, ifd0, endian)
    gps_off = None
    for i in range(count):
        eoff = ifd0 + 2 + i * 12
        if eoff + 12 > len(buf):
            break
        if _u16(buf, eoff, endian) == GPS_IFD_TAG:
            gps_off = _u32(buf, eoff + 8, endian)
            break

    if gps_off:
        _zero_ifd_values(buf, gps_off, endian)
    _remove_tag_from_ifd(buf, ifd0, GPS_IFD_TAG, endian)
    return bytes(buf)


def strip_gps_from_xmp(payload: bytes) -> bytes:
    nul = payload.find(b"\x00")
    if nul < 0:
        return payload
    header, xml = payload[: nul + 1], payload[nul + 1 :]
    try:
        text = xml.decode("utf-8")
    except UnicodeDecodeError:
        return payload
    text = re.sub(r"<[^:>\s]+:GPS[^>]*/>", "", text, flags=re.I)
    text = re.sub(r"<[^:>\s]+:GPS[^>]*>.*?</[^>]+>", "", text, flags=re.I | re.S)
    return header + text.encode("utf-8")


def strip_gps_from_jpeg(data: bytes) -> bytes:
    if data[:2] != b"\xff\xd8":
        raise ValueError("not a JPEG")
    out = bytearray(b"\xff\xd8")
    i = 2
    while i < len(data):
        if data[i] != 0xFF:
            raise ValueError("invalid JPEG marker")
        while i < len(data) and data[i] == 0xFF:
            i += 1
        if i >= len(data):
            break
        marker = data[i]
        i += 1
        if marker == 0xD9:
            out += b"\xff\xd9"
            break
        if marker == 0xDA or 0xD0 <= marker <= 0xD7:
            out += bytes([0xFF, marker])
            out += data[i:]
            break
        if i + 2 > len(data):
            break
        seglen = struct.unpack_from(">H", data, i)[0]
        payload = data[i + 2 : i + seglen]
        i += seglen
        if marker == 0xE1 and payload.startswith(b"Exif\x00\x00"):
            payload = b"Exif\x00\x00" + strip_gps_from_tiff(payload[6:])
        elif marker == 0xE1 and payload.startswith(b"http://ns.adobe.com/xap/1.0/\x00"):
            payload = strip_gps_from_xmp(payload)
        new_seg = bytes([0xFF, marker]) + struct.pack(">H", len(payload) + 2) + payload
        out += new_seg
    return bytes(out)


def strip_file(path: Path) -> bool:
    original = path.read_bytes()
    updated = strip_gps_from_jpeg(original)
    if updated == original:
        return False
    path.write_bytes(updated)
    return True


def main() -> int:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <jpeg> [jpeg...]", file=sys.stderr)
        return 1
    for arg in sys.argv[1:]:
        path = Path(arg)
        if not path.is_file():
            print(f"Error: file not found: {path}", file=sys.stderr)
            return 1
        strip_file(path)
        print(f"Stripped GPS from {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
