import sys
import pyparsing as pp 
from pyparsing import ParserElement, ParseException
from typing import Annotated, Optional

from app.regex_definitions import match_single_char
from app.regex_definitions import match_digits
from app.regex_definitions import alpha_numeric
from app.regex_definitions import positive_char_group as pcg
from app.regex_definitions import negative_char_group as ncg

FilterKeyType = Annotated[
    str, 
    pp.Literal("digit") | 
    pp.Literal("single_char") | 
    pp.Literal("alpha_numeric") |
    # -------
    pp.Literal("positive_char_group") |
    pp.Literal("negative_char_group")
    # ------
    ]

def parse_command_to_identify_filter_type(args) -> FilterKeyType:
    """ Parses the command line arguments to identify the filter type.
    Returns:
        FilterKeyType: The identified filter type.
    Raises:
        ValueError: If the command is invalid or the filter type is unrecognized.
    """
    # Define a simple grammar for recognizing \d (digit) or any single character pattern
    ParserElement.setDefaultWhitespaceChars('')  # Don't skip whitespace

    # ---- REGEX GRAMMAR ----
    # You can extend this grammar for more regex features as needed
    filter_type_ky = args[2]
    digit_pattern = pp.Literal("\\d")
    alpha_numeric_pattern = pp.Literal("\\w")

    # Basic validation of command structure
    if len(args) < 3:
        raise ValueError("Not enough arguments")
    
    if args[1] == "-E":
        pass
    else:
        raise ValueError("Expected first argument to be '-E'")

    # Filter type identification
    _identified_filter_type: FilterKeyType = "single_char"  # Default to single_char
    
    # --- DIGIT PATTERN CHECK ---
    try:
        # Try to parse the pattern as a digit pattern
        digit_pattern.parseString(filter_type_ky, parse_all=True)
        _identified_filter_type = "digit"
    except ParseException:
        pass
    
    # --- ALPHA NUMERIC PATTERN CHECK ---
    try:
        # Try to parse the pattern as a single character pattern
        alpha_numeric_pattern.parseString(filter_type_ky, parse_all=True)
        _identified_filter_type = "alpha_numeric"
    except ParseException:
        pass

    # --- POSITIVE CHAR GROUP PATTERN CHECK ---
    try:
        # Try to parse the pattern as a positive character group pattern
        pcg.POSITIVE_CHAR_GROUP.parseString(filter_type_ky, parse_all=True)
        _identified_filter_type = "positive_char_group"
    except ParseException:
        pass

    # --- NEGATIVE CHAR GROUP PATTERN CHECK ---
    try:
        # Try to parse the pattern as a negative character group pattern
        ncg.NEGATIVE_CHAR_GROUP.parseString(filter_type_ky, parse_all=True)
        _identified_filter_type = "negative_char_group"
    except ParseException:
        pass
    
    print(f"DEBUG :: Identified filter type :: {_identified_filter_type=}", file=sys.stderr)
    return _identified_filter_type


def grep(filter_key: FilterKeyType, input_line: str, search_pattern: Optional[str] = None) -> None:

    if filter_key == "digit":
        if match_digits.match_any_digit(input_line):
            exit(0)
 
    elif filter_key == "alpha_numeric":
        if alpha_numeric.match_alphanum(input_line):
            exit(0)

    elif filter_key == "single_char":
        # If not a digit pattern, treat as single char pattern
        if match_single_char.match_pattern(input_line, search_pattern):
            exit(0)

    elif filter_key in ("positive_char_group"):
        if pcg.match_char_group(input_line, search_pattern):
            exit(0)
    
    elif filter_key in ("negative_char_group"):
        if ncg.match_neg_char_group(input_line, search_pattern):
            exit(0)

    else:
        raise RuntimeError(f"Unhandled filter key: {filter_key}")

    # if not matched
    print(f"No match found :: {input_line=}, {search_pattern=}, {filter_key=}", file=sys.stderr)
    exit(1)


def main() -> None:
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)
    print(f"DEBUG :: {sys.argv=}", file=sys.stderr)

    # Parsing the command to determine the type of pattern
    _filter_key: FilterKeyType = parse_command_to_identify_filter_type(sys.argv)  # Validate command

    # Using the input parser to handle pattern matching
    grep(
        filter_key=_filter_key, 
        search_pattern=sys.argv[2], 
        input_line=sys.stdin.read()
        )


if __name__ == "__main__":
    main()
