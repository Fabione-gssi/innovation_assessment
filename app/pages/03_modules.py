from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from app.components.question_card import render_question
from app.state.session_manager import get_document, set_document, TEMPLATE_PATH
from core.models import AnswerOption, Question, SectionSummary
from core.recommendation import RecommendationService
from core.scoring import ScoringService
from core.services import AssessmentService

st.title("Moduli e domande custom")
document = get_document()
service = AssessmentService(TEMPLATE_PATH)
scorer = ScoringService()
recommender = RecommendationService()

scores = scorer.calculate(document.sections, document.question_bank, document.responses)
suggestions = recommender.suggest_modules(scores, document.responses)

st.caption("I moduli possono essere attivati manualmente oppure seguendo i suggerimenti automatici. Le domande custom create qui sono locali all'assessment corrente.")
if suggestions:
    st.subheader("Moduli suggeriti")
    for module_id, reason in suggestions.items():
        module_name = next((m.name for m in document.modules if m.id == module_id), module_id)
        st.info(f"{module_name}: {reason}")

changed = False
for module in document.modules:
    label = module.name
    help_text = module.description or None
    suggested = suggestions.get(module.id)
    cols = st.columns([4, 2])
    with cols[0]:
        new_value = st.checkbox(label, value=module.enabled, help=help_text, key=f"module_{module.id}")
        if suggested:
            st.caption(f"Suggerito: {suggested}")
    with cols[1]:
        st.write("Disponibile" if service.load_module_section_and_questions(module.id)[0] else "Template non ancora popolato")
    if new_value != module.enabled:
        module.enabled = new_value
        changed = True

if st.button("Applica configurazione moduli"):
    document = service.apply_active_modules(document)
    set_document(document)
    st.success("Configurazione moduli aggiornata")
elif changed:
    st.warning("Hai modificato la selezione dei moduli: clicca 'Applica configurazione moduli' per aggiornare sezioni e domande.")

# Render enabled module sections
response_map = {r.question_id: r for r in document.responses}
summary_map = {s.section_id: s for s in document.section_summaries}
enabled_module_sections = [s for s in sorted(document.sections, key=lambda s: s.order) if s.type == "module" and s.enabled]
if enabled_module_sections:
    st.subheader("Compilazione moduli attivi")
    selected_section = st.selectbox("Modulo attivo", options=enabled_module_sections, format_func=lambda s: s.name)
    section_questions = [q for q in document.question_bank if q.section_id == selected_section.id and q.active]
    with st.form(f"module_section_{selected_section.id}"):
        updated_responses = []
        for question in section_questions:
            st.markdown("---")
            updated_responses.append(render_question(question, response_map.get(question.id)))
        st.markdown("---")
        summary_seed = summary_map.get(selected_section.id, SectionSummary(section_id=selected_section.id))
        section_notes = st.text_area("Note modulo", value=summary_seed.section_notes, height=100)
        submitted = st.form_submit_button("Salva modulo")
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
        st.success("Modulo salvato")

st.subheader("Aggiungi domanda custom locale")
with st.form("custom_question_form"):
    all_sections = sorted(document.sections, key=lambda s: s.order)
    target_section = st.selectbox("Sezione target", options=all_sections, format_func=lambda s: s.name)
    qid = st.text_input("ID domanda", placeholder="es. LC_C5_01")
    text = st.text_input("Testo domanda")
    qtype = st.selectbox("Tipo", ["text_long", "text_short", "likert_1_5", "single_choice"])
    purpose = st.selectbox("Purpose", ["qualitative", "scoring", "hybrid"])
    scorable = st.checkbox("Contribuisce allo scoring", value=qtype in {"likert_1_5", "single_choice"} and purpose != "qualitative")
    required = st.checkbox("Obbligatoria", value=False)
    help_text = st.text_input("Help text")
    tags = st.text_input("Tag (separati da virgola)")
    options_text = st.text_area("Opzioni single choice (una per riga nel formato valore|etichetta|score)", height=100)
    submitted_custom = st.form_submit_button("Aggiungi domanda custom")

if submitted_custom:
    if not qid or not text:
        st.error("ID e testo domanda sono obbligatori")
    elif any(q.id == qid for q in document.question_bank):
        st.error("Esiste già una domanda con questo ID")
    elif scorable and qtype == "single_choice" and not options_text.strip():
        st.error("Per una single choice scorable devi definire le opzioni con score")
    else:
        options = []
        if qtype == "single_choice" and options_text.strip():
            for line in options_text.splitlines():
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 2:
                    score = float(parts[2]) if len(parts) > 2 and parts[2] != "" else None
                    options.append(AnswerOption(value=parts[0], label=parts[1], score=score))
        question = Question(
            id=qid,
            section_id=target_section.id,
            module_id=target_section.id if target_section.type == "module" else None,
            text=text,
            type=qtype,
            question_purpose=purpose,
            scorable=scorable,
            required=required,
            default_weight=1.0 if scorable else 0.0,
            options=options,
            help_text=help_text,
            allows_comment=True,
            allows_na=True,
            custom_origin="local_custom",
            reportable=True,
            finding_relevance="medium",
            tags=[t.strip() for t in tags.split(",") if t.strip()],
        )
        document.question_bank.append(question)
        set_document(document)
        st.success("Domanda custom aggiunta all'assessment corrente")
