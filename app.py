"""
Innovation Assessment Tool
Entry point Streamlit.
Conforme UNI 11814:2021 · UNI EN ISO 56001:2024
"""
import streamlit as st
import json, uuid
from datetime import datetime

from config import (
    APP_TITLE, APP_SUBTITLE, APP_VERSION, APP_ICON, PAGE_CONFIG,
    MODULES, MODULE_MAP, MODULE_IDS, CATEGORIES, QUESTION_TYPES,
)
from models.schema import AssessmentData
from models.questions import (
    get_questions_for_module, get_scorable_questions, QUESTIONS_BY_MODULE,
)
from engine.scoring import (
    compute_all_scores, compute_global_score, compute_completion_rate,
    get_maturity_label, get_maturity_color,
)
from engine.analysis import gap_analysis, auto_generate_roadmap
from ui.components import (
    inject_custom_css, render_module_header, render_question,
    render_maturity_badge, render_progress_bar, render_score_card, render_priority_tag,
)
from ui.dashboard import render_dashboard
from io_handlers.json_handler import save_to_json_bytes, load_from_json_file
from io_handlers.excel_handler import save_to_excel, load_from_excel
from dataclasses import asdict


# ═══════════════════════════════════════════════════════════════════════════
# INIZIALIZZAZIONE
# ═══════════════════════════════════════════════════════════════════════════
st.set_page_config(**PAGE_CONFIG)

def _get_data() -> AssessmentData:
    """Ritorna (o crea) i dati di assessment nella sessione."""
    if "assessment_data" not in st.session_state:
        st.session_state.assessment_data = AssessmentData()
        st.session_state.assessment_data.touch()
    return st.session_state.assessment_data

def _set_data(data: AssessmentData):
    st.session_state.assessment_data = data

inject_custom_css()
data = _get_data()


# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR — NAVIGAZIONE
# ═══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"## {APP_ICON} {APP_TITLE}")
    st.caption(APP_SUBTITLE)
    st.markdown("---")

    # ── Navigazione principale ─────────────────────────────────────────
    pages = [
        "🏠 Home",
        "🏢 Dati azienda",
    ]
    # Moduli di assessment
    for mod in MODULES:
        completion = compute_completion_rate(data)
        mod_comp = completion["modules"].get(mod["id"], {})
        rate = mod_comp.get("rate", 0)
        badge = f" ({rate:.0f}%)" if rate > 0 else ""
        pages.append(f"{mod['icon']} {mod['name'][:22]}{badge}")

    pages += [
        "➕ Domande custom",
        "📊 Dashboard",
        "🗺️ Roadmap",
        "💾 Import/Export",
    ]

    selected = st.radio("Navigazione", pages, label_visibility="collapsed")

    st.markdown("---")

    # ── Mini progress ──────────────────────────────────────────────────
    completion = compute_completion_rate(data)
    gl = completion["global"]
    st.markdown(f"**Progresso globale: {gl['rate']:.0f}%**")
    render_progress_bar(gl["rate"], 100, "#1D9E75")
    st.caption(f"{gl['answered']}/{gl['total']} domande completate")

    st.markdown("---")
    st.caption(f"v{APP_VERSION}")


# ═══════════════════════════════════════════════════════════════════════════
# PAGINA: HOME
# ═══════════════════════════════════════════════════════════════════════════
if selected == "🏠 Home":
    st.markdown(f"# {APP_ICON} {APP_TITLE}")
    st.markdown(f"*{APP_SUBTITLE}*")
    st.markdown("---")

    st.markdown("""
    Benvenuto nel tool di **Innovation Assessment** progettato per supportare
    l'Innovation Manager nella raccolta strutturata, nell'analisi e nella definizione
    delle priorità di intervento.

    Il tool è organizzato in **10 moduli di assessment** allineati alla struttura
    della norma **UNI EN ISO 56001:2024** (Sistema di gestione per l'innovazione — Requisiti)
    e coerente con le competenze dell'Innovation Manager definite nella **UNI 11814:2021**.
    """)

    st.markdown("### Come usare il tool")
    st.markdown("""
    1. **Dati azienda** — Inserisci le informazioni base del cliente
    2. **Moduli 1-10** — Compila le domande di assessment (puoi procedere in qualsiasi ordine)
    3. **Domande custom** — Aggiungi domande personalizzate se necessario
    4. **Dashboard** — Visualizza i risultati, la gap analysis e le raccomandazioni
    5. **Roadmap** — Genera e personalizza la roadmap di intervento
    6. **Import/Export** — Salva e carica l'assessment in formato JSON o Excel
    """)

    # Mappa moduli
    st.markdown("### Moduli di assessment")
    for cat_id, cat_info in CATEGORIES.items():
        st.markdown(f"**{cat_info['label']}**")
        cat_modules = [m for m in MODULES if m["category"] == cat_id]
        cols = st.columns(min(len(cat_modules), 3))
        for i, mod in enumerate(cat_modules):
            with cols[i % len(cols)]:
                comp = completion["modules"].get(mod["id"], {})
                rate = comp.get("rate", 0)
                n_qs = comp.get("total", 0)
                st.markdown(f"""
                <div class="assessment-card fade-in">
                    <div style="font-size:1.5rem;margin-bottom:0.3rem">{mod['icon']}</div>
                    <strong>{mod['name']}</strong><br>
                    <span style="font-size:0.8rem;color:#5F5E5A">{mod['iso_ref']} · {n_qs} domande</span><br>
                    <span style="font-size:0.8rem;color:#1D9E75">Completamento: {rate:.0f}%</span>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("")


# ═══════════════════════════════════════════════════════════════════════════
# PAGINA: DATI AZIENDA
# ═══════════════════════════════════════════════════════════════════════════
elif selected == "🏢 Dati azienda":
    st.markdown("## 🏢 Dati azienda e assessor")
    st.markdown("Informazioni generali sull'organizzazione oggetto dell'assessment.")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Organizzazione")
        data.company_name = st.text_input("Nome azienda", value=data.company_name, key="company_name")
        data.company_sector = st.text_input("Settore", value=data.company_sector, key="company_sector",
                                            help="Es: Manifatturiero, Servizi, IT, Food, Energia, ecc.")
        data.company_size = st.selectbox("Dimensione",
            ["", "Micro (< 10 dipendenti)", "Piccola (10-49)", "Media (50-249)", "Grande (250+)"],
            index=["", "Micro (< 10 dipendenti)", "Piccola (10-49)", "Media (50-249)", "Grande (250+)"].index(data.company_size) if data.company_size in ["", "Micro (< 10 dipendenti)", "Piccola (10-49)", "Media (50-249)", "Grande (250+)"] else 0,
            key="company_size",
        )
        data.company_revenue = st.text_input("Fatturato (indicativo)", value=data.company_revenue, key="company_revenue",
                                              help="Es: 5M€, 50M€, 500M€")
        data.company_employees = st.text_input("N. dipendenti", value=data.company_employees, key="company_employees")

    with col2:
        st.markdown("#### Assessor")
        data.assessor_name = st.text_input("Nome assessor", value=data.assessor_name, key="assessor_name")
        data.assessor_role = st.text_input("Ruolo", value=data.assessor_role, key="assessor_role",
                                           help="Es: Innovation Manager, Consulente, CTO")
        st.markdown("#### Target di maturità")
        st.caption("Imposta il livello target (1-5) per ciascun modulo. Default: 3.")
        for mod in MODULES:
            current_target = data.target_levels.get(mod["id"], 3)
            val = st.slider(f"{mod['icon']} {mod['name'][:25]}", 1, 5, current_target, key=f"target_{mod['id']}")
            data.target_levels[mod["id"]] = val

    st.markdown("#### Descrizione dell'organizzazione")
    data.company_description = st.text_area(
        "Descrizione", value=data.company_description, key="company_desc",
        height=120, help="Breve descrizione dell'attività, prodotti/servizi, mercato di riferimento.",
    )
    data.touch()


# ═══════════════════════════════════════════════════════════════════════════
# PAGINE: MODULI DI ASSESSMENT (1-10)
# ═══════════════════════════════════════════════════════════════════════════
else:
    # Trova il modulo selezionato
    current_module = None
    for mod in MODULES:
        if mod["icon"] in selected and mod["name"][:15] in selected:
            current_module = mod
            break

    if current_module:
        render_module_header(current_module["id"])

        questions = get_questions_for_module(current_module["id"], data.custom_questions)
        scorable = get_scorable_questions(current_module["id"], data.custom_questions)

        # Progress del modulo
        comp = compute_completion_rate(data)["modules"].get(current_module["id"], {})
        st.markdown(f"**Progresso: {comp.get('answered', 0)}/{comp.get('total', 0)} domande** ({comp.get('rate', 0):.0f}%)")
        render_progress_bar(comp.get("rate", 0), 100, "#3B3689")
        st.markdown("---")

        # Render domande
        for i, q in enumerate(questions):
            st.markdown(f"##### Domanda {i+1}")
            if q.get("iso_ref"):
                st.caption(f"Riferimento: {q['iso_ref']}")
            render_question(q, data, key_prefix=current_module["id"])
            st.markdown("---")

        # Punteggio modulo live
        result = compute_all_scores(data).get(current_module["id"])
        if result and result.score > 0:
            st.markdown("### Risultato modulo")
            col1, col2, col3 = st.columns(3)
            with col1:
                render_score_card("Punteggio", result.score, get_maturity_color(result.maturity_level))
            with col2:
                render_maturity_badge(result.maturity_level)
                st.caption(get_maturity_label(result.maturity_level))
            with col3:
                render_score_card("Gap", result.gap, "#E24B4A" if result.gap > 1 else "#1D9E75")

    # ── Domande custom ─────────────────────────────────────────────────
    elif "Domande custom" in selected:
        st.markdown("## ➕ Domande personalizzate")
        st.markdown("Aggiungi domande custom a qualsiasi modulo. Verranno integrate nel calcolo dei punteggi.")
        st.markdown("---")

        # Lista domande custom esistenti
        if data.custom_questions:
            st.markdown("### Domande aggiunte")
            for i, q in enumerate(data.custom_questions):
                mod_name = MODULE_MAP.get(q.get("module", ""), {}).get("name", q.get("module", ""))
                with st.expander(f"{q.get('text', 'Domanda')[:60]}... — {mod_name}"):
                    st.markdown(f"**Modulo:** {mod_name}")
                    st.markdown(f"**Tipo:** {QUESTION_TYPES.get(q.get('type', ''), q.get('type', ''))}")
                    st.markdown(f"**Peso:** {q.get('weight', 1.0)}")
                    if q.get("tip"):
                        st.markdown(f"**Tip:** {q['tip']}")
                    if st.button(f"🗑️ Rimuovi", key=f"del_custom_{i}"):
                        data.custom_questions.pop(i)
                        st.rerun()
            st.markdown("---")

        # Form aggiunta
        st.markdown("### Aggiungi nuova domanda")
        with st.form("add_custom_question", clear_on_submit=True):
            cq_module = st.selectbox("Modulo", [m["id"] for m in MODULES],
                                      format_func=lambda x: f"{MODULE_MAP[x]['icon']} {MODULE_MAP[x]['name']}")
            cq_text = st.text_area("Testo della domanda", height=80)
            cq_type = st.selectbox("Tipo", list(QUESTION_TYPES.keys()),
                                    format_func=lambda x: QUESTION_TYPES[x])
            cq_options = st.text_input("Opzioni (separate da virgola, per scelta singola/multipla)",
                                        help="Es: Opzione A, Opzione B, Opzione C")
            col1, col2 = st.columns(2)
            with col1:
                cq_weight = st.number_input("Peso", min_value=0.0, max_value=3.0, value=1.0, step=0.1)
            with col2:
                cq_required = st.checkbox("Obbligatoria", value=False)
            cq_tip = st.text_input("Suggerimento di compilazione")

            if st.form_submit_button("➕ Aggiungi domanda", use_container_width=True):
                if cq_text.strip():
                    new_q = {
                        "id": f"custom_{uuid.uuid4().hex[:8]}",
                        "module": cq_module,
                        "type": cq_type,
                        "text": cq_text.strip(),
                        "options": [o.strip() for o in cq_options.split(",") if o.strip()] if cq_options else [],
                        "weight": cq_weight,
                        "required": cq_required,
                        "tip": cq_tip,
                        "iso_ref": "",
                    }
                    data.custom_questions.append(new_q)
                    data.touch()
                    st.success(f"Domanda aggiunta al modulo {MODULE_MAP[cq_module]['name']}!")
                    st.rerun()
                else:
                    st.error("Inserisci il testo della domanda.")

    # ── Dashboard ──────────────────────────────────────────────────────
    elif "Dashboard" in selected:
        st.markdown("## 📊 Dashboard risultati")
        st.markdown("---")
        render_dashboard(data)

    # ── Roadmap standalone ─────────────────────────────────────────────
    elif "Roadmap" in selected:
        st.markdown("## 🗺️ Roadmap di intervento")
        st.markdown("---")

        # Generazione automatica
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🔄 Genera automatica", use_container_width=True):
                data.roadmap = auto_generate_roadmap(data)
                data.touch()
                st.rerun()

        # Aggiunta manuale
        with st.expander("➕ Aggiungi azione manuale"):
            with st.form("add_roadmap_item", clear_on_submit=True):
                ri_title = st.text_input("Titolo azione")
                ri_desc = st.text_area("Descrizione", height=80)
                ri_module = st.selectbox("Modulo riferimento", [""] + [m["id"] for m in MODULES],
                                          format_func=lambda x: f"{MODULE_MAP[x]['icon']} {MODULE_MAP[x]['name']}" if x else "— Nessuno —")
                c1, c2, c3 = st.columns(3)
                with c1:
                    ri_priority = st.selectbox("Priorità", ["critical", "high", "medium", "low"],
                                                format_func=lambda x: {"critical": "🔴 Critica", "high": "🟠 Alta", "medium": "🟡 Media", "low": "🟢 Bassa"}.get(x, x))
                with c2:
                    ri_effort = st.selectbox("Effort", ["low", "medium", "high"])
                with c3:
                    ri_impact = st.selectbox("Impatto", ["low", "medium", "high"])
                c1, c2 = st.columns(2)
                with c1:
                    ri_timeframe = st.text_input("Timeframe", placeholder="Es: Q1 2025, 0-3 mesi")
                with c2:
                    ri_owner = st.text_input("Owner")

                if st.form_submit_button("➕ Aggiungi", use_container_width=True):
                    if ri_title.strip():
                        data.roadmap.append({
                            "id": f"ri_{uuid.uuid4().hex[:8]}",
                            "title": ri_title.strip(),
                            "description": ri_desc.strip(),
                            "module_id": ri_module,
                            "priority": ri_priority,
                            "effort": ri_effort,
                            "impact": ri_impact,
                            "timeframe": ri_timeframe,
                            "owner": ri_owner,
                            "status": "planned",
                            "notes": "",
                        })
                        data.touch()
                        st.rerun()

        # Mostra roadmap
        if data.roadmap:
            for i, item in enumerate(data.roadmap):
                if isinstance(item, dict):
                    mod_info = MODULE_MAP.get(item.get("module_id", ""), {})
                    with st.expander(f"{mod_info.get('icon', '📌')} {item.get('title', 'Azione')}"):
                        st.markdown(f"**Descrizione:** {item.get('description', '-')}")
                        c1, c2, c3, c4 = st.columns(4)
                        with c1:
                            render_priority_tag(item.get("priority", "medium"))
                        with c2:
                            st.caption(f"Effort: {item.get('effort', '-')}")
                        with c3:
                            st.caption(f"Impatto: {item.get('impact', '-')}")
                        with c4:
                            new_status = st.selectbox("Stato", ["planned", "in_progress", "done"],
                                                       index=["planned", "in_progress", "done"].index(item.get("status", "planned")),
                                                       key=f"status_{i}")
                            data.roadmap[i]["status"] = new_status

                        if item.get("timeframe"):
                            st.caption(f"📅 {item['timeframe']}")
                        if item.get("owner"):
                            st.caption(f"👤 {item['owner']}")

                        if st.button("🗑️ Rimuovi", key=f"del_road_{i}"):
                            data.roadmap.pop(i)
                            data.touch()
                            st.rerun()
        else:
            st.info("Nessuna azione nella roadmap. Genera automaticamente dai risultati o aggiungi azioni manualmente.")

    # ── Import/Export ──────────────────────────────────────────────────
    elif "Import/Export" in selected:
        st.markdown("## 💾 Import / Export")
        st.markdown("Salva e carica l'assessment completo in formato JSON o Excel.")
        st.markdown("---")

        # Prima calcola i risultati per includerli nell'export
        results = compute_all_scores(data)
        data.module_results = {k: asdict(v) for k, v in results.items()}
        data.touch()

        tab_export, tab_import = st.tabs(["📤 Export (Download)", "📥 Import (Upload)"])

        with tab_export:
            st.markdown("### Download assessment")
            company = data.company_name.replace(" ", "_") if data.company_name else "assessment"
            ts = datetime.now().strftime("%Y%m%d")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 📄 JSON")
                st.caption("Formato canonico, leggibile e versionabile.")
                st.download_button(
                    "⬇️ Scarica JSON",
                    data=save_to_json_bytes(data),
                    file_name=f"{company}_assessment_{ts}.json",
                    mime="application/json",
                    use_container_width=True,
                )
            with col2:
                st.markdown("#### 📊 Excel")
                st.caption("Formato tabellare per condivisione e analisi.")
                st.download_button(
                    "⬇️ Scarica Excel",
                    data=save_to_excel(data),
                    file_name=f"{company}_assessment_{ts}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                )

        with tab_import:
            st.markdown("### Carica assessment")
            st.warning("⚠️ L'import sovrascrive i dati correnti. Esporta prima se necessario.")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 📄 JSON")
                json_file = st.file_uploader("Carica file JSON", type=["json"], key="json_upload")
                if json_file:
                    try:
                        loaded = load_from_json_file(json_file)
                        _set_data(loaded)
                        st.success(f"Assessment caricato: {loaded.company_name or 'Senza nome'}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Errore nel caricamento: {e}")

            with col2:
                st.markdown("#### 📊 Excel")
                excel_file = st.file_uploader("Carica file Excel", type=["xlsx"], key="excel_upload")
                if excel_file:
                    try:
                        loaded = load_from_excel(excel_file)
                        _set_data(loaded)
                        st.success(f"Assessment caricato: {loaded.company_name or 'Senza nome'}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Errore nel caricamento: {e}")

            st.markdown("---")
            st.markdown("#### 🔄 Reset")
            if st.button("🗑️ Nuovo assessment (reset completo)", type="secondary"):
                st.session_state.assessment_data = AssessmentData()
                st.session_state.assessment_data.touch()
                st.rerun()
