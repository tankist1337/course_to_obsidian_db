from abc import ABC, abstractmethod
import os

from path.validator.path_exception import (
    NonePathException,
    NonDirectoryPathException,
    NotExistingPathException,
)


class IPathValidator(ABC):
    @abstractmethod
    def validate(path):
        pass


class NonePathValidator(IPathValidator):
    def validate(self, path):
        if path is None:
            raise NonePathException("The directory path is None")


# todo: Review this class os.path.isdir
class NonDirectoryPathValidator(IPathValidator):
    def validate(self, path):
        if not os.path.isdir(path):
            raise NonDirectoryPathException("The directory path is not a directory")


# todo: Review this class os.path.exists
class NotExistingPathValidator(IPathValidator):
    def validate(self, path):
        if not os.path.exists(path):
            raise NotExistingPathException("The directory path does not exist")
