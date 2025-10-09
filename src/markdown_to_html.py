# from blocks import markdown_to_blocks, block_to_block_type, BlockType, get_heading_tag, get_block_text
# from htmlnode import HTMLNode
# from nodestohtml import text_to_textnodes
# from textnode import text_node_to_html_node, TextNode, TextType
# from parentnode import ParentNode
# import re
# from leafnode import LeafNode

# def markdown_to_html_node(markdown):
#     blocks = markdown_to_blocks(markdown)
    
#     for block in blocks:
#         block_type = block_to_block_type(block)
#         htmlnodes = newHTMLNode(block, block_type)

#     parent = ParentNode('div', children=htmlnodes)
    
#     return parent


# def newHTMLNode(block, blocktype):
#     if blocktype == BlockType.PARAGRAPH:
#         children = text_to_children(block)
#         return ParentNode('p', children)
#     elif blocktype == BlockType.HEADING:
#         tag = get_heading_tag(block)
#         children = text_to_children(block)
#         return ParentNode(tag, children)
#     elif blocktype == BlockType.QUOTE:
#         children = text_to_children(block)
#         return ParentNode('blockquote', children)
#     elif blocktype == BlockType.UNORDERED_LIST:
#         children = unordered_list_children(block)
#         parent = ParentNode('ul', children)
#         return parent
#     elif blocktype == BlockType.ORDERED_LIST:
#         children = ordered_list_children(block)
#         return ParentNode('ol', children)
#     elif blocktype == BlockType.CODE:
#         node = text_node_to_html_node(TextNode(get_block_text(block), TextType.CODE))
#         return node
    

# def text_to_children(block):
#     textnodes = text_to_textnodes(block)
#     htmlnodes = []
#     if len(textnodes) > 1:
#         for i in textnodes:
#             htmlnodes.append(text_node_to_html_node(i))
#     else: htmlnodes.append(textnodes)
#     return htmlnodes

# def unordered_list_children(block):
#     children = []
#     for line in block.splitlines():
#         if line.startswith('- '):
#             children_nodes = text_to_children(line[2:].strip())
#             children.append(HTMLNode('li', children=children_nodes))
#     return children

# def ordered_list_children(block):
#     children = []
#     for line in block.splitlines():
#         if re.match(r'\d+ ', line):
#             line = re.sub('^\d+ ', '')
#             children_nodes = text_to_children(line)
#             children.append(HTMLNode('li', children=children_nodes))
#     return children


# python
from blocks import markdown_to_blocks, block_to_block_type, BlockType, get_heading_tag, get_block_text
from nodestohtml import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType
from parentnode import ParentNode
from leafnode import LeafNode
import re

# python
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        node = newHTMLNode(block, block_type)
        if node is not None:
            children.append(node)
    return ParentNode('div', children)

def newHTMLNode(block, blocktype):
    # python
    if blocktype == BlockType.CODE:
        raw = get_block_text(block, blocktype)  # inner lines only, preserve newlines and trailing \n
        return ParentNode('pre', [ParentNode('code', [LeafNode(None, raw)])])

    elif blocktype == BlockType.PARAGRAPH:
        text = normalize_inline_text(get_block_text(block, blocktype))
        if not text:
            return None
        return ParentNode('p', text_to_children(text))

    elif blocktype == BlockType.HEADING:
        tag = get_heading_tag(block)
        text = normalize_inline_text(get_block_text(block, blocktype))
        return ParentNode(tag, text_to_children(text))

    elif blocktype == BlockType.QUOTE:
        text = normalize_inline_text(get_block_text(block, blocktype))
        return ParentNode('blockquote', text_to_children(text))
    
    elif blocktype == BlockType.UNORDERED_LIST:
        return ParentNode('ul', unordered_list_children(block))
    elif blocktype == BlockType.ORDERED_LIST:
        return ParentNode('ol', ordered_list_children(block))
    # elif blocktype == BlockType.CODE:
    #     raw = get_block_text(block, blocktype)  # preserve newlines, no inline parsing
    #     code_leaf = LeafNode(None, raw)  # plain text inside <code>
    #     return ParentNode('pre', [ParentNode('code', [code_leaf])])
    else:
        text = get_block_text(block, blocktype).strip().replace("\n", " ")
        if not text:
            return None
        return ParentNode('p', text_to_children(text))

def text_to_children(text):
    return [text_node_to_html_node(tn) for tn in text_to_textnodes(text)]

def unordered_list_children(block):
    items = []
    for line in block.splitlines():
        s = line.lstrip()
        if s.startswith('- '):
            content = s[2:].strip()
            items.append(ParentNode('li', text_to_children(content)))
    return items

def ordered_list_children(block):
    items = []
    for line in block.splitlines():
        m = re.match(r'^\s*\d+\.\s+', line)
        if m:
            content = re.sub(r'^\s*\d+\.\s+', '', line).strip()
            items.append(ParentNode('li', text_to_children(content)))
    return items

def normalize_inline_text(s: str) -> str:
    # strip leading/trailing, replace any run of whitespace/newlines with a single space
    return re.sub(r'\s+', ' ', s.strip())