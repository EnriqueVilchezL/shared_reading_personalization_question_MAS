from agents.core.base_lm_config import LMConfiguration
from agents.questions.questioner import QuestionerAgent
from roles.questions.wh_questioner import WhQuestionerRole


class WhQuestionerAgent(QuestionerAgent):
    """
    Agent that creates wh questions for a story.
    """

    def __init__(
        self,
        lm_config: LMConfiguration | None = None,
    ):
        super().__init__(
            name="wh_questioner",
            roles=[WhQuestionerRole()],
            lm_config=lm_config,
        )
