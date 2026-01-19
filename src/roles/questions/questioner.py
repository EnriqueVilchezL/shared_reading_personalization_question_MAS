from domain.evaluation_aggregate.criteria import Criteria
from roles.langfuse_role import LangFuseRole
from roles.permissions.last_message_permission import LastMessagePermission


class QuestionerRole(LangFuseRole):
    """
    Role that creates questions for a story.
    """

    def __init__(self, criteria: Criteria, activities: list[str] = None):

        super().__init__(
            name="questioner",
            permissions=[LastMessagePermission()],
            activities=activities or [],
        )
        self.criteria: Criteria = criteria

        self.configure({
            "criteria": self.criteria.type,
            "description": self.criteria.description,
            "tips": "".join(f"- {indicator}\n" for indicator in self.criteria.indicators)
        })
