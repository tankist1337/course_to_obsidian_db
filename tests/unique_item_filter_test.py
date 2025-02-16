import unittest

from directory.unique_item_filter import StringUniqueItemFilter


class TestStringUniqueItemFilter(unittest.TestCase):
    def setUp(self):
        self.unique_item_filter = StringUniqueItemFilter()

    def test_filter_without_duplicates(self):
        items = ["item1", "item2", "item3"]

        filtered_items = self.unique_item_filter.filter(items)

        expected_list = items
        self.assertListEqual(
            filtered_items, expected_list, "Filtered items aren't as expected"
        )

    def test_filter_with_duplicates(self):
        items = ["item1", "item2", "item1", "item1", "item3", "item2", "item1", "item4"]

        filtered_items = self.unique_item_filter.filter(items)

        expected_list = ["item1", "item2", "item3", "item4"]
        self.assertListEqual(
            filtered_items, expected_list, "Filtered items aren't as expected"
        )

    def test_filter_all_duplicates(self):
        items = ["item", "item", "item", "item", "item"]

        filtered_items = self.unique_item_filter.filter(items)

        expected_list = ["item"]
        self.assertListEqual(
            filtered_items, expected_list, "Filtered items aren't as expected"
        )

    def test_filter_with_empty_items(self):
        items = []

        filtered_items = self.unique_item_filter.filter(items)

        expected_list = []
        self.assertListEqual(
            filtered_items, expected_list, "Filtered items must be empty"
        )
