from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Iterable, List, Mapping, Optional


class ActionType(str, Enum):
    WEB_FETCH = "web_fetch"
    FILE_WRITE = "file_write"
    TOOL_CALL = "tool_call"


@dataclass(frozen=True)
class PolicyCaps:
    max_tool_calls: int = 30
    max_file_writes: int = 5
    max_web_fetches: int = 8
    max_runtime_seconds: int = 300


@dataclass
class PolicyState:
    tool_calls: int = 0
    file_writes: int = 0
    web_fetches: int = 0


@dataclass
class PolicyDecision:
    allowed: bool
    reason: str
    quarantine: bool = False


@dataclass
class RunContext:
    run_id: str
    role: str
    prompt: str
    state: PolicyState = field(default_factory=PolicyState)
    quarantined: bool = False
    quarantine_reason: Optional[str] = None


SUSPICIOUS_PROMPT_PATTERNS: List[str] = [
    "ignore previous instructions",
    "ignore all previous",
    "disregard safety",
    "system prompt",
    "reveal hidden instructions",
    "override policy",
    "disable guardrails",
    "bypass restrictions",
]


class PolicyEngine:
    def __init__(
        self,
        caps: Optional[PolicyCaps] = None,
        suspicious_patterns: Optional[Iterable[str]] = None,
    ) -> None:
        self.caps = caps or PolicyCaps()
        self._patterns = [p.lower() for p in (suspicious_patterns or SUSPICIOUS_PROMPT_PATTERNS)]

    def preflight(self, context: RunContext, runtime_seconds: int) -> PolicyDecision:
        if runtime_seconds > self.caps.max_runtime_seconds:
            return PolicyDecision(
                allowed=False,
                reason=f"runtime cap exceeded: {runtime_seconds}s > {self.caps.max_runtime_seconds}s",
            )
        prompt_check = self.detect_prompt_injection(context.prompt)
        if not prompt_check.allowed:
            self._quarantine(context, prompt_check.reason)
            return prompt_check
        return PolicyDecision(True, "preflight passed")

    def detect_prompt_injection(self, prompt: str) -> PolicyDecision:
        normalized = prompt.lower()
        for pattern in self._patterns:
            if pattern in normalized:
                return PolicyDecision(
                    allowed=False,
                    reason=f"prompt injection pattern detected: '{pattern}'",
                    quarantine=True,
                )
        return PolicyDecision(True, "prompt clean")

    def authorize_action(self, context: RunContext, action: ActionType) -> PolicyDecision:
        if context.quarantined:
            return PolicyDecision(False, f"run quarantined: {context.quarantine_reason}", quarantine=True)

        if action == ActionType.TOOL_CALL:
            if context.state.tool_calls + 1 > self.caps.max_tool_calls:
                return self._deny_with_quarantine(context, "tool call cap exceeded")
            context.state.tool_calls += 1
            return PolicyDecision(True, "tool call allowed")

        if action == ActionType.FILE_WRITE:
            if context.state.file_writes + 1 > self.caps.max_file_writes:
                return self._deny_with_quarantine(context, "file write cap exceeded")
            context.state.file_writes += 1
            context.state.tool_calls += 1
            return PolicyDecision(True, "file write allowed")

        if action == ActionType.WEB_FETCH:
            if context.state.web_fetches + 1 > self.caps.max_web_fetches:
                return self._deny_with_quarantine(context, "web fetch cap exceeded")
            context.state.web_fetches += 1
            context.state.tool_calls += 1
            return PolicyDecision(True, "web fetch allowed")

        return self._deny_with_quarantine(context, f"unknown action type: {action}")

    def _deny_with_quarantine(self, context: RunContext, reason: str) -> PolicyDecision:
        self._quarantine(context, reason)
        return PolicyDecision(False, reason, quarantine=True)

    @staticmethod
    def _quarantine(context: RunContext, reason: str) -> None:
        context.quarantined = True
        context.quarantine_reason = reason

    @staticmethod
    def quarantine_record(context: RunContext) -> Mapping[str, object]:
        return {
            "run_id": context.run_id,
            "role": context.role,
            "quarantined": context.quarantined,
            "reason": context.quarantine_reason,
            "counters": {
                "tool_calls": context.state.tool_calls,
                "file_writes": context.state.file_writes,
                "web_fetches": context.state.web_fetches,
            },
        }
