from domain.evaluation_aggregate.criteria import Criteria
from roles.langfuse_role import LangFuseRole
from roles.permissions.last_message_permission import LastMessagePermission


class DeepReviewCriticRole(LangFuseRole):
    """
    Role that evaluates some aspect of a personalization response.
    """

    def __init__(self, criteria: Criteria, activities: list[str] = None):

        super().__init__(
            name="personalization_deep_review_critic",
            permissions=[LastMessagePermission()],
            activities=activities or [],
        )
        self.criteria: Criteria = criteria

        self.configure({
            "criteria": self.criteria.type,
            "description": self.criteria.description,
            "indicators": "".join(f"- {indicator}\n" for indicator in self.criteria.indicators)
        })

class ConsultantCriticRole(LangFuseRole):
    """
    Role that evaluates some aspect of a personalization response.
    """

    def __init__(self, criteria: Criteria, activities: list[str] = None):

        super().__init__(
            name="personalization_consultant_critic",
            permissions=[LastMessagePermission()],
            activities=activities or [],
        )
        self.criteria: Criteria = criteria

        self.configure({
            "criteria": self.criteria.type,
            "description": self.criteria.description,
            "indicators": "".join(f"- {indicator}\n" for indicator in self.criteria.indicators)
        })
