from agents.core.base_lm_config import LMConfiguration
from agents.questions.questioner import QuestionerAgent
from roles.questions.distancing_questioner import DistancingQuestionerRole


class DistancingQuestionerAgent(QuestionerAgent):
    """
    Agent that creates distancing questions for a story.
    """

    def __init__(
        self,
        lm_config: LMConfiguration | None = None,
    ):
        super().__init__(
            name="distancing_questioner",
            roles=[DistancingQuestionerRole()],
            lm_config=lm_config,
        )
