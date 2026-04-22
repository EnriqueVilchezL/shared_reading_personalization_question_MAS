from collections.abc import MutableSet


class ActivityCollection(MutableSet):
    def __init__(self, iterable=None):
        self._data = {}  # id(item) -> item
        if iterable:
            for item in iterable:
                self.add(item)

    def __contains__(self, item):
        return id(item) in self._data

    def __iter__(self):
        return iter(self._data.values())

    def __len__(self):
        return len(self._data)

    def add(self, item):
        self._data[id(item)] = item

    def discard(self, item):
        self._data.pop(id(item), None)
