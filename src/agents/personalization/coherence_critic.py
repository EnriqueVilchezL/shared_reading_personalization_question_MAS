from agents.core.base_lm_config import LMConfiguration
from agents.personalization.critic import CriticAgent
from roles.core.base_role import RoleCollection, RoleMode
from roles.personalization.coherence_critic import (
    CoherenceConsultantCriticRole,
    CoherenceDeepReviewCriticRole,
)


class CoherenceCriticAgent(CriticAgent):
    """
    Agent that evaluates personalization responses based on user preferences.
    """

    def __init__(self):
        super().__init__(
            name="coherence_critic",
            roles=RoleCollection(
                [CoherenceDeepReviewCriticRole(), CoherenceConsultantCriticRole()],
                mode=RoleMode.OR,
            ),
            lm_config=LMConfiguration(base_model="qwen3:8b", reasoning=True),
        )
