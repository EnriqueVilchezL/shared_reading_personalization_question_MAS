from roles.personalization.criteria import MORAL_CRITERIA as CRITERIA
from roles.personalization.critic import ConsultantCriticRole, DeepReviewCriticRole


class MoralDeepReviewCriticRole(DeepReviewCriticRole):
    """
    Role that evaluates the moral of a personalization response.
    """

    def __init__(self):
        super().__init__(criteria=CRITERIA)


class MoralConsultantCriticRole(ConsultantCriticRole):
    """
    Role that evaluates the moral of a personalization response based on a query.
    """

    def __init__(self):
        super().__init__(criteria=CRITERIA)
