param(
  [string]$ExpectedRepo = "Musashi94/AgentDojo",
  [string]$Version = "v0.3.0"
)

$ErrorActionPreference = "Stop"

if (-not $Version.StartsWith("v0.")) {
  Write-Host "Skip remote guard: version '$Version' is not v0.x"
  exit 0
}

if (-not (Test-Path ".git/config")) {
  throw "Git config not found (.git/config)."
}

$config = Get-Content -Raw .git/config
$originBlock = [regex]::Match($config, "(?s)\[remote \"origin\"\](.*?)(\r?\n\[|$)")
if (-not $originBlock.Success) {
  throw "Blocked: missing origin remote. Expected repository: $ExpectedRepo"
}

$urlMatch = [regex]::Match($originBlock.Groups[1].Value, "url\s*=\s*(.+)")
if (-not $urlMatch.Success) {
  throw "Blocked: origin exists but has no url. Expected repository: $ExpectedRepo"
}

$url = $urlMatch.Groups[1].Value.Trim()
if ($url -notmatch "Musashi94/AgentDojo(\.git)?$") {
  throw "Blocked: origin remote mismatch. Found '$url', expected repo '$ExpectedRepo'"
}

Write-Host "Remote guard passed: origin -> $url"
