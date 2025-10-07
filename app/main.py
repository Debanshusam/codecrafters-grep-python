import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!
from app.regex_definitions import match_single_char
from app.regex_definitions import match_digits

def match_pattern(input_line, pattern):
    if len(pattern) == 1:
        print("Matching :: Single character pattern")
        return pattern in input_line
    else:
        raise RuntimeError(f"Unhandled pattern: {pattern}")


def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    # Uncomment this block to pass the first stage
    if match_single_char.match_pattern(input_line, pattern):
        exit(0)
    
    # MATCH ANY DIGIT
    if sys.argv[2] == "\d":
        if match_digits.match_any_digit(input_line):
            exit(0)

    print("No match found")
    exit(1)
    



if __name__ == "__main__":
    main()
