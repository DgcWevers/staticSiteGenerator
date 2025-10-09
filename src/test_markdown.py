import unittest
from blocks import block_to_block_type, BlockType, get_block_text, get_heading_tag, markdown_to_blocks
from nodestohtml import text_to_textnodes
from textnode import text_node_to_html_node
from leafnode import LeafNode
from parentnode import ParentNode
from markdown_to_html import markdown_to_html_node


class TestAI(unittest.TestCase):

    def test_heading_detection_and_text(self):
        b = "# Hello World"
        self.assertEqual(block_to_block_type(b),BlockType.HEADING)
        self.assertEqual(get_heading_tag(b),"h1")
        self.assertEqual(get_block_text(b, BlockType.HEADING), "Hello World")

    def test_heading_without_space_is_paragraph(self):
        b = "##No space"
        self.assertEqual(block_to_block_type(b), BlockType.PARAGRAPH)

    def test_quote_multiline(self):
        b = "> line one\n> line two"
        self.assertEqual(block_to_block_type(b), BlockType.QUOTE)
        self.assertEqual(get_block_text(b, BlockType.QUOTE), "line one\nline two")

    def test_unordered_list_detection(self):
        b = "- a\n- b\n- c"
        self.assertEqual(block_to_block_type(b), BlockType.UNORDERED_LIST)

    def test_ordered_list_detection(self):
        b = "1. a\n2. b\n3. c"
        self.assertEqual(block_to_block_type(b), BlockType.ORDERED_LIST)

    def test_list_rejects_bad_prefix(self):
        b = "1) a\n2) b"
        self.assertEqual(block_to_block_type(b), BlockType.PARAGRAPH)

    def test_codeblock_single_line(self):
        b = "```print('hi')```"
        self.assertEqual(block_to_block_type(b), BlockType.CODE)
        self.assertEqual(get_block_text(b, BlockType.CODE), "print('hi')")

    def test_codeblock_multiline_preserve_newlines_and_trailing(self):
        b = "```\nline1\n\nline3\n```"
        self.assertEqual(block_to_block_type(b), BlockType.CODE)
        t = get_block_text(b, BlockType.CODE)
        self.assertEqual(t, "line1\n\nline3\n")

    def test_markdown_to_blocks_preserves_fenced_blocks(self):
        md = "para\n\n```\ncode\nblock\n```\n\nnext"
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 3)
        self.assertTrue(blocks[1].startswith("```") and blocks[1].endswith("```"))


    def test_inline_strong_emphasis_and_code(self):
        text = "This is **bold** and _italic_ and `code`."
        nodes = text_to_textnodes(text)
        # Ensure mapping to HTML nodes maintains order and types
        html_nodes = [text_node_to_html_node(n) for n in nodes]
        html = "".join(n.to_html() for n in html_nodes)
        self.assertEqual(html, "This is <b>bold</b> and <i>italic</i> and <code>code</code>.")

    def test_parentnode_requires_tag_and_children(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode(None, "x")])
        # empty children list is allowed
        ParentNode("div", [])

    def test_parentnode_props_rendering(self):
        from htmlnode import HTMLNode
        class TestNode(HTMLNode):
            def to_html(self): return "x"
        p = ParentNode("div", [TestNode(None, None, None, None)], props={"class": "c", "id": "i"})
        html = p.to_html()
        self.assertTrue(html.startswith("<div"))
        self.assertTrue(' class="c"' in html and ' id="i"' in html)
        self.assertTrue(html.endswith("</div>"))

    def test_nested_parentnodes(self):
        inner = ParentNode("span", [LeafNode("b", "bold")])
        outer = ParentNode("div", [inner])
        self.assertEqual(outer.to_html(), "<div><span><b>bold</b></span></div>")

    def test_markdown_to_html_mixed_document(self):
        md = """# Title

This is **bolded** paragraph
with a line break.

> quoted _text_

- item 1
- item 2

```
code line 1
code line 2
    ```"""

        root = markdown_to_html_node(md)
        html = root.to_html()
        self.assertTrue(html.startswith("<div>"))
        self.assertTrue("<h1>Title</h1>" in html)
        self.assertTrue("<p>This is <b>bolded</b> paragraph with a line break.</p>" in html)
        self.assertTrue("<blockquote>quoted <i>text</i></blockquote>" in html)
        self.assertTrue("<ul><li>item 1</li><li>item 2</li></ul>" in html)
        self.assertTrue("<pre><code>code line 1\ncode line 2\n</code></pre>" in html)
        self.assertTrue(html.endswith("</div>"))


    def test_paragraph_collapses_internal_whitespace(self):
        md = "This is\nsplit   over\tlines"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is split over lines</p></div>")

    def test_empty_paragraph_skipped(self):
        md = "\n\n"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div></div>")