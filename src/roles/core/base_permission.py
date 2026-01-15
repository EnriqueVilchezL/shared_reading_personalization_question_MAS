from abc import ABC, abstractmethod
from collections.abc import MutableSet


class Permission(ABC):
    name: str

    def __init__(self, name: str):
        """
        Initializes the permission with the given name.
        """
        self.name = name

    def __call__(self, *args, **kwds):
        return self.apply(*args, **kwds)

    @abstractmethod
    def apply(self, data: any) -> any:
        """
        Applies the permission to the given data.

        Args:
            data (any): The data to which the permission is applied.

        Returns:
            any: The data after applying the permission.
        """
        ...

class PermissionCollection(MutableSet):
    def __init__(self, iterable=None):
        self._data = set(iterable or [])

    def __contains__(self, item):
        return item in self._data

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __call__(self, *args, **kwds):
        return self.apply(*args, **kwds)

    def add(self, item):
        self._data.add(item)

    def discard(self, item):
        self._data.discard(item)
        return iter(self._data)

    def apply(self, data: any) -> any:
        """
        Applies all permissions in the collection to the given data.

        Args:
            data (any): The data to which the permissions are applied.

        Returns:
            any: The data after applying all permissions.
        """
        for permission in self._data:
            data = permission(data)
        return data
