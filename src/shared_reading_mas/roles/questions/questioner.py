from shared_reading_mas.domain.evaluation_aggregate.category import Category
from shared_reading_mas.roles.langfuse_role import LangFuseRole
from shared_reading_mas.roles.permissions.last_message_permission import (
    LastMessagePermission,
)
from shared_reading_mas.roles.questions.types import (
    COMPLETION_TYPE,
    DISTANCING_TYPE,
    OPEN_ENDED_TYPE,
    RECALL_TYPE,
    WH_TYPE,
)


class QuestionerRole(LangFuseRole):
    """
    Role that creates prompts for a story.
    """

    def __init__(self, prompt: Category, activities: list[str] = None):

        super().__init__(
            name="questioner",
            permissions=[LastMessagePermission()],
            activities=activities or [],
        )
        self.prompt: Category = prompt

        self.configure({
            "type": self.prompt.type,
            "description": self.prompt.description,
            "tips": "".join(f"- {indicator}\n" for indicator in self.prompt.indicators)
        })

class CompletionQuestionerRole(QuestionerRole):
    """
    Role that creates completion questions for a story.
    """

    def __init__(self):
        super().__init__(prompt=COMPLETION_TYPE)

class RecallQuestionerRole(QuestionerRole):
    """
    Role that creates recall questions for a story.
    """

    def __init__(self):
        super().__init__(prompt=RECALL_TYPE)

class WhQuestionerRole(QuestionerRole):
    """
    Role that creates WH questions for a story.
    """

    def __init__(self):
        super().__init__(prompt=WH_TYPE)

class OpenEndedQuestionerRole(QuestionerRole):
    """
    Role that creates open-ended questions for a story.
    """

    def __init__(self):
        super().__init__(prompt=OPEN_ENDED_TYPE)

class DistancingQuestionerRole(QuestionerRole):
    """
    Role that creates distancing questions for a story.
    """

    def __init__(self):
        super().__init__(prompt=DISTANCING_TYPE)


class QuestionerEditorRole(LangFuseRole):
    """
    Role that edits the questions responses based on user feedback.
    """

    def __init__(self):
        super().__init__(
            name="questioner_editor",
            permissions=[LastMessagePermission()],
            activities=[],
        )
