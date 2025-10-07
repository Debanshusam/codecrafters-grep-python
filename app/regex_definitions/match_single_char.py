def match_pattern(input_line: str, pattern: str) -> bool:
    if len(pattern) == 1:
        print("Matching :: Single character pattern")
        return pattern in input_line
    else:
        raise RuntimeError(f"Unhandled pattern: {pattern}")