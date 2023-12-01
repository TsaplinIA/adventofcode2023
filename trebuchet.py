import re


def lines(path: str):
    with open(path) as file:
        while line := file.readline():
            yield line.strip()


def predicate(num: int | None, char: str, left: bool = False):
    conditions = [char.isdigit()]
    conditions.append(num is None) if left else ...

    if all(conditions):
        return int(char)
    return num


def restore_line_number_part1(line: str):
    right_digit = None
    left_digit = None
    for char in line:
        left_digit = predicate(left_digit, char, left=True)
        right_digit = predicate(right_digit, char, left=False)

    result = 10 * left_digit if left_digit else 0
    result += right_digit if right_digit else 0
    while result < 10:
        result = result * 10 + result

    return result


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


def restore_line_number_part2(line: str):
    right_digit = None
    left_digit = None
    words = {
        word: {
            'length': len(word),
            'digit': digit,
            'match_count': 0,
        }
        for word, digit in word_to_digit.items()
    }

    for char in line:
        current_digit = int(char) if char.isdigit() else None
        for word, word_info in words.items():
            if char == word[word_info['match_count']]:
                word_info['match_count'] += 1
            else:
                word_info['match_count'] = int(char == word[0])

            if word_info['match_count'] == word_info['length']:
                current_digit = word_info['digit']
                word_info['match_count'] = 0
        if current_digit is not None:
            right_digit = current_digit
            left_digit = current_digit if left_digit is None else left_digit

    result = 10 * left_digit if left_digit else 0
    result += right_digit if right_digit else 0
    while result < 10:
        result = result * 10 + result

    return result


def restore_calibration_value(path: str, restore_line_func):
    return sum([restore_line_func(line) for line in lines(path)])


def restore_line_number_part2_regex(line: str):
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


if __name__ == '__main__':
    part1_answer = restore_calibration_value(
        'inputs/trebuchet.in',
        restore_line_number_part1,
    )

    part2_answer = restore_calibration_value(
        'inputs/trebuchet.in',
        restore_line_number_part2,
    )

    par2_regex_answer = restore_calibration_value(
        'inputs/trebuchet.in',
        restore_line_number_part2_regex,
    )

    print(f"{part1_answer=}")  # 55386
    print(f"{part2_answer=}")  # 54824
    print(f"{par2_regex_answer=}")  # 54824
