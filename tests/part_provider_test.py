import unittest
from unittest.mock import MagicMock

from entry.entry import Directory
from part.part import Part
from part.part_converter import PartConverter
from part.part_provider import PartProvider


class TestPartProvider(unittest.TestCase):
    def setUp(self):
        path_provider = MagicMock()
        path_provider.get.return_value = "directory/for/tests/"

        self.directory_provider = MagicMock()
        self.directory_provider.get.return_value = {
            Directory(
                name="directory1",
                directory_path="directory/for/tests/",
                path="directory/for/tests/directory1",
            )
        }

        part_converter = PartConverter()
        self.part_provider = PartProvider(
            path_provider=path_provider,
            directory_provider=self.directory_provider,
            converter=part_converter,
        )

    def test_get(self):
        parts = self.part_provider.get()

        expected_parts = {
            Part(
                directory=Directory(
                    name="directory1",
                    directory_path="directory/for/tests/",
                    path="directory/for/tests/directory1",
                ),
            )
        }
        self.assertEqual(
            parts,
            expected_parts,
            "The parts aren't the same as expected",
        )

    def test_get_no_parts(self):
        self.directory_provider.get.return_value = set()

        parts = self.part_provider.get()

        self.assertEqual(len(parts), 0, "It must be empty")
