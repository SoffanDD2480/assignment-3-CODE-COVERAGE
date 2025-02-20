"""Test suite to test the Internal class.

    For now, only _format(), get_input_dialog and get_embed functions are tested.
"""
import unittest

from discord import Embed

from bot.exts.utils.internal import Internal
from tests.helpers import MockBot


class TestInternal(unittest.TestCase):
    """Tests for Internal class."""

    def setUp(self) -> None:
        """Set up Internal class for testing."""
        self.embed = Embed()
        self.bot = MockBot()
        self.internal = Internal(self.bot)

    def test_format_no_input(self):
        """Test formatting with no output."""
        (_, out) = self.internal._format("", None)

        self.assertIsNone(out, None)

    def test_format_embed(self):
        """Test formatting with some output."""
        (res, out) = self.internal._format("", Embed())

        self.assertIsInstance(out, Embed)
        self.assertEqual(True, "Embed" in res)

    def test_get_input_dialog_empty_list(self):
        """Test getting the input dialog with empy list."""
        (res, out) = self.internal._format("", "")

        self.assertEqual(res, "In [0]: \nOut[0]: ")

    def test_get_input_dialog_return(self):
        """Test getting the input dialog with non-empy list, with a return row, removing the return keyword."""
        (res, out) = self.internal._format("test 1\nreturn hi", "")

        self.assertEqual(True, "return hi" not in res and "hi" in res)

    def test_get_prettified_dict(self):
        """Test getting a prettified dict."""
        (res, out) = self.internal._format("", {"10": [1, 2, 3], "20": 456, "30": 7.89})

        self.assertEqual(True, "{'10': [1, 2, 3], '20': 456, '30': 7.89}" in res)
        self.assertIsNone(out, None)

    def test_get_prettified_compact(self):
        """Test getting a compacted output"""

        (res, out) = self.internal._format("", "".join([f"Test {i}\n" for i in range(30)]))

        self.assertEqual(True, "Test 0" in res and "Test 15" not in res and "Test 29" in res)
