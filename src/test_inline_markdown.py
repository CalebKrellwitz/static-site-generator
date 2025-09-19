import unittest

from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_delimiter
from textnode import TextNode, TextType

class TestExtractMarkdownImages(unittest.TestCase):
    def test_good_images(self):
        markdown_text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(markdown_text),
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        )

    def test_links_not_caught(self):
        markdown_text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_images(markdown_text),
            []
        )
        
class TestExtractMarkdownLinks(unittest.TestCase):
    def test_good_links(self):
        markdown_text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_links(markdown_text),
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        )

    def test_images_not_caught(self):
        markdown_text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_links(markdown_text),
            []
        )

    def test_normal_brackets(self):
        markdown_text = "This is not a [link]"
        self.assertEqual(
            extract_markdown_links(markdown_text),
            []
        )

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_bold(self):
        old_node1 = TextNode("This is a **bold** word", TextType.PLAIN)
        old_node2 = TextNode("The last word is **bold**", TextType.PLAIN)
        self.assertEqual(
            split_nodes_delimiter([old_node1, old_node2], '**', TextType.BOLD),
            [
                TextNode("This is a ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.PLAIN),
                TextNode("The last word is ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode("", TextType.PLAIN)
            ]
        )
    
    def test_italic(self):
        old_node1 = TextNode("This is an _italicized_ word", TextType.PLAIN)
        old_node2 = TextNode("The last word is _italicized_", TextType.PLAIN)
        self.assertEqual(
            split_nodes_delimiter([old_node1, old_node2], '_', TextType.ITALIC),
            [
                TextNode("This is an ", TextType.PLAIN),
                TextNode("italicized", TextType.ITALIC),
                TextNode(" word", TextType.PLAIN),
                TextNode("The last word is ", TextType.PLAIN),
                TextNode("italicized", TextType.ITALIC),
                TextNode("", TextType.PLAIN)
            ]
        )
    
    def test_code(self):
        old_node1 = TextNode("This is a `code` word", TextType.PLAIN)
        old_node2 = TextNode("The last word is `code`", TextType.PLAIN)
        self.assertEqual(
            split_nodes_delimiter([old_node1, old_node2], '`', TextType.CODE),
            [
                TextNode("This is a ", TextType.PLAIN),
                TextNode("code", TextType.CODE),
                TextNode(" word", TextType.PLAIN),
                TextNode("The last word is ", TextType.PLAIN),
                TextNode("code", TextType.CODE),
                TextNode("", TextType.PLAIN)
            ]
        )
    
    def test_non_plain_input(self):
        old_node1 = TextNode("This node is **already** italicized", TextType.ITALIC)
        old_node2 = TextNode("The last word is **bold**", TextType.PLAIN)
        self.assertEqual(
            split_nodes_delimiter([old_node1, old_node2], '**', TextType.BOLD),
            [
                TextNode("This node is **already** italicized", TextType.ITALIC),
                TextNode("The last word is ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode("", TextType.PLAIN)
            ]
        )

    def test_invalid_markdown(self):
        bad_node = TextNode("This is **invalid Markdown", TextType.PLAIN)
        self.assertRaisesRegex(
            Exception,
            "missing closing delimiter; invalid Markdown syntax",
            split_nodes_delimiter,
            [bad_node], '**', TextType.BOLD
        )

if __name__ == "__main__":
    unittest.main()
