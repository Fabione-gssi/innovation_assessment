from __future__ import annotations

import streamlit as st

from core.services import AssessmentService


TEMPLATE_PATH = "templates/core_question_bank.json"


def get_document():
    if "document" not in st.session_state:
        service = AssessmentService(TEMPLATE_PATH)
        st.session_state.document = service.create_empty_assessment()
    return st.session_state.document


def set_document(document):
    st.session_state.document = document
