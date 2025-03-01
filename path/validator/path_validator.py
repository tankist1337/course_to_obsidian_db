from abc import ABC, abstractmethod
import os

from base.validator import IValidator
from path.validator.path_exception import (
    NonePathException,
    NonDirectoryPathException,
    NotExistingPathException,
)


class IPathValidator(IValidator[str | None], ABC):
    @abstractmethod
    def validate(self, item: str | None):
        pass


class NonePathValidator(IPathValidator):
    def validate(self, item):
        if item is None:
            raise NonePathException("The path must be not None")


class NonFilePathValidator(IPathValidator):
    def validate(self, item):
        if not os.path.isfile(item):
            raise NonDirectoryPathException(f"The path {item} is not a file")


# todo: Review this class os.path.isdir
class NonDirectoryPathValidator(IPathValidator):
    def validate(self, item):
        if not os.path.isdir(item):  # type: ignore
            raise NonDirectoryPathException(f"The path {item} is not a directory")


# todo: Review this class os.path.exists
class ExistingPathValidator(IPathValidator):
    def validate(self, item):
        if not os.path.exists(item):  # type: ignore
            raise NotExistingPathException(f"The path {item} doesn't exist")
