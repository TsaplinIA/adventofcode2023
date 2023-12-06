import re
from typing import Sequence


def get_info(path: str):
    maps_dict = {}
    with open(path) as file:
        seed_numbers = tuple([
            int(digit)
            for digit in re.findall(r"\d+", file.readline())
        ])

        for map_text in re.finditer(r"(\w+)-to-(\w+) map:([\s\d]*)", file.read()):
            first_word = map_text.group(1)
            second_word = map_text.group(2)
            maps_dict[first_word] = {'threesomes': [], 'next': second_word}
            for threesome in re.findall(r"(?:\s+\d+){3}", map_text.group(3)):
                threesome = tuple(map(int, threesome.strip().split()))
                threesome = (threesome[1], threesome[0] - threesome[1], threesome[2])
                maps_dict[first_word]['threesomes'].append(threesome)

        return seed_numbers, maps_dict


def map_join(first_map: list, second_map: list):
    map3_list = []
    borders = set()
    for a, a_delta, a_count in first_map:
        borders.add(a + a_delta)
        borders.add(a + a_delta + a_count)
    for b, b_delta, b_count in second_map:
        borders.add(b)
        borders.add(b + b_count)

    borders = sorted(borders)

    segments = []
    for i in range(len(borders) - 1):
        segments.append((borders[i], borders[i + 1]))

    for segment in segments:
        segment_start = segment[0]

        left_delta = 0
        for a, a_delta, a_count in first_map:
            if (a + a_delta) <= segment_start < (a + a_delta + a_count):
                left_delta = a_delta
                break

        right_delta = 0
        for b, b_delta, b_count in second_map:
            if b <= segment_start < (b + b_count):
                right_delta = b_delta
                break

        c = segment_start - left_delta
        c_delta = left_delta + right_delta
        c_count = segment[1] - segment[0]
        map3_list.append((c, c_delta, c_count))
    return map3_list


def build_seed_to_location_map(maps: dict) -> list[tuple]:
    while (next_element := maps['seed']['next']) != 'location':
        first_map = maps['seed']['threesomes']
        second_map = maps[next_element]['threesomes']
        new_map = map_join(first_map, second_map)
        maps['seed']['threesomes'] = new_map
        maps['seed']['next'] = maps[next_element]['next']
    return sorted(maps['seed']['threesomes'], key=lambda x: x[0])


def get_new_number(num: int, threesomes: list[tuple]):
    for start, delta, count in threesomes:
        if num < start:
            continue
        if num >= start + count:
            continue
        return num + delta
    return num


def get_min_location_part1(path: str):
    seeds, maps = get_info(path)
    seed_to_loc_threesomes = build_seed_to_location_map(maps)
    locations = [get_new_number(seed, seed_to_loc_threesomes) for seed in seeds]
    return min(locations)


def pairs(seq: Sequence):
    i = 0
    while i < len(seq) - 1:
        yield seq[i], seq[i + 1]
        i += 2


def get_min_location_part2_v2(path: str):
    seeds, maps = get_info(path)
    seed_to_loc_threesomes = build_seed_to_location_map(maps)
    seed_to_loc_threesomes = sorted(
        seed_to_loc_threesomes,
        key=lambda x: x[0] + x[1]
    )
    seeds = sorted(pairs(seeds), key=lambda x: x[0])
    for start, delta, count in seed_to_loc_threesomes:
        for seed_start, seed_count in seeds:
            if seed_start + seed_count - 1 < start:
                # last seed < first segment seed
                continue
            if seed_start >= start + count:
                # first seed > last segment seed
                continue
            return max(seed_start, start) + delta


if __name__ == '__main__':
    part1_example_result = get_min_location_part1('inputs/seed.example.in')
    print(part1_example_result)  # 35

    part1_result = get_min_location_part1('inputs/seed.in')
    print(part1_result)  # 227653707

    part2_example_result = get_min_location_part2_v2('inputs/seed.example.in')
    print(part2_example_result)  # 46

    part2_result = get_min_location_part2_v2('inputs/seed.in')
    print(part2_result)  # 78775051
