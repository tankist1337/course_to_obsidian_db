from abc import ABC, abstractmethod
import argparse
from path.validator.path_validator import IPathValidator


class IPathProvider(ABC):
    @abstractmethod
    def get(self) -> str:
        pass


class CliPathProvider(IPathProvider):
    # todo: refactor this method for single responsibility
    def get(self) -> str:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--path",
            help="Path to the directory where the course parts will be exported.",
        )

        args = parser.parse_args()
        path = args.path

        return path


class PathManager(IPathProvider):
    def __init__(
        self,
        provider: IPathProvider,
        validator_manager: IPathValidator,
    ):
        self.provider = provider
        self.validator_manager = validator_manager

    def get(self) -> str:
        path = self.provider.get()
        self.validator_manager.validate(path)

        return path
