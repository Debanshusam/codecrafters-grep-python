import unittest
import pyparsing as pp
import logging
logger = logging.getLogger(__name__)

DIGIT_PATTERN = pp.Literal("\\d")

def match_digit(input_line: str) -> bool:
    
    
    if input_line.isdigit():
        logger.debug(f"Matched :: Any digit pattern with {input_line}")
        return True
    
    logger.info(f"Not Found :: Any digit pattern in :: {input_line}")
    return False

class TestMatchAnyDigit(unittest.TestCase):
    def test_contains_digits(self):
        self.assertTrue(match_digit("abc123"))
        self.assertTrue(match_digit("mixed123text"))
        self.assertTrue(match_digit("1"))
        self.assertTrue(match_digit("0abc"))

    def test_no_digits(self):
        self.assertFalse(match_digit("no digits here"))
        self.assertFalse(match_digit("!@#$%^&*()"))
        self.assertFalse(match_digit(""))
        self.assertFalse(match_digit("abcdef"))
        self.assertFalse(match_digit("a"))

if __name__ == "__main__":
    unittest.main(verbosity=2)