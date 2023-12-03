import re
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


if __name__ == '__main__':
    example_parts_sum_res = parts_sum('inputs/gear_ratios.example.in')
    print(example_parts_sum_res)  # 4361

    parts_sum_res = parts_sum('inputs/gear_ratios.in')
    print(parts_sum_res)  # 531932

    example_gear_ratios_sum = gear_ratios_sum('inputs/gear_ratios.example.in')
    print(example_gear_ratios_sum)  # 467835

    gear_ratios_sum_res = gear_ratios_sum('inputs/gear_ratios.in')
    print(gear_ratios_sum_res)  # 73646890
