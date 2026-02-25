$ErrorActionPreference = "Stop"

./scripts/check-git-remote.ps1 -ExpectedRepo "Musashi94/AgentDojo" -Version "v0.3.0"

if (-not (Test-Path ".env")) {
  if (Test-Path ".env.example") {
    Write-Host "No .env found, creating from .env.example"
    Copy-Item .env.example .env
  } else {
    throw "Missing .env and .env.example"
  }
}

./scripts/lint-telemetry-schema.ps1 -SchemaPath telemetry/schema-v1.json
$null = Get-Content -Raw dashboards/dashboard-v1.json | ConvertFrom-Json

$required = @("APP_ENV","APP_SERVICE","APP_VERSION","APP_REGION","APP_PORT","TELEMETRY_SCHEMA_PATH")
$envMap = @{}
Get-Content .env | ForEach-Object {
  if ($_ -match "^\s*#" -or $_ -match "^\s*$") { return }
  $k,$v = $_ -split "=",2
  $envMap[$k.Trim()] = $v.Trim()
}
foreach ($k in $required) {
  if (-not $envMap.ContainsKey($k) -or [string]::IsNullOrWhiteSpace($envMap[$k])) {
    throw "Missing required .env key: $k"
  }
}

Write-Host "Local checks passed."
