
import pyparsing as pp 
from pyparsing import ParserElement, ParseException
import logging
import sys
from dataclasses import dataclass


from .types import FilterKeyType
from typing import Optional

from regex_definitions import (
    alpha_numeric, 
    positive_char_group as pcg, 
    negative_char_group as ncg,
    single_digit,
    match_single_char as msc
)

logger = logging.getLogger(__name__)


class RegexDefinitiions:
    def __init__(self):
        self.start_of_expr_flags: list[str] = ["-E"]
        self.meta_chars: list[str]=[
                'w', "W",  # Any alphanumeric character
                "d","D",  # Any digit,
                "[^", # Negated character group
                "[",  # Start of a character group class
                ]
        
        self.operators: list[str] = [
                '*', # 0 or more
                '+', # 1 or more
                '?', # 0 or 1
                '|', # Alternation
                
                '.', # Any character except newline
            ]
        
        self.match_any_in_group: list[str] = [
                '[]', # Character group
                '[^]', # Negated character group
            ]
        
        self.match_all_in_group: list[str] = [
            '(', # Start of group
            ')', # End of group
        ]


class RegexParser:
    
    def __init__(self):
        
        
        self._regex_expr: Optional[str] = None
        self._user_input: Optional[str] = None
        self._matched_groups: dict[str, str] = {}
        self._final_match_state: bool = False
        self._args = None
        self._regex_tokens: list[tuple[str]] = []
        self._regex_defs = RegexDefinitiions()
    
    def __repr__(self):
        logger.debug(f"# ---- Regex Parser State ---- #")
        logger.debug(f"{self._regex_tokens=}")
        logger.debug(f"{self._regex_expr=}")
        logger.debug(f"{self._user_input=}")
        logger.debug(f"{self._matched_groups=}")
        logger.debug(f"{self._match_state=}")
        logger.debug(f"{self._args=}")
    
    # ---------
    def parse(self, args: list[str], usr_input: str) -> None:
        # Standard Lexical checks
        logger.info(f"Starting parsing with Lex checks...")
        self._args = args
        self._lex_checks()
        self._regex_expr = args[2]
        self._user_input = usr_input 
        logger.debug(f"DEBUG :: {self._regex_expr=}, {self._user_input=}")

        # Tokenize the regex expression
        logger.info(f"Starting regex tokenization...")
        self._regex_tokens = self.parse_regex_tokens(self._regex_expr)

        # Parse the input char by char
        logger.info(f"Starting regex matching...")
        self._parse_and_match_usr_inp_char_by_char()

        # Analyse the match state
        logger.info(f"Analysing final match state...")
        self._analyse_match_state()
        
        # Debug current state
        self.__repr()

    # ---------
    def _lex_checks(self) -> None:
        if len(self._args) < 3:
            raise ValueError("Not enough arguments")
        
        if self._args[1] not in self._regex_defs.start_of_expr_flags:
            raise ValueError(f"Invalid flag {self._args[1]}. Expected one of {self._regex_defs.start_of_expr_flags}")

        logger.debug(f"Lexical checks passed :: {self._args=}")

    def parse_regex_tokens(self, regex_expr):
        """
        Parses a simple regex string to identify metacharacters (flags/special sequences) 
        and literal characters, primarily handling the backslash escape.
        """
        logger.info(f"Starting regex token parsing...")
        tokens = []
        i = 0

        while i < len(regex_expr):
            char = regex_expr[i]

            if char == '\\':
                # 1. Backslash encountered: This is the start of an escape sequence.
                i += 1
                if i < len(regex_expr):
                    next_char = regex_expr[i]

                    # Check for common metacharacter sequences (flags)
                    # This list should be extensive in a real parser, e.g., \s, \w, \b, etc.
                    if next_char in self._regex_defs.meta_chars:
                        tokens.append(['METACHAR', '\\' + next_char, False])  # False indicates not yet matched

                    # Check for escaped special characters (literal versions of metachars)
                    # E.g., \* becomes a literal *, not a quantifier. In this case, \d 
                    # is classified above, but if the regex was \*, it would be treated differently.
                    # For this specific example, all '\' + char are classified as METACHAR
                    # since we only check \d. A real parser would have a full list.
                    # For simplicity in this case, we treat \d as METACHAR:
                    else:
                        tokens.append(['METACHAR', '\\' + next_char, False])
                else:
                    # Backslash at the very end of the string is usually an error
                    tokens.append(['ERROR', '\\', False])

            elif char in self._regex_defs.operators:
                # 2. Other Metacharacters (operators/quantifiers/anchors)
                tokens.append(['OPERATOR', char, False])

            elif char in self._regex_defs.match_any_in_group:
                tokens.append(['MATCH_ANY_GROUP', char, False])

            elif char in self._regex_defs.match_all_in_group:
                tokens.append(['MATCH_ALL_GROUP', char, False])
            else:
                # 3. Literal Character (everything else)
                tokens.append(['LITERAL', char, False])

            i += 1
        
        logger.debug(f"Parsed tokens :: {tokens=}")
        logger.info(f"Completed regex token parsing.")

        return tokens
    # ---------
    def _parse_and_match_usr_inp_char_by_char(self) -> None:
        """
        In regex Matching the regex pattern is supposed to be sub-string of the input line.
        """
        # To be used to match substring, to maintain match streak
        _match_substring = self._user_input[::]
        
        for i in range(0, len(self._regex_tokens)):
            each_regex_token = self._regex_tokens[i] 
            
            match_start_index: int = 0
            first_match_index: Optional[int] = None
            match_end_index: Optional[int] = None
            
            _break_match_loop: bool = False  # When regex match streak breaks

            
            if _break_match_loop:   
                break
            
            
            for j in range(match_start_index,len(_match_substring)): 
                match_found: bool = False  # reset for each matching attempt
                each_input_char = _match_substring[j]

                logger.debug(f"Attempting to match token {each_regex_token} with {each_input_char}")

                match_found = self._match(each_regex_token, each_input_char)
                logger.debug(f"# ------ {match_found=}")
                
                # Updating the state of each regex token match
                self._regex_tokens[i][-1]=match_found

                if match_found:
                    first_match_index = j if first_match_index is None else first_match_index
                    match_start_index = j+1  # Next match has to start from next char of user input
                    _match_substring = _match_substring[j+1::]
                    break  # No need to check further input characters for this token
                else:
                    # do nothing, keep looking for a match with next regex token
                    if first_match_index is None:
                        # First match still not found
                        pass
                    elif first_match_index is not None:
                        # If we had a previous match but current char didn't match, we can break
                        _break_match_loop = True
                        logger.warning(f"Breaking out of match loop as no further match possible for token: {each_regex_token=}")
                        break
                    else:
                        # Wait for first match to happen
                        pass
            
    # ---------
    def _match(self, regex_token: tuple[str], input_char: str) -> bool:
        _match_found: bool = False

        if regex_token[0] == "METACHAR":
            _match_found: bool = self._metachar_matching(regex_token, input_char)
        
        elif regex_token[0] == "LITERAL":
            _match_found: bool = self._literal_matching(regex_token, input_char)
        else:
            raise RuntimeError(f"Unhandled token type: {regex_token[0]}")
        
        return _match_found
    
    def _metachar_matching(self, regex_token: tuple[str], input_char: str) -> bool:
        _match_found: bool = False

        if regex_token[1] == r"\d":
            _match_found = single_digit.match_digit(input_char)
                    
        elif regex_token[1] == r"\w":
            _match_found =  alpha_numeric.match_alphanum(input_char)
                
        else:
            raise RuntimeError(f"Unhandled metacharacter: {regex_token[1]}")
        
        return _match_found
    
    def _group_matching(self, regex_token: tuple[str], input_char: str) -> None:
        if regex_token[0] == "MATCH_ANY_GROUP":
            if regex_token[1] == "[]":
                # Positive character group matching
                if pcg.match_char_group(input_char, regex_token[1]):
                    _match_found = True
                    logger.debug(f"Matched POSITIVE CHAR GROUP pattern :: {input_char=}")
                # else:
                #     self._match_state = False
                #     logger.debug(f"DEBUG :: No match for POSITIVE CHAR GROUP pattern :: {input_char=}")
            elif regex_token[1] == "[^]":
                # Negative character group matching
                if ncg.match_neg_char_group(input_char, regex_token[1]):
                    _match_found = True
                    logger.debug(f"Matched NEGATIVE CHAR GROUP pattern :: {input_char=}")
                # else:
                #     self._match_state = False
                #     logger.debug(f"DEBUG :: No match for NEGATIVE CHAR GROUP pattern :: {input_char=}")
            else:
                raise RuntimeError(f"Unhandled group type: {regex_token[1]}")

    def _literal_matching(self, regex_token: tuple[str], input_char: str) -> bool:
        _match_found: bool = False

        if regex_token[1] == input_char:
            _match_found = True
            logger.debug(f"Matched LITERAL pattern :: {regex_token[1]} with {input_char=}")
        # else:
        #     self._match_state = False
        #     logger.debug(f"DEBUG :: No match for LITERAL pattern :: {input_char=}")
        
        return _match_found
    # ---------
    def _analyse_match_state(self) -> None:
        logger.debug(f"{self._regex_tokens=}")
        for each_token in self._regex_tokens:
            if each_token[-1] is False:
                logger.info(f"Match failed for : {each_token=}")
                exit(1)
        logger.info(f"All tokens matched successfully!")
        exit(0)
    
    
        

        




