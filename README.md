# AgentDojo

Daily autonomous upskilling for OpenClaw agent teams.

AgentDojo runs short, safe micro-drills and generates a compact daily learning digest.

## Product Principles
- Quality first
- Cost-aware by default
- Safety always enforced

## What You Get
- Configurable daily schedule and intensity
- Hard budget guardrails (token and optional cost)
- Source quality scoring
- Prompt-injection defensive handling
- Audit-ready run records
- Short daily report

## Folder Layout

```text
agentdojo/
  SKILL.md
  CHANGELOG.md
  LICENSE
  .gitignore
  config/
    agentdojo.config.yaml
    drills/
      leadarchitect.yaml
      backend.yaml
      frontend.yaml
  docs/
    architecture.md
    threat-model.md
    scoring-rubric.md
    publishing.md
  templates/
    daily-report-template.md
```

## Quick Start
1. Copy the folder into your skills workspace.
2. Edit `config/agentdojo.config.yaml`.
3. Set your schedule, budget, and selected agents.
4. Add cron jobs (examples in `docs/architecture.md`).
5. Run a pilot for 7 days.

## Default Configuration (Opinionated)
- Run time: 04:00 local timezone
- Priority weights: Quality > Cost > Safety
- Source policy: Open web allowed with strict filtering and risk scoring
- Daily budget: user-configurable

## ClawHub Publish
See `docs/publishing.md`.
