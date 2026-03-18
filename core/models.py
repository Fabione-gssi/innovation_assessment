from __future__ import annotations

from datetime import date
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field, model_validator

QuestionType = Literal[
    "single_choice",
    "multi_choice",
    "likert_1_5",
    "yes_no_comment",
    "numeric",
    "text_short",
    "text_long",
]
QuestionPurpose = Literal["scoring", "qualitative", "hybrid"]
ConfidenceLevel = Literal["low", "medium", "high"]
EvidenceType = Literal["percezione", "intervista", "documento", "dato"]
SectionType = Literal["core", "module"]
CustomOrigin = Literal["core", "module", "local_custom", "library_custom"]


class AnswerOption(BaseModel):
    value: str
    label: str
    score: Optional[float] = None


class Alignment(BaseModel):
    uni_11814: List[str] = Field(default_factory=list)
    iso_56001: List[str] = Field(default_factory=list)


class Question(BaseModel):
    id: str
    section_id: str
    module_id: Optional[str] = None
    text: str
    type: QuestionType
    question_purpose: QuestionPurpose = "scoring"
    scorable: bool = False
    required: bool = False
    default_weight: float = 1.0
    options: List[AnswerOption] = Field(default_factory=list)
    help_text: str = ""
    placeholder: str = ""
    allows_comment: bool = True
    allows_na: bool = True
    custom_origin: CustomOrigin = "core"
    reportable: bool = True
    finding_relevance: Literal["low", "medium", "high"] = "medium"
    tags: List[str] = Field(default_factory=list)
    alignment: Alignment = Field(default_factory=Alignment)
    active: bool = True

    @model_validator(mode="after")
    def validate_scorable(self) -> "Question":
        if self.scorable and self.type in {"text_short", "text_long"}:
            raise ValueError("Text questions cannot be directly scorable in v1.")
        if self.scorable and self.type in {"single_choice", "likert_1_5", "yes_no_comment"} and not self.options:
            # likert and yes/no can be synthesized automatically; single choice should define options
            if self.type == "single_choice":
                raise ValueError("Scorable single_choice questions require options with score mapping.")
        return self


class Section(BaseModel):
    id: str
    name: str
    type: SectionType = "core"
    order: int = 0
    description: str = ""
    enabled: bool = True
    is_required: bool = True
    notes_enabled: bool = True


class Module(BaseModel):
    id: str
    name: str
    enabled: bool = False
    description: str = ""
    activation_reason: Optional[str] = None


class Response(BaseModel):
    question_id: str
    value: Any = None
    value_label: str = ""
    comment: str = ""
    not_applicable: bool = False
    confidence: ConfidenceLevel = "medium"
    evidence_type: EvidenceType = "intervista"
    evidence_note: str = ""
    assessor_summary: str = ""
    insight_tags: List[str] = Field(default_factory=list)
    issue_flags: List[str] = Field(default_factory=list)


class SectionSummary(BaseModel):
    section_id: str
    section_notes: str = ""
    section_summary: str = ""
    section_confidence: ConfidenceLevel = "medium"
    key_issues: List[str] = Field(default_factory=list)
    recommended_followups: List[str] = Field(default_factory=list)


class SectionScore(BaseModel):
    maturity: float = 0.0
    impact: float = 0.0
    feasibility: float = 0.0
    current_risk: float = 0.0
    intervention_risk: float = 0.0
    coverage: float = 0.0
    confidence_index: float = 0.0


class Finding(BaseModel):
    id: str
    area: str
    severity: Literal["low", "medium", "high"]
    title: str
    description: str
    evidence: List[str] = Field(default_factory=list)
    maturity_gap: float = 0.0
    business_impact: float = 0.0
    feasibility: float = 0.0
    current_risk: float = 0.0
    intervention_risk: float = 0.0
    recommendation_hint: str = ""


class Initiative(BaseModel):
    id: str
    title: str
    description: str = ""
    linked_findings: List[str] = Field(default_factory=list)
    stream: str = ""
    expected_outcome: str = ""
    owner: str = ""
    time_horizon: str = ""
    effort: str = ""
    dependencies: List[str] = Field(default_factory=list)
    priority_class: str = ""
    success_kpis: List[str] = Field(default_factory=list)
    notes: str = ""


class RoadmapItem(BaseModel):
    id: str
    initiative_id: str
    time_horizon: str
    stream: str
    priority_class: str
    owner: str = ""
    dependencies: List[str] = Field(default_factory=list)
    success_kpis: List[str] = Field(default_factory=list)
    status: str = "proposed"
    notes: str = ""


class AssessmentMeta(BaseModel):
    assessment_id: str = "ASS-NEW"
    client_name: str = ""
    sector: str = ""
    company_size: str = ""
    scope: str = "azienda"
    assessor_name: str = ""
    assessment_date: date = Field(default_factory=date.today)
    mode: str = "intervista_guidata"
    status: str = "draft"
    objectives: List[str] = Field(default_factory=list)
    active_modules: List[str] = Field(default_factory=list)
    template_version: str = "1.0.0"
    schema_version: str = "1.0.0"


class AssessmentDocument(BaseModel):
    schema_version: str = "1.0.0"
    template_version: str = "1.0.0"
    assessment: AssessmentMeta
    sections: List[Section] = Field(default_factory=list)
    modules: List[Module] = Field(default_factory=list)
    question_bank: List[Question] = Field(default_factory=list)
    responses: List[Response] = Field(default_factory=list)
    section_summaries: List[SectionSummary] = Field(default_factory=list)
    scores: Dict[str, Dict[str, SectionScore] | SectionScore | Dict[str, Any]] = Field(default_factory=dict)
    findings: List[Finding] = Field(default_factory=list)
    initiatives: List[Initiative] = Field(default_factory=list)
    roadmap: List[RoadmapItem] = Field(default_factory=list)
    audit_meta: Dict[str, Any] = Field(default_factory=dict)
