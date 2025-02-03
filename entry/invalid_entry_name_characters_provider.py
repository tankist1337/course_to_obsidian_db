from abc import ABC, abstractmethod


class IInvalidEntryNameCharactersProvider(ABC):
    @abstractmethod
    def get(self):
        pass


class LinuxInvalidEntryNameCharactersProvider(IInvalidEntryNameCharactersProvider):
    def get(self):
        return {"/"}
