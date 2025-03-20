import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)
        
    def test_eq_url(self):
        node1 = TextNode("This is a link", TextType.LINK, 'https://boot.dev')
        node2 = TextNode("This is a link", TextType.LINK, 'https://boot.dev')
        self.assertEqual(node1, node2)
    
    def test_ne_text(self):
        node1 = TextNode("This is a link!", TextType.LINK, 'https://boot.dev')
        node2 = TextNode("This is a link", TextType.LINK, 'https://boot.dev')
        self.assertNotEqual(node1, node2)
    
    def test_ne_type(self):
        node1 = TextNode("This is a link", TextType.LINK, 'https://boot.dev')
        node2 = TextNode("This is a link", TextType.IMAGE, 'https://boot.dev')
        self.assertNotEqual(node1, node2)
        
    def test_ne_url(self):
        node1 = TextNode("This is a link", TextType.IMAGE, 'https://boot.dev')
        node2 = TextNode("This is a link", TextType.IMAGE, 'https://boot.dev/')
        self.assertNotEqual(node1, node2)
    
    def test_ne_url_none(self):
        node1 = TextNode("This is a link", TextType.IMAGE)
        node2 = TextNode("This is a link", TextType.IMAGE, 'https://boot.dev/')
        self.assertNotEqual(node1, node2)
        
if __name__ == "__main__":
    unittest.main()
        