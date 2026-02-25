$ErrorActionPreference = "Stop"

New-Item -ItemType Directory -Force -Path .local | Out-Null

if (-not (Test-Path "telemetry/schema-v1.json")) {
  throw "Missing telemetry/schema-v1.json"
}
if (-not (Test-Path "dashboards/dashboard-v1.json")) {
  throw "Missing dashboards/dashboard-v1.json"
}
if (-not (Test-Path "ops/canary-policy-v1.yaml")) {
  throw "Missing ops/canary-policy-v1.yaml"
}

$null = Get-Content -Raw telemetry/schema-v1.json | ConvertFrom-Json
$null = Get-Content -Raw dashboards/dashboard-v1.json | ConvertFrom-Json

"build_ok $(Get-Date -Format o)" | Set-Content .local/build.ok
Write-Host "Local build checks passed."
