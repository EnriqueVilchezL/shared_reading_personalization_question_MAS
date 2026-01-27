from domain.evaluation_aggregate.criteria import Criteria
from roles.questions.questioner import QuestionerRole

CRITERIA = Criteria(
    type="W: Wh-questions",
    description="The child is asked **what, where, when, who, and why questions**.",
    indicators=[
        "The questions should help the child learn vocabulary that appears in the book"
    ]
)

class WhQuestionerRole(QuestionerRole):
    """
    Role that creates wh-questions for a story.
    """

    def __init__(self):
        super().__init__(criteria=CRITERIA)
