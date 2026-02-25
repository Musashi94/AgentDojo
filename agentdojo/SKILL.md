# agentdojo-core

Provider-agnostic orchestration and daily learning policy for OpenClaw environments.

## Purpose
Define, in one portable config:
- when agents proactively report,
- how often and how deeply they learn,
- which channels/targets they use,
- and which safety gates protect auto-improvement.

## Files
- `dojo.config.yaml` — runtime policy and defaults
- `dojo.schema.json` — schema for validation

## Core model
1. `learning_profiles` define budget/depth/schedule presets (`lowcost|balanced|intensive`).
2. `profile` selects active preset.
3. `learning` controls global safety and sources.
4. `proactive.routes` maps events to OpenClaw channels/targets.

## Safety defaults
- Skill installation requires human review.
- Guardrail changes require human review.
- Rollback is enabled on failed validation.
- Quiet-hours supported to suppress noisy reports.

## Recommended rollout
1. Start with `profile: lowcost` + `mode: propose_only`.
2. Review suggestions for 3-7 days.
3. Move to `balanced` when signal quality is stable.

## ClawHub packaging notes
When publishing this as a ClawHub skill, include:
- this `SKILL.md`
- `dojo.config.yaml` example
- `dojo.schema.json`
- release notes for config-breaking changes
