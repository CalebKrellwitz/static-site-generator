import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)

    def test_not_eq_tag(self):
        node = HTMLNode(tag="exampletag")
        node2 = HTMLNode(tag="differenttag")
        self.assertNotEqual(node, node2)

    def test_not_eq_value(self):
        node = HTMLNode(value="example text for value")
        node2 = HTMLNode(value="different text for value")
        self.assertNotEqual(node, node2)

    def test_not_eq_children(self):
        child = HTMLNode(tag="tag1")
        child2 = HTMLNode(tag="tag2")
        child3 = HTMLNode(tag="tag3")
        child4 = HTMLNode(tag="tag4")

        node = HTMLNode(children=[child, child2, child3])
        node2 = HTMLNode(children=[child, child2, child4])
        self.assertNotEqual(node, node2)

    def test_not_eq_props(self):
        node = HTMLNode(props={"href": "https://www.boot.dev"})
        node2 = HTMLNode(props={"href": "https://github.com"})
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode(props={
            "href": "https://www.boot.dev",
            "target": "_blank",
        })
        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev" target="_blank"')

class TestLeafNode(unittest.TestCase):
    def test_to_html_no_value(self):
        bad_leaf = LeafNode(None, None)
        self.assertRaises(ValueError, bad_leaf.to_html)

    def test_to_html_no_tag(self):
        leaf = LeafNode(None, "example text")
        self.assertEqual(leaf.to_html(), "example text")

    def test_to_html_yes_tag(self):
        leaf = LeafNode('p', "example text")
        self.assertEqual(leaf.to_html(), "<p>example text</p>")

    def test_to_html_tag_and_props(self):
        leaf = LeafNode('a', "Click me!", {"href": "https://www.boot.dev"})
        self.assertEqual(leaf.to_html(), '<a href="https://www.boot.dev">Click me!</a>')

if __name__ == "__main__":
    unittest.main()
