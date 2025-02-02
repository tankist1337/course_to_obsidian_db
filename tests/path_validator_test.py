import unittest

from path.validator.path_exception import (
    NonePathException,
    NotDirectoryException,
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
