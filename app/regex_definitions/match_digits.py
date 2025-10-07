import unittest

def match_pattern(input_line: str, pattern: str) -> bool:
    if len(pattern) == 1 and pattern.isdigit():
        print("Matching :: Single digit pattern")
        return pattern in input_line
    else:
        raise RuntimeError(f"Unhandled pattern: {pattern}")

def match_any_digit(input_line: str) -> bool:
    print(f"Matching :: Any digit pattern in :: {input_line}")
    return any(char.isdigit() for char in input_line)

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

if __name__ == "__main__":
    unittest.main(verbosity=2)