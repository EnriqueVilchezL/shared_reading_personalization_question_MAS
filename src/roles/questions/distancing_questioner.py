from domain.evaluation_aggregate.criteria import Criteria
from roles.questions.questioner import QuestionerRole

CRITERIA = Criteria(
    type="D: Distancing",
    description="The child is asked questions that **relate their own life to the story**.",
    indicators=[
        "The questions should help the child develop their vocabulary and conversational and narrative skills",
        "The questions should help the child form a connection between the story and the real world"
    ]
)

class DistancingQuestionerRole(QuestionerRole):
    """
    Role that creates distancing questions for a story.
    """

    def __init__(self):
        super().__init__(criteria=CRITERIA)
