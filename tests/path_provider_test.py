import argparse
import unittest
from unittest.mock import patch

from path.provider.path_provider import CliPathProvider


# todo: review following TestCliArgumentsPathProvider
class TestCliPathProvider(unittest.TestCase):
    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(path="/home/course/path"),
    )
    def test_get_path(self, mock_parse_args):
        provider = CliPathProvider()

        path = provider.get_path()

        self.assertEqual(path, "/home/course/path")

    @patch(
        "argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(path=None)
    )
    def test_get_path_with_none(self, mock_parse_args):
        provider = CliPathProvider()

        path = provider.get_path()

        self.assertIsNone(path)
