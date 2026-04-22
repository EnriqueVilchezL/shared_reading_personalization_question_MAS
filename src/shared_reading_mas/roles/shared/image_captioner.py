from shared_reading_mas.roles.langfuse_role import LangFuseRole
from shared_reading_mas.roles.permissions.last_message_permission import (
    LastMessagePermission,
)


class ImageCaptionerRole(LangFuseRole):
    """
    Role that captions images.
    """

    def __init__(self):
        super().__init__(
            name="image_captioner",
            permissions=[LastMessagePermission()],
            activities=[],
        )
