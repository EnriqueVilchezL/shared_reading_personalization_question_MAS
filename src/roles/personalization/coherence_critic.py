from domain.evaluation_aggregate.criteria import Criteria
from roles.personalization.critic import ConsultantCriticRole, DeepReviewCriticRole

CRITERIA = Criteria(
    type="la coherencia",
    description="Que la historia tenga un desarrollo lógico, sin rupturas o elementos inconexos al integrar la personalización.",
    indicators=[
        "Inicio, nudo y desenlace bien definidos.",
        "Secuencia causa-efecto clara.",
        "Ausencia de cabos sueltos o contradicciones argumentales.",
    ],
)

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
