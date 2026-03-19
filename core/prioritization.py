from __future__ import annotations

from typing import List

from core.models import Finding, Initiative


class PrioritizationService:
    @staticmethod
    def priority_index(finding: Finding, urgency: float = 1.0) -> float:
        gap = max(1.0, finding.maturity_gap)
        impact = max(1.0, finding.business_impact)
        feasibility = max(1.0, finding.feasibility)
        risk_penalty = max(10.0, finding.intervention_risk)
        return round((gap * impact * feasibility * urgency) / risk_penalty / 100.0, 1)

    @staticmethod
    def priority_class(index: float, finding: Finding) -> str:
        if finding.current_risk >= 75 and finding.intervention_risk <= 35:
            return "Risk mitigation"
        if index >= 130:
            return "Quick win"
        if index >= 90:
            return "Foundational"
        if index >= 60:
            return "Strategic bet"
        if index >= 35:
            return "Monitor only"
        return "Not now"

    def findings_to_initiatives(self, findings: List[Finding]) -> List[Initiative]:
        initiatives: List[Initiative] = []
        ranked = []
        for finding in findings:
            p_index = self.priority_index(finding)
            ranked.append((finding, p_index, self.priority_class(p_index, finding)))
        ranked.sort(key=lambda x: x[1], reverse=True)

        for rank, (finding, p_index, p_class) in enumerate(ranked, start=1):
            initiatives.append(
                Initiative(
                    id=f"I-{rank:03d}",
                    title=finding.title,
                    description=finding.recommendation_hint or finding.description,
                    linked_findings=[finding.id],
                    stream=self._infer_stream(finding),
                    expected_outcome=self._infer_outcome(finding),
                    effort=self._infer_effort(finding),
                    priority_class=p_class,
                    priority_index=p_index,
                    priority_rank=rank,
                    time_horizon=self._infer_horizon(p_class),
                    success_kpis=self._infer_kpis(finding),
                    notes=f"Priority index: {p_index}",
                )
            )
        return initiatives

    @staticmethod
    def _infer_stream(finding: Finding) -> str:
        area = finding.area.lower()
        if "digit" in area or "dat" in area:
            return "data"
        if "ai" in area or "innov" in area:
            return "ai"
        if "process" in area or "organ" in area:
            return "processi"
        if "kpi" in area or "manager" in area:
            return "management_kpi"
        if "strateg" in area or "leader" in area:
            return "governance"
        return "trasversale"

    @staticmethod
    def _infer_effort(finding: Finding) -> str:
        if finding.intervention_risk <= 20 and finding.feasibility >= 70:
            return "low"
        if finding.intervention_risk <= 40 and finding.feasibility >= 55:
            return "medium"
        return "high"

    @staticmethod
    def _infer_horizon(priority_class: str) -> str:
        mapping = {
            "Quick win": "0_3_months",
            "Risk mitigation": "0_3_months",
            "Foundational": "3_6_months",
            "Strategic bet": "6_12_months",
            "Monitor only": "12_plus_months",
            "Not now": "12_plus_months",
        }
        return mapping.get(priority_class, "6_12_months")

    @staticmethod
    def _infer_outcome(finding: Finding) -> str:
        if "dato" in finding.title.lower() or "data" in finding.title.lower():
            return "Migliorare qualità, accessibilità e affidabilità del dato"
        if "ai" in finding.title.lower():
            return "Portare use case AI su basi realistiche e governate"
        return "Ridurre gap di maturità e aumentare capacità esecutiva"

    @staticmethod
    def _infer_kpis(finding: Finding) -> list[str]:
        area = finding.area.lower()
        if "digit" in area or "dat" in area:
            return ["data_quality_score", "system_integration_coverage"]
        if "kpi" in area or "manager" in area:
            return ["kpi_adoption_rate", "review_cadence_compliance"]
        if "process" in area or "organ" in area:
            return ["process_cycle_time", "handoff_error_rate"]
        if "ai" in area or "innov" in area:
            return ["qualified_use_cases", "pilot_to_scale_rate"]
        return ["initiative_completion_rate"]
