from langfuse import get_client

from exceptions import RoleException
from roles.core.base_permission import Permission
from roles.core.base_role import Role


class LangFuseRole(Role):
    def __init__(
        self,
        name: str,
        permissions: list[Permission] = None,
        activities: list[any] = None,
        protocols: list[str] = None,
    ):
        super().__init__(name, permissions, activities, protocols)

    def _instructions(self) -> str:
        try:
            # Transform to instruction
            prompt = get_client().get_prompt(self.name, type="chat")
            system_prompt = prompt.compile()[0]

            return system_prompt["content"]

        except Exception as e:
            raise RoleException(
                f"Couldn't retreive the role {self.name} from LangFuse. Please check if the role is correctly registered."
                + f" Error: {str(e)}"
            )
