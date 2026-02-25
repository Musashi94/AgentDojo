from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


class SchemaRegistry:
    def __init__(self, schema_dir: Path) -> None:
        self.schema_dir = schema_dir

    def load(self, name: str, version: str = "v1") -> Dict[str, Any]:
        target = self.schema_dir / f"{name}.{version}.json"
        if not target.exists():
            raise FileNotFoundError(f"schema not found: {target}")
        return json.loads(target.read_text(encoding="utf-8"))

    def validate_required(self, payload: Dict[str, Any], name: str, version: str = "v1") -> None:
        schema = self.load(name, version)
        required = schema.get("required", [])
        missing = [k for k in required if k not in payload]
        if missing:
            raise ValueError(f"missing required fields for {name}.{version}: {', '.join(missing)}")
