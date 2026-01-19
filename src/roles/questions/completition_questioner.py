from domain.evaluation_aggregate.criteria import Criteria
from roles.questions.questioner import QuestionerRole

CRITERIA = Criteria(
    type="C: Completar",
    description="Se le pide al niño o niña **completar una frase o palabra**.",
    indicators=[
        "Se empieza con una pregunta que invite al niño o niña a completar con una frase o palabra y luego se deja un espacio en blanco al final de una oración",
        "Las preguntas pueden concentrarse en las estructuras del lenguaje (rima y repetición)"
    ]
)

class CompletitionQuestionerRole(QuestionerRole):
    """
    Role that creates completion questions for a story.
    """

    def __init__(self):
        super().__init__(criteria=CRITERIA)

