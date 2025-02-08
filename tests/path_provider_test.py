from abc import ABC
import argparse
import unittest
from unittest.mock import patch
from base.validator import ValidatorManager
from path.provider.path_provider import IPathProvider, PathManager
from path.validator.path_exception import (
    NonDirectoryPathException,
    NonePathException,
    NotExistingPathException,
)
from path.validator.path_validator import (
    NonePathValidator,
)

from path.provider.path_provider import CliPathProvider
from tests.path_validator_test import (
    FakeNonDirectoryPathValidator,
    FakeNotExistingPathValidator,
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
        self.provider = FakeCliPathProvider(FakeGoodPathStrategy())
        none_path_validator = NonePathValidator()
        self.not_existing_path_validator = FakeNotExistingPathValidator()
        self.non_directory_path_validator = FakeNonDirectoryPathValidator()
        validators = [
            none_path_validator,
            self.not_existing_path_validator,
            self.non_directory_path_validator,
        ]
        validator_manager = ValidatorManager[str](validators)
        self.path_manager = PathManager(self.provider, validator_manager)

    def test_get(self):
        self.provider.set_strategy(FakeGoodPathStrategy())

        actual = self.path_manager.get()

        expected = "directory/for/tests/"
        self.assertEqual(actual, expected, "The actual path isn't the same as expected")

    def test_get_with_none(self):
        self.provider.set_strategy(FakeNoneStrategy())

        with self.assertRaises(NonePathException):
            self.path_manager.get()

    def test_get_with_not_existing_path(self):
        self.not_existing_path_validator.existing_path_dictionary = {
            self.provider.get(): False
        }

        with self.assertRaises(NotExistingPathException):
            self.path_manager.get()

    def test_get_with_non_directory_path(self):
        self.non_directory_path_validator.update_directories(
            {self.provider.get(): False}
        )

        with self.assertRaises(NonDirectoryPathException):
            self.path_manager.get()


class FakeCliPathStrategy(IPathProvider, ABC):
    def get(self):
        pass


class FakeGoodPathStrategy(FakeCliPathStrategy):
    def get(self):
        return "directory/for/tests/"


class FakeNoneStrategy(FakeCliPathStrategy):
    def get(self):
        return None


class FakeCliPathProvider(IPathProvider):
    def __init__(self, strategy: FakeCliPathStrategy = None):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def get(self):
        return self.strategy.get()
