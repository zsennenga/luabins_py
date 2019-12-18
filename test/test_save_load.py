from io import BytesIO
from typing import List, Any

import pytest

from luabins import encode_luabin, decode_luabin


def assert_save_load(value: List[Any], comparison_value=None):
    comparison_value = comparison_value or value
    assert decode_luabin(BytesIO(encode_luabin(value))) == comparison_value


def test_nil():
    assert_save_load([None])


def test_true():
    assert_save_load([True])


def test_false():
    assert_save_load([False])


def test_numbers():
    assert_save_load([0])
    assert_save_load([1])
    assert_save_load([-1])
    assert_save_load([0.0])
    assert_save_load([1.0])
    assert_save_load([-1.0])
    assert_save_load([0.5])
    assert_save_load([-0.5])


def test_string():
    assert_save_load([""])
    assert_save_load(["test"])


def test_table():
    assert_save_load([{}])
    assert_save_load([{"test": "test"}])
    assert_save_load([{1.0: "test"}])
    assert_save_load([{1.0: 0}])
    assert_save_load([{0: "test"}])
    assert_save_load([{0: 0.0}])
    assert_save_load([{True: True}])
    assert_save_load([{False: False}])
    assert_save_load([{"test": {"test": "test"}}])
    assert_save_load([[]], [{}])
    assert_save_load([["test"]], [{1.0: "test"}])


def test_errors():
    data = [i for i in range(252)]

    with pytest.raises(Exception):
        assert_save_load(data)

    with pytest.raises(Exception):
        assert_save_load([{None: "test"}])

    with pytest.raises(Exception):
        assert_save_load([float("bad")])
