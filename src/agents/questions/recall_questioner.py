from agents.core.base_lm_config import LMConfiguration
from agents.questions.questioner import QuestionerAgent
from roles.questions.recall_questioner import RecallQuestionerRole


class RecallQuestionerAgent(QuestionerAgent):
    """
    Agent that creates recall questions for a story.
    """

    def __init__(
        self,
        lm_config: LMConfiguration | None = None,
    ):
        super().__init__(
            name="recall_questioner",
            roles=[RecallQuestionerRole()],
            lm_config=lm_config,
        )
