import unittest

from path.validator.path_exception import (
    NonePathException,
    NonDirectoryPathException,
    NotExistingPathException,
)
from path.validator.path_validator import (
    IPathValidator,
    NonePathValidator,
)


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


class TestNonDirectoryPathValidator(unittest.TestCase):
    def test_validate_is_directory(self):
        path = "directory/for/tests/"
        validator = FakeNonDirectoryPathValidator(directories_dictionary={path: True})

        validator.validate(path)

    def test_validate_is_not_directory(self):
        path = "directory/for/tests/raise.txt"
        validator = FakeNonDirectoryPathValidator(directories_dictionary={path: False})

        with self.assertRaises(NonDirectoryPathException):
            validator.validate(path)


class TestNotExistingPathValidator(unittest.TestCase):
    def test_validate_is_existing(self):
        path = "directory/for/tests/raise.txt"
        validator = FakeNotExistingPathValidator(existing_path_dictionary={path: True})

        validator.validate(path)

    def test_validate_is_not_existing(self):
        path = "directory/for/tests/raise.png"
        validator = FakeNotExistingPathValidator(existing_path_dictionary={path: False})

        with self.assertRaises(NotExistingPathException):
            validator.validate(path)


class FakeNotExistingPathValidator(IPathValidator):
    def __init__(self, existing_path_dictionary: dict[str, bool] = None):
        self.existing_path_dictionary = existing_path_dictionary

    def validate(self, item):
        if self.existing_path_dictionary is not None:
            if self.existing_path_dictionary.get(item) is not True:
                raise NotExistingPathException(f'The path "{item}" does not exist')
        else:
            # All paths are existing
            pass


class FakeNonDirectoryPathValidator(IPathValidator):
    def __init__(self, directories_dictionary: dict[str, bool] = None):
        self.directories_dictionary = directories_dictionary

    def validate(self, item):
        if self.directories_dictionary is not None:
            if self.directories_dictionary.get(item) is not True:
                raise NonDirectoryPathException(f'The path "{item}" isn\'t a directory')
        else:
            # All paths are directories
            pass
