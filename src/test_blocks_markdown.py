import unittest
from blocks_markdown import BlockType, block_to_block_type, markdown_to_blocks, markdown_to_html_node


class TestBlocksMarkdown(unittest.TestCase):
    def test_markdown_to_blocks_empty(self):
        actual = markdown_to_blocks("")
        expected = []
        self.assertListEqual(actual, expected)

    def test_markdown_to_blocks_none(self):
        actual = markdown_to_blocks(None)
        expected = []
        self.assertListEqual(actual, expected)

    def test_markdown_to_blocks_valid(self):
        actual = markdown_to_blocks("""
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
""")
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

    def test_ordered_list(self):
        self.assertEqual(
            BlockType.ORDERED_LIST,
            block_to_block_type("1. line one\n2. line two\n3. line three"),
        )

    def test_ordered_list_malformed(self):
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type("1. line one\n2 line two\n3. line three"),
        )

    def test_unordered_list(self):
        self.assertEqual(
            BlockType.UNORDERED_LIST,
            block_to_block_type("- line one\n- line two\n- line three"),
        )

    def test_unordered_list_malformed(self):
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type("- line one\n line two\n- line three"),
        )

    def test_paragraph(self):
            md = """
This is **bolded** paragraph
text in a p
tag here

"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
            )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()
