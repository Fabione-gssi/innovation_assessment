from __future__ import annotations

from collections import defaultdict
from typing import Dict, List

from core.models import Question, Response, Section, SectionSummary


class QualitativeSynthesizer:
    def build_section_summaries(
        self,
        sections: List[Section],
        questions: List[Question],
        responses: List[Response],
        existing: List[SectionSummary] | None = None,
    ) -> List[SectionSummary]:
        existing_map: Dict[str, SectionSummary] = {s.section_id: s for s in (existing or [])}
        question_map = {q.id: q for q in questions}
        section_notes = defaultdict(list)
        section_issue_flags = defaultdict(set)
        section_tags = defaultdict(set)

        for response in responses:
            question = question_map.get(response.question_id)
            if not question:
                continue
            if question.question_purpose in {"qualitative", "hybrid"} and response.value:
                section_notes[question.section_id].append(str(response.value).strip())
            if response.comment:
                section_notes[question.section_id].append(response.comment.strip())
            for flag in response.issue_flags:
                section_issue_flags[question.section_id].add(flag)
            for tag in response.insight_tags:
                section_tags[question.section_id].add(tag)

        summaries: List[SectionSummary] = []
        for section in sections:
            seed = existing_map.get(section.id, SectionSummary(section_id=section.id))
            collected = section_notes.get(section.id, [])
            auto_summary = " ".join(collected[:2])[:300] if collected else seed.section_summary
            summaries.append(
                SectionSummary(
                    section_id=section.id,
                    section_notes=seed.section_notes,
                    section_summary=auto_summary,
                    section_confidence=seed.section_confidence,
                    key_issues=sorted(section_issue_flags.get(section.id, set())),
                    recommended_followups=sorted(section_tags.get(section.id, set()))[:5],
                )
            )
        return summaries
