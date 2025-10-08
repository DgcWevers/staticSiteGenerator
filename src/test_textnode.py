import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode 
from leafnode import LeafNode 
from parentnode import ParentNode
from markdowntohtml import split_nodes_delimiter


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


if __name__ == "__main__":
    unittest.main()