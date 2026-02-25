import json
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from src.models import RunState
from src.schema_registry import SchemaRegistry
from src.state_machine import InvalidTransitionError, RunStateMachine


def test_state_machine_valid_transitions() -> None:
    assert RunStateMachine.transition(RunState.CREATED, RunState.PREFLIGHT_PASSED) == RunState.PREFLIGHT_PASSED
    assert RunStateMachine.transition(RunState.PERSISTED, RunState.REPORTED) == RunState.REPORTED


def test_state_machine_invalid_transition_raises() -> None:
    with pytest.raises(InvalidTransitionError):
        RunStateMachine.transition(RunState.CREATED, RunState.SCORED)


def test_schema_registry_required_fields() -> None:
    schema_dir = pathlib.Path(__file__).resolve().parents[1] / "src" / "schemas"
    registry = SchemaRegistry(schema_dir)

    payload = {
        "run_id": "r1",
        "role": "backend",
        "prompt": "safe",
        "state": "created",
        "started_at": "2026-02-25T00:00:00Z",
        "runtime_seconds": 10,
    }
    registry.validate_required(payload, "run_record")

    with pytest.raises(ValueError):
        registry.validate_required({"run_id": "r1"}, "score_record")

    schema = registry.load("run_record")
    assert json.loads(json.dumps(schema))["title"] == "RunRecord v1"
