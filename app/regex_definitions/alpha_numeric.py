import unittest
import pyparsing as pp
import logging
logger = logging.getLogger(__name__)

ALPHA_NUMERIC_PATTERN = pp.Literal("\\w")


def match_alphanum(input_line: str) -> bool:
    """ Check if the input_line consists any of alphanumeric characters.
    An alphanumeric character is either a letter (a-z, A-Z) or a digit (0-9).
    
    NOTE: Additionally Match undrscore (_) as alphanumeric to align with \w regex behavior.
    """
    for char in input_line:
        if char.isalnum() or char == '_':  # Including underscore as alphanumeric
            logger.debug(f"Matching :: Any alphanumeric pattern in :: {input_line}, Found :: {char}")
            return True
        
    logger.info(f"Matching :: alphanumeric pattern in :: {input_line}")
    return False

class TestAlphaNumeric(unittest.TestCase):
    def test_all_alphanumeric(self):
        self.assertTrue(match_alphanum("abc123"))

    def test_only_digits(self):
        self.assertTrue(match_alphanum("123456"))

    def test_only_letters(self):
        self.assertTrue(match_alphanum("abcdef"))

    def test_with_special_characters(self):
        self.assertTrue(match_alphanum("abc123!@#"))
        self.assertFalse(match_alphanum("$!?"))
    
    def test_with_underscore(self):
        self.assertTrue(match_alphanum("÷×=_=+÷"))
        self.assertTrue(match_alphanum("___"))
        self.assertTrue(match_alphanum("_"))

    def test_empty_string(self):
        self.assertFalse(match_alphanum(""))

    def test_with_spaces(self):
        self.assertTrue(match_alphanum("abc 123"))

    def test_single_alphanumeric(self):
        self.assertTrue(match_alphanum("a"))
        self.assertTrue(match_alphanum("1"))

    def test_single_non_alphanumeric(self):
        self.assertFalse(match_alphanum("!"))

if __name__ == "__main__":
    unittest.main(verbosity=2)