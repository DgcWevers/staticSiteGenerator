# from enum import Enum
# import re


# def markdown_to_blocks(markdown):
#     block_strings = []
#     block_strings = markdown.split('\n\n')
#     block_strings[:] = [x for x in block_strings if x]
#     block_strings[:] = [x.strip('\n') for x in block_strings]
#     return block_strings

# class BlockType(Enum):
#     PARAGRAPH = 'paragraph'
#     HEADING = 'heading'
#     CODE = 'code'
#     QUOTE = 'quote'
#     UNORDERED_LIST = 'unordered_list'
#     ORDERED_LIST = 'ordered_list'

# def block_to_block_type(block):
#     if re.match(r'\#{1,6}\s\w', block):
#         return BlockType.HEADING
#     elif block.strip().startswith("```") and block.strip().endswith("```"):
#         return BlockType.CODE
#     elif block.startswith('>'):
#         return BlockType.QUOTE
#     lines = [ln.lstrip() for ln in block.splitlines() if ln.strip()]
#     if lines and all(ln.startswith('- ') for ln in lines):
#         return BlockType.UNORDERED_LIST
#     if lines and all(f"{i}. " == ln[:len(f"{i}. ")] for i, ln in enumerate(lines, 1)):
#         return BlockType.ORDERED_LIST
#     return BlockType.PARAGRAPH

# def get_block_text(block, blocktype):
#     if blocktype == BlockType.HEADING:
#         while block.startswith('#'):
#             block = block.lstrip('#')
#         return block.strip()
#     elif blocktype == BlockType.CODE:
#         while block.startswith('`'):
#             block = block.lstrip('`')
#         while block.endswith('`'):
#             block = block.rstrip('`')
#         return block.strip()
#     elif blocktype == BlockType.QUOTE:
#         return block.lstrip('> ').strip()
#     else:
#         return block

# def get_heading_tag(block):
#     if block.startswith('# '):
#         return 'h1'
#     elif block.startswith('## '):
#         return 'h2'
#     elif block.startswith('### '):
#         return 'h3'
#     elif block.startswith('#### '):
#         return 'h4'
#     elif block.startswith('##### '):
#         return 'h5'
#     elif block.startswith('###### '):
#         return 'h6'
#     else:
#         raise KeyError("Error: wrong number of '#' at the start of the block. Is it a header?")

# python
import re
import textwrap
from enum import Enum

def markdown_to_blocks(markdown):
    lines = markdown.splitlines()
    blocks = []
    buf = []
    in_code = False
    for line in lines:
        if line.strip().startswith("```"):
            if not in_code:
                # starting code fence
                in_code = True
                buf = [line]
            else:
                # ending code fence
                buf.append(line)
                blocks.append("\n".join(buf))
                buf = []
                in_code = False
            continue
        if in_code:
            buf.append(line)
            continue
        # outside code: blank line separates blocks
        if line.strip() == "":
            if buf:
                blocks.append("\n".join(buf))
                buf = []
        else:
            buf.append(line)
    if buf:
        blocks.append("\n".join(buf))
    # drop empty blocks
    return [b for b in blocks if b.strip()]

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def block_to_block_type(block):
    s = block.lstrip()
    if re.match(r'#{1,6}\s+\S', s):
        return BlockType.HEADING
    if s.startswith("```") and s.rstrip().endswith("```"):
        return BlockType.CODE
    if s.startswith('>'):
        return BlockType.QUOTE
    lines = [ln.lstrip() for ln in block.splitlines() if ln.strip()]
    if lines and all(ln.startswith('- ') for ln in lines):
        return BlockType.UNORDERED_LIST
    if lines and all(re.match(rf'^{i}\.\s+', ln) for i, ln in enumerate(lines, 1)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def get_block_text(block, blocktype):
    if blocktype == BlockType.HEADING:
        return re.sub(r'^#{1,6}\s+', '', block.lstrip()).strip()

    if blocktype == BlockType.CODE:
        lines = block.splitlines()
        if len(lines) == 1:
            s = lines[0].strip()
            if s.startswith("```") and s.endswith("```") and len(s) >= 6:
                return s[3:-3].strip()
            return block
        # multi-line fenced code
        if lines[0].strip().startswith("```") and lines[-1].strip().startswith("```"):
            inner = "\n".join(lines[1:-1])
            inner = textwrap.dedent(inner)
            return inner if inner.endswith("\n") else inner + "\n"
        return block

    if blocktype == BlockType.QUOTE:
        cleaned = "\n".join(re.sub(r'^\s*>\s?', '', ln) for ln in block.splitlines())
        return cleaned.strip()

    return block

def get_heading_tag(block):
    s = block.lstrip()
    hashes = len(s) - len(s.lstrip('#'))
    if 1 <= hashes <= 6 and s[hashes:hashes+1] == ' ':
        return f'h{hashes}'
    raise KeyError("Error: wrong number of '#' at the start of the block. Is it a header?")