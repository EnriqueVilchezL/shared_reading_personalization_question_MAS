from roles.personalization.criteria import VALUE_CRITERIA as CRITERIA
from roles.personalization.critic import ConsultantCriticRole, DeepReviewCriticRole


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
