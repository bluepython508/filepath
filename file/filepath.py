import copy
import os
from .exceptions import PathError
from .utils import abspath

class FilePath:
    def __init__(self, path='.', exist_required=True, ensure=None):
        self.path_list = []
        self.exist_required = exist_required
        self.ensure = ensure
        self.path = path

    @property
    def path(self):
        return os.path.join(*self.path_list)

    @path.setter
    def path(self, value):
        if self.exist_required:
            if self.ensure:
                if self.ensure.lower().startswith('dir'):
                    FilePath(value, False).mkdir(exist_ok=True)
                elif self.ensure.lower().startswith('file'):
                    FilePath(value, False).mkfile(exist_ok=True)
            elif not os.path.exists(value):
                raise PathError("Path %s does not exist.")
            value = abspath(value)
        self.path_list = os.path.split(value)

    def getChild(self, child=None, exist_required=None, ensure=None):
        if not child:
            return copy.copy(self)
        new_file = FilePath(self.path, (self.exist_required if exist_required is None else exist_required),
                            (self.ensure if ensure is None else ensure))
        new_file.path = os.path.join(self.path, child)
        return new_file

    __getitem__ = getChild

    def child(self, child=None):
        if not child:
            return self
        self.path = os.path.join(self.path, child)
        return self

    def ls(self):
        return os.listdir(self.path)

    def mkdir(self, new=None, exist_ok=False):
        newDir = self.getChild(new)
        if (not exist_ok) and newDir.exists:
            raise PathError("Path %s exists" % newDir.path)
        elif newDir.exists:
            return
        os.makedirs(newDir.path, exist_ok=exist_ok)

    def mkfile(self, new=None, exist_ok=False):
        newDir = self.getChild(new)
        if (not exist_ok) and newDir.exists:
            raise PathError("Path %s exists" % newDir.path)
        elif newDir.exists:
            return
        newDir.open(mode='w').close()


    @property
    def exists(self):
        return os.path.exists(self.path)

    def open(self, file=None, mode='r'):
        return open(self.getChild(file).path, mode)

    @property
    def isdir(self):
        return os.path.isdir(self.path)

    @property
    def isfile(self):
        return os.path.isfile(self.path)

    @property
    def readable(self):
        return os.access(self.path, os.R_OK)

    @property
    def writable(self):
        return os.access(self.path, os.W_OK)

    @property
    def executable(self):
        return os.access(self.path, os.X_OK)