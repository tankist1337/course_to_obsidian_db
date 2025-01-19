import unittest

from path.validator.path_exception import (
    InvalidCharactersPathException,
    NonePathException,
    NotDirectoryException,
    NotExistingPathException,
)
from path.validator.path_validator import (
    IPathValidator,
    LinuxInvalidCharactersPathValidator,
    NonePathValidator,
)
from path.validator.invalid_characters_for_path_provider import (
    InvalidCharactersForPathProvider,
    LinuxInvalidCharactersForPathProvider,
)


class FakeInvalidCharactersPathMaker:
    def __init__(self, invalid_characters_provider: InvalidCharactersForPathProvider):
        self.invalid_characters_provider = invalid_characters_provider

    def get_invalid_paths(self, path="to/project"):
        invalid_characters = self.invalid_characters_provider.get_characters()
        invalid_paths = []

        for character in invalid_characters:
            invalid_path = self.__put_character_in_center(path, character)
            invalid_paths.append(invalid_path)

        return invalid_paths

    def __put_character_in_center(self, path, character):
        center_index = int(len(path) / 2)
        return path[:center_index] + character + path[center_index:]


class TestLinuxInvalidCharactersPathValidator(unittest.TestCase):
    def setUp(self):
        self.invalid_characters_provider = LinuxInvalidCharactersForPathProvider()
        self.validator = LinuxInvalidCharactersPathValidator(
            self.invalid_characters_provider
        )

    def test_validate_without_incorrect_characters(self):
        path = "directory/for/tests/"

        self.validator.validate(path)

    def test_validate_with_incorrect_characters(self):
        maker = FakeInvalidCharactersPathMaker(self.invalid_characters_provider)
        path = "directory/for/tests/"
        invalid_paths = maker.get_invalid_paths(path)

        for invalid_path in invalid_paths:
            with self.assertRaises(InvalidCharactersPathException):
                self.validator.validate(invalid_path)


class TestNonePathValidator(unittest.TestCase):
    def setUp(self):
        self.validator = NonePathValidator()

    def test_validate_without_none(self):
        path = "directory/for/tests/"

        self.validator.validate(path)

    def test_validate_with_none(self):
        path = None

        with self.assertRaises(NonePathException):
            self.validator.validate(path)


class TestNotDirectoryValidator(unittest.TestCase):
    def test_validate_is_directory(self):
        validator = FakeNotDirectoryValidator(is_dir=True)

        path = "directory/for/tests/"

        validator.validate(path)

    def test_validate_is_not_directory(self):
        validator = FakeNotDirectoryValidator(is_dir=False)

        path = "directory/for/tests/raise.txt"

        with self.assertRaises(NotDirectoryException):
            validator.validate(path)


class FakeNotDirectoryValidator(IPathValidator):
    def __init__(self, is_dir=True):
        self.is_dir = is_dir

    def validate(self, path):
        if not self.is_dir:
            raise NotDirectoryException("The directory path is not a directory")


class TestNotExistingPathValidator(unittest.TestCase):
    def test_validate_is_existing(self):
        validator = FakeNotExistingPathValidator(is_existing=True)

        path = "directory/for/tests/raise.txt"

        validator.validate(path)

    def test_validate_is_not_existing(self):
        validator = FakeNotExistingPathValidator(is_existing=False)

        path = "directory/for/tests/raise.png"

        with self.assertRaises(NotExistingPathException):
            validator.validate(path)


class FakeNotExistingPathValidator(IPathValidator):
    def __init__(self, is_existing=True):
        self.is_existing = is_existing

    def validate(self, path):
        if not self.is_existing:
            raise NotExistingPathException("The directory path does not exist")
