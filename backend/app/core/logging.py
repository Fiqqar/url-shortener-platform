import logging
import sys

_configured = False


def configure_logging(level: str = "INFO") -> None:
    global _configured
    if _configured:
        return
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(message)s "
        "%(method)s %(path)s %(status_code)s %(duration_ms)s %(request_id)s",
        stream=sys.stdout,
    )
    _configured = True


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
