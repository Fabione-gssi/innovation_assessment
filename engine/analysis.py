"""
Motore di analisi: gap analysis, prioritizzazione, matrice impatto/effort.
"""
from __future__ import annotations
from models.schema import AssessmentData, ModuleResult, RoadmapItem
from engine.scoring import compute_all_scores
from config import MODULES, MODULE_MAP
import uuid


def gap_analysis(results: dict[str, ModuleResult]) -> list[dict]:
    """Genera la gap analysis AS-IS vs TO-BE per ogni modulo."""
    gaps = []
    for mod in MODULES:
        r = results.get(mod["id"])
        if r and r.score > 0:
            gaps.append({
                "module_id": mod["id"],
                "module_name": mod["name"],
                "icon": mod["icon"],
                "as_is": r.score,
                "to_be": r.target_level,
                "gap": r.gap,
                "maturity_level": r.maturity_level,
                "completion": f"{r.answered}/{r.total}",
                "priority": _gap_to_priority(r.gap),
            })
    # Ordina per gap decrescente
    gaps.sort(key=lambda x: x["gap"], reverse=True)
    return gaps


def _gap_to_priority(gap: float) -> str:
    if gap >= 3.0:
        return "critical"
    elif gap >= 2.0:
        return "high"
    elif gap >= 1.0:
        return "medium"
    return "low"


def generate_recommendations(results: dict[str, ModuleResult]) -> list[dict]:
    """Genera raccomandazioni basate sui risultati."""
    recs = []
    for mod in MODULES:
        r = results.get(mod["id"])
        if not r or r.score == 0:
            continue
        if r.gap > 0:
            recs.append({
                "module_id": mod["id"],
                "module_name": mod["name"],
                "icon": mod["icon"],
                "priority": _gap_to_priority(r.gap),
                "current_level": r.maturity_level,
                "target_level": r.target_level,
                "recommendation": _get_recommendation(mod["id"], r.maturity_level),
            })
    recs.sort(key=lambda x: {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(x["priority"], 4))
    return recs


def _get_recommendation(module_id: str, level: int) -> str:
    """Genera raccomandazione contestualizzata al modulo e al livello."""
    recs = {
        "m01_contesto": {
            1: "Avviare un'analisi strutturata del contesto (PESTEL, SWOT). Mappare gli stakeholder e le loro aspettative.",
            2: "Formalizzare l'analisi del contesto in documenti aggiornati. Definire l'intento di innovazione.",
            3: "Integrare l'analisi del contesto nei processi decisionali. Aggiornare periodicamente.",
            4: "Ottimizzare il monitoraggio continuo del contesto con strumenti digitali e intelligence.",
        },
        "m02_leadership": {
            1: "Sensibilizzare l'alta direzione sull'importanza dell'innovazione. Definire ruoli e responsabilità base.",
            2: "Formalizzare la politica di innovazione. Assegnare risorse dedicate. Comunicare la visione.",
            3: "Sviluppare la strategia di innovazione. Integrare nel piano strategico aziendale.",
            4: "Promuovere una cultura dell'innovazione diffusa. Implementare incentivi e riconoscimenti.",
        },
        "m03_pianificazione": {
            1: "Definire obiettivi di innovazione SMART. Avviare la gestione del rischio per l'innovazione.",
            2: "Strutturare il portafoglio innovazione. Definire criteri di selezione e bilanciamento.",
            3: "Implementare pianificazione strutturata con milestone e review periodiche.",
            4: "Ottimizzare la collaborazione esterna (open innovation, ecosistemi, partnership).",
        },
        "m04_supporto": {
            1: "Allocare budget e risorse dedicate all'innovazione. Mappare le competenze esistenti.",
            2: "Sviluppare un piano di formazione sull'innovazione. Adottare strumenti base.",
            3: "Strutturare la gestione IP. Implementare strumenti collaborativi avanzati.",
            4: "Ottimizzare la gestione delle informazioni documentate. Knowledge management evoluto.",
        },
        "m05_processi": {
            1: "Definire un processo base di innovazione (idea → concept → prototipo → implementazione).",
            2: "Introdurre gate di validazione e criteri di selezione. Avviare la prototipazione.",
            3: "Strutturare il processo con stage-gate o agile. Validare sistematicamente con utenti/mercato.",
            4: "Implementare processi iterativi e flessibili. Integrare con i processi aziendali core.",
        },
        "m06_valutazione": {
            1: "Definire KPI base per l'innovazione (n. idee, progetti attivi, budget allocato).",
            2: "Implementare il monitoraggio sistematico dei KPI. Avviare audit interni.",
            3: "Strutturare il riesame di direzione. Analizzare trend e benchmark.",
            4: "Implementare dashboard real-time. Collegare KPI innovazione a KPI business.",
        },
        "m07_digitale": {
            1: "Avviare la digitalizzazione dei processi core. Assessment infrastruttura IT.",
            2: "Integrare i sistemi informativi. Implementare strumenti collaborativi.",
            3: "Adottare cloud e piattaforme avanzate. Rafforzare la cybersecurity.",
            4: "Implementare approccio data-driven. Automazione avanzata dei processi.",
        },
        "m08_ai_readiness": {
            1: "Avviare la data governance. Valutare la qualità dei dati esistenti.",
            2: "Sviluppare competenze base in data analytics. Identificare casi d'uso AI.",
            3: "Lanciare POC su casi d'uso prioritari. Strutturare pipeline dati.",
            4: "Scalare le soluzioni AI in produzione. Implementare governance AI e MLOps.",
        },
        "m09_gestionale": {
            1: "Mappare i processi core. Definire organigramma e responsabilità chiare.",
            2: "Standardizzare i processi decisionali. Avviare il change management.",
            3: "Ottimizzare i processi con approccio lean. Implementare KPI gestionali.",
            4: "Sviluppare la resilienza organizzativa. Integrare innovazione nel modello gestionale.",
        },
        "m10_miglioramento": {
            1: "Introdurre il ciclo PDCA. Avviare la raccolta di lessons learned.",
            2: "Strutturare la gestione delle non conformità. Definire azioni correttive.",
            3: "Implementare il knowledge management. Benchmarking sistematico.",
            4: "Promuovere il miglioramento continuo a tutti i livelli. Best practices sharing.",
        },
    }
    mod_recs = recs.get(module_id, {})
    return mod_recs.get(level, "Consolidare il livello attuale e pianificare il passaggio al livello successivo.")


def auto_generate_roadmap(data: AssessmentData) -> list[dict]:
    """Genera automaticamente una roadmap basata sulla gap analysis."""
    results = compute_all_scores(data)
    gaps = gap_analysis(results)
    recs = generate_recommendations(results)
    roadmap = []

    timeframes = {"critical": "0-3 mesi", "high": "3-6 mesi", "medium": "6-12 mesi", "low": "12-18 mesi"}

    for rec in recs:
        if rec["priority"] in ("critical", "high", "medium"):
            roadmap.append({
                "id": f"ri_{uuid.uuid4().hex[:8]}",
                "title": f"Miglioramento {rec['module_name']}",
                "description": rec["recommendation"],
                "module_id": rec["module_id"],
                "priority": rec["priority"],
                "effort": "medium",
                "impact": "high" if rec["priority"] in ("critical", "high") else "medium",
                "timeframe": timeframes.get(rec["priority"], "6-12 mesi"),
                "owner": "",
                "status": "planned",
                "notes": f"Gap: {results[rec['module_id']].gap:.1f} — Da livello {rec['current_level']} a {rec['target_level']}",
            })

    return roadmap
