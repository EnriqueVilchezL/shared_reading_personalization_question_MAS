from roles.langfuse_role import LangFuseRole
from roles.permissions.last_message_permission import LastMessagePermission


class PersonalizerRole(LangFuseRole):
    """
    Role that personalizes the responses based on user preferences.
    """

    def __init__(self):
        super().__init__(
            name="personalizer",
            permissions=[LastMessagePermission()],
            activities=[],
        )

class PersonalizerEditorRole(LangFuseRole):
    """
    Role that edits the personalized responses based on user feedback.
    """

    def __init__(self):
        super().__init__(
            name="personalizer_editor",
            permissions=[LastMessagePermission()],
            activities=[],
        )
