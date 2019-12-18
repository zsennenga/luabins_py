import os

from luabins import decode_luabin, encode_luabin


def open_and_assert(filename, expected):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, "rb") as f:
        assert decode_luabin(f) == expected

    path = os.path.join(os.path.dirname(__file__), "output_" + filename)
    with open(path, "wb") as f:
        f.write(encode_luabin(expected))


def test_integration():
    open_and_assert("basic.bin", [1, "two", {1.0: "three", 2.0: 4}])
    open_and_assert("basic2.bin", [1, "two", {1.0: "three", 2.0: 4.0}])
    open_and_assert("basic3.bin", [1, "two", {1.0: "three", 2.0: {1.0: "four", 2.0: 4.0}}])
    open_and_assert("basic4.bin", [None, True, False])
    open_and_assert("basic5.bin", [{"test": "test"}])




