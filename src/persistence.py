from __future__ import annotations

import json
from pathlib import Path
from typing import Dict


class PersistenceLayer:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.paths: Dict[str, Path] = {
            "state": root / "state",
            "runs": root / "state" / "runs",
            "scores": root / "state" / "scores",
            "audit": root / "audit",
            "reports": root / "reports",
        }
        for path in self.paths.values():
            path.mkdir(parents=True, exist_ok=True)

    def write_run(self, run_id: str, payload: dict) -> Path:
        target = self.paths["runs"] / f"{run_id}.json"
        target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return target

    def write_score(self, run_id: str, score: float) -> Path:
        target = self.paths["scores"] / f"{run_id}.json"
        target.write_text(json.dumps({"run_id": run_id, "score": score}, indent=2), encoding="utf-8")
        return target

    def append_audit(self, event: dict) -> Path:
        target = self.paths["audit"] / "events.ndjson"
        with target.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")
        return target

    def write_report(self, run_id: str, content: str) -> Path:
        target = self.paths["reports"] / f"{run_id}.md"
        target.write_text(content, encoding="utf-8")
        return target
