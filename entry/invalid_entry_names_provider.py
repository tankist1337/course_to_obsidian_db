from abc import ABC, abstractmethod


class IInvalidEntryNamesProvider(ABC):
    @abstractmethod
    def get(self) -> set[str]:
        pass


class LinuxInvalidEntryNamesProvider(IInvalidEntryNamesProvider):
    def get(self) -> set[str]:
        return {".", "..", ""}
