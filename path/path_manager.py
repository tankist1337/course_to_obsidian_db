from abc import ABC, abstractmethod

from path.provider.path_provider import IPathProvider
from path.validator.path_validator_manager import IPathValidatorManager


class IPathManager(ABC):
    @abstractmethod
    def get_path() -> str:
        pass


class PathManager(IPathManager):
    def __init__(
        self,
        path_provider: IPathProvider,
        path_validator_manager: IPathValidatorManager,
    ):
        self.path_provider = path_provider
        self.path_validator_manager = path_validator_manager

    def get_path(self) -> str:
        path = self.path_provider.get_path()
        self.path_validator_manager.validate(path)

        return path
