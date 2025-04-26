import re
from enum import Enum

from htmlnode import (
    ParentNode,
    LeafNode,
)
from markdown_inline import (
    text_to_textnodes,
)
from textnode import (
    text_node_to_html_node,
)


class BlockType(Enum):
    PARAGRAPH = "PARAGRAPH"
    HEADING = "HEADING"
    CODE = "CODE"
    QUOTE = "QUOTE"
    UNORDERED_LIST = "UNORDERED_LIST"
    ORDERED_LIST = "ORDERED_LIST"


def markdown_to_blocks(markdown):
    """Split a markdown document into blocks of text"""
    blocks = []
    for block in markdown.split("\n\n"):
        block = block.strip()
        if len(block) > 0:
            blocks.append(block)
    return blocks


def block_to_block_type(block):
    """Determine the block type of a block of text"""
    heading_pattern = r"^#{1,6}\s+"
    if re.match(heading_pattern, block):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    is_ordered_list = True
    for idx, line in enumerate(lines):
        if not line.startswith(f"{idx + 1}. "):
            is_ordered_list = False
            break
    if is_ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    """Convert a markdown document to a single HTMLNode"""
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        tag = block_type_to_html_tag(block_type, block)
        text = normalize_text(block, block_type)

        match block_type:
            case BlockType.CODE:
                children = [LeafNode("code", text)]
            case BlockType.ORDERED_LIST | BlockType.UNORDERED_LIST:
                children = text_to_list_items(text)
            case _:
                children = text_to_children(text)

        block_nodes.append(ParentNode(tag, children))

    return ParentNode("div", block_nodes)


def text_to_children(text):
    """Converts plain text to HTMLNodes"""
    text_nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return html_nodes


def text_to_list_items(text):
    """Convert a list-type block of text into its child nodes"""
    line_children = [text_to_children(line) for line in text.split("\n")]
    return [ParentNode("li", children) for children in line_children]


def normalize_text(text, block_type=None):
    """Normalize block text, removing any block-level markdown"""
    match block_type:
        case BlockType.CODE:
            return text[4:-3]
        case BlockType.ORDERED_LIST | BlockType.UNORDERED_LIST | BlockType.QUOTE:
            return "\n".join(
                [line.split(" ", 1)[1].strip() for line in text.split("\n")]
            )
        case BlockType.HEADING:
            return text.split(" ", 1)[1].strip()
        case _:
            return " ".join(text.split("\n")).strip()


def block_type_to_html_tag(block_type, text):
    """Returns the HTML tag corresponding with the block type"""
    match block_type:
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.HEADING:
            count = len(text.split(" ")[0])
            return f"h{count}"
        case BlockType.CODE:
            return "pre"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"
