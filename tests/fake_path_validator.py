from abc import ABC, abstractmethod
import unittest

from path.validator.path_exception import (
    NonDirectoryPathException,
    NonFilePathException,
    NotExistingPathException,
)
from path.validator.path_validator import IPathValidator


class IFakeExistingPathValidator(IPathValidator, ABC):
    @abstractmethod
    def set(self, *args: dict[str, bool]):
        pass

    @abstractmethod
    def update(self, *args: dict[str, bool]):
        pass


class FakeExistingPathValidator(IFakeExistingPathValidator):
    def __init__(self, existing_path_dictionary: dict[str, bool] | None = None):
        self._existing_path_dictionary = existing_path_dictionary

    def __merge_dictionaries(self, *args: dict[str, bool]):
        merged_dictionary = {}
        for dictionary in args:
            merged_dictionary.update(dictionary)

        return merged_dictionary

    def set(self, *args: dict[str, bool]):
        self._existing_path_dictionary = self.__merge_dictionaries(*args)

    def update(self, *args: dict[str, bool]):
        existing_paths = self.__merge_dictionaries(*args)

        if self._existing_path_dictionary:
            self._existing_path_dictionary.update(existing_paths)
        else:
            self.set(existing_paths)

    def validate(self, item):
        if self._existing_path_dictionary is not None:
            if not self._existing_path_dictionary.get(item):  # type: ignore
                raise NotExistingPathException(f'The path "{item}" does not exist')
        else:
            # All paths are existing
            pass


class IFakeDirectoryPathValidator(IPathValidator, ABC):
    @abstractmethod
    def set(self, *args: dict[str, bool]):
        pass

    @abstractmethod
    def update(self, *args: dict[str, bool]):
        pass


class FakeDirectoryPathValidator(IFakeDirectoryPathValidator):
    def __init__(self, directory_dictionary: dict[str, bool] | None = None):
        self._directory_dictionary = directory_dictionary

    def __merge_dictionaries(self, *args: dict[str, bool]):
        merged_dictionary = {}
        for dictionary in args:
            merged_dictionary.update(dictionary)

        return merged_dictionary

    def set(self, *args: dict[str, bool]):
        self._directory_dictionary = self.__merge_dictionaries(*args)

    def update(self, *args: dict[str, bool]):
        directories = self.__merge_dictionaries(*args)

        if self._directory_dictionary:
            self._directory_dictionary.update(directories)
        else:
            self.set(directories)

    def validate(self, item):
        if self._directory_dictionary is not None:
            if not self._directory_dictionary.get(item):  # type: ignore
                raise NonDirectoryPathException(f'The path "{item}" isn\'t a directory')
        else:
            # All paths are directories
            pass


class IFakeFilePathValidator(IPathValidator, ABC):
    @abstractmethod
    def set(self, *args: dict[str, bool]):
        pass

    @abstractmethod
    def update(self, *args: dict[str, bool]):
        pass


class FakeFilePathValidator(IFakeFilePathValidator):
    def __init__(self, file_dictionary: dict[str, bool] | None = None):
        self._file_dictionary = file_dictionary

    def __merge_dictionaries(self, *args: dict[str, bool]):
        merged_dictionary = {}
        for dictionary in args:
            merged_dictionary.update(dictionary)

        return merged_dictionary

    def set(self, *args: dict[str, bool]):
        self._file_dictionary = self.__merge_dictionaries(*args)

    def update(self, *args: dict[str, bool]):
        files = self.__merge_dictionaries(*args)

        if self._file_dictionary:
            self._file_dictionary.update(files)
        else:
            self.set(files)

    def validate(self, item):
        if self._file_dictionary is not None:
            if not self._file_dictionary.get(item):  # type: ignore
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
