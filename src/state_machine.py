from __future__ import annotations

from typing import Dict, Iterable, Set

from src.models import RunState


class InvalidTransitionError(ValueError):
    pass


class RunStateMachine:
    _transitions: Dict[RunState, Set[RunState]] = {
        RunState.CREATED: {RunState.PREFLIGHT_PASSED, RunState.QUARANTINED, RunState.FAILED},
        RunState.PREFLIGHT_PASSED: {RunState.DRILL_SELECTED, RunState.QUARANTINED, RunState.FAILED},
        RunState.DRILL_SELECTED: {RunState.EXECUTED, RunState.QUARANTINED, RunState.FAILED},
        RunState.EXECUTED: {RunState.SCORED, RunState.QUARANTINED, RunState.FAILED},
        RunState.SCORED: {RunState.PERSISTED, RunState.FAILED},
        RunState.PERSISTED: {RunState.REPORTED, RunState.FAILED},
        RunState.REPORTED: set(),
        RunState.QUARANTINED: set(),
        RunState.FAILED: set(),
    }

    @classmethod
    def can_transition(cls, source: RunState, target: RunState) -> bool:
        return target in cls._transitions[source]

    @classmethod
    def transition(cls, source: RunState, target: RunState) -> RunState:
        if not cls.can_transition(source, target):
            raise InvalidTransitionError(f"invalid transition: {source.value} -> {target.value}")
        return target

    @classmethod
    def allowed_targets(cls, source: RunState) -> Iterable[RunState]:
        return cls._transitions[source]
