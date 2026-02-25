# Automation Runbook: Auto-PR + Auto-Merge

## Ziel
Automatisierter Flow für `feat/*` Branches:
1. Push auf `feat/*` erstellt automatisch einen PR nach `main`.
2. CI läuft verpflichtend (`build-and-test`).
3. PRs mit Label `automerge` werden auf Auto-Merge gestellt.
4. Merge erfolgt automatisch, sobald Required Checks grün sind.

## Bereits im Repo eingerichtet
- `.github/workflows/ci.yml`
- `.github/workflows/feature-pr-auto-open.yml`
- `.github/workflows/enable-automerge.yml`

## Einmalig im GitHub-Repo konfigurieren (CLI)

> Voraussetzung: `gh auth login` mit Admin-Rechten auf das Repository.

```bash
# 1) Auto-merge Feature im Repo aktivieren
gh repo edit Musashi94/AgentDojo --enable-auto-merge

# 2) Branch protection für main mit required status checks
# Hinweis: Erwarteter Check-Name ist exakt: "build-and-test"
gh api \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  repos/Musashi94/AgentDojo/branches/main/protection \
  -f required_status_checks.strict=true \
  -f enforce_admins=true \
  -f required_pull_request_reviews.dismiss_stale_reviews=true \
  -f required_pull_request_reviews.required_approving_review_count=1 \
  -f restrictions= \
  -F required_status_checks.contexts[]="build-and-test"
```

## Optional: Merge Queue (wenn Plan/Org unterstützt)

```bash
gh api \
  -X PATCH \
  -H "Accept: application/vnd.github+json" \
  repos/Musashi94/AgentDojo \
  -f allow_auto_merge=true \
  -f allow_merge_commit=false \
  -f allow_squash_merge=true
```

Danach in den Repository Settings UI:
- `Branch protection rule` für `main`
- Option `Require merge queue` aktivieren (falls verfügbar)

## Empfohlenes Team-Handling
- Entwickler arbeiten auf `feat/<ticket>-<kurzname>`.
- Für Auto-Merge Label `automerge` setzen.
- Ohne Label bleibt PR normal manuell mergebar.

## Risiken / Hinweise
- Workflow `enable-automerge` benötigt, dass GitHub Auto-Merge im Repo erlaubt ist.
- Wenn Required Check-Name sich ändert, Branch Protection muss angepasst werden.
- Bei Fork-PRs können Token-Rechte eingeschränkt sein; Flow ist primär für interne Branches.
- Review-Pflicht (1 Approver) kann Auto-Merge blocken, bis Review vorliegt.
