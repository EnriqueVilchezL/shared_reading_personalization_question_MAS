from agents.core.base_lm_config import LMConfiguration
from agents.questions.questioner import QuestionerAgent
from roles.questions.open_ended_questioner import OpenEndedQuestionerRole


class OpenEndedQuestionerAgent(QuestionerAgent):
    """
    Agent that creates open ended questions for a story.
    """

    def __init__(
        self,
        lm_config: LMConfiguration | None = None,
    ):
        super().__init__(
            name="open_ended_questioner",
            roles=[OpenEndedQuestionerRole()],
            lm_config=lm_config,
        )
