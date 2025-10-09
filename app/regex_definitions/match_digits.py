import unittest
import pyparsing as pp
import logging
logger = logging.getLogger(__name__)

DIGIT_PATTERN = pp.Literal("\\d")

def match_any_digit(input_line: str) -> bool:
    
    for char in input_line:
        if char.isdigit():
            logger.debug(f"Matching :: Any digit pattern in :: {input_line}, Found :: {char}")
            return True
    logger.info(f"Matching :: Any digit pattern in :: {input_line}, Not Found")
    return False

class TestMatchAnyDigit(unittest.TestCase):
    def test_contains_digits(self):
        self.assertTrue(match_any_digit("abc123"))
        self.assertTrue(match_any_digit("mixed123text"))
        self.assertTrue(match_any_digit("1"))
        self.assertTrue(match_any_digit("0abc"))

    def test_no_digits(self):
        self.assertFalse(match_any_digit("no digits here"))
        self.assertFalse(match_any_digit("!@#$%^&*()"))
        self.assertFalse(match_any_digit(""))
        self.assertFalse(match_any_digit("abcdef"))
        self.assertFalse(match_any_digit("a"))

if __name__ == "__main__":
    unittest.main(verbosity=2)