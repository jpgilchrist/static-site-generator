import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):

    def test_empty_props_to_html(self):
        node = HTMLNode()
        self.assertEqual("", node.props_to_html())

    def test_single_props_to_html(self):
        node = HTMLNode(props={"href": "https://boot.dev"})
        self.assertEqual(
            node.props_to_html(), ' href="https://boot.dev"'
        )

    def test_multiple_props_to_html(self):
        node = HTMLNode(props={"href": "https://boot.dev", "target": "_blank"})
        self.assertEqual(
            node.props_to_html(), ' href="https://boot.dev" target="_blank"'
        )


if __name__ == "__main__":
    unittest.main()
