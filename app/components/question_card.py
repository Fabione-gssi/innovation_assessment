from __future__ import annotations

from typing import Any, List, Optional

import streamlit as st

from core.models import Question, Response


CONFIDENCE_OPTIONS = ["low", "medium", "high"]
EVIDENCE_OPTIONS = ["percezione", "intervista", "documento", "dato"]


def render_question(question: Question, existing: Optional[Response] = None) -> Response:
    existing = existing or Response(question_id=question.id)
    st.markdown(f"**{question.text}**")
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
        labels = {
            1: "1 - Molto basso / assente",
            2: "2 - Basso",
            3: "3 - Medio",
            4: "4 - Buono",
            5: "5 - Molto buono",
        }
        current = int(existing.value) if str(existing.value).isdigit() else 3
        value = st.radio(
            f"Risposta {question.id}",
            options=list(labels.keys()),
            index=list(labels.keys()).index(current),
            horizontal=True,
            format_func=lambda x: labels[x],
            key=f"{question.id}_value",
            label_visibility="collapsed",
        )
        value_label = labels.get(int(value), "")
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
            height=100 if question.type == "text_long" else 70,
            label_visibility="collapsed",
        )

    comment = existing.comment
    if question.allows_comment:
        comment = st.text_area(
            f"Commento {question.id}",
            value=existing.comment,
            height=70,
            key=f"{question.id}_comment",
            placeholder="Commento, evidenze o precisazioni",
            label_visibility="collapsed",
        )

    col1, col2 = st.columns(2)
    with col1:
        confidence = st.selectbox(
            "Confidence",
            CONFIDENCE_OPTIONS,
            index=CONFIDENCE_OPTIONS.index(existing.confidence),
            key=f"{question.id}_confidence",
        )
    with col2:
        evidence_type = st.selectbox(
            "Fonte",
            EVIDENCE_OPTIONS,
            index=EVIDENCE_OPTIONS.index(existing.evidence_type),
            key=f"{question.id}_evidence_type",
        )

    evidence_note = st.text_input(
        f"Nota evidenza {question.id}",
        value=existing.evidence_note,
        key=f"{question.id}_evidence_note",
        label_visibility="collapsed",
        placeholder="Fonte, documento o nota di supporto",
    )

    return Response(
        question_id=question.id,
        value=value,
        value_label=value_label,
        comment=comment,
        not_applicable=False,
        confidence=confidence,
        evidence_type=evidence_type,
        evidence_note=evidence_note,
        assessor_summary=existing.assessor_summary,
        insight_tags=existing.insight_tags,
        issue_flags=existing.issue_flags,
    )
