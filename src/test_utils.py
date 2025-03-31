import unittest
from unittest import TestCase

from src.utils import extract_title


class TestExtractTitle(TestCase):

    def test_extract_title_from_markdown_base(self):
        markdown = """
# My Title
"""
        title = extract_title(markdown)
        self.assertEqual(title, "My Title")

    def test_extract_title_from_markdown_with_no_match(self):
        markdown = """
**This has no title**

```
some _code_
```
"""
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title_from_markdown_with_multiple_matches(self):
        markdown = """
# Title One
## Title Three
# Title Two
"""
        title = extract_title(markdown)
        self.assertEqual(title, "Title One")


if __name__ == '__main__':
    unittest.main()
