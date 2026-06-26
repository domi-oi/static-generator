import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("<p>", "www.google.com", None, {"href": "www.google.com", "target": "_blank"})
        print(node.props_to_html())
        print(node)

        node2 = HTMLNode("<h1>", "www.twitter.com", None, {"href": "www.twitter.com", "target": "_full"})
        print(node2.props_to_html())
        print(node2)

        node3 = HTMLNode("<div>", "www.cool.com", None, {"href": "www.cool.com", "target": "_full"})
        print(node3.props_to_html())
        print(node3)

    def test_leaf_to_html_p(self):
        node10 = LeafNode("p", "Hello, world!")
        self.assertEqual(node10.to_html(), "<p>Hello, world!</p>")
        node11 = LeafNode("b", "Hello, world!")
        self.assertEqual(node11.to_html(), "<b>Hello, world!</b>")
        node12 = LeafNode("h1", "Hello, world!")
        self.assertEqual(node12.to_html(), "<h1>Hello, world!</h1>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        print(parent_node)
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
         parent_node.to_html(),
         "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

if __name__ == "__main__":
    unittest.main()