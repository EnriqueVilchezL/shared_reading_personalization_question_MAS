from agents.core.base_lm_config import LMConfiguration
from agents.personalization.critic import CriticAgent
from roles.core.base_role import RoleCollection, RoleMode
from roles.personalization.style_critic import (
    StyleConsultantCriticRole,
    StyleDeepReviewCriticRole,
)


class StyleCriticAgent(CriticAgent):
    """
    Agent that evaluates personalization responses based on user preferences.
    """

    def __init__(self):
        super().__init__(
            name="style_critic",
            roles=RoleCollection(
                [StyleDeepReviewCriticRole(), StyleConsultantCriticRole()],
                mode=RoleMode.OR,
            ),
            lm_config=LMConfiguration(base_model="qwen3:8b", reasoning=True),
        )
