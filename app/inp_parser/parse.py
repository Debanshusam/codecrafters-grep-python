
import pyparsing as pp 
from pyparsing import ParserElement, ParseException
import logging

from .types import FilterKeyType

logger = logging.getLogger(__name__)

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
        match_digits.DIGIT_PATTERN.parseString(filter_type_ky, parse_all=True)
        _identified_filter_type = "digit"
    except ParseException:
        pass
    
    # --- ALPHA NUMERIC PATTERN CHECK ---
    try:
        # Try to parse the pattern as a single character pattern
        alpha_numeric.ALPHA_NUMERIC_PATTERN.parseString(filter_type_ky, parse_all=True)
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
    
    logger.debug(f"DEBUG :: Identified filter type :: {_identified_filter_type=}", file=sys.stderr)
    return _identified_filter_type

def regex_expr_mathching():
    """ Placeholder for future regex expression matching logic 
    - read input char by char and match against the pattern
    - if the Match is successful, then move to next char in input and match
    - if the Match is unsuccessful, then break and return no match
    """
    pass