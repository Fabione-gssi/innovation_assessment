from core.models import Question, Response, Section
from core.scoring import ScoringService


def test_likert_scoring():
    section = Section(id="C1", name="Test")
    question = Question(
        id="Q1",
        section_id="C1",
        text="Test",
        type="likert_1_5",
        scorable=True,
    )
    response = Response(question_id="Q1", value=5)
    scores = ScoringService().calculate([section], [question], [response])
    assert scores["sections"]["C1"]["maturity"] == 100.0
