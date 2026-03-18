from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from app.state.session_manager import get_document, set_document
from core.prioritization import PrioritizationService

st.title("Prioritization")
document = get_document()
service = PrioritizationService()

if not document.findings:
    st.warning("Nessun finding disponibile. Vai prima in Analysis.")
else:
    rows = []
    for finding in document.findings:
        idx = service.priority_index(finding)
        p_class = service.priority_class(idx, finding)
        rows.append(
            {
                "finding_id": finding.id,
                "area": finding.area,
                "title": finding.title,
                "severity": finding.severity,
                "priority_index": idx,
                "priority_class": p_class,
                "gap": finding.maturity_gap,
                "impact": finding.business_impact,
                "feasibility": finding.feasibility,
                "current_risk": finding.current_risk,
                "intervention_risk": finding.intervention_risk,
            }
        )
    df = pd.DataFrame(rows).sort_values(by=["priority_index", "current_risk"], ascending=False)
    st.dataframe(df, use_container_width=True)

    if st.button("Genera iniziative proposte"):
        document.initiatives = service.findings_to_initiatives(document.findings)
        set_document(document)
        st.success(f"Generate {len(document.initiatives)} iniziative proposte")

    if document.initiatives:
        st.subheader("Iniziative generate")
        st.dataframe(pd.DataFrame([i.model_dump() for i in document.initiatives]), use_container_width=True)
