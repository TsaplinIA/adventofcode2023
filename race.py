import re


def lines(path: str):
    with open(path) as file:
        while line := file.readline():
            yield line.strip()


def get_wins_count(x, m):
    a_max = x // 2
    count = 0
    while (a_max - count) * (x - (a_max - count)) > m:
        count += 1
    count = count * 2 if x % 2 else count * 2 - 1
    return count


def input_generator(path: str):
    lines_gen = lines(path)
    first_line = lines_gen.send(None)
    second_line = lines_gen.send(None)

    ts = map(int, first_line.split()[1:])
    ds = map(int, second_line.split()[1:])
    pairs_gen = zip(ts, ds)
    for i in pairs_gen:
        yield i


def part1(path: str):
    mul = 1
    for t, d in input_generator(path):
        mul *= get_wins_count(t, d)

    return mul


def part2_input(path: str):
    lines_gen = lines(path)
    first_line = lines_gen.send(None)
    second_line = lines_gen.send(None)

    x = int(''.join(first_line.split()[1:]))
    y = int(''.join(second_line.split()[1:]))
    return x, y


def part2(path: str):
    x, y = part2_input(path)
    return get_wins_count(x, y)


if __name__ == '__main__':
    # part1_example_res = part1('inputs/race.example.in')
    # print(part1_example_res)  # 288

    # part1_res = part1('inputs/race.in')
    # print(part1_res)  # 128700

    # part2_example_res = part2('inputs/race.example.in')
    # print(part2_example_res)  # 71503

    part2_res = part2('inputs/race.in')
    print(part2_res)  # 39594072
