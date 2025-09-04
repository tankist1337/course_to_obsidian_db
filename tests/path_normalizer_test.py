import unittest

from entry.path_normalizer import DirectoryPathNormalizer
from entry.separator_provider import LinuxSeparatorProvider


class TestPathNormalizer(unittest.TestCase):
    def setUp(self):
        separator_provider = LinuxSeparatorProvider()
        self.normalizer = DirectoryPathNormalizer(separator_provider)

    def test_ensure_trailing_separator_when_available(self):
        directory_path = "directory/for/tests/"

        normalized_path = self.normalizer.ensure_trailing_separator(directory_path)

        expected = "directory/for/tests/"
        self.assertEqual(normalized_path, expected, "The path isn't as expected")

    def test_ensure_trailing_separator_when_absent(self):
        directory_path = "directory/for/tests"

        normalized_path = self.normalizer.ensure_trailing_separator(directory_path)

        expected = "directory/for/tests/"
        self.assertEqual(normalized_path, expected, "The path isn't as expected")
