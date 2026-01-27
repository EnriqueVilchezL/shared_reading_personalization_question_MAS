from roles.langfuse_role import LangFuseRole
from roles.permissions.last_message_permission import LastMessagePermission
from roles.questions.completion_questioner import CRITERIA as COMPLETION_CRITERIA
from roles.questions.distancing_questioner import CRITERIA as DISTANCING_CRITERIA
from roles.questions.open_ended_questioner import CRITERIA as OPEN_ENDED_CRITERIA
from roles.questions.recall_questioner import CRITERIA as RECALL_CRITERIA
from roles.questions.wh_questioner import CRITERIA as WH_CRITERIA


class AggregatorRole(LangFuseRole):
    """
    Role that creates aggregates questions for a story.
    """

    def __init__(self):

        super().__init__(
            name="questions_aggregator",
            permissions=[LastMessagePermission()],
            activities=[],
        )

        self.configure({
            "description": f"""
- {COMPLETION_CRITERIA.type} -> {COMPLETION_CRITERIA.description}
- {RECALL_CRITERIA.type} -> {RECALL_CRITERIA.description}
- {OPEN_ENDED_CRITERIA.type} -> {OPEN_ENDED_CRITERIA.description}
- {WH_CRITERIA.type} -> {WH_CRITERIA.description}
- {DISTANCING_CRITERIA.type} -> {DISTANCING_CRITERIA.description}
""",
        })
