from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class RunState(str, Enum):
    CREATED = "created"
    PREFLIGHT_PASSED = "preflight_passed"
    DRILL_SELECTED = "drill_selected"
    EXECUTED = "executed"
    SCORED = "scored"
    PERSISTED = "persisted"
    REPORTED = "reported"
    QUARANTINED = "quarantined"
    FAILED = "failed"


@dataclass
class RunRecord:
    run_id: str
    role: str
    prompt: str
    drill_id: Optional[str] = None
    state: RunState = RunState.CREATED
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    ended_at: Optional[str] = None
    runtime_seconds: int = 0
    score: Optional[float] = None
    quarantine_reason: Optional[str] = None
    artifacts: Dict[str, str] = field(default_factory=dict)
    events: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["state"] = self.state.value
        return data


@dataclass(frozen=True)
class Drill:
    drill_id: str
    role: str
    objective: str
    difficulty: str = "normal"


@dataclass
class ExecutionResult:
    output: str
    tokens_used: int
    tool_calls_used: int
    write_calls_used: int
    fetch_calls_used: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
