from __future__ import annotations

from typing import Dict, List, Optional

from core.models import Question, Response, Section, SectionScore

CONFIDENCE_MAP = {"low": 0.4, "medium": 0.7, "high": 1.0}


class ScoringService:
    def _normalize_response(self, question: Question, response: Optional[Response]) -> Optional[float]:
        if response is None or response.not_applicable:
            return None
        if question.type == "likert_1_5":
            try:
                value = int(response.value)
                return max(0.0, min(100.0, (value - 1) * 25.0))
            except (ValueError, TypeError):
                return None
        if question.type == "yes_no_comment":
            if str(response.value).lower() in {"yes", "true", "1"}:
                return 100.0
            if str(response.value).lower() in {"no", "false", "0"}:
                return 0.0
            return None
        if question.type == "single_choice":
            option_map = {option.value: option.score for option in question.options}
            score = option_map.get(str(response.value))
            return None if score is None else float(score)
        return None

    def calculate(self, sections: List[Section], questions: List[Question], responses: List[Response]) -> Dict[str, Dict]:
        response_map = {r.question_id: r for r in responses}
        section_scores: Dict[str, SectionScore] = {}

        for section in sections:
            section_questions = [q for q in questions if q.section_id == section.id and q.scorable and q.active]
            total_weight = 0.0
            weighted_score = 0.0
            answered = 0
            confidence_sum = 0.0
            for question in section_questions:
                response = response_map.get(question.id)
                normalized = self._normalize_response(question, response)
                if normalized is None:
                    continue
                weight = question.default_weight
                total_weight += weight
                weighted_score += normalized * weight
                answered += 1
                confidence_sum += CONFIDENCE_MAP.get((response.confidence if response else "medium"), 0.7)

            coverage = 100.0 * answered / len(section_questions) if section_questions else 0.0
            maturity = weighted_score / total_weight if total_weight else 0.0
            confidence_index = 100.0 * confidence_sum / answered if answered else 0.0
            # V1 heuristic placeholders for remaining axes.
            section_scores[section.id] = SectionScore(
                maturity=round(maturity, 1),
                impact=round(max(20.0, 100.0 - maturity), 1) if answered else 0.0,
                feasibility=round(40.0 + confidence_index * 0.4, 1) if answered else 0.0,
                current_risk=round(max(0.0, 100.0 - maturity * 0.8), 1) if answered else 0.0,
                intervention_risk=round(max(10.0, 60.0 - confidence_index * 0.3), 1) if answered else 0.0,
                coverage=round(coverage, 1),
                confidence_index=round(confidence_index, 1),
            )

        if section_scores:
            overall = SectionScore(
                maturity=round(sum(s.maturity for s in section_scores.values()) / len(section_scores), 1),
                impact=round(sum(s.impact for s in section_scores.values()) / len(section_scores), 1),
                feasibility=round(sum(s.feasibility for s in section_scores.values()) / len(section_scores), 1),
                current_risk=round(sum(s.current_risk for s in section_scores.values()) / len(section_scores), 1),
                intervention_risk=round(sum(s.intervention_risk for s in section_scores.values()) / len(section_scores), 1),
                coverage=round(sum(s.coverage for s in section_scores.values()) / len(section_scores), 1),
                confidence_index=round(sum(s.confidence_index for s in section_scores.values()) / len(section_scores), 1),
            )
        else:
            overall = SectionScore()

        return {
            "sections": {section_id: score.model_dump() for section_id, score in section_scores.items()},
            "overall": overall.model_dump(),
        }
