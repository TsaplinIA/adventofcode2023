import re
from collections import Counter, defaultdict


def lines(path: str):
    with open(path) as file:
        while line := file.readline():
            yield line.strip()


def line_matches(line: str):
    available_nums = re.search(r'(\s+\d+)+$', line)
    available_nums = available_nums.group().split()
    winner_nums = re.search(r':(\s+\d+)*', line)
    winner_nums = winner_nums.group()[1:].split()

    counter = Counter()
    counter.update(available_nums)

    return sum(map(lambda x: counter.get(x, 0), winner_nums))


def line_points(line: str):
    return 2 ** (win_count - 1) if (win_count := line_matches(line)) else 0


def sum_of_points(path: str):
    return sum(map(line_points, lines(path)))


def sum_of_cards(path: str):
    cards_counter = defaultdict(lambda: 1)
    cards_sum = 0
    for idx, line in enumerate(lines(path), start=1):
        win_count = line_matches(line)
        cards_sum += cards_counter[idx]
        for j in range(win_count):
            next_idx = idx + 1 + j
            cards_counter[next_idx] += cards_counter[idx]
    return cards_sum


if __name__ == '__main__':
    part1_example_result = sum_of_points('inputs/scratchcards.example.in')
    print(part1_example_result)  # 13

    part1_result = sum_of_points('inputs/scratchcards.in')
    print(part1_result)  # 19135

    part2_example_result = sum_of_cards('inputs/scratchcards.example.in')
    print(part2_example_result)  # 30

    part2_result = sum_of_cards('inputs/scratchcards.in')
    print(part2_result)  # 5704953
