from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from app.state.session_manager import get_document, set_document
from core.models import Initiative
from core.prioritization import PrioritizationService

st.title("Prioritization")
document = get_document()
service = PrioritizationService()

with st.expander("Come viene calcolata la priorità", expanded=True):
    st.markdown(
        "La priorità proposta è una stima euristica v1:  \n"
        "`priority_index = gap_maturity × impact × feasibility × urgency / risk_penalty`  \n\n"
        "Dove:  \n"
        "- **gap_maturity** = 100 - maturity della sezione o del finding  \n"
        "- **impact** = valore atteso dell'intervento  \n"
        "- **feasibility** = facilità relativa di esecuzione  \n"
        "- **risk_penalty** = penalizzazione del rischio di intervento  \n\n"
        "Le classi proposte sono: Quick win, Foundational, Strategic bet, Risk mitigation, Monitor only, Not now.  \n"
        "Questa pagina è **modificabile**: puoi correggere classi, ordine, owner, stream e orizzonte prima di salvare."
    )

if not document.findings:
    st.warning("Nessun finding disponibile. Vai prima in Analysis.")
    st.stop()

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
reference_df = pd.DataFrame(rows).sort_values(by=["priority_index", "current_risk"], ascending=False)
st.subheader("Reference view sui finding")
st.dataframe(reference_df, use_container_width=True)

if not document.initiatives:
    if st.button("Genera iniziative proposte dai finding"):
        document.initiatives = service.findings_to_initiatives(document.findings)
        set_document(document)
        st.rerun()
else:
    st.subheader("Iniziative modificabili")
    edit_df = pd.DataFrame([
        {
            "id": i.id,
            "title": i.title,
            "description": i.description,
            "stream": i.stream,
            "priority_index": i.priority_index,
            "priority_rank": i.priority_rank,
            "priority_class": i.priority_class,
            "time_horizon": i.time_horizon,
            "effort": i.effort,
            "owner": i.owner,
            "success_kpis": ", ".join(i.success_kpis),
            "dependencies": ", ".join(i.dependencies),
            "notes": i.notes,
        }
        for i in document.initiatives
    ]).sort_values(by=["priority_rank", "priority_index"], ascending=[True, False])

    edited_df = st.data_editor(
        edit_df,
        use_container_width=True,
        num_rows="dynamic",
        hide_index=True,
        column_config={
            "priority_index": st.column_config.NumberColumn(min_value=0.0, step=1.0),
            "priority_rank": st.column_config.NumberColumn(min_value=1, step=1),
            "priority_class": st.column_config.SelectboxColumn(options=["Quick win", "Foundational", "Strategic bet", "Risk mitigation", "Monitor only", "Not now"]),
            "time_horizon": st.column_config.SelectboxColumn(options=["0_3_months", "3_6_months", "6_12_months", "12_plus_months"]),
            "effort": st.column_config.SelectboxColumn(options=["low", "medium", "high"]),
            "stream": st.column_config.SelectboxColumn(options=["governance", "processi", "management_kpi", "data", "ai", "change", "trasversale"]),
        },
    )

    if st.button("Salva prioritizzazione"):
        document.initiatives = [
            Initiative(
                id=str(row["id"]),
                title=str(row.get("title", "")),
                description=str(row.get("description", "")),
                stream=str(row.get("stream", "trasversale")),
                priority_index=float(row.get("priority_index", 0) or 0),
                priority_rank=int(row.get("priority_rank", 1) or 1),
                priority_class=str(row.get("priority_class", "Foundational")),
                time_horizon=str(row.get("time_horizon", "6_12_months")),
                effort=str(row.get("effort", "medium")),
                owner=str(row.get("owner", "")),
                success_kpis=_split_csv(row.get("success_kpis", "")),
                dependencies=_split_csv(row.get("dependencies", "")),
                notes=str(row.get("notes", "")),
                manual_override=True,
            )
            for _, row in edited_df.iterrows()
        ]
        set_document(document)
        st.success("Prioritizzazione salvata")


def _split_csv(value: object) -> list[str]:
    return [item.strip() for item in str(value or "").split(",") if item.strip()]
