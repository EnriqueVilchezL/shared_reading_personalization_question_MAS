from agents.core.base_lm_config import LMConfiguration
from agents.personalization.critic import CriticAgent
from roles.core.base_role import RoleCollection, RoleMode
from roles.personalization.emotion_critic import (
    EmotionConsultantCriticRole,
    EmotionDeepReviewCriticRole,
)


class EmotionCriticAgent(CriticAgent):
    """
    Agent that evaluates personalization responses based on user preferences.
    """

    def __init__(
        self,
        lm_config: LMConfiguration | None = None,
    ):
        super().__init__(
            name="emotion_critic",
            roles=RoleCollection(
                [EmotionConsultantCriticRole(), EmotionDeepReviewCriticRole()],
                mode=RoleMode.OR,
            ),
            lm_config=lm_config,
        )
