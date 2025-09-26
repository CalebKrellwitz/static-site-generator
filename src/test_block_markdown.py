import unittest

from block_markdown import BlockType, block_to_block_type, markdown_to_blocks

class TestBlockToBlockType(unittest.TestCase):
    def test_heading_1(self):
        block = "# This is a heading"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING
        )

    def test_heading_6(self):
        block = "###### This is a heading"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING
        )

    def test_bad_heading_7(self):
        block = "####### This is a bad heading"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_code_block(self):
        block = "```This is a code block```"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE
        )

    def test_bad_code_block(self):
        block = "```This is a bad code``` block"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_quote_block(self):
        block = '''>This is a quote
>This is also part of the quote
>'''
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE
        )

    def test_bad_quote_block(self):
        block = '''>This is a bad quote
>This is also part of the bad quote
'''
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_single_line_quote(self):
        block = ">This is a one line quote"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE
        )

    def test_unordered_list(self):
        block = '''- This
- is
- an
- unordered
- list
- '''
        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST
        )

    def test_bad_unordered_list(self):
        block = '''- This
- is
- a
- bad
- unordered
- list
-'''
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_single_line_unordered_list(self):
        block = "- This is a one line unordered list"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST
        )

    def test_ordered_list(self):
        block = '''1. This
2. is
3. an
4. ordered
5. list
6. 
7. 
8. 
9. 
10. '''
        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST
        )

    def test_bad_ordered_list(self):
        block = '''1. This
2. is
3. a
4. bad
5. ordered
6. list
7. 
8. 
9. 
10.'''
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

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
