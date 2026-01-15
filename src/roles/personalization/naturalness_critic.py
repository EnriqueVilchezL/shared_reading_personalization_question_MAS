from domain.evaluation_aggregate.criteria import Criteria
from roles.personalization.critic import ConsultantCriticRole, DeepReviewCriticRole

CRITERIA = Criteria(
    type="la naturalidad",
    description="Los nombres, lugares o elementos personalizados se insertan fluidamente, sin parecer añadidos forzados.",
    indicators=[
        "Los personajes personalizados cumplen un rol funcional.",
        "Las modificaciones respetan la lógica del universo narrativo.",
        "No hay inserciones artificiosas."
    ]
)

class NaturalnessDeepReviewCriticRole(DeepReviewCriticRole):
    """
    Role that evaluates the naturalness of a personalization response.
    """

    def __init__(self):
        super().__init__(criteria=CRITERIA)

class NaturalnessConsultantCriticRole(ConsultantCriticRole):
    """
    Role that evaluates the naturalness of a personalization response based on a query.
    """

    def __init__(self):
        super().__init__(criteria=CRITERIA)
