from domain.evaluation_aggregate.criteria import Criteria
from roles.questions.questioner import QuestionerRole

CRITERIA = Criteria(
    type="C: Completion",
    description="The child is asked to **complete a sentence or a word**.",
    indicators=[
        "It starts with a question that invites the child to complete with a sentence or word, and then a blank space is left at the end of a sentence",
        "The questions can focus on language structures (rhyme and repetition)"
    ]
)

class CompletionQuestionerRole(QuestionerRole):
    """
    Role that creates completion questions for a story.
    """

    def __init__(self):
        super().__init__(criteria=CRITERIA)
