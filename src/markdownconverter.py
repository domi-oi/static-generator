from textnode import TextNode, TextType, text_node_to_html_node
import re 
from blocktype import block_to_block_type, BlockType
from htmlnode import HTMLNode, ParentNode, LeafNode

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        text_from_old = old_node.text
        get_images = extract_markdown_images(text_from_old)
        
        for image, link in get_images:  
            split_nodes = text_from_old.split(f"![{image}]({link})", 1)
            if len(split_nodes) == 0:
                continue
            if split_nodes[0] != "":
                new_nodes.append(TextNode(split_nodes[0], TextType.TEXT))
            new_nodes.append(TextNode(image, TextType.IMAGE, link))
            text_from_old = split_nodes[1]
        if text_from_old:
            new_nodes.append(TextNode(text_from_old, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        text_from_old = old_node.text
        get_link = extract_markdown_links(text_from_old)
        
        for alt, link in get_link:  
            split_nodes = text_from_old.split(f"[{alt}]({link})", 1)
            if len(split_nodes) == 0:
                continue
            if split_nodes[0] != "":
                new_nodes.append(TextNode(split_nodes[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, link))
            text_from_old = split_nodes[1]
        if text_from_old:
            new_nodes.append(TextNode(text_from_old, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    #(!\[[a-z]*[A-Z]*\])(\(https:\/\/\w\))

    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return (matches)

    

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return (matches)


def text_to_textnodes(text):

    old_nodes = [TextNode(text, TextType.TEXT)]
    old_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
    old_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
    old_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
    old_nodes = split_nodes_image(old_nodes)
    old_nodes = split_nodes_link(old_nodes) 

    return old_nodes

def markdown_to_blocks(markdown) -> list[str]:
    split_blocks = markdown.split("\n\n")
    extracted_blocks = []
    for block in split_blocks:
        block = block.strip()
        if block == "" or block  == " ":
            continue
        extracted_blocks.append(block)
    return extracted_blocks
        

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        node = create_html_node(block, block_type)
        nodes.append(node)
    return ParentNode("div", nodes)


def create_html_node(block, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            split_block = block.split("\n")
            rejoined = " ".join(split_block)
            node = ParentNode("p", text_to_children(rejoined))
            return node
        case BlockType.HEADING:
            heading_count = block[:7].count("#")
            stripped = block.lstrip("# ")
            node = ParentNode(f"h{heading_count}", text_to_children(stripped))
            return node
        case BlockType.QUOTE:
#            region split_block = block.split(">")
#            for split in block:
#                split = split.lstrip(">")
#            rejoined = " ".join(split_block)
#            rejoined_split = rejoined.split("\n")
#            final = " ".join(rejoined_split)
#            print(f"\n\n{rejoined}")
#            node = ParentNode("blockquote", text_to_children(rejoined))

            lines = block.split("\n")
            new_lines = []
            for line in lines:
                if not line.startswith(">"):
                    raise ValueError("invalid quote block")
                new_lines.append(line.lstrip(">").strip())
            content = " ".join(new_lines)
            node = ParentNode("blockquote", text_to_children(content))
            return node
        case BlockType.UNORDERED_LIST:
            split_block = block.split("\n")
            html_nodes = []
            for split in split_block:
                split = split[2:]
                children = text_to_children(split.strip())
                html_nodes.append(ParentNode("li", children))
            node = ParentNode("ul", html_nodes)
            return node
        case BlockType.ORDERED_LIST:
            split_block = block.split("\n")
            html_nodes = []
            for split in split_block:
                split = split[2:]
                children = text_to_children(split.strip())
                html_nodes.append(ParentNode("li", children))
            node = ParentNode("ol", html_nodes)
            return node
        case BlockType.CODE:
            block = block[4:-3]
            smolnode = LeafNode("code", block)
            node = ParentNode("pre", [smolnode])
            return node
        case _:
            raise Exception("No BlockType detected!")


def text_to_children(text):
    nodes = text_to_textnodes(text)
    converted_nodes = []
    for node in nodes:
        converted_nodes.append(text_node_to_html_node(node))

    return converted_nodes

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        if block.startswith("# "):
            temp_block = block.lstrip("#")
            temp_block = temp_block.strip()
            return temp_block
    raise Exception("no head?")