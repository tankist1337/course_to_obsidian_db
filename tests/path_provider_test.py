import argparse
import unittest
from unittest.mock import MagicMock, patch
from base.validator import ValidatorManager
from path.provider.path_provider import PathManager
from path.validator.path_exception import (
    NonDirectoryPathException,
    NonePathException,
    NotExistingPathException,
)
from path.validator.path_validator import (
    NonePathValidator,
)

from path.provider.path_provider import CliPathProvider
from tests.fake_path_validator import (
    FakeDirectoryPathValidator,
    FakeExistingPathValidator,
)


# todo: review following TestCliArgumentsPathProvider
class TestCliPathProvider(unittest.TestCase):
    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(path="/home/course/path"),
    )
    def test_get(self, mock_parse_args):
        provider = CliPathProvider()

        path = provider.get()

        self.assertEqual(path, "/home/course/path")

    @patch(
        "argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(path=None)
    )
    def test_get_with_none(self, mock_parse_args):
        provider = CliPathProvider()

        path = provider.get()

        self.assertIsNone(path)


class TestPathManager(unittest.TestCase):
    def setUp(self):
        self.provider = MagicMock()
        self.provider.get.return_value = "directory/for/tests/"
        none_path_validator = NonePathValidator()
        existing_path_validator = MagicMock()
        existing_path_validator.validate.side_effect = (
            FakeExistingPathValidator.validate
        )
        directory_path_validator = MagicMock()
        directory_path_validator.validate.side_effect = (
            FakeDirectoryPathValidator.validate
        )
        validators = [
            none_path_validator,
            existing_path_validator,
            directory_path_validator,
        ]
        validator_manager = ValidatorManager[str](validators)
        self.path_manager = PathManager(self.provider, validator_manager)

    def test_get(self):
        actual = self.path_manager.get()

        expected = "directory/for/tests/"
        self.assertEqual(actual, expected, "The actual path isn't the same as expected")

    def test_get_with_none(self):
        self.provider.get.return_value = None

        with self.assertRaises(NonePathException):
            self.path_manager.get()

    def test_get_with_not_existing_path(self):
        self.provider.get.return_value = "not_existing_path"

        with self.assertRaises(NotExistingPathException):
            self.path_manager.get()

    def test_get_with_non_directory_path(self):
        self.provider.get.return_value = "directory/for/tests/file2"

        with self.assertRaises(NonDirectoryPathException):
            self.path_manager.get()
