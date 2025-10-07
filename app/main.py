import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!
from app.regex_definitions import match_single_char
from app.regex_definitions import match_digits
from pyparsing import Literal, ParserElement, ParseException
from typing import Annotated

FilterKeyType = Annotated[str, Literal("digit") | Literal("single_char")]

def parse_command_to_identify_filter_type(args) -> FilterKeyType:
    # Define a simple grammar for recognizing \d (digit) or any single character pattern
    ParserElement.setDefaultWhitespaceChars('')  # Don't skip whitespace

    # REGEX GRAMMAR
    # You can extend this grammar for more regex features as needed
    filter_type_ky = args[2]
    digit_pattern = Literal(r"\d")

    # Basic validation of command structure
    if len(args) < 3:
        raise ValueError("Not enough arguments")
    
    if args[1] == "-E":
        pass
    else:
        raise ValueError("Expected first argument to be '-E'")

    # Filter type identification
    try:
        # Try to parse the pattern as a digit pattern
        digit_pattern.parseString(filter_type_ky, parse_all=True)
        return "digit"
    except ParseException:
        return "single_char"

def grep(filter_key: FilterKeyType, search_pattern: str, input_line: str):

    if filter_key == "digit":
        if match_digits.match_any_digit(input_line):
            exit(0)

    elif filter_key == "single_char":
        # If not a digit pattern, treat as single char pattern
        if match_single_char.match_pattern(input_line, search_pattern):
            exit(0)

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

    
    exit(1)


if __name__ == "__main__":
    main()
