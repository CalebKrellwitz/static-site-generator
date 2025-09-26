import re

from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ORDERED_LIST = "ordered list"
    UNORDERED_LIST = "unordered list"

def block_to_block_type(block):
    if re.match(r"#{1,6} ", block):
        return BlockType.HEADING
    elif re.fullmatch(r"```[\s\S]*```", block):
        return BlockType.CODE
    elif re.fullmatch(r"(^>.*\n)*(^>.*)", block, re.M):
        return BlockType.QUOTE
    elif re.fullmatch(r"(^- .*\n)*(^- .*)", block, re.M):
        return BlockType.UNORDERED_LIST
    elif block[0:3] == "1. ":
        lines = block.split('\n')
        for i in range(len(lines)):
            if ' ' not in lines[i]:
                return BlockType.PARAGRAPH
            prefix, line = lines[i].split(' ', maxsplit=1)
            if prefix != f"{i + 1}.":
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip() != ""]

if __name__ == "__main__":
    test()
