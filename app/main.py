from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from app.state.session_manager import get_document

st.set_page_config(page_title="Assessment Console", layout="wide")
st.title("Assessment Console")
document = get_document()

st.sidebar.success("Progetto scaffold caricato")
st.sidebar.write(f"Cliente: {document.assessment.client_name or 'N/D'}")
st.sidebar.write(f"Stato: {document.assessment.status}")

st.markdown(
    """
    Questo scaffold implementa la struttura base del tool di assessment:
    setup, core assessment, analisi, roadmap ed export/import.
    Usa il menu multipagina di Streamlit per navigare.
    """
)
