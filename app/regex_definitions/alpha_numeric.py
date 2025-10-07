import unittest

def match_alphanum(input_line: str) -> bool:
    is_alpha_numeric: bool = False
    for char in input_line:
        if char.isalnum():
            # print(f"Matching :: Any alphanumeric pattern in :: {input_line}, Found :: {char}")
            is_alpha_numeric = True
        else:
            print(f"Not Matching :: Any alphanumeric pattern in :: {input_line}")
            return False
    print(f"Matching :: alphanumeric pattern in :: {input_line}")
    return is_alpha_numeric

class TestAlphaNumeric(unittest.TestCase):
    def test_all_alphanumeric(self):
        self.assertTrue(match_alphanum("abc123"))

    def test_only_digits(self):
        self.assertTrue(match_alphanum("123456"))

    def test_only_letters(self):
        self.assertTrue(match_alphanum("abcdef"))

    def test_with_special_characters(self):
        self.assertFalse(match_alphanum("abc123!@#"))
        self.assertFalse(match_alphanum("$!"))

    def test_empty_string(self):
        self.assertFalse(match_alphanum(""))

    def test_with_spaces(self):
        self.assertFalse(match_alphanum("abc 123"))

    def test_single_alphanumeric(self):
        self.assertTrue(match_alphanum("a"))
        self.assertTrue(match_alphanum("1"))

    def test_single_non_alphanumeric(self):
        self.assertFalse(match_alphanum("!"))

if __name__ == "__main__":
    unittest.main()