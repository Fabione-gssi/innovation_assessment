"""
Dashboard di visualizzazione risultati.
Radar chart, KPI, gap analysis, matrice impatto/effort, roadmap.
"""
from __future__ import annotations
import streamlit as st
import plotly.graph_objects as go
from config import MODULES, MODULE_MAP, MATURITY_LEVELS, PRIORITY_LEVELS
from engine.scoring import (
    compute_all_scores, compute_global_score, compute_completion_rate,
    get_maturity_label, get_maturity_color,
)
from engine.analysis import gap_analysis, generate_recommendations, auto_generate_roadmap
from ui.components import (
    render_maturity_badge, render_progress_bar, render_score_card, render_priority_tag,
)
from dataclasses import asdict


def render_dashboard(data):
    """Render completa della dashboard risultati."""
    results = compute_all_scores(data)
    # Salva risultati nel data model
    data.module_results = {k: asdict(v) for k, v in results.items()}

    global_score = compute_global_score(results)
    completion = compute_completion_rate(data)

    # ── KPI summary row ────────────────────────────────────────────────
    st.markdown("### 📊 Quadro di sintesi")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_score_card("Score globale", global_score, "#3B3689")
    with c2:
        avg_maturity = round(global_score) if global_score > 0 else 0
        color = get_maturity_color(avg_maturity) if avg_maturity > 0 else "#888"
        render_score_card("Maturità media", avg_maturity, color, "")
        if avg_maturity > 0:
            render_maturity_badge(avg_maturity)
    with c3:
        render_score_card("Completamento", completion["global"]["rate"], "#1D9E75", "%")
    with c4:
        gaps = gap_analysis(results)
        critical_count = sum(1 for g in gaps if g["priority"] in ("critical", "high"))
        render_score_card("Gap critici/alti", critical_count, "#E24B4A" if critical_count > 0 else "#1D9E75", "")

    st.markdown("---")

    # ── Radar chart ────────────────────────────────────────────────────
    col_radar, col_table = st.columns([3, 2])

    with col_radar:
        st.markdown("### 🕸️ Mappa di maturità")
        _render_radar_chart(results, data)

    with col_table:
        st.markdown("### 📋 Dettaglio per modulo")
        _render_results_table(results, completion)

    st.markdown("---")

    # ── Gap analysis ───────────────────────────────────────────────────
    st.markdown("### 🔍 Gap analysis")
    _render_gap_analysis(results, data)

    st.markdown("---")

    # ── Raccomandazioni ────────────────────────────────────────────────
    st.markdown("### 💡 Raccomandazioni")
    _render_recommendations(results)

    st.markdown("---")

    # ── Roadmap ────────────────────────────────────────────────────────
    st.markdown("### 🗺️ Roadmap")
    _render_roadmap(data, results)


def _render_radar_chart(results, data):
    """Render del radar chart con plotly."""
    categories = []
    scores = []
    targets = []

    for mod in MODULES:
        r = results.get(mod["id"])
        if r:
            categories.append(mod["name"][:25])
            scores.append(r.score)
            targets.append(data.target_levels.get(mod["id"], 3))

    if not scores or all(s == 0 for s in scores):
        st.info("Compila almeno alcune domande per visualizzare il radar chart.")
        return

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=targets + [targets[0]],
        theta=categories + [categories[0]],
        fill="toself",
        name="Target",
        line=dict(color="rgba(59,54,137,0.3)", dash="dash"),
        fillcolor="rgba(59,54,137,0.05)",
    ))

    fig.add_trace(go.Scatterpolar(
        r=scores + [scores[0]],
        theta=categories + [categories[0]],
        fill="toself",
        name="AS-IS",
        line=dict(color="#3B3689", width=2),
        fillcolor="rgba(59,54,137,0.15)",
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 5], tickmode="linear", dtick=1),
            angularaxis=dict(tickfont=dict(size=10)),
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        margin=dict(l=80, r=80, t=20, b=40),
        height=420,
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_results_table(results, completion):
    """Tabella riassuntiva dei risultati per modulo."""
    for mod in MODULES:
        r = results.get(mod["id"])
        comp = completion["modules"].get(mod["id"], {})
        if r and r.score > 0:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"**{mod['icon']} {mod['name'][:28]}**")
            with col2:
                st.markdown(f"**{r.score:.1f}**/5")
            with col3:
                render_maturity_badge(r.maturity_level)
            render_progress_bar(r.score, 5, get_maturity_color(r.maturity_level))
            st.caption(f"Completamento: {comp.get('answered', 0)}/{comp.get('total', 0)} domande")
            st.markdown("")


def _render_gap_analysis(results, data):
    """Visualizzazione gap analysis con barre orizzontali."""
    gaps = gap_analysis(results)
    if not gaps:
        st.info("Compila almeno alcune domande per visualizzare la gap analysis.")
        return

    # Bar chart AS-IS vs TO-BE
    fig = go.Figure()

    names = [g["module_name"][:25] for g in gaps]
    as_is = [g["as_is"] for g in gaps]
    to_be = [g["to_be"] for g in gaps]

    fig.add_trace(go.Bar(
        y=names, x=as_is, name="AS-IS (attuale)",
        orientation="h", marker_color="#3B3689",
        text=[f"{v:.1f}" for v in as_is], textposition="inside",
    ))
    fig.add_trace(go.Bar(
        y=names, x=to_be, name="TO-BE (target)",
        orientation="h", marker_color="rgba(59,54,137,0.25)",
        text=[f"{v:.0f}" for v in to_be], textposition="inside",
    ))

    fig.update_layout(
        barmode="overlay",
        xaxis=dict(range=[0, 5.5], title="Livello maturità"),
        yaxis=dict(autorange="reversed"),
        height=max(300, len(gaps) * 50),
        margin=dict(l=20, r=20, t=10, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Dettaglio gap
    for g in gaps:
        if g["gap"] > 0:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"**{g['icon']} {g['module_name']}**")
            with col2:
                st.markdown(f"Gap: **{g['gap']:.1f}**")
            with col3:
                render_priority_tag(g["priority"])


def _render_recommendations(results):
    """Mostra le raccomandazioni prioritizzate."""
    recs = generate_recommendations(results)
    if not recs:
        st.info("Compila almeno alcune domande per generare le raccomandazioni.")
        return

    for rec in recs:
        with st.expander(f"{rec['icon']} {rec['module_name']} — Livello {rec['current_level']} → {rec['target_level']}"):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(rec["recommendation"])
            with col2:
                render_priority_tag(rec["priority"])


def _render_roadmap(data, results):
    """Render della roadmap con possibilità di generazione automatica."""
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Genera roadmap automatica", use_container_width=True):
            data.roadmap = auto_generate_roadmap(data)
            st.rerun()

    if not data.roadmap:
        st.info("Premi 'Genera roadmap automatica' per creare una roadmap basata sulla gap analysis, oppure aggiungi azioni manualmente nella sezione dedicata.")
        return

    # Raggruppamento per timeframe
    timeframes = {}
    for item in data.roadmap:
        if isinstance(item, dict):
            tf = item.get("timeframe", "Non pianificato")
            if tf not in timeframes:
                timeframes[tf] = []
            timeframes[tf].append(item)

    for tf, items in timeframes.items():
        st.markdown(f"**📅 {tf}**")
        for item in items:
            mod_info = MODULE_MAP.get(item.get("module_id", ""), {})
            col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
            with col1:
                st.markdown(f"{mod_info.get('icon', '')} **{item.get('title', '')}**")
                st.caption(item.get("description", "")[:120])
            with col2:
                render_priority_tag(item.get("priority", "medium"))
            with col3:
                st.caption(f"Effort: {item.get('effort', '-')}")
            with col4:
                st.caption(f"Stato: {item.get('status', '-')}")
        st.markdown("")
