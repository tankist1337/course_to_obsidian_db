from abc import ABC, abstractmethod
from entry.entry_name_provider import OsListdirEntryNameProvider
from entry.invalid_entry_names_provider import IInvalidEntryNameProvider


class FakeOsListdirEntryNamesStrategy(OsListdirEntryNameProvider, ABC):
    @abstractmethod
    def get(self, directory_path) -> set[str]:
        pass


class FakeNeutralStrategy(FakeOsListdirEntryNamesStrategy):
    def get(self, directory_path) -> set[str]:
        return {"file1", "directory1", "all_good.txt"}


class FakeNoEntryNamesStrategy(FakeOsListdirEntryNamesStrategy):
    def get(self, directory_path) -> set[str]:
        return set()


class FakeNoDirectoriesStrategy(FakeOsListdirEntryNamesStrategy):
    def get(self, directory_path) -> set[str]:
        return {"file1", "file2"}


class FakeNoFilesStrategy(FakeOsListdirEntryNamesStrategy):
    def get(self, directory_path) -> set[str]:
        return {"directory1", "directory2"}


class FakeInvalidCharactersInName(FakeOsListdirEntryNamesStrategy):
    def __init__(self, entry_with_invalid_characters_maker):
        self.entry_with_invalid_characters_maker = entry_with_invalid_characters_maker

    def get(self, directory_path):
        invalid_entries = self.entry_with_invalid_characters_maker.get()

        return {entry.name for entry in invalid_entries}


class FakeInvalidNamesStrategy(FakeOsListdirEntryNamesStrategy):
    def __init__(self, invalid_names_provider: IInvalidEntryNameProvider):
        self.invalid_names_provider = invalid_names_provider

    def get(self, directory_path):
        return self.invalid_names_provider.get()


class FakeOsListdirEntryNamesProvider(OsListdirEntryNameProvider):
    def __init__(self, strategy: FakeOsListdirEntryNamesStrategy | None = None):
        if strategy is None:
            strategy = FakeNeutralStrategy()

        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def get(self, directory_path) -> set[str]:
        if self.strategy:
            return self.strategy.get(directory_path)
        raise TypeError
