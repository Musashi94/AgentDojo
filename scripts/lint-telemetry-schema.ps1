param(
  [string]$SchemaPath = "telemetry/schema-v1.json"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $SchemaPath)) {
  Write-Error "Schema file not found: $SchemaPath"
}

$raw = Get-Content -Raw -Path $SchemaPath
try {
  $json = $raw | ConvertFrom-Json
} catch {
  Write-Error "Schema is not valid JSON: $($_.Exception.Message)"
}

$requiredTop = @(
  "event_name","event_type","timestamp","service","version",
  "environment","region","release_id","trace_id","status"
)

foreach ($f in $requiredTop) {
  if ($json.required -notcontains $f) {
    Write-Error "Missing required field in schema.required: $f"
  }
}

$eventTypeEnum = $json.properties.event_type.enum
$mustTypes = @("release","deployment","error","latency","quality","cost","rollback")
foreach ($t in $mustTypes) {
  if ($eventTypeEnum -notcontains $t) {
    Write-Error "Missing event_type enum value: $t"
  }
}

Write-Host "Telemetry schema lint passed ($SchemaPath)."
