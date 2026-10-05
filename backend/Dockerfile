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

# Harden the final image against stale/vendored package metadata.
# The base layer and the builder overlay can each contribute a versioned
# dist-info dir (e.g. msgpack-1.1.2 AND msgpack-1.2.3); pip considers the
# requirement satisfied by the newer copy and never removes the stale one,
# but Trivy scans every dist-info (and any SBOM) it finds. None of
# libpcre2-8-0/msgpack/urllib3/setuptools/pip are needed at runtime - the
# app serves traffic without them - so purge all copies from site-packages
# (a no-op for paths that do not exist), drop the pip tooling entirely,
# and keep only the OS security upgrade.
RUN apt-get update \
    && apt-get install -y --no-install-recommends --only-upgrade libpcre2-8-0 \
    && rm -rf /var/lib/apt/lists/* \
    && python -c "import glob, os, shutil, site; [(shutil.rmtree(p, ignore_errors=True) if os.path.isdir(p) else os.remove(p)) for sp in site.getsitepackages() for pat in ('msgpack*', 'urllib3*', 'setuptools*', 'pkg_resources*', '*.cdx.json') for p in glob.glob(sp + '/' + pat)]; shutil.rmtree('/usr/local/lib/python3.13/ensurepip', ignore_errors=True)" \
    && pip uninstall -y pip

RUN useradd --create-home appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
