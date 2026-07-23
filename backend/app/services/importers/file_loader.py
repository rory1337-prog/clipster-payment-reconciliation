from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class FileLoader:
    @staticmethod
    def load(path: str | Path) -> list[dict[str, Any]]:
        with open(path, encoding="utf-8") as f:
            return json.load(f)