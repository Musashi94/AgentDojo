# SortPilot Autopilot Runbook (No-Manual Flow)

## Goal
One command to run an automated visual smoke test and produce screenshots for all main app sections.

## What is implemented now
- Script: `C:\oc_projects\SortPilot\scripts\run-visual-smoke.ps1`
- Driver: `C:\oc_projects\SortPilot\scripts\visual-smoke.cjs`
- Output: `C:\oc_projects\SortPilot\artifacts\screens\*.png` + `summary.txt`

Covered pages:
- Dashboard
- Inbox
- Locations
- Rules
- Smart Folders
- Info & Legal
- Settings

## Run
```powershell
cd C:\oc_projects\SortPilot
powershell -ExecutionPolicy Bypass -File scripts/run-visual-smoke.ps1
```

## Notes
- This is browser-level visual validation (fast, repeatable).
- Full native Tauri action testing (with `invoke` bridge behavior) still needs direct Tauri-window automation channel.
- Use this smoke run as the default proactive status heartbeat artifact for every test cycle.
