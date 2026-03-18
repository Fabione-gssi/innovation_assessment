from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from core.models import AssessmentDocument, Question, Response, Section, SectionSummary, Module, AssessmentMeta


class ExcelRepository:
    @staticmethod
    def save(document: AssessmentDocument, path: str | Path) -> None:
        path = Path(path)
        with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
            pd.DataFrame([document.assessment.model_dump(mode="json")]).to_excel(writer, sheet_name="Metadata", index=False)
            pd.DataFrame([s.model_dump() for s in document.sections]).to_excel(writer, sheet_name="Sections_Modules", index=False)
            pd.DataFrame([m.model_dump() for m in document.modules]).to_excel(writer, sheet_name="Modules", index=False)
            question_rows = []
            for q in document.question_bank:
                row = q.model_dump()
                row["options"] = json.dumps(row["options"], ensure_ascii=False)
                row["alignment"] = json.dumps(row["alignment"], ensure_ascii=False)
                row["tags"] = json.dumps(row["tags"], ensure_ascii=False)
                question_rows.append(row)
            pd.DataFrame(question_rows).to_excel(writer, sheet_name="Question_Bank", index=False)
            response_rows = []
            for r in document.responses:
                row = r.model_dump()
                row["insight_tags"] = json.dumps(row["insight_tags"], ensure_ascii=False)
                row["issue_flags"] = json.dumps(row["issue_flags"], ensure_ascii=False)
                response_rows.append(row)
            pd.DataFrame(response_rows).to_excel(writer, sheet_name="Responses", index=False)
            summary_rows = []
            for s in document.section_summaries:
                row = s.model_dump()
                row["key_issues"] = json.dumps(row["key_issues"], ensure_ascii=False)
                row["recommended_followups"] = json.dumps(row["recommended_followups"], ensure_ascii=False)
                summary_rows.append(row)
            pd.DataFrame(summary_rows).to_excel(writer, sheet_name="Section_Summaries", index=False)
            scores = document.scores.get("sections", {})
            score_rows = [{"section_id": k, **v} for k, v in scores.items()]
            pd.DataFrame(score_rows).to_excel(writer, sheet_name="Scores", index=False)
            pd.DataFrame([f.model_dump() for f in document.findings]).to_excel(writer, sheet_name="Findings", index=False)
            pd.DataFrame([i.model_dump() for i in document.initiatives]).to_excel(writer, sheet_name="Priorities", index=False)
            pd.DataFrame([r.model_dump() for r in document.roadmap]).to_excel(writer, sheet_name="Roadmap", index=False)

    @staticmethod
    def load(path: str | Path) -> AssessmentDocument:
        path = Path(path)
        xls = pd.ExcelFile(path)
        metadata = pd.read_excel(xls, "Metadata").fillna("")
        sections_df = pd.read_excel(xls, "Sections_Modules").fillna("")
        modules_df = pd.read_excel(xls, "Modules").fillna("") if "Modules" in xls.sheet_names else pd.DataFrame()
        questions_df = pd.read_excel(xls, "Question_Bank").fillna("")
        responses_df = pd.read_excel(xls, "Responses").fillna("") if "Responses" in xls.sheet_names else pd.DataFrame()
        summaries_df = pd.read_excel(xls, "Section_Summaries").fillna("") if "Section_Summaries" in xls.sheet_names else pd.DataFrame()

        sections = [Section(**row) for row in sections_df.to_dict(orient="records")]
        modules = [Module(**row) for row in modules_df.to_dict(orient="records")]
        questions = []
        for row in questions_df.to_dict(orient="records"):
            row["options"] = json.loads(row.get("options", "[]") or "[]")
            row["alignment"] = json.loads(row.get("alignment", "{}") or "{}")
            row["tags"] = json.loads(row.get("tags", "[]") or "[]")
            questions.append(Question(**row))
        responses = []
        for row in responses_df.to_dict(orient="records"):
            row["insight_tags"] = json.loads(row.get("insight_tags", "[]") or "[]") if isinstance(row.get("insight_tags", ""), str) else row.get("insight_tags", [])
            row["issue_flags"] = json.loads(row.get("issue_flags", "[]") or "[]") if isinstance(row.get("issue_flags", ""), str) else row.get("issue_flags", [])
            responses.append(Response(**row))
        summaries = []
        for row in summaries_df.to_dict(orient="records"):
            row["key_issues"] = json.loads(row.get("key_issues", "[]") or "[]") if isinstance(row.get("key_issues", ""), str) else row.get("key_issues", [])
            row["recommended_followups"] = json.loads(row.get("recommended_followups", "[]") or "[]") if isinstance(row.get("recommended_followups", ""), str) else row.get("recommended_followups", [])
            summaries.append(SectionSummary(**row))
        meta_row = metadata.to_dict(orient="records")[0] if not metadata.empty else {}
        assessment = AssessmentMeta(**meta_row)

        return AssessmentDocument(
            assessment=assessment,
            sections=sections,
            modules=modules,
            question_bank=questions,
            responses=responses,
            section_summaries=summaries,
        )
