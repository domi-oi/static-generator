from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str):

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block[:3] == "```" and block[:-3]:
        return BlockType.CODE
    if block[0] == ">":
        block_split = block.split("\n")
        quote = False
        for blocks in block_split:
            if blocks[0] == ">":
                quote = True
            else:
                quote = False
        if quote:
            return BlockType.QUOTE
    if block[:2] == "- ":
        block_split = block.split("\n")
        unordered = False
        for blocks in block_split:
            if blocks[:2] == "- ":
                unordered = True
        if unordered:
            return BlockType.UNORDERED_LIST
    if block[:2] == "1.":
        block_split = block.split("\n")
        counter = 1
        for blocks in block_split:
            if blocks[:2] == f"{counter}.":
                counter += 1
        if counter == len(block_split)+1:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH