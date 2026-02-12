from roles.personalization.criteria import NATURALNESS_CRITERIA as CRITERIA
from roles.personalization.critic import ConsultantCriticRole, DeepReviewCriticRole


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
