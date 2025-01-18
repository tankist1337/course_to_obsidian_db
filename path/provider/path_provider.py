from abc import ABC, abstractmethod
import argparse


class IPathProvider(ABC):
    @abstractmethod
    def get_path() -> str:
        pass


class CliPathProvider(IPathProvider):
    # todo: refactor this method for single responsibility
    def get_path(self) -> str:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--path",
            help="Path to the directory where the course parts will be exported.",
        )

        args = parser.parse_args()
        path = args.path

        return path
