import unittest
from webpage import extract_title # type: ignore

class TestWebpage(unittest.TestCase):
    def test_extract_title(self):
        h1 = extract_title("asdlfkjdf\n# Header one\nasdlfkjsadfkj")
        self.assertEqual(h1, 'Header one')
    
    def test_extract_title_fail(self):
        try:
            extract_title("asdlfkjdf\n## Header one\nasdlfkjsadfkj")
            self.fail("Test should fail: h1 should not include two '##'")
        except Exception:
            pass