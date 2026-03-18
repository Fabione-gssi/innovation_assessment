from core.models import Finding, Response, Section
from core.prioritization import PrioritizationService
from core.recommendation import RecommendationService


def test_module_suggestion_for_low_data_quality():
    suggestions = RecommendationService().suggest_modules(
        {"sections": {"C5": {"maturity": 40}}},
        [Response(question_id="C5_Q02", value=1), Response(question_id="C5_Q03", value=1)],
    )
    assert "M4" in suggestions


def test_priority_classification():
    finding = Finding(
        id="F1",
        area="Digitale, dati e tecnologia",
        severity="high",
        title="Data foundation insufficiente",
        description="...",
        maturity_gap=60,
        business_impact=85,
        feasibility=70,
        current_risk=80,
        intervention_risk=25,
    )
    service = PrioritizationService()
    idx = service.priority_index(finding)
    assert idx > 100
    assert service.priority_class(idx, finding) in {"Quick win", "Risk mitigation", "Foundational"}
