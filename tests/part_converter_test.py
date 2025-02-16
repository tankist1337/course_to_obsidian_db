import unittest

from entry.entry import Directory
from part.part import Part
from part.part_converter import PartConverter


class TestPartConverter(unittest.TestCase):
    def setUp(self):
        self.converter = PartConverter()

    def test_convert(self):
        directories = {
            Directory(
                name="directory1",
                directory_path="directory1/",
                path="directory1/directory1",
            ),
            Directory(
                name="directory2",
                directory_path="directory1/",
                path="directory1/directory2",
            ),
        }

        parts = self.converter.convert(directories)

        expected_parts = {
            Part(
                directory=Directory(
                    name="directory1",
                    directory_path="directory1/",
                    path="directory1/directory1",
                )
            ),
            Part(
                directory=Directory(
                    name="directory2",
                    directory_path="directory1/",
                    path="directory1/directory2",
                )
            ),
        }
        self.assertEqual(parts, expected_parts, "Parts aren't the same as expected")

    def test_convert_with_empty_directories(self):
        directories = set[Directory]()

        parts = self.converter.convert(directories)

        self.assertEqual(len(parts), 0, "There must be no parts")
