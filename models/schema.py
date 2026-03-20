"""
Schema dati per l'assessment.
Struttura canonica per persistenza JSON/Excel.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any
import json, copy


@dataclass
class Answer:
    """Singola risposta a una domanda."""
    question_id: str = ""
    value: Any = None          # int per scale, str per text, list per multi_choice
    notes: str = ""            # note aggiuntive opzionali
    answered_at: str = ""      # ISO timestamp

    def is_answered(self) -> bool:
        if self.value is None:
            return False
        if isinstance(self.value, str) and self.value.strip() == "":
            return False
        return True


@dataclass
class ModuleResult:
    """Risultati aggregati di un modulo."""
    module_id: str = ""
    score: float = 0.0         # punteggio medio 1-5
    max_score: float = 5.0
    answered: int = 0
    total: int = 0
    maturity_level: int = 1    # 1-5
    gap: float = 0.0           # distanza dal target
    target_level: int = 3      # livello target impostabile


@dataclass
class RoadmapItem:
    """Singola azione nella roadmap."""
    id: str = ""
    title: str = ""
    description: str = ""
    module_id: str = ""
    priority: str = "medium"   # critical, high, medium, low
    effort: str = "medium"     # low, medium, high
    impact: str = "medium"     # low, medium, high
    timeframe: str = ""        # es. "Q1 2025", "0-3 mesi"
    owner: str = ""
    status: str = "planned"    # planned, in_progress, done
    notes: str = ""


@dataclass
class AssessmentData:
    """Root del modello dati — formato canonico di persistenza."""
    # ── Metadati ────────────────────────────────────────────────────────
    version: str = "1.0.0"
    created_at: str = ""
    updated_at: str = ""
    assessor_name: str = ""
    assessor_role: str = ""

    # ── Dati azienda ────────────────────────────────────────────────────
    company_name: str = ""
    company_sector: str = ""
    company_size: str = ""           # micro, small, medium, large
    company_revenue: str = ""
    company_employees: str = ""
    company_description: str = ""

    # ── Risposte (dict: question_id → Answer) ──────────────────────────
    answers: dict = field(default_factory=dict)

    # ── Domande custom aggiunte dall'utente ─────────────────────────────
    custom_questions: list = field(default_factory=list)

    # ── Risultati calcolati ─────────────────────────────────────────────
    module_results: dict = field(default_factory=dict)

    # ── Roadmap ─────────────────────────────────────────────────────────
    roadmap: list = field(default_factory=list)

    # ── Target levels per modulo ────────────────────────────────────────
    target_levels: dict = field(default_factory=dict)

    def touch(self):
        """Aggiorna il timestamp di modifica."""
        self.updated_at = datetime.now().isoformat()
        if not self.created_at:
            self.created_at = self.updated_at

    def set_answer(self, question_id: str, value: Any, notes: str = ""):
        self.answers[question_id] = asdict(Answer(
            question_id=question_id,
            value=value,
            notes=notes,
            answered_at=datetime.now().isoformat(),
        ))
        self.touch()

    def get_answer(self, question_id: str) -> dict | None:
        return self.answers.get(question_id)

    def get_answer_value(self, question_id: str, default=None):
        ans = self.answers.get(question_id)
        if ans and ans.get("value") is not None:
            return ans["value"]
        return default

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    @classmethod
    def from_dict(cls, data: dict) -> "AssessmentData":
        obj = cls()
        for k, v in data.items():
            if hasattr(obj, k):
                setattr(obj, k, v)
        return obj

    @classmethod
    def from_json(cls, json_str: str) -> "AssessmentData":
        return cls.from_dict(json.loads(json_str))
