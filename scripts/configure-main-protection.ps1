param(
  [string]$Owner = "Musashi94",
  [string]$Repo = "AgentDojo"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
  throw "GitHub CLI (gh) is required."
}

$payload = @{
  required_status_checks = @{
    strict = $true
    contexts = @("remote_guard", "telemetry_lint", "dashboard_contract_check")
  }
  enforce_admins = $true
  required_pull_request_reviews = @{
    dismiss_stale_reviews = $true
    require_code_owner_reviews = $false
    required_approving_review_count = 1
  }
  restrictions = $null
  required_linear_history = $true
  allow_force_pushes = $false
  allow_deletions = $false
  block_creations = $false
  required_conversation_resolution = $true
  lock_branch = $false
  allow_fork_syncing = $true
} | ConvertTo-Json -Depth 6

$payload | gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  "/repos/$Owner/$Repo/branches/main/protection" \
  --input - | Out-Null

Write-Host "Branch protection applied: $Owner/$Repo main"
