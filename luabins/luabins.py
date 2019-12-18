import math
from io import BytesIO
from typing import Any, List, Dict

from luabins.byte_utils import _read_int, _read_short_short_int, _read_number, _read_string, _build_number, \
    _build_string
from luabins.constants import *


def _read_table(stream: BytesIO) -> Dict[Any, Any]:
    table = {}

    array_size = _read_int(stream)
    hash_size = _read_int(stream)
    total_size = array_size + hash_size

    if array_size < 0 or hash_size < 0:
        raise Exception("Invalid table sizes")

    for i in range(total_size):
        key = _load_value(stream)
        if key is None:
            raise Exception("Key in a table cannot be none")
        elif isinstance(key, float) and math.isnan(key):
            raise Exception("Key may not be NaN")
        table[key] = _load_value(stream)

    return table


def _build_table(table: Dict[Any, Any]) -> bytes:
    # This isn't TOTALLY accurate, but it's also not important that it's perfect
    array_size = len([key for key in table.keys() if isinstance(key, int)])
    hash_size = len(table.keys()) - array_size

    result = array_size.to_bytes(LUA_INT_LENGTH, LUA_BYTEORDER) + hash_size.to_bytes(LUA_INT_LENGTH, LUA_BYTEORDER)

    for (key, value) in table.items():
        result += _save_value(key)
        result += _save_value(value)

    return result


def _load_value(stream: BytesIO) -> Any:
    value_type = _read_short_short_int(stream)

    if value_type == LUABINS_NIL:
        return None
    elif value_type == LUABINS_FALSE:
        return False
    elif value_type == LUABINS_TRUE:
        return True
    elif value_type == LUABINS_NUMBER:
        return _read_number(stream)
    elif value_type == LUABINS_STRING:
        return _read_string(stream)
    elif value_type == LUABINS_TABLE:
        return _read_table(stream)
    else:
        raise Exception(f"Unknown type {value_type}")


def _save_value(value: Any) -> bytes:
    if value is None:
        return LUABINS_NIL.to_bytes(1, LUA_BYTEORDER)
    if value is False:
        return LUABINS_FALSE.to_bytes(1, LUA_BYTEORDER)
    if value is True:
        return LUABINS_TRUE.to_bytes(1, LUA_BYTEORDER)
    if isinstance(value, (int, float)):
        return LUABINS_NUMBER.to_bytes(1, LUA_BYTEORDER) + _build_number(float(value))
    if isinstance(value, str):
        return LUABINS_STRING.to_bytes(1, LUA_BYTEORDER) + _build_string(value)
    if isinstance(value, dict):
        return LUABINS_TABLE.to_bytes(1, LUA_BYTEORDER) + _build_table(value)
    if isinstance(value, list):
        as_dict = {index + 1: value_at_index for (index, value_at_index) in enumerate(value)}
        return LUABINS_TABLE.to_bytes(1, LUA_BYTEORDER) + _build_table(as_dict)
    else:
        raise Exception(f"Unknown type {type(value)}")


def decode_luabins(stream: BytesIO) -> List[Any]:
    num_items = _read_short_short_int(stream)

    if num_items > 250:
        raise Exception("Max items in a serialized blob for luabin is 250")

    values = []

    for i in range(num_items):
        values.append(_load_value(stream))

    if len(stream.read(1)) != 0:
        raise Exception(f"Read {num_items} values, but we still have more data in the stream! Data corrupt?")

    return values


def encode_luabins(values: List[Any]) -> bytes:
    output = len(values).to_bytes(1, LUA_BYTEORDER)

    for value in values:
        output += _save_value(value)

    return output
