import logging
import sys

from app.core.request_context import request_id_context

_configured = False


class _RequestContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        for field in ("method", "path", "status_code", "duration_ms"):
            if not hasattr(record, field):
                setattr(record, field, "-")
        if not hasattr(record, "request_id"):
            record.request_id = request_id_context.get()
        return True


def configure_logging(level: str = "INFO") -> None:
    global _configured
    if _configured:
        return
    handler = logging.StreamHandler(sys.stdout)
    handler.addFilter(_RequestContextFilter())
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s %(message)s "
            "%(method)s %(path)s %(status_code)s %(duration_ms)s %(request_id)s"
        )
    )
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        handlers=[handler],
    )
    _configured = True


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
