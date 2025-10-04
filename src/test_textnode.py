import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode # type: ignore
from leafnode import LeafNode # type: ignore


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



if __name__ == "__main__":
    unittest.main()