import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode 
from leafnode import LeafNode 
from parentnode import ParentNode
from nodestohtml import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from nodestohtml import split_nodes_image, split_nodes_link, text_to_textnodes
from blocks import markdown_to_blocks, block_to_block_type, BlockType, get_block_text, get_heading_tag
from markdown_to_html import unordered_list_children, text_to_children, markdown_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_none(self):
        node = TextNode('test', TextType.TEXT, url=None)
        node2 = TextNode('test', TextType.TEXT, url='https://google.com')
        self.assertNotEqual(node, node2)
    
    def test_text_type(self):
        node = TextNode("test",TextType.BOLD)
        node2 = TextNode("test", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode(props = {'href':'https://www.google.com', 'target':'_blank'})
        self.assertEqual(node.props_to_html(),' href="https://www.google.com" target="_blank"')

    def test_HTMLNode_printing(self):
        node = HTMLNode(tag='sdf', value='sdfs')
        self.assertEqual(repr(node), "HTMLNode with tag:sdf, value:sdfs, children:None, props:None")

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

class TextMarkdownToHtml(unittest.TestCase):
    def test_markdown_to_html(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        result = [TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT)]
        self.assertEqual(new_nodes, result)

    def test_markdown_to_html_bold(self):
        node = TextNode("This is text with a **code block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        result = [TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.BOLD),
                TextNode(" word", TextType.TEXT)]
        self.assertEqual(new_nodes, result)

    # def test_markdown_to_html_bold(self):
    #     node = TextNode("This is text with a **code block** word and **bold** block", TextType.TEXT)
    #     new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    #     result = [TextNode("This is text with a ", TextType.TEXT),
    #             TextNode("code block", TextType.BOLD),
    #             TextNode(" word and ", TextType.TEXT),
    #             TextNode("bold", TextType.BOLD),
    #             TextNode(" block", TextType.TEXT)]
    #     self.assertEqual(new_nodes, result)


    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_mult(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_to_textnodes(self):
        node = TextNode("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
                        TextType.TEXT)
        new_nodes = text_to_textnodes(node.text)
        self.assertListEqual([
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev")
        ], new_nodes)

class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_2(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )
    
    def test_block_to_block_type(self):
        block = """1. This is the first list item in a list block
2. This is a list item
3. This is another list item"""
        blocktype = block_to_block_type(block)
        self.assertEqual(blocktype, BlockType.ORDERED_LIST)
    
    def test_block_to_block_type_incorrect(self):
        block = """1. This is the first list item in a list block
3. This is a list item
5. This is another list item"""
        blocktype = block_to_block_type(block)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered(self):
        block = """- This is the first list item in a list block
- This is a list item
- This is another list item"""
        blocktype = block_to_block_type(block)
        self.assertEqual(blocktype, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_heading(self):
        block = "##### Header title"
        blocktype = block_to_block_type(block)
        self.assertEqual(blocktype, BlockType.HEADING)


    def test_get_block_text(self):
        block = "### Header title"
        blocktype = block_to_block_type(block)
        block_text = get_block_text(block, blocktype)
        self.assertEqual(block_text, "Header title")

    def test_get_block_text_quote(self):
        block = "> Quote here"
        blocktype = block_to_block_type(block)
        block_text = get_block_text(block, blocktype)
        self.assertEqual(block_text, "Quote here")

    def test_get_block_text_code(self):
        block = "```code here python3 run asdflkj```"
        blocktype = block_to_block_type(block)
        block_text = get_block_text(block, blocktype)
        self.assertEqual(block_text, "code here python3 run asdflkj")

    def test_get_heading_tag(self):
        heading = '#### Heading text'
        tag = get_heading_tag(heading)
        self.assertEqual(tag, 'h4')

# class TestMarkdownToHMTL(unittest.TestCase):
#     def test_unordered_list_children(self):
#         block = "- First item\n- Second item\n- Third item"
#         children = unordered_list_children(block)
#         #children_html = [HTMLNode('li', 'First item'), HTMLNode('li', 'Second item'), HTMLNode('li', 'Third item')]
#         parent = ParentNode('ul',children=children)
#         #parent_html = ParentNode('ul', children_html)
#         parent_str = "[HTMLNode with tag:li, value:None, children:[TextNode(First item, text, None)], props:None, HTMLNode with tag:li, value:None, children:[TextNode(Second item, text, None)], props:None, HTMLNode with tag:li, value:None, children:[TextNode(Third item, text, None)], props:None]"
#         self.assertEqual(parent.to_html(), parent_str)


    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()