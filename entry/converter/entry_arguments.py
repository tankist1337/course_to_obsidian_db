from abc import ABC


class ArgumentsToConvertToEntry(ABC):
    pass


class SingleEntryArguments(ArgumentsToConvertToEntry):
    def __init__(self, name: str, directory_path: str):
        self.name = name
        self.directory_path = directory_path


class SetEntryArguments(ArgumentsToConvertToEntry):
    def __init__(self, names: set[str], directory_path: str):
        self.names = names
        self.directory_path = directory_path
