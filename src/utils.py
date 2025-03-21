from leafnode import LeafNode
from textnode import TextNode, TextType
from typing import List


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimeter: str, text_type: TextType
):
    new_nodes: List[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            sections = old_node.text.split(delimeter)
            num_sections = len(sections)
            if num_sections > 2:
                if num_sections % 2 == 0:
                    for i in range(num_sections - 2):
                        if sections[i] == "":
                            continue
                        if i % 2 == 0:
                            new_nodes.append(TextNode(sections[i], TextType.TEXT))
                        else:
                            new_nodes.append(TextNode(sections[i], text_type))
                    new_nodes.append(
                        TextNode(delimeter.join(sections[-2:]), TextType.TEXT)
                    )
                else:
                    for i in range(num_sections):
                        if sections[i] == "":
                            continue
                        if i % 2 == 0:
                            new_nodes.append(TextNode(sections[i], TextType.TEXT))
                        else:
                            new_nodes.append(TextNode(sections[i], text_type))
            else:
                new_nodes.append(TextNode(delimeter.join(sections), TextType.TEXT))
    return new_nodes
