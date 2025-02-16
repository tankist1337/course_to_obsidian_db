import unittest

from path.validator.path_exception import (
    NonDirectoryPathException,
    NonFilePathException,
    NotExistingPathException,
)
from path.validator.path_validator import IPathValidator


class FakeNotExistingPathValidator(IPathValidator):
    def __init__(self, existing_path_dictionary: dict[str, bool] | None = None):
        self.existing_path_dictionary = existing_path_dictionary

    def set_existing_paths(self, existing_path_dictionary: dict[str, bool]):
        self.existing_path_dictionary = existing_path_dictionary

    def update_existing_paths(self, *args: dict[str, bool]):
        merged_dictionary = {}
        for dictionary in args:
            merged_dictionary.update(dictionary)

        if self.existing_path_dictionary:
            self.existing_path_dictionary.update(merged_dictionary)
        else:
            self.set_existing_paths(merged_dictionary)

    def validate(self, item):
        if self.existing_path_dictionary is not None:
            if not self.existing_path_dictionary.get(item):  # type: ignore
                raise NotExistingPathException(f'The path "{item}" does not exist')
        else:
            # All paths are existing
            pass


class FakeNonDirectoryPathValidator(IPathValidator):
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


class FakeNonFilePathValidator(IPathValidator):
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
