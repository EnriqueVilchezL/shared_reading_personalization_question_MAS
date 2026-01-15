from domain.evaluation_aggregate.criteria import Criteria
from roles.personalization.critic import ConsultantCriticRole, DeepReviewCriticRole

CRITERIA = Criteria(
    type="el valor narrativo añadido",
    description="Que la personalización no sea solo cosmética, sino que enriquezca la historia o fortalezca la conexión con el lector infantil.",
    indicators=[
        "Personalizaciones significativas para el lector.",
        "Mejora de la inmersión o identificación emocional.",
    ]
)

class ValueDeepReviewCriticRole(DeepReviewCriticRole):
    """
    Role that evaluates the added narrative value of a personalization response.
    """

    def __init__(self):
        super().__init__(criteria=CRITERIA)

class ValueConsultantCriticRole(ConsultantCriticRole):
    """
    Role that evaluates the added narrative value of a personalization response based on a query.
    """

    def __init__(self):
        super().__init__(criteria=CRITERIA)
