"""
Motore di scoring per il calcolo dei punteggi di maturità.
Calcola: score per modulo, maturity level, gap analysis, score globale.
"""
from __future__ import annotations
from models.schema import AssessmentData, ModuleResult
from models.questions import get_scorable_questions, QUESTIONS_BY_ID
from config import MODULES, MATURITY_LEVELS


def compute_module_score(data: AssessmentData, module_id: str) -> ModuleResult:
    """Calcola il punteggio di maturità per un singolo modulo."""
    scorable = get_scorable_questions(module_id, data.custom_questions)
    if not scorable:
        return ModuleResult(module_id=module_id)

    total_weight = 0.0
    weighted_sum = 0.0
    answered_count = 0

    for q in scorable:
        qid = q["id"]
        weight = q.get("weight", 1.0)
        ans = data.get_answer_value(qid)

        if ans is not None:
            # Normalizza yes_no a scala 1-5
            if q["type"] == "yes_no":
                score_map = {"Sì": 5, "Parziale": 3, "No": 1}
                val = score_map.get(ans, 0)
            elif q["type"] == "scale":
                val = int(ans) if isinstance(ans, (int, float, str)) and str(ans).isdigit() else 0
            else:
                val = int(ans) if isinstance(ans, (int, float)) else 0

            if val > 0:
                weighted_sum += val * weight
                total_weight += weight
                answered_count += 1
        else:
            total_weight += weight  # conta nel totale ma non nel punteggio

    score = weighted_sum / total_weight if total_weight > 0 else 0.0
    target = data.target_levels.get(module_id, 3)
    maturity = max(1, min(5, round(score))) if score > 0 else 0

    return ModuleResult(
        module_id=module_id,
        score=round(score, 2),
        max_score=5.0,
        answered=answered_count,
        total=len(scorable),
        maturity_level=maturity,
        gap=round(max(0, target - score), 2),
        target_level=target,
    )


def compute_all_scores(data: AssessmentData) -> dict[str, ModuleResult]:
    """Calcola i punteggi per tutti i moduli."""
    results = {}
    for mod in MODULES:
        result = compute_module_score(data, mod["id"])
        results[mod["id"]] = result
    return results


def compute_global_score(results: dict[str, ModuleResult]) -> float:
    """Calcola il punteggio globale medio pesato."""
    scores = [r.score for r in results.values() if r.score > 0]
    return round(sum(scores) / len(scores), 2) if scores else 0.0


def compute_completion_rate(data: AssessmentData) -> dict:
    """Calcola il tasso di completamento per modulo e globale."""
    from models.questions import get_questions_for_module
    module_rates = {}
    total_answered = 0
    total_questions = 0

    for mod in MODULES:
        qs = get_questions_for_module(mod["id"], data.custom_questions)
        answered = sum(1 for q in qs if data.get_answer_value(q["id"]) is not None)
        module_rates[mod["id"]] = {
            "answered": answered,
            "total": len(qs),
            "rate": round(answered / len(qs) * 100, 1) if qs else 0,
        }
        total_answered += answered
        total_questions += len(qs)

    return {
        "modules": module_rates,
        "global": {
            "answered": total_answered,
            "total": total_questions,
            "rate": round(total_answered / total_questions * 100, 1) if total_questions > 0 else 0,
        },
    }


def get_maturity_label(level: int) -> str:
    """Ritorna l'etichetta del livello di maturità."""
    return MATURITY_LEVELS.get(level, {}).get("label", "N/D")


def get_maturity_color(level: int) -> str:
    """Ritorna il colore del livello di maturità."""
    return MATURITY_LEVELS.get(level, {}).get("color", "#888")
