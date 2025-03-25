import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_eq_url(self):
        node1 = TextNode("This is a link", TextType.LINK, "https://boot.dev")
        node2 = TextNode("This is a link", TextType.LINK, "https://boot.dev")
        self.assertEqual(node1, node2)

    def test_ne_text(self):
        node1 = TextNode("This is a link!", TextType.LINK, "https://boot.dev")
        node2 = TextNode("This is a link", TextType.LINK, "https://boot.dev")
        self.assertNotEqual(node1, node2)

    def test_ne_type(self):
        node1 = TextNode("This is a link", TextType.LINK, "https://boot.dev")
        node2 = TextNode("This is a link", TextType.IMAGE, "https://boot.dev")
        self.assertNotEqual(node1, node2)

    def test_ne_url(self):
        node1 = TextNode("This is a link", TextType.IMAGE, "https://boot.dev")
        node2 = TextNode("This is a link", TextType.IMAGE, "https://boot.dev/")
        self.assertNotEqual(node1, node2)

    def test_ne_url_none(self):
        node1 = TextNode("This is a link", TextType.IMAGE)
        node2 = TextNode("This is a link", TextType.IMAGE, "https://boot.dev/")
        self.assertNotEqual(node1, node2)


class TestTextNodeToHTMLNode(unittest.TestCase):

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


if __name__ == "__main__":
    unittest.main()
