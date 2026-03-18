
from core.services import AssessmentService
TEMPLATE_PATH = "templates/core_question_bank.json"


def test_all_module_templates_load():
    service = AssessmentService(TEMPLATE_PATH)
    modules = service.available_module_templates()
    assert len(modules) == 9

    loaded = {}
    for module in modules:
        section, questions = service.load_module_section_and_questions(module.id)
        loaded[module.id] = (section, questions)

    for module_id in ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9"]:
        section, questions = loaded[module_id]
        assert section is not None, f"{module_id} should have a template"
        assert any(q.question_purpose == "qualitative" for q in questions)
        assert any(q.scorable for q in questions)

    for module_id in ["M2", "M7", "M8", "M9"]:
        section, questions = loaded[module_id]
        assert len(questions) >= 8, f"{module_id} should have a complete question bank"


def test_apply_active_modules_adds_sections_and_questions():
    service = AssessmentService(TEMPLATE_PATH)
    document = service.create_empty_assessment()

    for module in document.modules:
        module.enabled = module.id in {"M2", "M7", "M8", "M9"}

    updated = service.apply_active_modules(document)
    section_ids = {s.id for s in updated.sections}
    question_section_ids = {q.section_id for q in updated.question_bank}

    for module_id in {"M2", "M7", "M8", "M9"}:
        assert module_id in section_ids
        assert module_id in question_section_ids
