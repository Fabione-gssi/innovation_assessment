from __future__ import annotations

import json
from pathlib import Path

from core.models import AssessmentDocument


class JsonRepository:
    @staticmethod
    def save(document: AssessmentDocument, path: str | Path) -> None:
        Path(path).write_text(
            document.model_dump_json(indent=2),
            encoding="utf-8",
        )

    @staticmethod
    def load(path: str | Path) -> AssessmentDocument:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        return AssessmentDocument(**payload)
