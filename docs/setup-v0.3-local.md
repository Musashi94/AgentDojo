# v0.3 Minimal Local Setup (reproducible)

## 1) Prepare env

```powershell
Copy-Item .env.example .env
```

## 2) Run checks (includes mandatory origin guard)

```powershell
./scripts/check-local.ps1
```

> This blocks if `origin` is missing or not `Musashi94/AgentDojo`.

## 3) Build local artifacts

```powershell
./scripts/build-local.ps1
```

## 4) Start local run bootstrap

```powershell
./scripts/start-local.ps1
```

## Expected outputs

- `.local/build.ok`
- `.local/telemetry-events.ndjson`

If checks fail, fix `.env` required keys or schema/dashboard JSON validity first.
