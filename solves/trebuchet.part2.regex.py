import re

word_to_digit = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}

def lines(path: str):
    with open(path) as file:
        while line := file.readline():
            yield line.strip()


def restore_line_number(line: str):
    literals = [str(item) for pair in word_to_digit.items() for item in pair]
    left_pattern = rf'\b\w*?({"|".join(literals)})\w*\b'
    right_pattern = rf'\b\w*({"|".join(literals)})\w*?\b'

    right_digit = re.match(right_pattern, line).group(1)
    left_digit = re.match(left_pattern, line).group(1)
    right_digit = word_to_digit.get(right_digit) or int(right_digit)
    left_digit = word_to_digit.get(left_digit) or int(left_digit)

    result = 10 * left_digit if left_digit else 0
    result += right_digit if right_digit else 0
    result = result * 11 if result < 10 else result

    return result


def restore_calibration_value(path: str):
    return sum([restore_line_number(line) for line in lines(path)])


if __name__ == '__main__':
    result = restore_calibration_value('../inputs/trebuchet.in')
    print(result)  # 54824
