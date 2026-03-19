from __future__ import annotations

from typing import Any, Optional

import streamlit as st

from core.models import Question, Response


CONFIDENCE_OPTIONS = ["low", "medium", "high"]
EVIDENCE_OPTIONS = ["percezione", "intervista", "documento", "dato"]


LIKERT_LABELS = {
    1: "1 - Molto basso / assente",
    2: "2 - Basso",
    3: "3 - Medio",
    4: "4 - Buono",
    5: "5 - Molto buono",
}


def render_question(question: Question, existing: Optional[Response] = None, *, compact: bool = True) -> Response:
    existing = existing or Response(question_id=question.id)
    badge = {
        "scoring": "Scoring",
        "qualitative": "Qualitativa",
        "hybrid": "Ibrida",
    }.get(question.question_purpose, question.question_purpose)

    st.markdown(f"**{question.text}**  ")
    st.caption(f"{badge} · ID {question.id}{' · obbligatoria' if question.required else ''}")
    if question.help_text:
        st.caption(question.help_text)

    value: Any = existing.value
    value_label = existing.value_label

    if question.type == "single_choice":
        option_labels = [opt.label for opt in question.options]
        option_values = [opt.value for opt in question.options]
        current_index = option_values.index(str(existing.value)) if str(existing.value) in option_values else None
        selected = st.selectbox(
            f"Risposta {question.id}",
            options=[""] + option_labels,
            index=(current_index + 1) if current_index is not None else 0,
            label_visibility="collapsed",
            key=f"{question.id}_value",
        )
        if selected:
            idx = option_labels.index(selected)
            value = option_values[idx]
            value_label = selected
        else:
            value = None
            value_label = ""
    elif question.type == "likert_1_5":
        current = int(existing.value) if str(existing.value).isdigit() else 3
        value = st.radio(
            f"Risposta {question.id}",
            options=list(LIKERT_LABELS.keys()),
            index=list(LIKERT_LABELS.keys()).index(current),
            horizontal=True,
            format_func=lambda x: LIKERT_LABELS[x],
            key=f"{question.id}_value",
            label_visibility="collapsed",
        )
        value_label = LIKERT_LABELS.get(int(value), "")
    elif question.type == "yes_no_comment":
        selected = st.radio(
            f"Risposta {question.id}", ["yes", "no"],
            index=0 if str(existing.value).lower() in {"yes", "true", "1"} else 1,
            horizontal=True,
            key=f"{question.id}_value",
            label_visibility="collapsed",
        )
        value = selected
        value_label = selected
    elif question.type == "text_short":
        value = st.text_input(
            f"Risposta {question.id}",
            value=str(existing.value or ""),
            placeholder=question.placeholder,
            key=f"{question.id}_value",
            label_visibility="collapsed",
        )
    else:
        value = st.text_area(
            f"Risposta {question.id}",
            value=str(existing.value or ""),
            placeholder=question.placeholder,
            key=f"{question.id}_value",
            height=110 if question.type == "text_long" else 80,
            label_visibility="collapsed",
        )

    not_applicable = existing.not_applicable
    if question.allows_na:
        not_applicable = st.checkbox("Non applicabile", value=existing.not_applicable, key=f"{question.id}_na")
        if not_applicable:
            value = None
            value_label = ""

    comment = existing.comment
    if question.allows_comment:
        comment_label = "Commento / evidenze"
        if compact:
            with st.expander(comment_label, expanded=bool(existing.comment or existing.evidence_note)):
                comment = st.text_area(
                    f"Commento {question.id}",
                    value=existing.comment,
                    height=70,
                    key=f"{question.id}_comment",
                    placeholder="Commento, eccezioni, esempi o note utili",
                    label_visibility="collapsed",
                )
                confidence, evidence_type, evidence_note = _render_evidence_fields(question.id, existing)
        else:
            comment = st.text_area(
                f"Commento {question.id}",
                value=existing.comment,
                height=70,
                key=f"{question.id}_comment",
                placeholder="Commento, eccezioni, esempi o note utili",
                label_visibility="collapsed",
            )
            confidence, evidence_type, evidence_note = _render_evidence_fields(question.id, existing)
    else:
        with st.expander("Evidenze e affidabilità", expanded=bool(existing.evidence_note)):
            confidence, evidence_type, evidence_note = _render_evidence_fields(question.id, existing)

    return Response(
        question_id=question.id,
        value=value,
        value_label=value_label,
        comment=comment,
        not_applicable=not_applicable,
        confidence=confidence,
        evidence_type=evidence_type,
        evidence_note=evidence_note,
        assessor_summary=existing.assessor_summary,
        insight_tags=existing.insight_tags,
        issue_flags=existing.issue_flags,
    )


def _render_evidence_fields(question_id: str, existing: Response):
    col1, col2 = st.columns(2)
    with col1:
        confidence = st.selectbox(
            "Affidabilità della risposta",
            CONFIDENCE_OPTIONS,
            index=CONFIDENCE_OPTIONS.index(existing.confidence),
            key=f"{question_id}_confidence",
        )
    with col2:
        evidence_type = st.selectbox(
            "Fonte principale",
            EVIDENCE_OPTIONS,
            index=EVIDENCE_OPTIONS.index(existing.evidence_type),
            key=f"{question_id}_evidence_type",
        )

    evidence_note = st.text_input(
        f"Nota evidenza {question_id}",
        value=existing.evidence_note,
        key=f"{question_id}_evidence_note",
        label_visibility="collapsed",
        placeholder="Fonte, documento o nota di supporto",
    )
    return confidence, evidence_type, evidence_note
