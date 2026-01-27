from agents.core.base_lm_config import LMConfiguration
from agents.questions.questioner import QuestionerAgent
from roles.questions.completion_questioner import CompletionQuestionerRole


class CompletionQuestionerAgent(QuestionerAgent):
    """
    Agent that creates completion questions for a story.
    """

    def __init__(
        self,
        lm_config: LMConfiguration | None = None,
    ):
        super().__init__(
            name="completition_questioner",
            roles=[CompletionQuestionerRole()],
            lm_config=lm_config,
        )
