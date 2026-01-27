from domain.evaluation_aggregate.criteria import Criteria
from roles.personalization.critic import ConsultantCriticRole, DeepReviewCriticRole

CRITERIA = Criteria(
    type="emotional impact",
    description="That the personalized story manages to move, entertain, and maintain the interest of the child reader.",
    indicators=[
        "The story would generate positive reactions (laughter, surprise, attention).",
        "The story would generate a desire to reread it or share it.",
    ]
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
