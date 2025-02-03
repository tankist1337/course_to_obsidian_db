import unittest

from entry.separator_provider import LinuxSeparatorProvider


class TestLinuxSeparatorProvider(unittest.TestCase):
    def test_get(self):
        provider = LinuxSeparatorProvider()

        separator = provider.get()

        self.assertEqual(separator, "/", "The separator isn't as expected")
