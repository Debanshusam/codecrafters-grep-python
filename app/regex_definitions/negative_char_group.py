import unittest
import pyparsing as pp 
from pyparsing import ParserElement, ParseException
import logging
logger = logging.getLogger(__name__)

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
NEGATIVE_CHAR_GROUP = (
    pp.Literal('[').suppress() +
    pp.Literal('^').suppress() +
    CHAR_GROUP_CONTENT("content") +
    pp.Literal(']').suppress()
)

def _extract_groups(pattern):
    try:
        result = NEGATIVE_CHAR_GROUP.parse_string(pattern)
        logger.debug(f"DEBUG {result.dump()=}")
        logger.debug(f"DEBUG singles :: {result.single_char if hasattr(result, 'single_char') else 'N/A'}")

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
        
        logger.debug(f"DEBUG formatted_ranges :: {formatted_ranges}")

        return singles, formatted_ranges
    except pp.ParseException as e:
        logger.exception(f"Parse error: {e}")
        return [], []


def match_neg_char_group(input_line: str, match_pattern: str) -> bool:
    """ Check if the input_line consists any of characters in match_pattern.

    Negative character groups match any character that is not present within a pair of square brackets.

    Examples:

    [^abc] should match "cat", since "t" is not in the set "a", "b", or "c".
    [^abc] should not match "cab", since all characters are in the set.
    """
    single_char_pattern, range_char_pattern = _extract_groups(match_pattern)
    logger.debug(f"DEBUG {input_line=}")
    logger.debug(f"DEBUG {match_pattern=}")

    if len(input_line) == 0:
        return True  # Empty input should always match negative char group
    elif len(single_char_pattern) == 0 and len(range_char_pattern) == 0:
        return True  # No exclusions means everything matches

    # Check for single characters
    _single_chars_match_ctr={"matched": 0, "not_matched": 0, "total": len(input_line)} 

    # Expanding range patterns to individual characters for easier checking
    _expanded_single_char_pattern = list()
    for each_range in range_char_pattern:
        if (
            not isinstance(each_range, list) 
            and 
            len(each_range) < 3
        ):
            raise ValueError(f"Invalid range parsed: {each_range}")
        else:
            _expanded_single_char_pattern.extend(
                [chr(c) for c in range(ord(each_range[0]), ord(each_range[-1]) + 1)]
            )
    # Extending the single_char_pattern with expanded range characters and remove duplicated characters
    _expanded_single_char_pattern.extend(set(single_char_pattern))
    _expanded_single_char_pattern_dict = {char: False for char in _expanded_single_char_pattern}
    for char in input_line:
        logger.debug(f"DEBUG Checking char {char} in {input_line}")
        if char in _expanded_single_char_pattern_dict:
            _expanded_single_char_pattern_dict[char] = True
            _single_chars_match_ctr["matched"] += 1
        else:
            _single_chars_match_ctr["not_matched"] += 1

    logger.debug(f"DEBUG _single_chars_match_ctr :: {_single_chars_match_ctr}")
    logger.debug(f"DEBUG _expanded_single_char_pattern_dict :: {_expanded_single_char_pattern_dict}")

    if False not in _expanded_single_char_pattern_dict.values():
        # All characters in input_line are found in the negative char group pattern
        return False
    else:
        # At least one character in input_line is not found in the negative char group pattern
        return True

class TestNegativeCharGroup(unittest.TestCase):
    def test_single_char_not_in_group(self):
        self.assertTrue(match_neg_char_group("d", "[^abc]"))  # 'd' not in 'a','b','c'
        self.assertTrue(match_neg_char_group("xyz", "[^abc]"))  # all not in group

    def test_single_char_in_group(self):
        self.assertFalse(match_neg_char_group("a", "[^abc]"))  # 'a' in group
        self.assertFalse(match_neg_char_group("apple", "[^abc]"))  # 'a' in group
        self.assertFalse(match_neg_char_group("cab", "[^abc]"))  # all in group

    def test_char_range_not_in_group(self):
        self.assertTrue(match_neg_char_group("z", "[^a-c]"))  # 'z' not in 'a-c'
        self.assertTrue(match_neg_char_group("xyz", "[^a-c]"))  # all not in range

    def test_char_range_in_group(self):
        self.assertFalse(match_neg_char_group("a", "[^a-c]"))  # 'a' in range
        self.assertFalse(match_neg_char_group("abc", "[^a-c]"))  # all in range

    def test_mixed_group(self):
        self.assertTrue(match_neg_char_group("m", "[^a-ce-g]"))  # 'm' not in group or ranges
        self.assertFalse(match_neg_char_group("e", "[^a-ce-g]"))  # 'e' in range

    def test_empty_input(self):
        self.assertTrue(match_neg_char_group("", "[^abc]"))  # empty input should be True

    def test_empty_pattern(self):
        self.assertTrue(match_neg_char_group("abc", "[^]"))  # no exclusions, so always True

    def test_non_alpha_characters(self):
        self.assertTrue(match_neg_char_group("1", "[^a-c]"))  # '1' not in 'a-c'
        self.assertTrue(match_neg_char_group("-", "[^a-c]"))  # '-' not in 'a-c'
        


if __name__ == "__main__":
    unittest.main(verbosity=2)


