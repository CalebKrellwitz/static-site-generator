import unittest

from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link
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

class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        self.assertEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            split_nodes_image([node])
        )

    def test_start_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)This is text that starts with an image and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        self.assertEqual(
            [
                TextNode("", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("This is text that starts with an image and another ", TextType.PLAIN),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            split_nodes_image([node])
        )

    def test_duplicate_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another identical ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        self.assertEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another identical ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            split_nodes_image([node])
        )

    def test_multiple_nodes(self):
        node1 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        node2 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        self.assertEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            split_nodes_image([node1, node2])
        )

class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            split_nodes_link([node])
        )

    def test_start_link(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png)This is text that starts with a link and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        self.assertEqual(
            [
                TextNode("", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("This is text that starts with a link and another ", TextType.PLAIN),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            split_nodes_link([node])
        )

    def test_duplicate_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another identical [link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another identical ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            split_nodes_link([node])
        )

    def test_multiple_nodes(self):
        node1 = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        node2 = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            split_nodes_link([node1, node2])
        )

if __name__ == "__main__":
    unittest.main()
