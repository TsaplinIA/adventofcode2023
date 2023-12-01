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


def restore_calibration_value(path: str):
    return sum([restore_line_number(line) for line in lines(path)])


if __name__ == '__main__':
    result = restore_calibration_value('inputs/trebuchet.in')
    print(result)  # 54824
