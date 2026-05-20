"""Tiny JSON-backed mock store. PostgreSQL-ready shape — swap out for SQLModel later."""
from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Any

DATA_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "store.json"


class MockDB:
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._state: dict[str, list[dict[str, Any]]] = {
            "payments": [],
            "activity": [],
            "followups": [],
            "merchants": [
                {
                    "id": "mch_demo",
                    "name": "Falcon AC Services",
                    "city": "Dubai",
                    "country": "AE",
                    "default_currency": "AED",
                }
            ],
        }

    def load(self) -> None:
        with self._lock:
            if DATA_FILE.exists():
                try:
                    self._state = json.loads(DATA_FILE.read_text())
                except json.JSONDecodeError:
                    pass
            DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    def flush(self) -> None:
        with self._lock:
            DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
            DATA_FILE.write_text(json.dumps(self._state, indent=2, default=str))

    def table(self, name: str) -> list[dict[str, Any]]:
        with self._lock:
            return self._state.setdefault(name, [])

    def insert(self, name: str, row: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            self._state.setdefault(name, []).append(row)
            self.flush()
            return row

    def update(self, name: str, row_id: str, patch: dict[str, Any]) -> dict[str, Any] | None:
        with self._lock:
            for row in self._state.get(name, []):
                if row.get("id") == row_id:
                    row.update(patch)
                    self.flush()
                    return row
            return None

    def find(self, name: str, row_id: str) -> dict[str, Any] | None:
        with self._lock:
            for row in self._state.get(name, []):
                if row.get("id") == row_id:
                    return row
            return None


db = MockDB()
