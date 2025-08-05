import unittest

from htmlnode import HTMLNode


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
            "href": "https://www.google.com",
            "target": "_blank",
        })
        print(f'\nTest of props_to_html():\n{node.props}\nconverts to\n{node.props_to_html()}')

if __name__ == "__main__":
    unittest.main()
