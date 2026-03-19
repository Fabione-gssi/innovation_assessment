from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from app.state.session_manager import get_document, set_document
from core.recommendation import RecommendationService
from core.scoring import ScoringService
from core.synthesis import QualitativeSynthesizer

st.title("Analysis")
document = get_document()
scorer = ScoringService()
synt = QualitativeSynthesizer()
recommender = RecommendationService()

with st.expander("Come leggere punteggi, insight e finding", expanded=True):
    st.markdown(
        "**Punteggi**  \n"
        "- **Maturity**: media pesata delle domande scorable della sezione.  \n"
        "- **Coverage**: quota di domande scorable con risposta valida.  \n"
        "- **Confidence index**: affidabilità media delle risposte, basata su low/medium/high.  \n"
        "- **Impact, feasibility, current risk, intervention risk**: indicatori euristici v1 derivati dai punteggi e dalla confidenza.  \n\n"
        "**Insight**  \n"
        "Le risposte aperte e le note di sezione non generano score diretto ma alimentano sintesi qualitative e finding.  \n\n"
        "**Finding**  \n"
        "I finding vengono proposti quando emergono gap di maturità, incoerenze o pattern di rischio nelle risposte."
    )

document.scores = scorer.calculate(document.sections, document.question_bank, document.responses)
document.section_summaries = synt.build_section_summaries(document.sections, document.question_bank, document.responses, document.section_summaries)
document.findings = recommender.generate_findings(document.sections, document.question_bank, document.responses, document.scores)
set_document(document)

overall = document.scores.get("overall", {})
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Maturity", overall.get("maturity", 0))
col2.metric("Coverage", overall.get("coverage", 0))
col3.metric("Confidence", overall.get("confidence_index", 0))
col4.metric("Current risk", overall.get("current_risk", 0))
col5.metric("Findings", len(document.findings))

section_scores = document.scores.get("sections", {})
if section_scores:
    st.subheader("Score per sezione")
    df = pd.DataFrame.from_dict(section_scores, orient="index").reset_index(names=["section_id"])
    df["section_name"] = df["section_id"].map({s.id: s.name for s in document.sections})
    st.dataframe(df[["section_id", "section_name", "maturity", "impact", "feasibility", "current_risk", "intervention_risk", "coverage", "confidence_index"]], use_container_width=True)

if document.findings:
    st.subheader("Findings preliminari")
    findings_df = pd.DataFrame([
        {
            "id": f.id,
            "area": f.area,
            "severity": f.severity,
            "title": f.title,
            "gap": f.maturity_gap,
            "impact": f.business_impact,
            "feasibility": f.feasibility,
            "current_risk": f.current_risk,
            "intervention_risk": f.intervention_risk,
        }
        for f in document.findings
    ])
    st.dataframe(findings_df, use_container_width=True)

st.subheader("Sintesi qualitative")
for summary in document.section_summaries:
    section_name = next((s.name for s in document.sections if s.id == summary.section_id), summary.section_id)
    with st.expander(section_name, expanded=False):
        st.write(summary.section_summary or "Nessuna sintesi automatica disponibile")
        if summary.section_notes:
            st.caption(f"Note assessor: {summary.section_notes}")
        if summary.key_issues:
            st.write("Issue flags:", ", ".join(summary.key_issues))
        if summary.recommended_followups:
            st.write("Follow-up / tag:", ", ".join(summary.recommended_followups))
