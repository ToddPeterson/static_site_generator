import re

from textnode import (
    TextNode,
    TextType,
)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """Split a list of TextNode based on an inline delimiter"""
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError(f"Unmatched delimeter: {delimiter}")

        in_delimeter = True
        for part in sections:
            in_delimeter = not in_delimeter
            if len(part) == 0:
                continue
            node_type = text_type if in_delimeter else TextType.TEXT
            new_nodes.append(TextNode(part, node_type))
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        matches = extract_markdown_images(original_text)

        # For each img, add TextNodes for the text before the img, and the img itself
        # then update `original_text` to be the remaining text
        for match in matches:
            img_alt, img_link = match
            img_str = f"![{img_alt}]({img_link})"
            sections = original_text.split(img_str, 1)

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(img_alt, TextType.IMAGE, img_link))
            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        matches = extract_markdown_links(original_text)

        # For each link, add TextNodes for the text before the link, and the link itself
        # then update `original_text` to be the remaining text
        for match in matches:
            link_text, link_url = match
            link_str = f"[{link_text}]({link_url})"
            sections = original_text.split(link_str, 1)

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            original_text = sections[1]
        
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    """Convert text into TextNode's, finding any inline markdown"""
    if len(text) == 0:
        return []

    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

