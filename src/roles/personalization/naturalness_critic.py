from domain.evaluation_aggregate.criteria import Criteria
from roles.personalization.critic import ConsultantCriticRole, DeepReviewCriticRole

CRITERIA = Criteria(
    type="naturalness",
    description="Personalized names, places, or elements are integrated smoothly, without feeling like forced additions.",
    indicators=[
        "Personalized characters fulfill a functional role.",
        "The modifications respect the logic of the narrative universe.",
        "There are no artificial insertions.",
    ]
)

class NaturalnessDeepReviewCriticRole(DeepReviewCriticRole):
    """
    Role that evaluates the naturalness of a personalization response.
    """

    def __init__(self):
        super().__init__(criteria=CRITERIA)

class NaturalnessConsultantCriticRole(ConsultantCriticRole):
    """
    Role that evaluates the naturalness of a personalization response based on a query.
    """

    def __init__(self):
        super().__init__(criteria=CRITERIA)
