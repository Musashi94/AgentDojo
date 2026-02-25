# Release Cadence v0.3

- Standard: weekly production release window.
- Hotfix: daily emergency lane, reduced scope + mandatory post-incident review.
- Hardening: monthly reliability/cost review, threshold recalibration, policy updates.

## Go/No-Go Gates

- Reliability: availability >= 99.5%, p95 latency <= 350ms, error_rate <= 2%
- Quality: change_failure_rate <= 15%, defect_escape_rate <= 3%
- Cost: release cost delta <= 12% vs baseline

If any gate fails during canary, auto-rollback to stable.
