import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.maxDiff = None
        
    def test_should_raise_error_with_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, None, None).to_html()

    def test_should_raise_error_with_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("p", None, None).to_html()

    def test_should_raise_error_with_empty_children(self):
        with self.assertRaises(ValueError):
            ParentNode("p", [], None).to_html()

    def test_should_handle_leaf_nodes(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_should_handle_props_through_tree(self):
        node = ParentNode(
            "div",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                ParentNode(
                    "div",
                    [LeafNode("span", "Hello world!", props={"style": "font-size: 2rem"})],
                    props={
                        "class": "inner-div",
                        "style": "margin-top: 8px"
                    }
                ),
            ],
            props={
                "id": "my-parent-div",
                "class": "parent-div",
                "style": "margin: 8px;",
            },
        )
        self.assertEqual(
            node.to_html(),
            '<div id="my-parent-div" class="parent-div" style="margin: 8px;"><b>Bold text</b>Normal text<i>italic text</i>Normal text<div class="inner-div" style="margin-top: 8px"><span style="font-size: 2rem">Hello world!</span></div></div>',
        )
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
