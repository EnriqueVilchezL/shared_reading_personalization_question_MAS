from agents.core.base_lm_config import LMConfiguration
from agents.personalization.critic import CriticAgent
from roles.core.base_role import RoleCollection, RoleMode
from roles.personalization.naturalness_critic import (
    NaturalnessConsultantCriticRole,
    NaturalnessDeepReviewCriticRole,
)


class NaturalnessCriticAgent(CriticAgent):
    """
    Agent that evaluates personalization responses based on user preferences.
    """

    def __init__(
        self,
        lm_config: LMConfiguration | None = None,
    ):
        super().__init__(
            name="naturalness_critic",
            roles=RoleCollection(
                [NaturalnessDeepReviewCriticRole(), NaturalnessConsultantCriticRole()],
                mode=RoleMode.OR,
            ),
            lm_config=lm_config,
        )
