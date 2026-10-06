# NEXT-STEPS — url-shortener-platform

> Dibikin 2026-10-05 dari kondisi real repo (bukan dari janji docs).
> Prinsip: kerja kecil-kecil, verifikasi dulu baru bilang done. Lihat `AGENTS.md` Hard Rules.

## Posisi sekarang (ringkas)

- [x] M1 Backend 100%: create, redirect 307, analytics, health/ready, Redis, tests + `/metrics` (2026-10-05: instrumentator 8.1.0, 36 tests hijau).
- [x] M2 Frontend 100%: Vite Vue-TS + router + flow create/copy/analytics, 12 tests hijau, build sukses (2026-10-05).
- [x] M3 Compose 100%: redis + backend + frontend via Compose, persistensi terverifikasi (2026-10-05).
- [x] M4 Terraform 100%: `backend` + `redis` + network + volume via Docker provider. Belum ada frontend & monitoring.
- [x] M5 CI 100%: 4 workflow + Dependabot hijau di Actions (2026-10-05).
- [x] M6 Prometheus/Grafana 100%: scrape `backend:8000/metrics` 15s + 12-panel dashboard ke-provision, terverifikasi dengan traffic real (2026-10-05).
- [x] M7 Alertmanager 100%: `alerts.yml` (BackendDown, HighErrorRate, HighLatency, RedisDown) + `alertmanager.yml` + Compose wiring, BackendDown firing→resolved terverifikasi (2026-10-06).
- [ ] M8 Locust 0%: cuma `.gitkeep`, belum ada `locustfile.py`.
- [ ] M9 Failure injection 0%.
- [ ] M10 Security/release 30%: code aman, pipeline belum ada.

Jangan lompat ke observability/infra sebelum app-nya beres (lihat `docs/getting-started/roadmap-and-dod.md`).

---

## Step 0 — Tutup M1 sampai 100% (fondasi)

Tujuan: backend beneran observable, tests hijau di mesin lo.

- [x] 0.1 Tambah `prometheus-fastapi-instrumentator` ke `backend/requirements.txt`
- [x] 0.2 Instrumentasi di `backend/app/main.py` + expose `GET /metrics` (pastikan label bounded, jangan ada URL/target di label)
- [x] 0.3 Nyalakan Redis lokal: `docker start url-redis` kalau gagal `docker run -d --name url-redis -p 6379:6379 redis:7-alpine`
- [x] 0.4 Verifikasi:
  ```powershell
  backend\.venv\Scripts\python -m ruff check backend
  backend\.venv\Scripts\python -m pytest backend/tests -q
  Copy-Item .env.example .env  # pertama kali aja
  cd backend; .\.venv\Scripts\Activate.ps1; uvicorn app.main:app --port 8000
  # di terminal lain:
  Invoke-RestMethod http://localhost:8000/health
  Invoke-RestMethod http://localhost:8000/metrics | Select-Object -First 5
  ```
- DoD: `ruff` bersih, `pytest` hijau, `/health`, `/ready`, `/metrics` hidup. Update `AGENTS.md` centang M1 full + catat endpoint metrics di `docs/backend/api-contract.md` kalau berubah.

## Step 1 — M2 Frontend Vue (user flow dasar)

Tujuan: user bisa create → lihat short URL → copy → lihat analytics.

- [x] 1.1 Scaffold: `cd frontend; npm create vite@latest . -- --template vue-ts` lalu `npm install`
- [x] 1.2 Struktur sesuai `AGENTS.md`: `src/components/`, `src/views/`, `src/services/`, `src/composables/`, `src/types/`, `src/router/`
- [x] 1.3 Fitur minimal aja dulu (jangan custom alias, auth, dsb):
  - form create `POST /api/v1/urls`
  - tampil short_url + tombol copy
  - view analytics `GET /api/v1/urls/{code}/analytics`
  - loading state + error state (400 invalid, 404 not found, 503 redis down)
- [x] 1.4 Tambah `frontend/Dockerfile` (nginx / node build, non-root) + `.dockerignore`
- [x] 1.5 Verifikasi:
  ```powershell
  cd frontend; npm install; npm run dev
  cd frontend; npm test -- --run
  cd frontend; npm run build
  ```
- DoD: flow manual jalan lawan backend lokal, `npm test -- --run` hijau, `npm run build` sukses, typecheck lolos. Centang M2.

## Step 2 — M3 Docker Compose (backend + frontend + redis)

Tujuan: `docker compose up` jalanin semuanya.

- [x] 2.1 Tambah service `frontend` di `docker-compose.yml` (build `./frontend`, port misal `5173:80` atau `3000:80`, `depends_on: backend`)
- [x] 2.2 Tambah service `prometheus`, `grafana`, `alertmanager`? **Jangan dulu.** Compose M3 = app stack aja (redis+backend+frontend). Monitoring masuk Step 5.
- [x] 2.3 Cek persistensi: `redis-data` volume tetap, coba `down` (tanpa `-v`) lalu `up` data masih ada
- [x] 2.4 Verifikasi:
  ```powershell
  docker compose up -d --build
  docker compose ps
  Invoke-RestMethod http://localhost:8000/health
  Invoke-RestMethod http://localhost:8000/ready
  docker compose logs backend --tail 50
  docker compose down
  ```
- DoD: 3 service healthy, frontend bisa hit backend via Compose network, `down` tanpa `-v`. Centang M3. Update `README.md` kalau port / perintah berubah.

## Step 3 — M4 Terraform (reproduksi infra Compose)

Tujuan: Terraform bisa bikin stack yang sama tanpa tabrakan port dengan Compose.

- [x] 3.1 Tambah resource `docker_image` + `docker_container` buat `frontend` di `infra/terraform/main.tf` (nama konsisten: `url-shortener-tf-frontend`)
- [x] 3.2 Pisahkan port: jangan pakai 8000 bareng Compose. Pakai variable `backend_port`, `frontend_port`. Default TF beda (misal 8001/3001) atau matikan salah satu stack saat test.
- [x] 3.3 Jangan commit state: pastikan `terraform.tfstate*`, `tfplan`, `*.tfplan`, `*.tfvars` tetap di `.gitignore` (sekarang sudah benar, state lokal lo untracked — pertahankan)
- [x] 3.4 Verifikasi dari repo root:
  ```powershell
  .\scripts\dev.ps1 tf-fmt
  .\scripts\dev.ps1 tf-validate
  .\scripts\dev.ps1 tf-plan
  .\scripts\dev.ps1 tf-apply
  docker ps --format "{{.Names}} {{.Status}}"
  .\scripts\dev.ps1 tf-destroy  # ketik DESTROY saat diminta
  ```
- DoD: `validate` lolos, `plan` di-review, `apply` hasilkan backend+redis+frontend sehat, `destroy` bersih. Centang M4.

## Step 4 — M5 CI (validasi otomatis)

Tujuan: tiap push ke-check otomatis, jangan andalkan manual.

- [x] 4.1 Buat `.github/workflows/backend.yml`: `ruff check`, `pytest`, `pip-audit`
- [x] 4.2 Buat `.github/workflows/frontend.yml`: `npm ci`, `npm run lint` (kalau ada), `npm test -- --run`, `npm run build`
- [x] 4.3 Buat `.github/workflows/docker.yml`: `docker build backend`, `docker build frontend`, `docker compose config`
- [x] 4.4 Buat `.github/workflows/terraform.yml`: `terraform fmt -check`, `init`, `validate`, `plan` (tanpa apply)
- [x] 4.5 Set permissions least-privilege di tiap workflow (`permissions: contents: read` dsb)
- [x] 4.6 Verifikasi: push ke branch, lihat Actions hijau. Jangan merge kalau merah.
- DoD: 4 workflow hijau, scan jalan, permission minimal. Centang M5.

## Step 5 — M6 Observability (Prometheus + Grafana beneran guna)

Tujuan: metrik backend kelihatan, bukan sekadar up.

- [x] 5.1 `monitoring/prometheus/prometheus.yml`: scrape `backend:8000/metrics` tiap 15s
- [x] 5.2 Tambah service prometheus+grafana ke Compose **atau** TF (pilih satu buat lokal, jangan dua-duanya nyala bareng). Rekomendasi: Compose dulu. (Compose; port host 9090/3001 bind localhost)
- [x] 5.3 `monitoring/grafana/provisioning/` + 1 dashboard: request rate, error rate (5xx), latency p95, URL create vs redirect count, Redis error/down (jadi 12 panel termasuk p50/p99, analytics, application errors, target up, process memory)
- [x] 5.4 Pastikan label bounded (method, route, status — jangan `url`, `code`, `target`)
- [x] 5.5 Verifikasi:
  ```powershell
  docker compose up -d --build prometheus grafana
  Invoke-RestMethod http://localhost:9090/-/healthy
  Invoke-RestMethod http://localhost:3001/api/health   # Grafana (3000 sudah dipakai frontend)
  # bikin 5 short URL + 10 redirect, cek grafik naik
  ```
- DoD: Prometheus scrape sukses, dashboard tunjukin 4 panel di atas. Centang M6.

## Step 6 — M7 Alerting (deteksi failure beneran)

Tujuan: kalau backend/redis mati, lo tahu dari alert, bukan dari user komplain.

- [x] 6.1 `monitoring/prometheus/rules/*.yml`: alert `BackendDown`, `HighErrorRate`, `HighLatency`, `RedisDown`
- [x] 6.2 `monitoring/alertmanager/alertmanager.yml`: route default, receiver log/webhook dulu (jangan spam email/Slack asli buat belajar)
- [x] 6.3 Test dengan failure injection manual: `docker stop <backend>` → alert `BackendDown` firing → `docker start` → resolved
- [x] 6.4 Verifikasi: screenshot / log Alertmanager tunjukin firing → resolved
- DoD: 4 alert bisa firing & recovery terverifikasi. Centang M7.

## Step 7 — M8 Load test (Locust baseline + stress)

Tujuan: tahu batas wajar, bukan asal klaim "cepat".

- [ ] 7.1 `loadtest/locustfile.py`: 3 skenario — baseline (10 user), stress (naik bertahap), recovery (spike lalu turun). Target HANYA env lokal (`localhost:8000`). Kasih guard `--host` + peringatan jangan tembak URL publik.
- [ ] 7.2 Jalankan baseline, catat RPS, p95, error%
  ```powershell
  cd loadtest; locust -f locustfile.py --host http://localhost:8000
  ```
- [ ] 7.3 Simpan hasil ringkas (misal `loadtest/results/baseline.md` — angka + spek laptop, bukan log mentah 100MB)
- DoD: baseline + stress + recovery ada hasil angka. Centang M8.

## Step 8 — M9 Failure injection & recovery (QA)

Tujuan: buktiin sistem bisa pulih, bukan cuma jalan saat happy path.

- [ ] 8.1 Matikan Redis 30 detik → `POST /api/v1/urls` harus 503 `Storage unavailable`, lalu nyalakan → normal lagi tanpa restart backend manual
- [ ] 8.2 Matikan backend → frontend tampilkan error state (bukan blank), nyalakan → flow normal
- [ ] 8.3 `docker compose down` lalu `up -d` → data Redis persist (cek 1 short URL lama masih redirect)
- [ ] 8.4 Catat hasil di `docs/quality/qa-validation.md` (pass/fail + langkah)
- DoD: 3 skenario di atas lolos. Centang M9.

## Step 9 — M10 Security & release (kunci sebelum pamer)

Tujuan: layak di-share sebagai portfolio tanpa malu.

- [ ] 9.1 Scan: `pip-audit`, `npm audit`, `trivy image url-shortener-backend:dev`, `trivy image url-shortener-frontend:dev`. Fix high/critical atau catat justifikasi.
- [ ] 9.2 Aktifkan Dependabot (`dependabot.yml`) buat pip + npm + docker
- [ ] 9.3 Checklist `docs/quality/security.md` + `docs/governance/documentation-and-scope.md` §251: no secrets, CORS restricted, Redis tidak expose publik, error tidak bocor, log tidak ada secret, TF state ignored, Actions least-privilege
- [ ] 9.4 Release: tag `v0.1.0`, pastikan `README.md`, `.env.example`, `Makefile`, `scripts/dev.ps1` sinkron dengan perintah real
- [ ] 9.5 Update `AGENTS.md` Current Status centang M1-M10
- DoD: scan bersih (atau ada justifikasi tertulis), checklist §251 lolos, release reproducible. Centang M10.

---

## Cara pakai file ini

1. Kerjain berurutan Step 0 → 9. Jangan loncat.
2. Satu step = satu PR/commit kecil. Contoh: `feat(metrics): expose /metrics`.
3. Tiap step harus ada perintah verifikasi di atas yang lo jalanin dan paste hasilnya.
4. Kalau stuck >30 menit di satu checkbox, stop, catat error, tanya — jangan ubah kontrak API diam-diam (dilarang `AGENTS.md` Hard Rules).
5. File ini boleh dicoret (`- [x]`) sesuai progres. Itu satu-satunya file progress yang boleh di-edit manual. Jangan edit `scripts/.backend-progress.txt` manual.

Mau mulai dari Step 0.1 sekarang?
