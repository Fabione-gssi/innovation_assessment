from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from app.state.session_manager import get_document, set_document
from core.models import RoadmapItem
from core.roadmap import RoadmapService

st.title("Roadmap")
document = get_document()
service = RoadmapService()

with st.expander("Come viene costruita la roadmap", expanded=True):
    st.markdown(
        "La roadmap proposta deriva dalla prioritizzazione salvata.  \n"
        "Ogni iniziativa viene mappata su:  \n"
        "- **orizzonte temporale**  \n"
        "- **stream**  \n"
        "- **classe di priorità**  \n"
        "- **owner, dipendenze, KPI di successo**  \n\n"
        "Anche questa pagina è modificabile: puoi cambiare sequenza, orizzonte, stream, stato e note prima di salvare."
    )

if not document.initiatives:
    st.warning("Nessuna iniziativa disponibile. Vai prima in Prioritization.")
    st.stop()

if not document.roadmap:
    if st.button("Genera roadmap proposta"):
        document.roadmap = service.initiatives_to_roadmap(document.initiatives)
        set_document(document)
        st.rerun()
else:
    roadmap_df = pd.DataFrame([
        {
            "id": item.id,
            "initiative_id": item.initiative_id,
            "sequence": item.sequence,
            "time_horizon": item.time_horizon,
            "stream": item.stream,
            "priority_class": item.priority_class,
            "owner": item.owner,
            "dependencies": ", ".join(item.dependencies),
            "success_kpis": ", ".join(item.success_kpis),
            "status": item.status,
            "notes": item.notes,
        }
        for item in document.roadmap
    ]).sort_values(by=["sequence", "time_horizon"])

    st.subheader("Roadmap modificabile")
    edited_df = st.data_editor(
        roadmap_df,
        use_container_width=True,
        num_rows="dynamic",
        hide_index=True,
        column_config={
            "sequence": st.column_config.NumberColumn(min_value=1, step=1),
            "time_horizon": st.column_config.SelectboxColumn(options=["0_3_months", "3_6_months", "6_12_months", "12_plus_months"]),
            "stream": st.column_config.SelectboxColumn(options=["governance", "processi", "management_kpi", "data", "ai", "change", "trasversale"]),
            "priority_class": st.column_config.SelectboxColumn(options=["Quick win", "Foundational", "Strategic bet", "Risk mitigation", "Monitor only", "Not now"]),
            "status": st.column_config.SelectboxColumn(options=["proposed", "validated", "approved", "parked"]),
        },
    )

    if st.button("Salva roadmap"):
        document.roadmap = [
            RoadmapItem(
                id=str(row["id"]),
                initiative_id=str(row.get("initiative_id", "")),
                sequence=int(row.get("sequence", 1) or 1),
                time_horizon=str(row.get("time_horizon", "6_12_months")),
                stream=str(row.get("stream", "trasversale")),
                priority_class=str(row.get("priority_class", "Foundational")),
                owner=str(row.get("owner", "")),
                dependencies=_split_csv(row.get("dependencies", "")),
                success_kpis=_split_csv(row.get("success_kpis", "")),
                status=str(row.get("status", "proposed")),
                notes=str(row.get("notes", "")),
            )
            for _, row in edited_df.iterrows()
        ]
        set_document(document)
        st.success("Roadmap salvata")

    st.subheader("Vista per orizzonte temporale")
    for horizon in ["0_3_months", "3_6_months", "6_12_months", "12_plus_months"]:
        subset = edited_df[edited_df["time_horizon"] == horizon]
        with st.expander(horizon, expanded=horizon == "0_3_months"):
            if subset.empty:
                st.caption("Nessun item")
            else:
                st.dataframe(subset[["sequence", "initiative_id", "stream", "priority_class", "status", "owner"]], use_container_width=True)


def _split_csv(value: object) -> list[str]:
    return [item.strip() for item in str(value or "").split(",") if item.strip()]
