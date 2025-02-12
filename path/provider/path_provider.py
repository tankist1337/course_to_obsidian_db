from abc import ABC, abstractmethod
import argparse
from base.validator import IValidator


class IPathProvider(ABC):
    @abstractmethod
    def get(self) -> str | None:
        pass


class IPathManager(ABC):
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


class PathManager(IPathManager):
    def __init__(
        self,
        provider: IPathProvider,
        validator: IValidator,
    ):
        self.provider = provider
        self.validator = validator

    def get(self) -> str:
        path = self.provider.get()
        self.validator.validate(path)

        return path  # type: ignore
