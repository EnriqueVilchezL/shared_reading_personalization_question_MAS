from roles.personalization.criteria import EMOTION_CRITERIA as CRITERIA
from roles.personalization.critic import (
    ConsultantCriticRole,
    DeepReviewCriticRole,
)


class EmotionDeepReviewCriticRole(DeepReviewCriticRole):
    """
    Role that evaluates the emotional impact of a personalization response.
    """

    def __init__(self):
        super().__init__(criteria=CRITERIA)


class EmotionConsultantCriticRole(ConsultantCriticRole):
    """
    Role that evaluates the emotional impact of a personalization response based on a query.
    """

    def __init__(self):
        super().__init__(criteria=CRITERIA)
