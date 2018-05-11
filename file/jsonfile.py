import copy
import json
from contextlib import ContextDecorator


class JSONFile(ContextDecorator):
    def __init__(self, filename):
        self.filename = filename
        self.__data_original = None
        self.reload()
        self.data = None

    @property
    def data_original(self):
        return copy.copy(self.__data_original)

    @data_original.setter
    def data_original(self, value):
        self.__data_original = value

    def save(self):
        if self.data_original == self.data:
            return
        json.dump(self.data, open(self.filename, 'w'))

    def reload(self):
        self.data = json.load(open(self.filename, mode='r'))
        self.data_original = copy.copy(self.data)

    close = save

    __exit__ = close

    __enter__ = lambda self: self
