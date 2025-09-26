import re
from textnode import TextNode, TextType

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue
        
        split_text = old_node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception("missing closing delimiter; invalid Markdown syntax")

        within_delimiter = False
        for sub_str in split_text:
            new_nodes.append(TextNode(sub_str, text_type if within_delimiter else TextType.PLAIN))
            within_delimiter = not within_delimiter

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        images = extract_markdown_images(remaining_text)
        for image in images:
            current_text, remaining_text = remaining_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(current_text) != 0:
                new_nodes.append(TextNode(current_text, TextType.PLAIN))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))

        if len(remaining_text) != 0:
            new_nodes.append(TextNode(remaining_text, TextType.PLAIN))
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        links = extract_markdown_links(remaining_text)
        for link in links:
            current_text, remaining_text = remaining_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(current_text) != 0:
                new_nodes.append(TextNode(current_text, TextType.PLAIN))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

        if len(remaining_text) != 0:
            new_nodes.append(TextNode(remaining_text, TextType.PLAIN))
    
    return new_nodes

def text_to_textnodes(text):
    text_nodes = [TextNode(text, TextType.PLAIN)]
    text_nodes = split_nodes_delimiter(text_nodes, '**', TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, '_', TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, '`', TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes
