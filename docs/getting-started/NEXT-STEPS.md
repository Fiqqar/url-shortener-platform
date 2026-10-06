# NEXT-STEPS — url-shortener-platform

> Updated 2026-10-06. The original milestone checklist is complete; `AGENTS.md` is the current status source. “All milestones done” means the learning-project deliverables were implemented and exercised. It does not mean this repository is production-ready for public traffic.

## Status

All ten milestones in `AGENTS.md` are checked. The previously verified baseline is 38 backend tests and 12 frontend tests; Locust recorded about 32 RPS at 10 users and 313 RPS at 100 users with no failures; backend-down, Redis-down, and monitoring-restart recovery drills passed. These are the recorded project results, not a guarantee for another host or deployment.

## Current follow-up work

1. Keep the public-create endpoint rate limited before exposing it to untrusted traffic. It has no authentication, quota, or per-client creation limit.
2. Decide Redis retention and backup/restore before storing valuable links. Local Compose/Terraform now cap Redis at `256mb` by default with `noeviction`, but URL and click keys have no expiry and there is no backup/restore automation.
3. Keep release verification and normal CI aligned. The tag workflow reruns backend and frontend checks on the tagged commit before publishing; it intentionally repeats these checks rather than trusting a different ref's workflow status.
4. Rebuild the frontend image when changing its API origin: `VITE_API_BASE_URL` is compiled into the Vite bundle at image build time.
5. Re-run the affected checks after changes. From the repository root, the Makefile targets are the source of truth for local commands; `AGENTS.md` documents their PowerShell equivalents.

These are focused follow-ups. They do not require Kubernetes, additional services, or another database for the learning-project scope.
