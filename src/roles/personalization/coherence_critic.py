from roles.personalization.criteria import COHERENCE_CRITERIA as CRITERIA
from roles.personalization.critic import ConsultantCriticRole, DeepReviewCriticRole


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
