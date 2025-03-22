import re
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


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            new_nodes.append(old_node)
        else:
            text = old_node.text
            for alt, url in images:
                sections = text.split(f"![{alt}]({url})", 1)
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                text = sections[1]
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            new_nodes.append(old_node)
        else:
            text = old_node.text
            for alt, url in links:
                sections = text.split(f"[{alt}]({url})", 1)
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(alt, TextType.LINK, url))
                text = sections[1]
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"(?<=\!)\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)


def text_to_text_nodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    for text_type in TextType:
        delimiter = text_type.get_delimiter()
        if delimiter is not None:
            nodes = split_nodes_delimiter(nodes, delimiter, text_type)
    
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_links(nodes)
    
    return nodes
        