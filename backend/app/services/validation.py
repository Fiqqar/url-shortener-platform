import re
from urllib.parse import urlparse

from app.core.exceptions import InvalidShortCodeError

CODE_RE = re.compile(r"^[0-9A-Za-z]{1,32}$")
MAX_URL_LENGTH = 2048


def validate_url(target: str) -> str:
    if not isinstance(target, str):
        raise ValueError("URL must be a string")
    target = target.strip()
    if not target or len(target) > MAX_URL_LENGTH:
        raise ValueError("URL length invalid")
    parsed = urlparse(target)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("URL must use http(s) with a valid host")
    return target


def validate_code(code: str) -> str:
    if not isinstance(code, str) or not CODE_RE.match(code):
        raise InvalidShortCodeError(f"Invalid short code: {code!r}")
    return code
