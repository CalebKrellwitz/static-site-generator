import unittest

from block_markdown import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_typical_markdown(self):
        markdown = '''# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item'''
        self.assertEqual(
            markdown_to_blocks(markdown),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )
    
    def test_multiple_newlines(self):
        markdown = '''This is text



This is more text after four newlines'''
        self.assertEqual(
            markdown_to_blocks(markdown),
            [
                "This is text",
                "This is more text after four newlines",
            ],
        )

    def test_stripping(self):
        markdown = '''     This is text with five leading and trailing spaces     

     

This is text after two newlines, five spaces, and two more newlines'''
        self.assertEqual(
            markdown_to_blocks(markdown),
            [
                "This is text with five leading and trailing spaces",
                "This is text after two newlines, five spaces, and two more newlines",
            ],
        )

if __name__ == "__main__":
    unittest.main()
