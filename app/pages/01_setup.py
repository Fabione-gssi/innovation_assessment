from __future__ import annotations

import io
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from app.state.session_manager import get_document, set_document
from persistence.excel_repository import ExcelRepository
from persistence.json_repository import JsonRepository

st.title("Setup assessment")
document = get_document()
meta = document.assessment

with st.form("setup_form"):
    meta.client_name = st.text_input("Cliente", value=meta.client_name)
    meta.assessor_name = st.text_input("Assessor", value=meta.assessor_name)
    meta.sector = st.text_input("Settore", value=meta.sector)
    meta.company_size = st.selectbox("Dimensione", ["", "micro", "piccola", "media", "grande"], index=["", "micro", "piccola", "media", "grande"].index(meta.company_size or ""))
    meta.mode = st.selectbox("Modalità", ["intervista_guidata", "workshop", "autocompilazione"], index=["intervista_guidata", "workshop", "autocompilazione"].index(meta.mode))
    objectives_raw = st.text_area("Obiettivi (uno per riga)", value="\n".join(meta.objectives))
    submitted = st.form_submit_button("Salva setup")
    if submitted:
        meta.objectives = [line.strip() for line in objectives_raw.splitlines() if line.strip()]
        document.assessment = meta
        set_document(document)
        st.success("Setup aggiornato")

st.subheader("Import")
uploaded = st.file_uploader("Carica JSON o Excel", type=["json", "xlsx"])
if uploaded:
    temp_path = ROOT / f"_tmp_import_{uploaded.name}"
    temp_path.write_bytes(uploaded.getvalue())
    if uploaded.name.endswith(".json"):
        document = JsonRepository.load(temp_path)
    else:
        document = ExcelRepository.load(temp_path)
    set_document(document)
    st.success("Assessment importato")

st.subheader("Export")
json_path = ROOT / "assessment_export.json"
excel_path = ROOT / "assessment_export.xlsx"
JsonRepository.save(document, json_path)
ExcelRepository.save(document, excel_path)

with open(json_path, "rb") as fh:
    st.download_button("Scarica JSON", fh.read(), file_name="assessment_export.json", mime="application/json")
with open(excel_path, "rb") as fh:
    st.download_button("Scarica Excel", fh.read(), file_name="assessment_export.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
