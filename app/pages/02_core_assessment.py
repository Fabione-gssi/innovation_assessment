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

st.title("Assessment")
document = get_document()
response_map = {r.question_id: r for r in document.responses}
summary_map = {s.section_id: s for s in document.section_summaries}

sections = [s for s in sorted(document.sections, key=lambda s: s.order) if s.enabled]
if not sections:
    st.warning("Nessuna sezione attiva. Attiva almeno un modulo nella pagina Moduli.")
    st.stop()

st.info(
    "Questa è la pagina centrale di compilazione. Qui trovi sia il core sia tutti i moduli attivi. "
    "La pagina Moduli serve per attivare/disattivare approfondimenti e aggiungere domande custom."
)

section_labels = {s.id: f"{s.order}. {s.name}" for s in sections}
section_ids = [s.id for s in sections]
completion_map = {}
for section in sections:
    qs = [q for q in document.question_bank if q.section_id == section.id and q.active]
    answered = 0
    for q in qs:
        r = response_map.get(q.id)
        if r and (r.value not in (None, "", []) or r.comment or r.evidence_note or r.not_applicable):
            answered += 1
    completion_map[section.id] = f"{answered}/{len(qs)}"

selected_section_id = st.session_state.get("selected_section_id", section_ids[0])
if selected_section_id not in section_ids:
    selected_section_id = section_ids[0]
current_index = section_ids.index(selected_section_id)

col_nav1, col_nav2, col_nav3 = st.columns([1, 4, 1])
with col_nav1:
    if st.button("← Precedente", disabled=current_index == 0):
        st.session_state.selected_section_id = section_ids[current_index - 1]
        st.rerun()
with col_nav2:
    selected_section_id = st.selectbox(
        "Dominio / sezione",
        options=section_ids,
        index=current_index,
        format_func=lambda sid: f"{section_labels[sid]} · completamento {completion_map[sid]}",
    )
    st.session_state.selected_section_id = selected_section_id
with col_nav3:
    if st.button("Successiva →", disabled=current_index == len(section_ids) - 1):
        st.session_state.selected_section_id = section_ids[current_index + 1]
        st.rerun()

selected_section = next(s for s in sections if s.id == selected_section_id)
section_questions = [q for q in document.question_bank if q.section_id == selected_section.id and q.active]
structured_questions = [q for q in section_questions if q.type not in {"text_short", "text_long"}]
qualitative_questions = [q for q in section_questions if q.type in {"text_short", "text_long"}]

st.subheader(selected_section.name)
if selected_section.description:
    st.caption(selected_section.description)

with st.expander("Come compilare questa sezione", expanded=False):
    st.markdown(
        "- Le domande **Scoring** alimentano i punteggi della sezione.  \n"
        "- Le domande **Qualitative** non generano punteggio diretto, ma influenzano insight, finding e roadmap.  \n"
        "- Nei campi di evidenza indica quanto la risposta è affidabile e su quale fonte si basa."
    )

with st.form(f"section_{selected_section.id}"):
    updated_responses = []

    if structured_questions:
        st.markdown("### Domande strutturate")
        for question in structured_questions:
            st.markdown("---")
            updated_responses.append(render_question(question, response_map.get(question.id), compact=True))

    if qualitative_questions:
        st.markdown("### Domande aperte")
        for question in qualitative_questions:
            st.markdown("---")
            updated_responses.append(render_question(question, response_map.get(question.id), compact=True))

    st.markdown("---")
    summary_seed = summary_map.get(selected_section.id, SectionSummary(section_id=selected_section.id))
    section_notes = st.text_area(
        "Osservazioni dell'assessor",
        value=summary_seed.section_notes,
        height=120,
        placeholder="Sintesi, eccezioni, contraddizioni emerse, elementi da approfondire",
    )

    save_col1, save_col2 = st.columns(2)
    submitted = save_col1.form_submit_button("Salva sezione")
    submitted_next = save_col2.form_submit_button("Salva e vai alla successiva")

if submitted or submitted_next:
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
    if submitted_next and current_index < len(section_ids) - 1:
        st.session_state.selected_section_id = section_ids[current_index + 1]
        st.rerun()
    st.success("Sezione salvata")
