from agents.core.base_lm_config import LMConfiguration
from agents.personalization.critic import CriticAgent
from roles.core.base_role import RoleCollection, RoleMode
from roles.personalization.moral_critic import (
    MoralConsultantCriticRole,
    MoralDeepReviewCriticRole,
)


class MoralCriticAgent(CriticAgent):
    """
    Agent that evaluates personalization responses based on user preferences.
    """

    def __init__(
        self,
        lm_config: LMConfiguration | None = None,
    ):
        super().__init__(
            name="moral_critic",
            roles=RoleCollection(
                [MoralDeepReviewCriticRole(), MoralConsultantCriticRole()],
                mode=RoleMode.OR,
            ),
            lm_config=lm_config,
        )
