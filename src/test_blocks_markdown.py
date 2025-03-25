import unittest
from blocks_markdown import markdown_to_blocks


class TestBlocksMardown(unittest.TestCase):
    def test_markdown_to_blocks_empty(self):
        input = ""
        actual = markdown_to_blocks(input)
        expected = []
        self.assertListEqual(actual, expected)

    def test_markdown_to_blocks_none(self):
        input = None
        actual = markdown_to_blocks(input)
        expected = []
        self.assertListEqual(actual, expected)

    def test_markdown_to_blocks_valid(self):
        input = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        actual = markdown_to_blocks(input)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]

        self.assertListEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
