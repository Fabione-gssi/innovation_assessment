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

st.sidebar.success("Progetto assessment caricato")
st.sidebar.write(f"Cliente: {document.assessment.client_name or 'N/D'}")
st.sidebar.write(f"Stato: {document.assessment.status}")
st.sidebar.write(f"Moduli attivi: {', '.join(document.assessment.active_modules) or 'nessuno'}")

st.markdown(
    """
    Questa versione aggiornata centralizza la compilazione nella pagina **Assessment**, rende separata la configurazione dei **Moduli**, 
    spiega in-app come funzionano punteggi e priorità, e permette di **modificare prioritizzazione e roadmap prima del salvataggio**.
    """
)
