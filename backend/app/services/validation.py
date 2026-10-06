import ipaddress
import re
from urllib.parse import urlsplit, urlunsplit

from app.core.exceptions import InvalidShortCodeError
from app.core.url_limits import MAX_URL_LENGTH

CODE_RE = re.compile(r"^[0-9A-Za-z]{1,32}$")
_HOST_LABEL_RE = re.compile(r"^(?!-)[a-z0-9-]{1,63}(?<!-)$")
_WS_OR_CONTROL_RE = re.compile(r"[\s\x00-\x1f\x7f]")


def _validate_hostname(hostname: str) -> str:
    # IP literals (v4/v6) are valid hosts as-is.
    try:
        ipaddress.ip_address(hostname)
        return hostname
    except ValueError:
        pass
    # IDN: normalize Unicode via IDNA; rejects invalid Unicode hostnames.
    try:
        encoded = hostname.encode("idna").decode("ascii")
    except UnicodeError as exc:
        raise ValueError("URL host is not valid IDN") from exc
    candidate = encoded.lower()
    # Allow single trailing dot (FQDN root).
    if candidate.endswith("."):
        candidate = candidate[:-1]
    if not candidate or len(candidate) > 253:
        raise ValueError("URL host length invalid")
    if candidate.replace(".", "").isdigit():
        raise ValueError("URL IP address invalid")
    for label in candidate.split("."):
        if not _HOST_LABEL_RE.match(label):
            raise ValueError("URL host label invalid")
    return encoded.lower()


def validate_url(target: str) -> str:
    if not isinstance(target, str):
        raise ValueError("URL must be a string")
    target = target.strip()
    if not target or len(target) > MAX_URL_LENGTH:
        raise ValueError("URL length invalid")
    if _WS_OR_CONTROL_RE.search(target):
        raise ValueError("URL must not contain whitespace or control characters")
    parsed = urlsplit(target)
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError("URL must use http(s) with a valid host")
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must use http(s) with a valid host")
    if "@" in parsed.netloc:
        raise ValueError("URL user information is not allowed")
    try:
        port = parsed.port
    except ValueError as exc:
        raise ValueError("URL port invalid") from exc
    if port is not None and not 1 <= port <= 65535:
        raise ValueError("URL port invalid")
    ascii_hostname = _validate_hostname(hostname)
    if parsed.netloc.startswith("["):
        closing_bracket = parsed.netloc.find("]")
        if closing_bracket < 0 or ":" not in hostname:
            raise ValueError("URL IPv6 host invalid")
        port_suffix = parsed.netloc[closing_bracket + 1 :]
        host = f"[{ascii_hostname}]"
    else:
        raw_host, separator, raw_port = parsed.netloc.partition(":")
        port_suffix = f":{raw_port}" if separator else ""
        host = ascii_hostname
    if port_suffix and (port is None or not port_suffix.startswith(":")):
        raise ValueError("URL port invalid")
    if not parsed.netloc.startswith("[") and raw_host.lower() != hostname.lower():
        raise ValueError("URL host invalid")
    canonical_netloc = f"{host}{port_suffix}"
    canonical = urlunsplit(
        (parsed.scheme, canonical_netloc, parsed.path, parsed.query, parsed.fragment)
    )
    if len(canonical) > MAX_URL_LENGTH:
        raise ValueError("URL length invalid")
    return canonical


def validate_code(code: str) -> str:
    if not isinstance(code, str) or not CODE_RE.match(code):
        raise InvalidShortCodeError(f"Invalid short code: {code!r}")
    return code
