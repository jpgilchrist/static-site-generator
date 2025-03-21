import unittest

from utils import text_node_to_html_node, split_nodes_delimiter
from textnode import TextNode, TextType


class TestUtils(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode(
            "boot dev logo",
            TextType.IMAGE,
            url="https://www.boot.dev/img/bootdev-logo-full-small.webp",
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["alt"], "boot dev logo")
        self.assertEqual(
            html_node.props["src"],
            "https://www.boot.dev/img/bootdev-logo-full-small.webp",
        )

    def test_image(self):
        node = TextNode("boot dev link", TextType.LINK, url="https://www.boot.dev/")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "boot dev link")
        self.assertEqual(html_node.props["href"], "https://www.boot.dev/")

    def test_split_delim(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_delim_multiple(self):
        node = TextNode(
            "This is text with a `code block` word and `another code block` there.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word and ", TextType.TEXT),
            TextNode("another code block", TextType.CODE),
            TextNode(" there.", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_delim_ending(self):
        node = TextNode("This is text with a `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_delim_beginning(self):
        node = TextNode("`code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("code block", TextType.CODE)]
        self.assertEqual(new_nodes, expected)

    def test_split_delim_stray_delimeter(self):
        node = TextNode("no code block` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("no code block` here", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_split_delim_bold(self):
        node = TextNode(
            "This is text with a **code block** word and **another code block** there.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.BOLD),
            TextNode(" word and ", TextType.TEXT),
            TextNode("another code block", TextType.BOLD),
            TextNode(" there.", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_delim_non_text(self):
        old_nodes = [TextNode("already a code block", TextType.CODE)]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(old_nodes, new_nodes)

    def test_split_delim_multiple_nodes(self):
        old_nodes = [
            TextNode(
                "This is text with a `code block` word and `another code block` there.",
                TextType.TEXT,
            ),
            TextNode("`code block`", TextType.TEXT),
            TextNode("already a code block", TextType.CODE),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word and ", TextType.TEXT),
            TextNode("another code block", TextType.CODE),
            TextNode(" there.", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode("already a code block", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()
