import pyparsing as pp 
from pyparsing import ParserElement, ParseException
from typing import Annotated
import logging

logger = logging.getLogger(__name__)

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

