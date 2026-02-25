from __future__ import annotations

from src.models import ExecutionResult, RunRecord


def render_run_report(record: RunRecord, result: ExecutionResult) -> str:
    return "\n".join(
        [
            f"# AgentDojo Run Report: {record.run_id}",
            "",
            f"- Role: {record.role}",
            f"- Drill: {record.drill_id}",
            f"- State: {record.state.value}",
            f"- Runtime (s): {record.runtime_seconds}",
            f"- Score: {record.score}",
            f"- Quarantined: {bool(record.quarantine_reason)}",
            f"- Quarantine reason: {record.quarantine_reason or 'n/a'}",
            "",
            "## Result",
            result.output,
        ]
    )
