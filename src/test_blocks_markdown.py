import unittest
from blocks_markdown import BlockType, block_to_block_type, markdown_to_blocks


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

    def test_heading_one(self):
        expected = BlockType.HEADING
        actual = block_to_block_type("# Heading 1")
        self.assertEqual(actual, expected)

    def test_heading_two(self):
        expected = BlockType.HEADING
        self.assertEqual(block_to_block_type("## Heading 2"), expected)

    def test_heading_three(self):
        expected = BlockType.HEADING
        self.assertEqual(block_to_block_type("### Heading 3"), expected)

    def test_heading_four(self):
        expected = BlockType.HEADING
        self.assertEqual(block_to_block_type("#### Heading 4"), expected)

    def test_heading_five(self):
        expected = BlockType.HEADING
        self.assertEqual(block_to_block_type("##### Heading 5"), expected)

    def test_heading_six(self):
        expected = BlockType.HEADING
        self.assertEqual(block_to_block_type("###### Heading 6"), expected)

    def test_heading_seven(self):
        expected = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type("####### Heading 7"), expected)

    def test_code_single_line(self):
        self.assertEqual(BlockType.CODE, block_to_block_type("```asdf```"))

    def test_code_multi_line(self):
        self.assertEqual(
            BlockType.CODE,
            block_to_block_type("```\nline one\nline two\nline three\n```"),
        )

    def test_code_malformed(self):
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type(
                "```\nline one\nline two\nline three\n```something after"
            ),
        )

    def test_quote(self):
        self.assertEqual(
            BlockType.QUOTE, block_to_block_type("> line one\n> line two\n> line three")
        )

    def test_quote_malformed(self):
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type("> line one\n line two\n> line three"),
        )

    def test_orderd_list(self):
        self.assertEqual(
            BlockType.ORDERED_LIST,
            block_to_block_type("1. line one\n2. line two\n3. line three"),
        )

    def test_ordered_list_malformed(self):
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type("1. line one\n2 line two\n3. line three"),
        )

    def test_unorderd_list(self):
        self.assertEqual(
            BlockType.UNORDERED_LIST,
            block_to_block_type("- line one\n- line two\n- line three"),
        )

    def test_unordered_list_malformed(self):
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type("- line one\n line two\n- line three"),
        )


if __name__ == "__main__":
    unittest.main()
