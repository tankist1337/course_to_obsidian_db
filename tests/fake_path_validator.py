from abc import ABC, abstractmethod
import unittest

from base.validator import StubValidator
from path.validator.path_exception import (
    NonDirectoryPathException,
    NonFilePathException,
    NotExistingPathException,
)
from path.validator.path_validator import IPathValidator


class IFakeNotExistingPathValidator(IPathValidator, ABC):
    @abstractmethod
    def set_existing_paths(self, *args: dict[str, bool]):
        pass

    @abstractmethod
    def update_existing_paths(self, *args: dict[str, bool]):
        pass

    @abstractmethod
    def validate(self, item):
        pass


class FakeStubNotExistingPathValidator(StubValidator, IFakeNotExistingPathValidator):
    def set_existing_paths(self, *args):
        pass

    def update_existing_paths(self, *args):
        pass


class FakeNotExistingPathValidator(IFakeNotExistingPathValidator):
    def __init__(self, existing_path_dictionary: dict[str, bool] | None = None):
        self.existing_path_dictionary = existing_path_dictionary

    def __merge_dictionaries(self, *args: dict[str, bool]):
        merged_dictionary = {}
        for dictionary in args:
            merged_dictionary.update(dictionary)

        return merged_dictionary

    def set_existing_paths(self, *args: dict[str, bool]):
        self.existing_path_dictionary = self.__merge_dictionaries(*args)

    def update_existing_paths(self, *args: dict[str, bool]):
        existing_paths = self.__merge_dictionaries(*args)

        if self.existing_path_dictionary:
            self.existing_path_dictionary.update(existing_paths)
        else:
            self.set_existing_paths(existing_paths)

    def validate(self, item):
        if self.existing_path_dictionary is not None:
            if not self.existing_path_dictionary.get(item):  # type: ignore
                raise NotExistingPathException(f'The path "{item}" does not exist')
        else:
            # All paths are existing
            pass


class IFakeNonDirectoryPathValidator(IPathValidator, ABC):
    @abstractmethod
    def set_directories(self, *args: dict[str, bool]):
        pass

    @abstractmethod
    def update_directories(self, *args: dict[str, bool]):
        pass

    @abstractmethod
    def validate(self, item):
        pass


class FakeStubNonDirectoryPathValidator(StubValidator, IFakeNonDirectoryPathValidator):
    def set_directories(self, *args):
        pass

    def update_directories(self, *args):
        pass


class FakeNonDirectoryPathValidator(IFakeNonDirectoryPathValidator):
    def __init__(self, directory_dictionary: dict[str, bool] | None = None):
        self.directory_dictionary = directory_dictionary

    def __merge_dictionaries(self, *args: dict[str, bool]):
        merged_dictionary = {}
        for dictionary in args:
            merged_dictionary.update(dictionary)

        return merged_dictionary

    def set_directories(self, *args: dict[str, bool]):
        self.directory_dictionary = self.__merge_dictionaries(*args)

    def update_directories(self, *args: dict[str, bool]):
        directories = self.__merge_dictionaries(*args)

        if self.directory_dictionary:
            self.directory_dictionary.update(directories)
        else:
            self.set_directories(directories)

    def validate(self, item):
        if self.directory_dictionary is not None:
            if not self.directory_dictionary.get(item):  # type: ignore
                raise NonDirectoryPathException(f'The path "{item}" isn\'t a directory')
        else:
            # All paths are directories
            pass


class IFakeNonFilePathValidator(IPathValidator, ABC):
    @abstractmethod
    def set_files(self, *args: dict[str, bool]):
        pass

    @abstractmethod
    def update_files(self, *args: dict[str, bool]):
        pass

    @abstractmethod
    def validate(self, item):
        pass


class FakeStubNonFilePathValidator(StubValidator, IFakeNonDirectoryPathValidator):
    def set_files(self, *args):
        pass

    def update_files(self, *args):
        pass


class FakeNonFilePathValidator(IFakeNonFilePathValidator):
    def __init__(self, file_dictionary: dict[str, bool] | None = None):
        self.file_dictionary = file_dictionary

    def __merge_dictionaries(self, *args: dict[str, bool]):
        merged_dictionary = {}
        for dictionary in args:
            merged_dictionary.update(dictionary)

        return merged_dictionary

    def set_files(self, *args: dict[str, bool]):
        self.file_dictionary = self.__merge_dictionaries(*args)

    def update_files(self, *args: dict[str, bool]):
        files = self.__merge_dictionaries(*args)

        if self.file_dictionary:
            self.file_dictionary.update(files)
        else:
            self.set_files(files)

    def validate(self, item):
        if self.file_dictionary is not None:
            if not self.file_dictionary.get(item):  # type: ignore
                raise NonFilePathException(f'The path "{item}" isn\'t a directory')
        else:
            # All paths are directories
            pass


class FakePathValidator(IPathValidator, unittest.TestCase):
    __called_with = list[str]()
    __called_times = 0

    def assert_called_times(self, expected: int):
        self.assertEqual(
            self.__called_times,
            expected,
            "Validator isn't called as often as expected",
        )

    def assert_called_with(self, expected: str):
        self.assertIn(
            expected,
            self.__called_with,
            "Validator isn't called with the expected path",
        )

    def validate(self, item):
        self.__called_with.append(item)  # type: ignore
        self.__called_times += 1
