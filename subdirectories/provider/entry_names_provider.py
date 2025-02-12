from abc import ABC, abstractmethod
import os


class IEntryNamesProvider(ABC):
    @abstractmethod
    def get(self, directory_path: str) -> set[str]:
        pass


class OsListdirEntryNamesProvider(IEntryNamesProvider):
    def get(self, directory_path: str) -> set[str]:
        return set(os.listdir(directory_path))
