from abc import ABC, abstractmethod
from collections.abc import MutableSet
from enum import Enum

from roles.core.base_activity import ActivityCollection
from roles.core.base_permission import Permission, PermissionCollection
from roles.core.base_protocol import ProtocolCollection


class SafeDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"

class RoleMode(Enum):
    AND = "and"
    OR = "or"

class Role(ABC):
    name: str
    """
    Name of the role.
    """

    permissions: PermissionCollection
    """
    Permissions of the role.
    """

    activities: ActivityCollection
    """
    Activities that the role can perform.
    """

    protocols: ProtocolCollection
    """
    Protocols associated with the role.
    """

    instructions: str
    """
    Instructions for the role.
    """

    def __init__(
        self,
        name: str,
        permissions: list[Permission] | None = None,
        activities: list[any] | None = None,
        protocols: list[str] | None = None,
    ):
        """
        Initializes the role with the given permissions and activities.

        Args:
            permissions (Optional[list[BasePermission]]): Permissions of the role.
            activities (Optional[list[any]]): Activities that the role can perform.
        """
        self.name = name
        self.permissions = (
            PermissionCollection(permissions)
            if permissions is not None
            else PermissionCollection()
        )
        self.activities = (
            ActivityCollection(activities)
            if activities is not None
            else ActivityCollection()
        )
        self.protocols = (
            ProtocolCollection(protocols)
            if protocols is not None
            else ProtocolCollection()
        )
        self.instructions = self._instructions()

    def configure(self, data: dict) -> str:
        """
        Compiles the instructions for the given data.

        Args:
            data (dict): The data to compile instructions for.

        Returns:
            str: The compiled instructions.
        """
        instruction = self.instructions.replace("{{", "{").replace("}}", "}")
        self.instructions = instruction.format_map(SafeDict(data))
        return self.instructions

    @abstractmethod
    def _instructions(self) -> str:
        """
        Gets the instructions for the role

        Returns:
            str: Instructions for the role.
        """
        ...

class RoleCollection(MutableSet):
    instructions: str
    """
    Combined instructions from active roles.
    """

    activities: ActivityCollection
    """
    Combined activities from active roles.
    """

    protocols: ProtocolCollection
    """
    Combined protocols from active roles.
    """

    def __init__(self, iterable=None, mode: RoleMode = RoleMode.AND):
        self._data = set(iterable or [])
        self.mode = mode

        # Only one role may be active in OR mode
        self._active_role = None

        if self.mode is RoleMode.OR and self._data:
            # Deterministically select one role
            self._active_role = next(iter(self._data))

        self.instructions = self._instructions()
        self.activities = self._activities()
        self.protocols = self._protocols()

    def __contains__(self, item):
        return item in self._data

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def add(self, item):
        """
        Adds a role to the collection.
        """
        self._data.add(item)

        if self.mode is RoleMode.OR and self._active_role is None:
            self._active_role = item

        self._rebuild()

    def discard(self, item):
        """
        Removes a role from the collection.
        """
        self._data.discard(item)

        if self.mode is RoleMode.OR and self._active_role == item:
            self._active_role = next(iter(self._data), None)

        self._rebuild()
        return iter(self._data)

    def get_active_role(self):
        """
        Gets the active role in OR mode.

        Returns:
            The active role, or None if no role is active.
        """
        if self.mode is not RoleMode.OR:
            raise ValueError("Active role is only valid in OR mode")

        return self._active_role

    def activate(self, role_type: type[Role]):
        """
        Activates a role in OR mode.
        Exactly one role must be active.

        Args:
            role_type: The role type to activate.
        """
        if self.mode is not RoleMode.OR:
            raise ValueError("Activation is only valid in OR mode")

        for role in self._data:
            if isinstance(role, role_type):
                self._active_role = role
                self._rebuild()

                return

        raise ValueError("Role type not in collection")

    def _roles_to_use(self):
        """
        Returns the roles to be used based on the collection mode.
        """
        if self.mode is RoleMode.AND:
            return self._data

        # OR mode: exactly one active role
        return {self._active_role} if self._active_role else set()

    def _rebuild(self):
        """
        Recomputes all aggregated artifacts.
        """
        self.instructions = self._instructions()
        self.activities = self._activities()
        self.protocols = self._protocols()

    def _instructions(self) -> str:
        """
        Gets the combined instructions from active roles.

        Returns:
            str: Combined instructions.
        """
        instructions = set()
        for role in self._roles_to_use():
            instruction = role.instructions
            if instruction:
                instructions.add(instruction)

        return "\n".join(instructions)

    def set_variables(self, data: dict) -> str:
        """
        Compiles the instructions for the given data.

        Args:
            data (dict): The data to compile instructions for.

        Returns:
            str: The compiled instructions.
        """
        instructions = set()
        for role in self._data:
            instruction = role.configure(data)
            if instruction:
                instructions.add(instruction)

        self._rebuild()
        return self.instructions

    def _activities(self) -> set[any]:
        """
        Gets all activities from active roles.

        Returns:
            set[any]: All activities.
        """
        activities = ActivityCollection()

        for role in self._roles_to_use():
            activities |= role.activities

        return activities

    def _protocols(self) -> set[str]:
        """
        Gets all protocols from active roles.

        Returns:
            set[str]: All protocols.
        """
        protocols = ProtocolCollection()

        for role in self._roles_to_use():
            protocols |= role.protocols

        return protocols

    def apply_permissions(self, data: dict) -> dict:
        """
        Applies permissions from active roles.

        Args:
            data (dict): The data to which the permissions are applied.

        Returns:
            dict: The data after applying permissions.
        """
        permissions = PermissionCollection()

        for role in self._roles_to_use():
            permissions |= role.permissions

        for permission in permissions:
            data = permission.apply(data)

        return data
