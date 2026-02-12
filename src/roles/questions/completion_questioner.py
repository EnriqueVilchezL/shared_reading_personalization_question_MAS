from domain.evaluation_aggregate.criteria import Criteria
from roles.questions.questioner import QuestionerRole

CRITERIA = Criteria(
    type="C: Completion",
    description="The child is asked to **complete a sentence or a word**.",
    indicators=[
        "The question invites the child to complete with a sentence or word",
        "The questions can focus on language structures (rhyme and repetition)"
    ],
    importance=None,
)

class CompletionQuestionerRole(QuestionerRole):
    """
    Role that creates completion questions for a story.
    """

    def __init__(self):
        super().__init__(criteria=CRITERIA)
