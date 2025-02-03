from abc import ABC, abstractmethod


class IInvalidEntryNamesProvider(ABC):
    @abstractmethod
    def get(self):
        pass


class LinuxInvalidEntryNamesProvider(IInvalidEntryNamesProvider):
    def get(self):
        return {".", "..", ""}
