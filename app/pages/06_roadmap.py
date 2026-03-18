from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from app.state.session_manager import get_document, set_document
from core.roadmap import RoadmapService

st.title("Roadmap")
document = get_document()
service = RoadmapService()

if not document.initiatives:
    st.warning("Nessuna iniziativa disponibile. Vai prima in Prioritization.")
else:
    if st.button("Genera roadmap proposta"):
        document.roadmap = service.initiatives_to_roadmap(document.initiatives)
        set_document(document)
        st.success(f"Creati {len(document.roadmap)} roadmap item")

if document.roadmap:
    df = pd.DataFrame([item.model_dump() for item in document.roadmap])
    st.subheader("Roadmap items")
    st.dataframe(df, use_container_width=True)

    st.subheader("Vista per orizzonte temporale")
    for horizon in ["0_3_months", "3_6_months", "6_12_months", "12_plus_months"]:
        subset = df[df["time_horizon"] == horizon]
        with st.expander(horizon, expanded=horizon == "0_3_months"):
            if subset.empty:
                st.caption("Nessun item")
            else:
                st.dataframe(subset[["initiative_id", "stream", "priority_class", "status", "notes"]], use_container_width=True)
