$ErrorActionPreference = "Stop"

./scripts/check-local.ps1
./scripts/build-local.ps1

New-Item -ItemType Directory -Force -Path .local | Out-Null
$stamp = Get-Date -Format o
$line = "{\"event_name\":\"local_start\",\"event_type\":\"deployment\",\"timestamp\":\"$stamp\",\"service\":\"ops-v0.3\",\"version\":\"v0.3.0\",\"environment\":\"dev\",\"region\":\"eu-central-1\",\"release_id\":\"local-v0.3\",\"trace_id\":\"local-start-0001\",\"status\":\"ok\"}"
Add-Content -Path .local/telemetry-events.ndjson -Value $line

Write-Host "v0.3 local run initialized."
Write-Host "Artifacts: .local/build.ok, .local/telemetry-events.ndjson"
