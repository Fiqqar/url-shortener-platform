import pytest

from app.core.base62 import ALPHABET, encode_base62


def test_examples_from_docs():
    assert encode_base62(1) == "1"
    assert encode_base62(10) == "A"
    assert encode_base62(61) == "z"
    assert encode_base62(62) == "10"


def test_zero():
    assert encode_base62(0) == ALPHABET[0]


def test_roundtrip_grows():
    assert encode_base62(62) == "10"
    assert encode_base62(62 * 62) == "100"


def test_rejects_negative():
    with pytest.raises(ValueError):
        encode_base62(-1)


def test_rejects_non_int():
    with pytest.raises(TypeError):
        encode_base62("1")
