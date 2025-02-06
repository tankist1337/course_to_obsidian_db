from abc import ABC, abstractmethod
import os


class IEntryNamesProvider(ABC):
    @abstractmethod
    def get(self, directory_path: str) -> list[str]:
        pass


class OsListdirEntryNamesProvider(IEntryNamesProvider):
    def get(self, directory_path: str) -> list[str]:
        return os.listdir(directory_path)
