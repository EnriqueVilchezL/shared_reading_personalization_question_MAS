from roles.personalization.criteria import STYLE_CRITERIA as CRITERIA
from roles.personalization.critic import ConsultantCriticRole, DeepReviewCriticRole


class StyleDeepReviewCriticRole(DeepReviewCriticRole):
    """
    Role that evaluates the style and expression of a personalization response.
    """

    def __init__(self):
        super().__init__(criteria=CRITERIA)


class StyleConsultantCriticRole(ConsultantCriticRole):
    """
    Role that evaluates the style and expression of a personalization response based on a query.
    """

    def __init__(self):
        super().__init__(criteria=CRITERIA)
