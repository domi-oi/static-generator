from blocktype import block_to_block_type, BlockType
import unittest

class TestBlockType(unittest.TestCase):
    def test_Code(self):
        text = """``` this is a code block haha ```"""

        self.assertEqual(BlockType.CODE, block_to_block_type(text))

    def test_Ordered(self):
        text = """1. bla bla \n2. bla bla \n3. bla bla \n4. bla bla"""

        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(text))

    def test_Unordered(self):
        text = "- haha haha \n- lol lol"

        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(text))

    def test_quote(self):
        text = ">haha haha \n> lol lol"

        self.assertEqual(BlockType.QUOTE, block_to_block_type(text))

    def test_heading(self):
        text = "###### I like comments lol"

        self.assertEqual(BlockType.HEADING, block_to_block_type(text))

    def test_paragraph(self):
        text = "HAHAHAHAHA \n nein"

        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(text))


    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)








if __name__ == "__main__":
    unittest.main()
