import unittest

def match_pattern(input_line: str, pattern: str) -> bool:
    if len(pattern) == 1:
        print("Matching :: Single character pattern")
        return pattern in input_line
    else:
        raise RuntimeError(f"Unhandled pattern: {pattern}")
    
class TestMatchSingleChar(unittest.TestCase):

    def test_single_char_pattern_found(self):
        self.assertTrue(match_pattern("hello", "e"))

    def test_single_char_pattern_not_found(self):
        self.assertFalse(match_pattern("hello", "z"))

    def test_single_char_pattern_at_start(self):
        self.assertTrue(match_pattern("apple", "a"))

    def test_single_char_pattern_at_end(self):
        self.assertTrue(match_pattern("banana", "a"))

    def test_single_char_pattern_multiple_occurrences(self):
        self.assertTrue(match_pattern("banana", "n"))

    def test_empty_input_line(self):
        self.assertFalse(match_pattern("", "a"))

    def test_empty_pattern_raises(self):
        with self.assertRaises(RuntimeError):
            match_pattern("hello", "")

    def test_multi_char_pattern_raises(self):
        with self.assertRaises(RuntimeError):
            match_pattern("hello", "ll")

    def test_pattern_is_space(self):
        self.assertTrue(match_pattern("a b c", " "))

    def test_pattern_is_special_char(self):
        self.assertTrue(match_pattern("foo@bar", "@"))

    def test_pattern_is_digit(self):
        self.assertTrue(match_pattern("abc123", "1"))

    def test_pattern_not_in_numeric_string(self):
        self.assertFalse(match_pattern("12345", "a"))

    def test_pattern_case_sensitive(self):
        self.assertFalse(match_pattern("Hello", "h"))
        self.assertTrue(match_pattern("Hello", "H"))

    def test_pattern_unicode_char(self):
        self.assertTrue(match_pattern("café", "é"))
        self.assertFalse(match_pattern("cafe", "é"))

if __name__ == "__main__":
    unittest.main(verbosity=2)