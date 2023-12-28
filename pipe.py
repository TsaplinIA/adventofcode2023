# |up|down|left|right|
# |x |x   |x   |x    |
directions = {
    'u': int('1000', 2),
    'd': int('0100', 2),
    'l': int('0010', 2),
    'r': int('0001', 2),
}

dir_to_delta = {
    8: (-1, 0),  # up
    4: (1, 0),  # down
    2: (0, -1),  # left
    1: (0, 1),  # right
}
dir_inverse = {
    8: 4,
    4: 8,
    2: 1,
    1: 2,
}

pipes = {
    '|': 12,
    '-': 3,
    'L': 9,
    'J': 10,
    '7': 6,
    'F': 5,
    '.': 0
}
d_to_pipe = {
    12: '│',
    3: '─',
    9: '└',
    10: '┘',
    6: '┐',
    5: '┌',
    0: '.',
    15: '┼',
}


def lines(path: str):
    with open(path) as file:
        while line := file.readline():
            yield line.strip()


import re


def get_map(path: str):
    pipe_map = []
    start = None
    for line in lines(path):
        pipe_map.append(line)
        if match := re.search(r'S', line):
            start = len(pipe_map) - 1, match.span()[0]
    return tuple(pipe_map), start


def part1(path: str):
    pipe_map, start = get_map(path)
    paths = []
    step_counts = [[-1] * len(pipe_map[0]) for _ in pipe_map]
    for direction, delta in dir_to_delta.items():
        # (line_idx, char_idx, in_direction, step_count)
        paths.append((start[0] + delta[0], start[1] + delta[1], direction, 0))

    max_step_count = 0
    while paths:
        line_idx, char_idx, in_direction, step_count = paths.pop(0)
        if line_idx < 0 or char_idx < 0:
            continue
        if line_idx > len(pipe_map) - 1 or char_idx > len(pipe_map[0]):
            continue
        if step_counts[line_idx][char_idx] != -1:
            continue
        pipe_digit = pipes[pipe_map[line_idx][char_idx]]
        if not pipe_digit & dir_inverse[in_direction]:
            continue

        new_direction = pipe_digit ^ dir_inverse[in_direction]
        new_step_count = step_count + 1
        new_line_idx = line_idx + dir_to_delta[new_direction][0]
        new_char_idx = char_idx + dir_to_delta[new_direction][1]
        paths.append((new_line_idx, new_char_idx, new_direction, new_step_count))

        max_step_count = max(max_step_count, new_step_count)
        step_counts[line_idx][char_idx] = new_step_count
    return max_step_count


def part2(path: str):
    i_count = 0
    pipe_map, start = get_map(path)
    paths = []
    for direction, delta in dir_to_delta.items():
        # (line_idx, char_idx, in_direction, side_map)
        side_map = [[0] * len(pipe_map[0]) for _ in pipe_map]
        paths.append((start[0] + delta[0], start[1] + delta[1], direction, side_map))
    while paths:
        line_idx, char_idx, in_direction, side_map = paths.pop(0)
        if line_idx < 0 or char_idx < 0:
            continue
        if line_idx > len(pipe_map) - 1 or char_idx > len(pipe_map[0]) - 1:
            continue
        pipe_char = pipe_map[line_idx][char_idx]
        if pipe_char == 'S':
            side_map[line_idx][char_idx] = 15
            i_count += sum_of_inner(side_map)
            continue
        pipe_digit = pipes[pipe_char]
        if not pipe_digit & dir_inverse[in_direction]:
            continue
        side_map[line_idx][char_idx] = pipe_digit

        new_direction = pipe_digit ^ dir_inverse[in_direction]
        new_line_idx = line_idx + dir_to_delta[new_direction][0]
        new_char_idx = char_idx + dir_to_delta[new_direction][1]
        paths.append((new_line_idx, new_char_idx, new_direction, side_map))
    return int(i_count / 2)


def sum_of_inner(side_map: list):
    for i in side_map:
        print(''.join(map(lambda x: d_to_pipe[x], i)))
    print("____________________")

    hcounts = []
    filter_digit = 4
    for line_idx in range(len(side_map)):
        count = []
        c = 0
        for char_idx in range(len(side_map[0])):
            filtered_pipe_num = filter_digit & side_map[line_idx][char_idx]

            c ^= int(bool(filtered_pipe_num))
            count.append(c) if not side_map[line_idx][char_idx] else count.append(0)
        hcounts.append(count)

    from collections import Counter
    counter = Counter()
    for count in hcounts:
        counter.update(count)
    res = counter.get(2, 0) + counter.get(1, 0)
    return res


if __name__ == '__main__':
    res_example_p1 = part1('inputs/pipe.example.p1.in')
    print(res_example_p1)  # 4

    res_p1 = part1('inputs/pipe.in')
    print(res_p1)  # 6640

    res_example_p2 = part2('inputs/pipe.example.p2.in')
    print(res_example_p2)  # 8

    res_p2 = part2('inputs/pipe.in')
    print(res_p2)  # 411
