import sys
import logging
from inp_parser.parse import RegexParser

logger = logging.getLogger(__name__)

def logging_config():
    logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(funcName)s: %(message)s'
)

def main() -> None:
    # Initialize logging
    logging_config()

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    logger.info("Logs from your program will appear here!")
    logger.debug(f"DEBUG :: {sys.argv=}")

    # Parsing the command to determine the type of pattern
    # _filter_key: FilterKeyType = parse_command_to_identify_filter_type(sys.argv)  # Validate command
    

    # Using the input parser to handle pattern matching
    # grep(
    #     filter_key=_filter_key, 
    #     search_pattern=sys.argv[2], 
    #     input_line=sys.stdin.read()
    #     )
    logger.debug(f"{sys.argv=}")
    _usr_input = sys.stdin.read().strip("\n")
    logger.debug(f"{_usr_input=}")

    parser = RegexParser()
    parser.parse(
        args=sys.argv, 
        usr_input=_usr_input
        )


if __name__ == "__main__":
    main()
