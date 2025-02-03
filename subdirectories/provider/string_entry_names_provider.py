from abc import ABC, abstractmethod
import os


class IStringEntryNamesProvider(ABC):
    @abstractmethod
    def get(self, directory_path: str) -> list[str]:
        pass


class OsListdirStringEntryNamesProvider(IStringEntryNamesProvider):
    def get(self, directory_path: str) -> list[str]:
        return os.listdir(directory_path)
