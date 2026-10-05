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
# tree: the app serves traffic without them). The stale copies must be
# deleted first: the base layer and the builder overlay each contribute a
# versioned dist-info dir (e.g. msgpack-1.1.2 AND msgpack-1.2.3), and pip
# considers the requirement satisfied by the newer copy, so it never
# removes the stale one - but Trivy scans every dist-info it finds.
# Purging by name is a no-op for paths that do not exist, and reinstalling
# the fixed versions keeps the image working if a future dependency needs
# these packages.
RUN apt-get update \
    && apt-get install -y --no-install-recommends --only-upgrade libpcre2-8-0 \
    && rm -rf /var/lib/apt/lists/* \
    && python -c "import glob, shutil, site; [shutil.rmtree(p) for sp in site.getsitepackages() for pat in ('msgpack*', 'urllib3*', 'setuptools*', 'pkg_resources*') for p in glob.glob(sp + '/' + pat)]" \
    && pip install --no-cache-dir --break-system-packages \
        "msgpack>=1.2.1" \
        "urllib3>=2.8.0" \
        "setuptools>=78.1.1"

RUN useradd --create-home appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
