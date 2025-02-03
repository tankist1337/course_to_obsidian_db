from abc import ABC, abstractmethod

from base.validator import IValidator
from path.provider.path_provider import IPathProvider


class IPathManager(ABC):
    @abstractmethod
    def get() -> str:
        pass


class PathManager(IPathManager):
    def __init__(
        self,
        path_provider: IPathProvider,
        path_validator_manager: IValidator[str],
    ):
        self.path_provider = path_provider
        self.path_validator_manager = path_validator_manager

    def get(self) -> str:
        path = self.path_provider.get()
        self.path_validator_manager.validate(path)

        return path
