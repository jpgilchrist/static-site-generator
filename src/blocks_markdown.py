import re
from enum import Enum

from inline_markdown import text_to_textnodes
from parentnode import ParentNode
from textnode import text_node_to_html_node, TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    if markdown is None:
        return []

    return list(
        filter(lambda x: x != "", map(lambda x: x.strip(), markdown.split("\n\n")))
    )


def block_to_block_type(block: str):
    lines = block.splitlines()

    if len(lines) == 1 and re.match(r"^#{1,6}\s.+$", lines[0]):
        return BlockType.HEADING

    if lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    if block.startswith("1. "):
        for i, line in enumerate(lines):
            if not line.startswith(f"{i + 1}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return list(map(text_node_to_html_node, text_nodes))


def code_to_html_node(block: str):
    text = block.strip('```').lstrip()
    text_node = TextNode(text, TextType.CODE)
    html_node = text_node_to_html_node(text_node)
    return ParentNode("pre", children=[html_node])


def paragraph_to_html_node(block: str):
    html_nodes = text_to_children(block.replace("\n", " "))
    return ParentNode("p", children=html_nodes)


def heading_to_html_node(block: str):
    heading_level = len(block) - len(block.lstrip("#"))
    return ParentNode(f"h{heading_level}", children=text_to_children(block[heading_level + 1:]))


def quote_to_html_node(block: str):
    quote_text = ' '.join(map(lambda x: x.lstrip("> "), block.splitlines()))
    return ParentNode("blockquote", children=text_to_children(quote_text))


def ordered_list_to_html_node(block: str):
    list_items = []
    for i, line in enumerate(block.splitlines()):
        list_items.append(ParentNode("li", children=text_to_children(line.lstrip(f"{i + 1}. "))))
    return ParentNode("ol", children=list_items)


def unordered_list_to_html_node(block: str):
    list_items = []
    for i, line in enumerate(block.splitlines()):
        list_items.append(ParentNode("li", children=text_to_children(line.lstrip("- "))))
    return ParentNode("ul", children=list_items)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.CODE:
                children.append(code_to_html_node(block))
            case BlockType.PARAGRAPH:
                children.append(paragraph_to_html_node(block))
            case BlockType.HEADING:
                children.append(heading_to_html_node(block))
            case BlockType.QUOTE:
                children.append(quote_to_html_node(block))
            case BlockType.ORDERED_LIST:
                children.append(ordered_list_to_html_node(block))
            case BlockType.UNORDERED_LIST:
                children.append(unordered_list_to_html_node(block))
            case _:
                raise Exception(f"Unknown block type: {block_type}")

    root_node = ParentNode("div", children=children)

    return root_node
