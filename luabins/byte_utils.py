import struct
from io import BytesIO

from luabins.constants import *


def _read_bytes_or_raise(stream: BytesIO, num_bytes: int) -> bytes:
    ret_bytes = stream.read(num_bytes)

    if len(ret_bytes) != num_bytes:
        raise Exception(f"Tried to get {num_bytes} but got {len(ret_bytes)}")

    return ret_bytes


def _read_short_short_int(stream: BytesIO) -> int:
    return int.from_bytes(_read_bytes_or_raise(stream, LUA_SHORT_SHORT_INT_LENGTH), LUA_BYTEORDER)


def _read_int(stream: BytesIO) -> int:
    return int.from_bytes(_read_bytes_or_raise(stream, LUA_INT_LENGTH), LUA_BYTEORDER)


def _read_number(stream: BytesIO) -> float:
    return struct.unpack("<d", _read_bytes_or_raise(stream, LUA_NUMBER_LENGTH))[0]


def _read_string(stream: BytesIO) -> str:
    length = _read_int(stream)

    string_bytes = _read_bytes_or_raise(stream, length)

    return string_bytes.decode(LUA_STR_ENCODING)


def _build_short_short_int(value: int) -> bytes:
    return value.to_bytes(LUA_SHORT_SHORT_INT_LENGTH, LUA_BYTEORDER)


def _build_int(value: int) -> bytes:
    return value.to_bytes(LUA_INT_LENGTH, LUA_BYTEORDER)


def _build_number(value: float) -> bytes:
    return struct.pack("<d", value)


def _build_string(value: str) -> bytes:
    len_bytes = len(value).to_bytes(LUA_INT_LENGTH, LUA_BYTEORDER)
    str_bytes = value.encode(LUA_STR_ENCODING)

    return len_bytes + str_bytes
