import os

from . import FilePath


class Path:
    """
    This is a class for working with PATHs, like PATH or MANPATH.

    It has the interface of a list. It loads the initial set from an environment variable,
    and converts each element into a :class:`~ostools.FilePath`, with ``exist_required`` set to false.
    """
    def __init__(self, envvar='PATH'):
        """
        Args:
            envvar (string): The environment variable to load the paths from.
        """
        self.envvar = envvar
        self.items = []
        self.load()

    def load(self):
        """
        Loads the
        """
        items = os.environ.get(self.envvar, '').split(':')
        for item in items:
            self.items.append(FilePath(item, exist_required=False))

    def __iter__(self):
        return iter(self.items)

    def __contains__(self, item):
        return item in self.items

    def __len__(self):
        return len(self.items)

    def __getitem__(self, item):
        return self.items[item]

    def __setitem__(self, key, value):
        self.items[key] = FilePath(value, exist_required=False)

    def __getattr__(self, item):
        return getattr(self.items, item)

    def append(self, item):
        self.items.append(FilePath(item, exist_required=False))

    def extend(self, items):
        for item in items:
            self.append(item)

    def insert(self, index, item):
        self.items.insert(index, FilePath(item, exist_required=False))
