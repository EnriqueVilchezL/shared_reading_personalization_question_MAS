from domain.evaluation_aggregate.criteria import Criteria
from roles.personalization.critic import ConsultantCriticRole, DeepReviewCriticRole

CRITERIA = Criteria(
    type="the moral",
    description="That the personalization does not contradict the lesson, value, or moral of the original story.",
    indicators=[
        "The central message remains intact.",
        "The ending preserves its ethical or symbolic meaning.",
        "The logic of the characters or the original intent is not distorted.",
    ]
)

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
