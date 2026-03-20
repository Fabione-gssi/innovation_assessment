"""
Componenti UI riusabili per Streamlit.
Widget standardizzati per domande, scoring, tips, progress.
"""
from __future__ import annotations
import streamlit as st
from config import MATURITY_LEVELS, QUESTION_TYPES, MODULE_MAP, MODULES


def inject_custom_css():
    """Inietta CSS custom per il tema professionale."""
    st.markdown("""
    <style>
    /* ── Palette e variabili ──────────────────────────────────────── */
    :root {
        --primary: #3B3689;
        --primary-light: #EEEDFE;
        --accent: #1D9E75;
        --accent-light: #E1F5EE;
        --warning: #EF9F27;
        --danger: #E24B4A;
        --text: #2C2C2A;
        --text-muted: #5F5E5A;
        --bg: #FAFAF8;
        --card-bg: #FFFFFF;
        --border: #E8E6DF;
    }

    /* ── Sidebar ─────────────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FF7276 0%, #FF7276 100%);
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] label {
        color: #FFFFFF !important;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }

    /* ── Cards ───────────────────────────────────────────────────── */
    .assessment-card {
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
        transition: box-shadow 0.2s;
    }
    .assessment-card:hover {
        box-shadow: 0 2px 12px rgba(59,54,137,0.08);
    }

    /* ── Module header ───────────────────────────────────────────── */
    .module-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.6rem 1rem;
        background: var(--primary-light);
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid var(--primary);
    }
    .module-header h3 {
        margin: 0;
        color: var(--primary);
        font-size: 1.1rem;
    }
    .module-header .iso-ref {
        font-size: 0.8rem;
        color: var(--text-muted);
        font-weight: 500;
    }

    /* ── Tip box ─────────────────────────────────────────────────── */
    .tip-box {
        background: #FFF9EE;
        border: 1px solid #F5DEB3;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        font-size: 0.85rem;
        color: #7A6528;
        margin-top: 0.3rem;
        margin-bottom: 0.8rem;
        line-height: 1.5;
    }

    /* ── Maturity badge ──────────────────────────────────────────── */
    .maturity-badge {
        display: inline-block;
        padding: 0.25rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        color: white;
    }

    /* ── Progress bar custom ─────────────────────────────────────── */
    .progress-container {
        background: #F1EFE8;
        border-radius: 6px;
        height: 8px;
        overflow: hidden;
        margin: 0.3rem 0;
    }
    .progress-fill {
        height: 100%;
        border-radius: 6px;
        transition: width 0.5s ease;
    }

    /* ── Score display ───────────────────────────────────────────── */
    .score-big {
        font-size: 2.4rem;
        font-weight: 700;
        line-height: 1;
        margin: 0;
    }
    .score-label {
        font-size: 0.8rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* ── Priority tags ───────────────────────────────────────────── */
    .priority-critical { background: #FCEBEB; color: #A32D2D; border: 1px solid #F09595; }
    .priority-high     { background: #FAEEDA; color: #854F0B; border: 1px solid #FAC775; }
    .priority-medium   { background: #EAF3DE; color: #3B6D11; border: 1px solid #C0DD97; }
    .priority-low      { background: #E1F5EE; color: #0F6E56; border: 1px solid #9FE1CB; }
    .priority-tag {
        display: inline-block;
        padding: 0.2rem 0.7rem;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 600;
    }

    /* ── Animations ──────────────────────────────────────────────── */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(12px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .fade-in { animation: fadeInUp 0.4s ease-out; }

    /* ── Misc ────────────────────────────────────────────────────── */
    div[data-testid="stExpander"] {
        border: 1px solid var(--border);
        border-radius: 10px;
        overflow: hidden;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)


def render_module_header(module_id: str):
    """Render l'header di un modulo con icona, nome e riferimento ISO."""
    mod = MODULE_MAP.get(module_id, {})
    st.markdown(f"""
    <div class="module-header fade-in">
        <span style="font-size:1.5rem">{mod.get('icon','')}</span>
        <div>
            <h3>{mod.get('name','')}</h3>
            <span class="iso-ref">{mod.get('iso_ref','')} · {mod.get('description','')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_tip(tip: str):
    """Mostra un tip di compilazione."""
    if tip:
        st.markdown(f'<div class="tip-box">💡 <strong>Suggerimento:</strong> {tip}</div>',
                     unsafe_allow_html=True)


def render_question(question: dict, data, key_prefix: str = "") -> None:
    """
    Render una singola domanda con il widget appropriato.
    Salva automaticamente la risposta in data.
    """
    qid = question["id"]
    qtype = question["type"]
    text = question["text"]
    tip = question.get("tip", "")
    options = question.get("options", [])
    required = question.get("required", False)

    # Label con indicatore obbligatorio
    label = f"{'🔹 ' if required else ''}{text}"
    key = f"{key_prefix}_{qid}"

    current = data.get_answer_value(qid)

    if qtype == "scale":
        val = st.select_slider(
            label, options=[0, 1, 2, 3, 4, 5],
            value=current if current and isinstance(current, int) else 0,
            format_func=lambda x: _scale_label(x),
            key=key,
        )
        if val and val > 0:
            data.set_answer(qid, val)
        render_tip(tip)

    elif qtype == "single_choice":
        opts = ["— Seleziona —"] + options
        idx = 0
        if current and current in options:
            idx = options.index(current) + 1
        val = st.selectbox(label, opts, index=idx, key=key)
        if val and val != "— Seleziona —":
            data.set_answer(qid, val)
        render_tip(tip)

    elif qtype == "multi_choice":
        defaults = current if isinstance(current, list) else []
        val = st.multiselect(label, options, default=defaults, key=key)
        if val:
            data.set_answer(qid, val)
        render_tip(tip)

    elif qtype == "yes_no":
        opts = ["— Seleziona —", "Sì", "Parziale", "No"]
        idx = 0
        if current in opts:
            idx = opts.index(current)
        val = st.selectbox(label, opts, index=idx, key=key)
        if val and val != "— Seleziona —":
            data.set_answer(qid, val)
        render_tip(tip)

    elif qtype == "text":
        val = st.text_area(label, value=current or "", key=key, height=100)
        if val and val.strip():
            data.set_answer(qid, val.strip())
        render_tip(tip)

    # Note aggiuntive (collapsible)
    with st.expander("📝 Aggiungi note", expanded=False):
        existing_notes = ""
        ans = data.get_answer(qid)
        if ans:
            existing_notes = ans.get("notes", "")
        notes = st.text_input("Note", value=existing_notes, key=f"{key}_notes", label_visibility="collapsed")
        if notes:
            current_val = data.get_answer_value(qid)
            if current_val is not None:
                data.set_answer(qid, current_val, notes)


def _scale_label(val: int) -> str:
    if val == 0:
        return "⬜ Non valutato"
    labels = {
        1: "1 — Iniziale",
        2: "2 — Ripetibile",
        3: "3 — Definito",
        4: "4 — Gestito",
        5: "5 — Ottimizzato",
    }
    return labels.get(val, str(val))


def render_maturity_badge(level: int):
    """Render un badge colorato per il livello di maturità."""
    info = MATURITY_LEVELS.get(level, {"label": "N/D", "color": "#888"})
    st.markdown(
        f'<span class="maturity-badge" style="background:{info["color"]}">'
        f'{level} — {info["label"]}</span>',
        unsafe_allow_html=True
    )


def render_progress_bar(value: float, max_val: float = 100, color: str = "#3B3689"):
    """Render una barra di progresso custom."""
    pct = min(100, max(0, value / max_val * 100)) if max_val > 0 else 0
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-fill" style="width:{pct}%;background:{color}"></div>
    </div>
    """, unsafe_allow_html=True)


def render_score_card(label: str, score: float, color: str = "#3B3689", suffix: str = "/5"):
    """Render una card con punteggio grande."""
    st.markdown(f"""
    <div style="text-align:center;padding:0.5rem">
        <p class="score-label">{label}</p>
        <p class="score-big" style="color:{color}">{score:.1f}<span style="font-size:1rem;color:#888">{suffix}</span></p>
    </div>
    """, unsafe_allow_html=True)


def render_priority_tag(priority: str):
    """Render un tag di priorità colorato."""
    labels = {"critical": "Critica", "high": "Alta", "medium": "Media", "low": "Bassa"}
    st.markdown(
        f'<span class="priority-tag priority-{priority}">{labels.get(priority, priority)}</span>',
        unsafe_allow_html=True,
    )
