import re


def lines(path: str):
    with open(path) as file:
        while line := file.readline():
            yield line.strip()


balls_info = {
    'red': 12,
    'green': 13,
    'blue': 14,
}


def valid_game(line: str) -> int:
    game_id = int(re.match(rf"Game\s+(\d+):", line).group(1))

    for match in re.findall(rf'[:;][^:;]+', line):
        for num, color in re.findall(rf'(\d+)\s+({"|".join(balls_info.keys())})', match):
            if int(num) > balls_info[color]:
                return 0
    return game_id


def sum_of_valid_games(path: str):
    lines_generator = lines(path)
    return sum(map(lambda line: valid_game(line), lines_generator))


def power_of_game(line: str) -> int:
    max_nums = {
        'red': 0,
        'green': 0,
        'blue': 0,
    }
    for match in re.findall(rf'[:;][^:;]+', line):
        for num, color in re.findall(rf'(\d+)\s+({"|".join(balls_info.keys())})', match):
            max_nums[color] = max(max_nums[color], int(num))

    power = 1
    for color, max_num in max_nums.items():
        power *= max_num
    return power


def sum_of_powers(path: str):
    lines_generator = lines(path)
    return sum(map(lambda line: power_of_game(line), lines_generator))


if __name__ == '__main__':
    valid_sum = sum_of_valid_games('inputs/cube_conundrum.in')
    print(valid_sum)  # 2256

    power_sum = sum_of_powers('inputs/cube_conundrum.in')
    print(power_sum)  # 74229
