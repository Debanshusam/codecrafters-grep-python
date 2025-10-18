
from typing import Optional
import sys
import logging

from inp_parser.types import FilterKeyType
from app.regex_definitions import match_single_char
from app.regex_definitions import single_digit
from app.regex_definitions import alpha_numeric
from app.regex_definitions import positive_char_group as pcg
from app.regex_definitions import negative_char_group as ncg

logger = logging.getLogger(__name__)

def grep(filter_key: FilterKeyType, input_line: str, search_pattern: Optional[str] = None) -> None:

    if filter_key == "digit":
        if single_digit.match_any_digit(input_line):
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
    logger.info(f"No match found :: {input_line=}, {search_pattern=}, {filter_key=}")
    exit(1)
