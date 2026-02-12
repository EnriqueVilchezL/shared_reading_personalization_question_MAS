from domain.evaluation_aggregate.criteria import Criteria
from roles.questions.questioner import QuestionerRole

CRITERIA = Criteria(
    type="R: Recall",
    description="The child is asked about **details from the section they have just read**.",
    indicators=[
        "The questions should help the child remember what has happened in the story",
        "The questions should help the child understand the plot of a story and describe sequences of events"
    ],
    importance=None,
)

class RecallQuestionerRole(QuestionerRole):
    """
    Role that creates recall questions for a story.
    """

    def __init__(self):
        super().__init__(criteria=CRITERIA)
