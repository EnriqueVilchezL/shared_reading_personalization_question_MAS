from domain.evaluation_aggregate.criteria import Criteria
from roles.personalization.critic import ConsultantCriticRole, DeepReviewCriticRole

CRITERIA = Criteria(
    type="el impacto emocional",
    description="Que el cuento personalizado logre emocionar, divertir y mantener el interés del lector infantil.",
    indicators=[
        "El cuento generaría reacciones positivas (risa, sorpresa, atención).",
        "El cuento generaría un deseo por releerlo o compartirlo.",
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
