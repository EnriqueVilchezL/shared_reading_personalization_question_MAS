from agents.core.base_lm_config import LMConfiguration
from agents.questions.questioner import QuestionerAgent
from roles.questions.completition_questioner import CompletitionQuestionerRole


class CompletitionQuestionerAgent(QuestionerAgent):
    """
    Agent that creates completion questions for a story.
    """

    def __init__(self):
        super().__init__(
            name="completition_questioner",
            roles=[CompletitionQuestionerRole()],
            lm_config=LMConfiguration(base_model="gemma3:4b"),
        )
