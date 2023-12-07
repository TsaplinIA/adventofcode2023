from collections import Counter

cards_to_number_p1 = {
    '2': '0',
    '3': '1',
    '4': '2',
    '5': '3',
    '6': '4',
    '7': '5',
    '8': '6',
    '9': '7',
    'T': '8',
    'J': '9',
    'Q': 'A',
    'K': 'B',
    'A': 'C',
}

points_to_number_p1 = {
    15: '0',
    18: '1',
    21: '2',
    33: '3',
    36: '4',
    84: '5',
    243: '6',
}

cards_to_number_p2 = {
    'J': '0',
    '2': '1',
    '3': '2',
    '4': '3',
    '5': '4',
    '6': '5',
    '7': '6',
    '8': '7',
    '9': '8',
    'T': '9',
    'Q': 'A',
    'K': 'B',
    'A': 'C',
}


def games(path: str):
    with open(path) as file:
        while game_str := file.readline().strip():
            hand, bet = game_str.split()
            bet = int(bet)
            yield hand, bet


def hand_number_p1(hand: str):
    counter = Counter()
    counter.update(hand)
    points = 0
    for _, count in counter.items():
        points += 3 ** count
    return points_to_number_p1[points]


def hand_number_p2(hand: str):
    counter = Counter()
    counter.update(hand)
    j = counter.pop('J', 0)
    mc = counter.most_common(1)[0] if j != 5 else ("J", None)
    counter.update(mc[0] * j) if j else ...
    points = 0
    for _, count in counter.items():
        points += 3 ** count
    return points_to_number_p1[points]


def hand_score(hand: str, part2: bool = False):
    numbers = [hand_number_p2(hand) if part2 else hand_number_p1(hand)]
    cards_to_number = cards_to_number_p2 if part2 else cards_to_number_p1
    for card in hand:
        numbers.append(cards_to_number[card])
    return int(''.join(numbers), 13)


def sum_of_wins(path: str, part2: bool = False):
    sorted_games = sorted(games(path), key=lambda x: hand_score(x[0], part2=part2))
    games_sum = 0
    for idx, (hand, bet) in enumerate(sorted_games, start=1):
        games_sum += bet * idx
    return games_sum


if __name__ == '__main__':
    part1_example_result = sum_of_wins('inputs/camel_cards.example.in')
    print(part1_example_result)  # 6440

    part1_result = sum_of_wins('inputs/camel_cards.in')
    print(part1_result)  # 256448566

    part2_example_result = sum_of_wins('inputs/camel_cards.example.in', part2=True)
    print(part2_example_result)  # 5905

    part2_result = sum_of_wins('inputs/camel_cards.in', part2=True)
    print(part2_result)  # 254412181
