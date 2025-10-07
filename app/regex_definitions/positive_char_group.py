import unittest
import pyparsing as pp 
from pyparsing import ParserElement, ParseException

# Matches a single character
SINGLE_CHAR = pp.Word(pp.alphas, exact=1).set_results_name("single_char", list_all_matches=True)

# Matches a character range like e-k
CHAR_RANGE = (
    pp.Word(pp.alphas, exact=1) +
    pp.Literal('-') +
    pp.Word(pp.alphas, exact=1)
).set_parse_action().set_results_name("char_range", list_all_matches=True)

# Matches one or more single characters or ranges
# CHAR_GROUP_CONTENT = pp.OneOrMore(single_char|char_range)
CHAR_GROUP_CONTENT = pp.OneOrMore(CHAR_RANGE|SINGLE_CHAR) # <-- char_range first

# Matches the whole group: [abc], [abce-kyz], [a-ex-z]
POSITIVE_CHAR_GROUP = (
    pp.Literal('[').suppress() +
    CHAR_GROUP_CONTENT("content") +
    pp.Literal(']').suppress()
)

def _extract_groups(pattern):
    try:
        result = POSITIVE_CHAR_GROUP.parse_string(pattern)
        print(f"DEBUG {result.dump()=}")
        print(f"DEBUG singles :: {result.single_char if hasattr(result, 'single_char') else 'N/A'}")
        # print(f"DEBUG ranges :: {result.char_range if hasattr(result, 'char_range') else 'N/A'}")

        singles = result.single_char if hasattr(result, "single_char") else []

        ranges = result.char_range if hasattr(result, "char_range") else []
        formatted_ranges = []
        if ranges:
            for each_range in ranges:
                if (
                    not isinstance(each_range, list) 
                    and 
                    len(each_range) < 3
                ):
                    raise ValueError(f"Invalid range parsed: {each_range}")
                formatted_ranges.append((each_range[0], each_range[-1]))
        
        print(f"DEBUG formatted_ranges :: {formatted_ranges}")

        return singles, formatted_ranges
    except pp.ParseException as e:
        print(f"Parse error: {e}")
        return [], []


def match_char_group(input_line: str, match_pattern: str) -> bool:
    """ Check if the input_line consists any of characters in match_pattern.
    """
    single_char_pattern, range_char_pattern = _extract_groups(match_pattern)
    print(f"DEBUG {input_line=}")
    print(f"DEBUG {match_pattern=}")

    # Check for single characters
    for char in input_line:
        print(f"DEBUG Checking char {char} in {input_line}")
        if char in list(single_char_pattern):
            return True
        else:
            # Check for ranges
            if range_char_pattern:
                for each_range in range_char_pattern:
                    start_range, end_range = each_range[0], each_range[-1]
                    print(f"DEBUG Checking range {start_range}-{end_range} for char {char}")
                    if start_range <= char <= end_range:
                        return True
    
    return False


class TestPositiveCharGroup(unittest.TestCase):
    def test_single_char_match(self):
        self.assertTrue(match_char_group("a", "[a]"))
        self.assertTrue(match_char_group("b", "[ab]"))
        self.assertFalse(match_char_group("c", "[ab]"))

    def test_char_range_match(self):
        self.assertTrue(match_char_group("c", "[a-c]"))
        self.assertTrue(match_char_group("b", "[a-c]"))
        self.assertFalse(match_char_group("d", "[a-c]"))

    def test_multiple_ranges_and_singles(self):
        self.assertTrue(match_char_group("e", "[a-ce-g]"))
        self.assertTrue(match_char_group("f", "[a-ce-g]"))
        self.assertTrue(match_char_group("a", "[a-ce-g]"))
        self.assertFalse(match_char_group("h", "[a-ce-g]"))

    def test_overlapping_ranges(self):
        self.assertTrue(match_char_group("d", "[a-dc-f]"))
        self.assertTrue(match_char_group("e", "[a-dc-f]"))
        self.assertFalse(match_char_group("g", "[a-dc-f]"))

    def test_non_alpha_characters(self):
        self.assertFalse(match_char_group("1", "[a-c]"))
        self.assertFalse(match_char_group("-", "[a-c]"))

    def test_empty_input(self):
        self.assertFalse(match_char_group("", "[a-c]"))

    def test_empty_pattern(self):
        self.assertFalse(match_char_group("a", "[]"))

    def test_multiple_input_chars(self):
        self.assertTrue(match_char_group("xyz", "[x]"))
        self.assertTrue(match_char_group("xyz", "[a-z]"))
        self.assertFalse(match_char_group("123", "[a-z]"))

    def test_invalid_range(self):
        # Should not match, but also should not raise
        self.assertFalse(match_char_group("a", "[z-a]"))

if __name__ == "__main__":
    unittest.main(verbosity=2)
    # print(match_char_group("xyz", "[x]"))
    # print(match_char_group("a", "[a]"))

