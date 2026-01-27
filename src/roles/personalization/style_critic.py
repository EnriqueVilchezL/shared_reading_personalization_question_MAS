from domain.evaluation_aggregate.criteria import Criteria
from roles.personalization.critic import ConsultantCriticRole, DeepReviewCriticRole

CRITERIA = Criteria(
    type="style",
    description="That the personalization does not alter the narrative voice, language level, or literary style of the story.",
    indicators=[
        "Consistency in linguistic register.",
        "Appropriate use of children’s vocabulary.",
        "No tonal shifts or stylistic breaks between the original and the new content.",
    ],
)

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
