FROM python:3.13-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY --from=builder /install /usr/local
COPY app ./app

# Patch packages that arrive via the base image with known HIGH CVEs
# (libpcre2-8-0, msgpack, urllib3, setuptools are not in our dependency
# tree: the app serves traffic without them). This must run in the final
# stage: a builder-stage install cannot remove the base layer's stale
# dist-info files because the COPY overlay only adds files, while pip/apt
# here act on the final filesystem directly. Lower bounds keep working if
# a newer base already ships fixed versions.
RUN apt-get update \
    && apt-get install -y --no-install-recommends --only-upgrade libpcre2-8-0 \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --break-system-packages \
        "msgpack>=1.2.1" \
        "urllib3>=2.8.0" \
        "setuptools>=78.1.1"

RUN useradd --create-home appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
