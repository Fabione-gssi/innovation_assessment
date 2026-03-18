from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from app.components.question_card import render_question
from app.state.session_manager import get_document, set_document
from core.models import Response, SectionSummary

st.title("Core assessment")
document = get_document()
response_map = {r.question_id: r for r in document.responses}
summary_map = {s.section_id: s for s in document.section_summaries}

sections = [s for s in sorted(document.sections, key=lambda s: s.order) if s.type == "core" and s.enabled]
selected_section = st.selectbox("Sezione", options=sections, format_func=lambda s: f"{s.order}. {s.name}")

section_questions = [q for q in document.question_bank if q.section_id == selected_section.id and q.active]
with st.form(f"section_{selected_section.id}"):
    updated_responses = []
    for question in section_questions:
        st.markdown("---")
        updated_responses.append(render_question(question, response_map.get(question.id)))
    st.markdown("---")
    summary_seed = summary_map.get(selected_section.id, SectionSummary(section_id=selected_section.id))
    section_notes = st.text_area("Note di sezione", value=summary_seed.section_notes, height=100)
    submitted = st.form_submit_button("Salva sezione")

if submitted:
    for response in updated_responses:
        response_map[response.question_id] = response
    summary_map[selected_section.id] = SectionSummary(
        section_id=selected_section.id,
        section_notes=section_notes,
        section_summary=summary_seed.section_summary,
        section_confidence=summary_seed.section_confidence,
        key_issues=summary_seed.key_issues,
        recommended_followups=summary_seed.recommended_followups,
    )
    document.responses = list(response_map.values())
    document.section_summaries = list(summary_map.values())
    set_document(document)
    st.success("Sezione salvata")
