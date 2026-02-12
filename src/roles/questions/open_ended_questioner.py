from domain.evaluation_aggregate.criteria import Criteria
from roles.questions.questioner import QuestionerRole

CRITERIA = Criteria(
    type="O: Open-ended Questions",
    description="The child is asked **open-ended questions**.",
    indicators=[
        "The questions should help the child improve their expressive language",
        "The questions should help the child develop their vocabulary and narrative skills"
    ],
    importance=None,
)

class OpenEndedQuestionerRole(QuestionerRole):
    """
    Role that creates open-ended questions for a story.
    """

    def __init__(self):
        super().__init__(criteria=CRITERIA)
