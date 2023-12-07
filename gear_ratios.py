import re
import uuid
from collections import defaultdict


def lines(path: str):
    with open(path) as file:
        while line := file.readline():
            yield line.strip()


def parts_sum(path: str):
    hitmap = defaultdict(dict)
    lines_generator = lines(path)
    for line_idx, line in enumerate(lines_generator):
        for match in re.finditer(rf'[^.\d]', line):
            el_idx = match.span()[0]

            hitmap[line_idx - 1][el_idx - 1] = True if line_idx > 0 and el_idx > 0 else ...
            hitmap[line_idx - 1][el_idx] = True if line_idx > 0 else ...
            hitmap[line_idx - 1][el_idx + 1] = True if line_idx > 0 else ...

            hitmap[line_idx][el_idx - 1] = True if el_idx > 0 else ...
            hitmap[line_idx][el_idx] = True
            hitmap[line_idx][el_idx + 1] = True

            hitmap[line_idx + 1][el_idx - 1] = True if el_idx > 0 else ...
            hitmap[line_idx + 1][el_idx] = True
            hitmap[line_idx + 1][el_idx + 1] = True

    main_sum = 0
    lines_generator = lines(path)
    for line_idx, line in enumerate(lines_generator):
        for match in re.finditer(rf'\d+', line):
            left, right = match.span()
            is_correct = False
            for el_idx in range(left, right):
                is_correct = is_correct or hitmap[line_idx].get(el_idx)
            if is_correct:
                main_sum += int(match.group())

    return main_sum


def gear_ratios_sum(path: str):
    gears = defaultdict(list)
    hitmap = defaultdict(dict)
    lines_generator = lines(path)
    for line_idx, line in enumerate(lines_generator):
        for match in re.finditer(rf'[\*]', line):
            el_idx = match.span()[0]

            hitmap[line_idx - 1][el_idx - 1] = (line_idx, el_idx) if line_idx > 0 and el_idx > 0 else ...
            hitmap[line_idx - 1][el_idx] = (line_idx, el_idx) if line_idx > 0 else ...
            hitmap[line_idx - 1][el_idx + 1] = (line_idx, el_idx) if line_idx > 0 else ...

            hitmap[line_idx][el_idx - 1] = (line_idx, el_idx) if el_idx > 0 else ...
            hitmap[line_idx][el_idx] = (line_idx, el_idx)
            hitmap[line_idx][el_idx + 1] = (line_idx, el_idx)

            hitmap[line_idx + 1][el_idx - 1] = (line_idx, el_idx) if el_idx > 0 else ...
            hitmap[line_idx + 1][el_idx] = (line_idx, el_idx)
            hitmap[line_idx + 1][el_idx + 1] = (line_idx, el_idx)

    lines_generator = lines(path)
    for line_idx, line in enumerate(lines_generator):
        for match in re.finditer(rf'\d+', line):
            left, right = match.span()
            is_correct = False
            for el_idx in range(left, right):
                is_correct = is_correct or hitmap[line_idx].get(el_idx)
            if is_correct:
                gears[is_correct].append(int(match.group()))

    main_sum = 0
    for gear, numbers in gears.items():
        if len(numbers) <= 1:
            continue
        multiplier = 1
        for num in numbers:
            multiplier *= num
        main_sum += multiplier

    return main_sum


def part_sum_v2(path: str):
    id_to_digits = {}
    digits = {}
    for line_idx, line in enumerate(lines(path)):
        for match in re.finditer(rf'\d+', line):
            d_id = uuid.uuid1()
            id_to_digits[d_id] = int(match.group())
            left, right = match.span()
            for i in range(left, right):
                digits[(line_idx, i)] = d_id

    parts_sum = 0
    for line_idx, line in enumerate(lines(path)):
        for match in re.finditer(rf'[^.\d]', line):
            nums = set()
            el_idx = match.span()[0]
            for x in range(el_idx - 1, el_idx + 2):
                for y in range(line_idx - 1, line_idx + 2):
                    nums.add(digit_id) if (digit_id := digits.get((y, x))) else ...
            parts_sum += sum(map(lambda x: id_to_digits[x], nums))

    return parts_sum


if __name__ == '__main__':
    example_parts_sum_res = parts_sum('inputs/gear_ratios.example.in')
    print(example_parts_sum_res)  # 4361

    example_parts_sum_res_v2 = part_sum_v2('inputs/gear_ratios.example.in')
    print(example_parts_sum_res_v2)  # 4361

    parts_sum_res = parts_sum('inputs/gear_ratios.in')
    print(parts_sum_res)  # 531932

    example_gear_ratios_sum = gear_ratios_sum('inputs/gear_ratios.example.in')
    print(example_gear_ratios_sum)  # 467835

    gear_ratios_sum_res = gear_ratios_sum('inputs/gear_ratios.in')
    print(gear_ratios_sum_res)  # 73646890
