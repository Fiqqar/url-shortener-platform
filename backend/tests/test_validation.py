import pytest

from app.core.exceptions import InvalidShortCodeError
from app.services.validation import validate_code, validate_url


def test_accepts_http_and_https():
    assert validate_url("https://example.com/a") == "https://example.com/a"
    assert validate_url("http://example.com") == "http://example.com"


def test_rejects_bad_scheme():
    with pytest.raises(ValueError):
        validate_url("ftp://example.com/file")


def test_rejects_missing_host():
    with pytest.raises(ValueError):
        validate_url("https:///no-host")


def test_rejects_empty_and_too_long():
    with pytest.raises(ValueError):
        validate_url("")
    with pytest.raises(ValueError):
        validate_url("https://example.com/" + "x" * 3000)


def test_accepts_mixed_case_scheme_trailing_dot_and_idn():
    assert validate_url("HTTPS://example.com./a") == "https://example.com./a"
    assert validate_url("https://例え.テスト/path").startswith("https://xn--")
    assert validate_url("https://[::1]:8443/path") == "https://[::1]:8443/path"


@pytest.mark.parametrize(
    "target",
    [
        "https://user:password@example.com/",
        "https://-bad.example/",
        "https://example..com/",
        "https://example.com:/",
        "https://example.com:65536/",
        "https://999.999.999.999/",
        "https://exa mple.com/",
    ],
)
def test_rejects_ambiguous_or_invalid_authority(target):
    with pytest.raises(ValueError):
        validate_url(target)


def test_valid_codes():
    assert validate_code("aB3xY7") == "aB3xY7"


def test_invalid_codes():
    for bad in ["", "a b", "a/b", "a+b", "x" * 33, "é"]:
        with pytest.raises(InvalidShortCodeError):
            validate_code(bad)
