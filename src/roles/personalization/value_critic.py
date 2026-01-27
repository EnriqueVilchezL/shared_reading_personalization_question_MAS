from domain.evaluation_aggregate.criteria import Criteria
from roles.personalization.critic import ConsultantCriticRole, DeepReviewCriticRole

CRITERIA = Criteria(
    type="added narrative value",
    description="That the personalization is not merely cosmetic, but enriches the story or strengthens the connection with the child reader.",
    indicators=[
        "Personalizations that are meaningful to the reader.",
        "Improved immersion or emotional identification.",
    ]
)

class ValueDeepReviewCriticRole(DeepReviewCriticRole):
    """
    Role that evaluates the added narrative value of a personalization response.
    """

    def __init__(self):
        super().__init__(criteria=CRITERIA)

class ValueConsultantCriticRole(ConsultantCriticRole):
    """
    Role that evaluates the added narrative value of a personalization response based on a query.
    """

    def __init__(self):
        super().__init__(criteria=CRITERIA)
