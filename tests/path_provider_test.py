import argparse
import unittest
from unittest.mock import patch
from base.validator import ValidatorManager
from path.provider.path_provider import IPathProvider, PathManager
from path.validator.path_validator import (
    NonePathValidator,
    NonDirectoryPathValidator,
    NotExistingPathValidator,
)

from path.provider.path_provider import CliPathProvider


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
    def test_get(self):
        provider = FakeCliPathProvider()
        validators = [
            NonePathValidator(),
            NotExistingPathValidator(),
            NonDirectoryPathValidator(),
        ]
        validator_manager = ValidatorManager[str](validators)
        path_manager = PathManager(provider, validator_manager)

        path = path_manager.get()

        self.assertEqual(path, "directory/for/tests/")

    def test_get_with_none(self):
        self.fail()

    def test_get_with_not_existing_path(self):
        self.fail()

    def test_get_with_non_directory_path(self):
        self.fail()


# Add strategy None, Not existing path, non directory path
class FakeCliPathProvider(IPathProvider):
    def get(self) -> str:
        return "directory/for/tests/"
