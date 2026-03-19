from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from app.state.session_manager import TEMPLATE_PATH, get_document, set_document
from core.models import AnswerOption, Question
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

st.caption(
    "Qui selezioni i moduli opzionali e aggiungi domande custom. La compilazione delle domande avviene invece nella pagina Assessment, "
    "così tutto il questionario resta in un unico flusso coerente."
)

with st.expander("Come funziona l'attivazione dei moduli", expanded=False):
    st.markdown(
        "- Il **core** serve per lo screening iniziale.  \n"
        "- I **moduli** servono per approfondire aree specifiche.  \n"
        "- Quando attivi un modulo, le sue domande compaiono nella pagina Assessment come nuove sezioni navigabili."
    )

if suggestions:
    st.subheader("Moduli suggeriti")
    for module_id, reason in suggestions.items():
        module_name = next((m.name for m in document.modules if m.id == module_id), module_id)
        st.info(f"{module_name}: {reason}")

changed = False
for module in document.modules:
    help_text = module.description or None
    suggested = suggestions.get(module.id)
    cols = st.columns([4, 2])
    with cols[0]:
        new_value = st.checkbox(module.name, value=module.enabled, help=help_text, key=f"module_{module.id}")
        if suggested:
            st.caption(f"Suggerito: {suggested}")
    with cols[1]:
        has_template = service.load_module_section_and_questions(module.id)[0] is not None
        st.write("Disponibile" if has_template else "Template mancante")
    if new_value != module.enabled:
        module.enabled = new_value
        changed = True

if st.button("Applica configurazione moduli"):
    document = service.apply_active_modules(document)
    set_document(document)
    st.success("Configurazione moduli aggiornata. Le sezioni attive ora sono disponibili nella pagina Assessment.")
elif changed:
    st.warning("Hai modificato la selezione dei moduli: clicca 'Applica configurazione moduli' per aggiornare le sezioni disponibili.")

st.subheader("Domande custom locali")
st.caption("Le domande create qui vengono aggiunte all'assessment corrente e poi compilate nella pagina Assessment, nella sezione selezionata.")
with st.form("custom_question_form"):
    all_sections = sorted([s for s in document.sections if s.enabled], key=lambda s: s.order)
    target_section = st.selectbox("Sezione target", options=all_sections, format_func=lambda s: s.name)
    qid = st.text_input("ID domanda", placeholder="es. LC_C5_01")
    text = st.text_input("Testo domanda")
    qtype = st.selectbox("Tipo", ["text_long", "text_short", "likert_1_5", "single_choice"])
    purpose = st.selectbox("Purpose", ["qualitative", "scoring", "hybrid"])
    scorable = st.checkbox("Contribuisce allo scoring", value=qtype in {"likert_1_5", "single_choice"} and purpose != "qualitative")
    required = st.checkbox("Obbligatoria", value=False)
    help_text = st.text_input("Help text")
    tags = st.text_input("Tag (separati da virgola)")
    options_text = st.text_area("Opzioni single choice (una per riga: valore|etichetta|score)", height=100)
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
        st.success("Domanda custom aggiunta. La trovi nella sezione selezionata dentro la pagina Assessment.")
