from __future__ import annotations

import json
from pathlib import Path
from typing import List

from core.models import AssessmentDocument, AssessmentMeta, Module, Question, Section


class AssessmentService:
    def __init__(self, template_path: str | Path):
        self.template_path = Path(template_path)
        self.modules_dir = self.template_path.parent / "modules"

    def _load_payload(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def load_template_questions(self) -> List[Question]:
        payload = self._load_payload(self.template_path)
        return [Question(**item) for item in payload["question_bank"]]

    def load_template_sections(self) -> List[Section]:
        payload = self._load_payload(self.template_path)
        return [Section(**item) for item in payload["sections"]]

    def available_module_templates(self) -> List[Module]:
        definitions = [
            ("M1", "Processi operativi", "m1_processes.json"),
            ("M2", "Governance e organizzazione", "m2_governance.json"),
            ("M3", "KPI e performance management", "m3_kpi.json"),
            ("M4", "Digital architecture & data", "m4_data_digital.json"),
            ("M5", "AI / data-driven transformation", "m5_ai.json"),
            ("M6", "Risk, compliance e change readiness", "m6_risk_change.json"),
            ("M7", "Innovation system alignment", "m7_innovation_system.json"),
            ("M8", "Portfolio e project governance", "m8_portfolio.json"),
            ("M9", "Customer, value proposition e market intelligence", "m9_market_customer.json"),
        ]
        modules = []
        for module_id, name, filename in definitions:
            desc = ""
            if filename and (self.modules_dir / filename).exists():
                payload = self._load_payload(self.modules_dir / filename)
                desc = payload.get("section", {}).get("description", "")
            modules.append(Module(id=module_id, name=name, description=desc))
        return modules

    def load_module_section_and_questions(self, module_id: str) -> tuple[Section | None, List[Question]]:
        filename_map = {
            "M1": "m1_processes.json",
            "M2": "m2_governance.json",
            "M3": "m3_kpi.json",
            "M4": "m4_data_digital.json",
            "M5": "m5_ai.json",
            "M6": "m6_risk_change.json",
            "M7": "m7_innovation_system.json",
            "M8": "m8_portfolio.json",
            "M9": "m9_market_customer.json",
        }
        filename = filename_map.get(module_id)
        if not filename:
            return None, []
        path = self.modules_dir / filename
        if not path.exists():
            return None, []
        payload = self._load_payload(path)
        return Section(**payload["section"]), [Question(**item) for item in payload["question_bank"]]

    def apply_active_modules(self, document: AssessmentDocument) -> AssessmentDocument:
        base_sections = [s for s in document.sections if s.type == "core"]
        extra_sections: List[Section] = []
        extra_questions: List[Question] = []

        for module in document.modules:
            if not module.enabled:
                continue
            section, questions = self.load_module_section_and_questions(module.id)
            if section is None:
                continue
            section.enabled = True
            extra_sections.append(section)
            extra_questions.extend(questions)

        final_sections = sorted(base_sections + extra_sections, key=lambda s: s.order)
        final_section_ids = {s.id for s in final_sections}

        preserved_questions = [
            q for q in document.question_bank
            if q.custom_origin in {"core", "local_custom", "library_custom"} and q.section_id in final_section_ids
        ]

        deduped_questions = {}
        for question in preserved_questions + extra_questions:
            deduped_questions[question.id] = question

        document.sections = final_sections
        document.question_bank = list(deduped_questions.values())
        document.assessment.active_modules = [m.id for m in document.modules if m.enabled]
        return document

    def create_empty_assessment(self) -> AssessmentDocument:
        sections = self.load_template_sections()
        questions = self.load_template_questions()
        modules = self.available_module_templates()
        return AssessmentDocument(
            assessment=AssessmentMeta(),
            sections=sections,
            modules=modules,
            question_bank=questions,
        )
