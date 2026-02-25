# End-to-End Auto-Merge Flow (v0.x)

## Zielbild

1. Agent pusht auf `agent/*` oder `agents/*`.
2. Workflow `agent-auto-pr-merge` erstellt automatisch PR nach `main` (oder nutzt bestehenden).
3. Auto-Merge wird per `gh pr merge --auto --squash` aktiviert.
4. Merge erfolgt erst bei grünen Pflicht-Checks (Branch Protection).
5. Bei Check-Fehlern markiert `pr-fallback-on-failure` den PR für manuellen Fallback.

## Branch-Schutz für `main` (verbindlich)

- Pull Request erforderlich
- Required checks: `remote_guard`, `telemetry_lint`, `dashboard_contract_check`
- Required approvals: mindestens 1
- Force-push/deletion verboten
- Conversation resolution erforderlich

Automatisierbar mit:

```powershell
./scripts/configure-main-protection.ps1 -Owner Musashi94 -Repo AgentDojo
```

## Fallback bei fehlschlagenden Checks

1. PR mit Label `fallback-manual-review` öffnen.
2. Fehlerursache im fehlgeschlagenen Check beheben.
3. Erneut pushen auf denselben Agent-Branch.
4. Nach grünen Checks greift Auto-Merge wieder automatisch.
