from textnode import TextNode, TextType

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
