from abc import ABC, abstractmethod
import os


class IEntryNameProvider(ABC):
    @abstractmethod
    def get(self, directory_path: str) -> set[str]:
        pass


class OsListdirEntryNameProvider(IEntryNameProvider):
    def get(self, directory_path: str) -> set[str]:
        return set(os.listdir(directory_path))
