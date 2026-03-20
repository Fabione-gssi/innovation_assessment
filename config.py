"""
Configurazione globale del tool di Innovation Assessment.
Allineato a UNI 11814:2021 e UNI EN ISO 56001:2024.
"""

APP_TITLE = "Innovation Assessment Tool"
APP_SUBTITLE = "Conforme UNI 11814:2021 · UNI EN ISO 56001:2024"
APP_VERSION = "1.0.0"
APP_ICON = "🔬"

# ── Maturity levels (scala 1-5) ─────────────────────────────────────────────
MATURITY_LEVELS = {
    1: {"label": "Iniziale",      "color": "#E24B4A", "desc": "Processi assenti o ad hoc, nessuna struttura formalizzata"},
    2: {"label": "Ripetibile",    "color": "#EF9F27", "desc": "Alcune pratiche esistono ma non sono standardizzate"},
    3: {"label": "Definito",      "color": "#BA7517", "desc": "Processi documentati e standardizzati a livello organizzativo"},
    4: {"label": "Gestito",       "color": "#639922", "desc": "Processi misurati, controllati e ottimizzati con KPI"},
    5: {"label": "Ottimizzato",   "color": "#1D9E75", "desc": "Miglioramento continuo sistematico, best-in-class"},
}

# ── Moduli di assessment (mappati a ISO 56001) ──────────────────────────────
MODULES = [
    {
        "id": "m01_contesto",
        "name": "Contesto dell'organizzazione",
        "iso_ref": "§4",
        "icon": "🏢",
        "description": "Comprensione dell'organizzazione, fattori interni/esterni, parti interessate, intento di innovazione",
        "category": "iso56001",
    },
    {
        "id": "m02_leadership",
        "name": "Leadership e strategia",
        "iso_ref": "§5",
        "icon": "🎯",
        "description": "Leadership, impegno, politica e strategia per l'innovazione, cultura, ruoli e responsabilità",
        "category": "iso56001",
    },
    {
        "id": "m03_pianificazione",
        "name": "Pianificazione",
        "iso_ref": "§6",
        "icon": "📋",
        "description": "Rischi e opportunità, obiettivi, portafoglio innovazione, strutture organizzative, collaborazione",
        "category": "iso56001",
    },
    {
        "id": "m04_supporto",
        "name": "Supporto e risorse",
        "iso_ref": "§7",
        "icon": "🛠️",
        "description": "Risorse, competenze, consapevolezza, comunicazione, informazioni documentate, proprietà intellettuale",
        "category": "iso56001",
    },
    {
        "id": "m05_processi",
        "name": "Processi di innovazione",
        "iso_ref": "§8",
        "icon": "⚙️",
        "description": "Identificazione opportunità, creazione concept, validazione, sviluppo e implementazione soluzioni",
        "category": "iso56001",
    },
    {
        "id": "m06_valutazione",
        "name": "Valutazione delle prestazioni",
        "iso_ref": "§9",
        "icon": "📊",
        "description": "Monitoraggio, misurazione, analisi, audit interno, riesame di direzione",
        "category": "iso56001",
    },
    {
        "id": "m07_digitale",
        "name": "Assessment digitale e tecnologico",
        "iso_ref": "§7-§8",
        "icon": "💻",
        "description": "Maturità digitale, infrastruttura IT, sistemi informativi, cybersecurity, cloud, integrazione",
        "category": "tech",
    },
    {
        "id": "m08_ai_readiness",
        "name": "AI e data readiness",
        "iso_ref": "§7-§8",
        "icon": "🤖",
        "description": "Qualità dati, ML, deep learning, RAG, reti neurali, agenti, governance AI, etica",
        "category": "tech",
    },
    {
        "id": "m09_gestionale",
        "name": "Assessment gestionale e manageriale",
        "iso_ref": "§5-§7",
        "icon": "👥",
        "description": "Modello organizzativo, processi decisionali, change management, KPI gestionali, resilienza",
        "category": "management",
    },
    {
        "id": "m10_miglioramento",
        "name": "Miglioramento continuo",
        "iso_ref": "§10",
        "icon": "🔄",
        "description": "Non conformità, azioni correttive, miglioramento continuo del sistema di gestione dell'innovazione",
        "category": "iso56001",
    },
]

MODULE_IDS = [m["id"] for m in MODULES]
MODULE_MAP = {m["id"]: m for m in MODULES}

# ── Categorie di moduli ─────────────────────────────────────────────────────
CATEGORIES = {
    "iso56001":    {"label": "ISO 56001 — Sistema di gestione innovazione", "color": "#534AB7"},
    "tech":        {"label": "Assessment digitale e tecnologico",           "color": "#185FA5"},
    "management":  {"label": "Assessment gestionale e manageriale",         "color": "#D85A30"},
}

# ── Tipi di domanda ─────────────────────────────────────────────────────────
QUESTION_TYPES = {
    "scale":         "Scala 1-5 (maturity)",
    "single_choice": "Scelta singola",
    "multi_choice":  "Scelta multipla",
    "text":          "Risposta aperta",
    "yes_no":        "Sì / No / Parziale",
}

# ── Priorità roadmap ────────────────────────────────────────────────────────
PRIORITY_LEVELS = {
    "critical": {"label": "Critica",  "color": "#E24B4A", "icon": "🔴"},
    "high":     {"label": "Alta",     "color": "#EF9F27", "icon": "🟠"},
    "medium":   {"label": "Media",    "color": "#639922", "icon": "🟡"},
    "low":      {"label": "Bassa",    "color": "#1D9E75", "icon": "🟢"},
}

# ── Streamlit page config ───────────────────────────────────────────────────
PAGE_CONFIG = {
    "page_title": APP_TITLE,
    "page_icon": APP_ICON,
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}
