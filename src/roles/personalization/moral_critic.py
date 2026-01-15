from domain.evaluation_aggregate.criteria import Criteria
from roles.personalization.critic import ConsultantCriticRole, DeepReviewCriticRole

CRITERIA = Criteria(
    type="la enseñanza",
    description="Que la personalización no contradiga la enseñanza, valor o moraleja del cuento original.",
    indicators=[
        "El mensaje central permanece intacto.",
        "El desenlace conserva el sentido ético o simbólico.",
        "No se tergiversa la lógica de los personajes ni la intención."
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
