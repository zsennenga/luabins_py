import os
from io import BytesIO

from luabins import decode_luabins, encode_luabins


def test_debug():
    path = os.path.join(os.path.dirname(__file__), "debug.bin")
    with open(path, "rb") as f:
        orig = f.read()
        decode1 = decode_luabins(BytesIO(orig))
        re_encoded = encode_luabins(decode1)
        decode2 = decode_luabins(BytesIO(re_encoded))
        assert decode2 == decode1
