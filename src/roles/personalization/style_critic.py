from domain.evaluation_aggregate.criteria import Criteria
from roles.personalization.critic import ConsultantCriticRole, DeepReviewCriticRole

CRITERIA = Criteria(
    type="el estilo",
    description="Que la personalización no altere la voz narrativa, el nivel del lenguaje ni el estilo literario del cuento.",
    indicators=[
        "Consistencia en el registro lingüístico.",
        "Uso adecuado del vocabulario infantil.",
        "No hay saltos de tono, ni rupturas estilísticas entre lo original y lo nuevo.",
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
