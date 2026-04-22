from collections.abc import MutableSet


class ProtocolCollection(MutableSet):
    def __init__(self, iterable=None):
        self._data = set(iterable or [])

    def __contains__(self, item):
        return item in self._data

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def add(self, item):
        self._data.add(item)

    def discard(self, item):
        self._data.discard(item)
        return iter(self._data)
