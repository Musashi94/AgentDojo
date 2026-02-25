from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List

from src.models import Drill, ExecutionResult, RunRecord, RunState
from src.persistence import PersistenceLayer
from src.policy_engine import ActionType, PolicyEngine, RunContext
from src.reporting import render_run_report
from src.scoring import ScoringEngine
from src.state_machine import RunStateMachine


class RuntimeExecutionKernel:
    def __init__(
        self,
        policy_engine: PolicyEngine,
        scoring_engine: ScoringEngine,
        persistence: PersistenceLayer,
        drills: List[Drill],
    ) -> None:
        self.policy_engine = policy_engine
        self.scoring_engine = scoring_engine
        self.persistence = persistence
        self.drills = drills

    def execute(self, run_id: str, role: str, prompt: str, runtime_seconds: int = 30) -> RunRecord:
        record = RunRecord(run_id=run_id, role=role, prompt=prompt, runtime_seconds=runtime_seconds)
        context = RunContext(run_id=run_id, role=role, prompt=prompt)

        preflight = self.policy_engine.preflight(context, runtime_seconds=runtime_seconds)
        self._emit_event(record, "preflight", preflight.reason)
        if not preflight.allowed:
            record.state = RunState.QUARANTINED if preflight.quarantine else RunState.FAILED
            record.quarantine_reason = context.quarantine_reason
            return self._persist_failure(record, context)

        record.state = RunStateMachine.transition(record.state, RunState.PREFLIGHT_PASSED)

        drill = self._select_drill(role)
        record.drill_id = drill.drill_id
        record.state = RunStateMachine.transition(record.state, RunState.DRILL_SELECTED)

        result = self._run_isolated(context, drill)
        if context.quarantined:
            record.state = RunState.QUARANTINED
            record.quarantine_reason = context.quarantine_reason
            return self._persist_failure(record, context, result)

        record.state = RunStateMachine.transition(record.state, RunState.EXECUTED)

        record.score = self.scoring_engine.score(result, quarantined=context.quarantined)
        record.state = RunStateMachine.transition(record.state, RunState.SCORED)

        self._persist_success(record, context, result)
        record.state = RunStateMachine.transition(record.state, RunState.PERSISTED)

        report = render_run_report(record, result)
        report_path = self.persistence.write_report(run_id, report)
        record.artifacts["report"] = str(report_path)
        record.state = RunStateMachine.transition(record.state, RunState.REPORTED)
        record.ended_at = datetime.now(timezone.utc).isoformat()
        self.persistence.write_run(run_id, record.to_dict())
        return record

    def _select_drill(self, role: str) -> Drill:
        candidates = [d for d in self.drills if d.role == role]
        if not candidates:
            raise ValueError(f"no drill found for role '{role}'")
        return candidates[0]

    def _run_isolated(self, context: RunContext, drill: Drill) -> ExecutionResult:
        sequence = [ActionType.TOOL_CALL, ActionType.WEB_FETCH, ActionType.FILE_WRITE, ActionType.TOOL_CALL]
        for action in sequence:
            decision = self.policy_engine.authorize_action(context, action)
            if not decision.allowed:
                return ExecutionResult("quarantined during execution", 0, 0, 0, 0)

        return ExecutionResult(
            output=f"Completed drill '{drill.objective}' safely.",
            tokens_used=480,
            tool_calls_used=context.state.tool_calls,
            write_calls_used=context.state.file_writes,
            fetch_calls_used=context.state.web_fetches,
        )

    def _persist_success(self, record: RunRecord, context: RunContext, result: ExecutionResult) -> None:
        run_path = self.persistence.write_run(record.run_id, record.to_dict())
        score_path = self.persistence.write_score(record.run_id, record.score or 0.0)
        audit_path = self.persistence.append_audit(
            {
                "run_id": record.run_id,
                "state": record.state.value,
                "quarantined": context.quarantined,
                "counters": {
                    "tool_calls": result.tool_calls_used,
                    "file_writes": result.write_calls_used,
                    "web_fetches": result.fetch_calls_used,
                },
            }
        )
        record.artifacts.update({"run": str(run_path), "score": str(score_path), "audit": str(audit_path)})

    def _persist_failure(
        self,
        record: RunRecord,
        context: RunContext,
        result: ExecutionResult | None = None,
    ) -> RunRecord:
        self.persistence.write_run(record.run_id, record.to_dict())
        self.persistence.append_audit(
            {
                "run_id": record.run_id,
                "state": record.state.value,
                "quarantined": context.quarantined,
                "reason": context.quarantine_reason,
                "result": result.to_dict() if result else None,
            }
        )
        record.ended_at = datetime.now(timezone.utc).isoformat()
        return record

    @staticmethod
    def _emit_event(record: RunRecord, event_type: str, message: str) -> None:
        record.events.append({"event": event_type, "message": message})
