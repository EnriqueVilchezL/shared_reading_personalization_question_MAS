from domain.evaluation_aggregate.criteria import Criteria
from roles.personalization.critic import ConsultantCriticRole, DeepReviewCriticRole

CRITERIA = Criteria(
    type="coherence",
    description="That the story has a logical development, without breaks or disconnected elements when integrating personalization.",
    indicators=[
        "Well-defined beginning, middle, and end.",
        "Clear cause-and-effect sequence.",
        "Absence of loose ends or plot contradictions.",
    ],
)

class CoherenceDeepReviewCriticRole(DeepReviewCriticRole):
    """
    Role that evaluates the coherence and consistency of a personalization response.
    """

    def __init__(self):
        super().__init__(criteria=CRITERIA)


class CoherenceConsultantCriticRole(ConsultantCriticRole):
    """
    Role that evaluates the coherence and consistency of a personalization response based on a query.
    """

    def __init__(self):
        super().__init__(criteria=CRITERIA)
