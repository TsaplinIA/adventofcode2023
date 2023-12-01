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


def restore_line_number(line: str):
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


def restore_calibration_value(path: str):
    return sum([restore_line_number(line) for line in lines(path)])


if __name__ == '__main__':
    result = restore_calibration_value('inputs/trebuchet.in')
    print(result)
