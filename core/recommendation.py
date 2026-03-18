from __future__ import annotations

from typing import Dict, List

from core.models import Finding, Question, Response, Section


class RecommendationService:
    """Rule-based recommendations for module suggestions and findings."""

    def suggest_modules(self, scores: Dict, responses: List[Response]) -> Dict[str, str]:
        response_map = {r.question_id: r for r in responses}
        suggestions: Dict[str, str] = {}

        def score(section_id: str, key: str = "maturity") -> float:
            return float(scores.get("sections", {}).get(section_id, {}).get(key, 0) or 0)

        # KPI / performance
        if self._response_low(response_map, "C4_Q01") or self._response_low(response_map, "C4_Q02"):
            suggestions["M3"] = "KPI e decisioni poco strutturati"

        # Data & digital
        if self._response_low(response_map, "C5_Q01") or self._response_low(response_map, "C5_Q02"):
            suggestions["M4"] = "Integrazione sistemi o qualità del dato insufficienti"

        # AI readiness
        ai_ambition = self._response_value(response_map, "C6_Q04")
        ai_readiness_low = self._response_low(response_map, "C6_Q05") or self._response_low(response_map, "C5_Q03")
        if ai_ambition is not None and ai_ambition >= 2 and ai_readiness_low:
            suggestions["M5"] = "Ambizione AI superiore alla readiness dati"
        elif score("C6") < 55:
            suggestions["M5"] = "Readiness AI/data-driven da approfondire"

        # Governance
        if self._response_low(response_map, "C2_Q04") or self._response_low(response_map, "C3_Q02"):
            suggestions["M2"] = "Ownership e criteri decisionali deboli"

        # Processes
        if self._response_low(response_map, "C3_Q01") or self._response_low(response_map, "C3_Q03"):
            suggestions["M1"] = "Processi e colli di bottiglia da approfondire"

        # Risk/change
        if self._response_low(response_map, "C6_Q02") or self._response_high(response_map, "C3_Q04"):
            suggestions["M6"] = "Fragilità organizzativa o change readiness bassa"

        # Portfolio
        if self._response_low(response_map, "C2_Q04"):
            suggestions["M8"] = "Prioritizzazione iniziative non strutturata"

        return suggestions

    def generate_findings(
        self,
        sections: List[Section],
        questions: List[Question],
        responses: List[Response],
        scores: Dict,
    ) -> List[Finding]:
        findings: List[Finding] = []
        response_map = {r.question_id: r for r in responses}

        section_by_id = {s.id: s for s in sections}
        for section in sections:
            section_score = scores.get("sections", {}).get(section.id, {})
            maturity = float(section_score.get("maturity", 0) or 0)
            risk = float(section_score.get("current_risk", 0) or 0)
            feasibility = float(section_score.get("feasibility", 0) or 0)
            impact = float(section_score.get("impact", 0) or 0)
            if maturity and maturity < 55:
                severity = "high" if maturity < 40 else "medium"
                title = f"Gap di maturità in {section.name}"
                desc = f"La sezione {section.name} mostra una maturità limitata ({maturity}/100), con rischio corrente {risk}/100."
                evidence = [q.id for q in questions if q.section_id == section.id and self._response_has_content(response_map.get(q.id))][:5]
                findings.append(
                    Finding(
                        id=f"F-{section.id}-GAP",
                        area=section.name,
                        severity=severity,
                        title=title,
                        description=desc,
                        evidence=evidence,
                        maturity_gap=round(100 - maturity, 1),
                        business_impact=impact,
                        feasibility=feasibility,
                        current_risk=risk,
                        intervention_risk=float(section_score.get("intervention_risk", 0) or 0),
                        recommendation_hint=f"Approfondire la sezione {section.name} e valutare interventi prioritari.",
                    )
                )

        # targeted findings
        if self._response_low(response_map, "C5_Q02") or self._response_low(response_map, "C5_Q03"):
            findings.append(
                Finding(
                    id="F-DATA-FOUNDATION",
                    area=section_by_id.get("C5").name if "C5" in section_by_id else "Digitale, dati e tecnologia",
                    severity="high",
                    title="Data foundation insufficiente",
                    description="Qualità, storicità o accessibilità del dato non sembrano sufficienti per decisioni evolute e iniziative AI.",
                    evidence=[q for q in ["C5_Q02", "C5_Q03", "C6_Q05"] if q in response_map],
                    maturity_gap=max(0.0, 100 - float(scores.get("sections", {}).get("C5", {}).get("maturity", 0) or 0)),
                    business_impact=85.0,
                    feasibility=65.0,
                    current_risk=75.0,
                    intervention_risk=30.0,
                    recommendation_hint="Costruire una iniziativa foundation su qualità, ownership e integrazione dati.",
                )
            )

        if self._response_low(response_map, "C2_Q04"):
            findings.append(
                Finding(
                    id="F-PORTFOLIO-GOV",
                    area=section_by_id.get("C2").name if "C2" in section_by_id else "Strategia, leadership e obiettivi",
                    severity="medium",
                    title="Criteri di prioritizzazione deboli",
                    description="Le iniziative rischiano di essere scelte senza un framework coerente di priorità, impatto e fattibilità.",
                    evidence=["C2_Q04"],
                    maturity_gap=max(0.0, 100 - float(scores.get("sections", {}).get("C2", {}).get("maturity", 0) or 0)),
                    business_impact=78.0,
                    feasibility=72.0,
                    current_risk=60.0,
                    intervention_risk=20.0,
                    recommendation_hint="Definire criteri standard per selezione e riesame del portafoglio iniziative.",
                )
            )

        if self._response_value(response_map, "C6_Q04") is not None and self._response_value(response_map, "C6_Q04") >= 2 and self._response_low(response_map, "C6_Q05"):
            findings.append(
                Finding(
                    id="F-AI-READINESS-MISMATCH",
                    area=section_by_id.get("C6").name if "C6" in section_by_id else "Innovazione, AI e readiness al cambiamento",
                    severity="high",
                    title="Mismatch tra ambizione AI e readiness reale",
                    description="Sono presenti use case o aspettative AI, ma la base dati e la readiness organizzativa non sono ancora adeguate.",
                    evidence=[q for q in ["C6_Q04", "C6_Q05", "C5_Q02", "C5_Q03"] if q in response_map],
                    maturity_gap=max(0.0, 100 - float(scores.get("sections", {}).get("C6", {}).get("maturity", 0) or 0)),
                    business_impact=88.0,
                    feasibility=55.0,
                    current_risk=68.0,
                    intervention_risk=35.0,
                    recommendation_hint="Separare use case AI veloci da prerequisiti dati/governance.",
                )
            )

        # de-duplicate by ID while preserving order
        unique: Dict[str, Finding] = {}
        for finding in findings:
            unique[finding.id] = finding
        return list(unique.values())

    @staticmethod
    def _response_has_content(response: Response | None) -> bool:
        if response is None:
            return False
        return bool(response.value not in (None, "", []) or response.comment or response.assessor_summary)

    @staticmethod
    def _response_value(response_map: Dict[str, Response], question_id: str) -> int | None:
        response = response_map.get(question_id)
        if not response or response.not_applicable:
            return None
        try:
            return int(response.value)
        except (TypeError, ValueError):
            # yes/no unsupported here
            return None

    def _response_low(self, response_map: Dict[str, Response], question_id: str) -> bool:
        value = self._response_value(response_map, question_id)
        return value is not None and value <= 1

    def _response_high(self, response_map: Dict[str, Response], question_id: str) -> bool:
        value = self._response_value(response_map, question_id)
        return value is not None and value >= 3
