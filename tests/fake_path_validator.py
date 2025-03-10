import unittest

from path.validator.path_exception import (
    NonDirectoryPathException,
    NonFilePathException,
    NotExistingPathException,
)
from path.validator.path_validator import IPathValidator


class FakeExistingPathValidator:
    @staticmethod
    def validate(path: str):
        existing_paths = set[str](
            {
                "directory/for/tests/",
                "directory/for/tests",
                "directory/for/tests/directory1",
                "directory/for/tests/file2",
                "directory/for/tests/file1.txt",
            }
        )

        if path not in existing_paths:
            raise NotExistingPathException(f"{path} isn't existing")


class FakeDirectoryPathValidator:
    @staticmethod
    def validate(path: str):
        directories = set[str](
            {
                "directory/for/tests/",
                "directory/for/tests",
                "directory/for/tests/directory1",
            }
        )

        if path not in directories:
            raise NonDirectoryPathException(f"{path} is not a directory")


class FakeFilePathValidator:
    @staticmethod
    def validate(path: str):
        files = set[str](
            {
                "directory/for/tests/file2",
                "directory/for/tests/file1.txt",
            }
        )

        if path not in files:
            raise NonFilePathException(f"{path} is not a file")


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
