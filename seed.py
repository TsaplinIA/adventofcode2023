import re
from collections import defaultdict
from functools import lru_cache
from typing import Iterable


def get_info(path: str):
    maps_dict = defaultdict(list)
    with open(path) as file:
        first_line = file.readline()
        seed_numbers = tuple([
            int(digit)
            for digit in re.findall(r"\d+", first_line)
        ])
        for map_text in re.finditer(r"(\w+)-to-(\w+) map:([\s\d]*)", file.read()):
            first_word = map_text.group(1)
            second_word = map_text.group(2)
            key = (first_word, second_word)
            for threesome in re.findall(r"(?:\s+\d+){3}", map_text.group(3)):
                threesome = tuple(map(int, threesome.strip().split()))
                maps_dict[key].append(threesome)
            maps_dict[key] = tuple(maps_dict[key])
        return seed_numbers, maps_dict


def get_info_v2(path: str):
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


@lru_cache
def get_dst_num(src_num, threesomes: tuple, step: str):
    for threesome in threesomes:
        if src_num < threesome[1]:
            continue
        if src_num >= threesome[1] + threesome[2]:
            continue
        delta = threesome[0] - threesome[1]
        return src_num + delta
    return src_num


def get_min_num(seeds: list, maps: dict, from_el: str, to_el: str):
    current_list = [(from_el, seed_num) for seed_num in seeds]
    next_list = []
    locations = []
    while current_list:
        for element_name, element_num in current_list:
            for (map_src, map_dst), threesomes in maps.items():
                if map_src != element_name:
                    continue
                dst_num = get_dst_num(element_num, threesomes, element_name)
                if map_dst == to_el:
                    locations.append(dst_num)
                else:
                    next_list.append((map_dst, dst_num))
        current_list = next_list
        next_list = []
    return min(locations)


def get_min_location_part1(path: str):
    seeds, maps = get_info(path)
    return get_min_num(seeds, maps, 'seed', 'location')


def join_all_maps(maps: dict, from_el: str, to_el: str):
    pass


def get_min_location_part1_v2(path: str):
    seeds, maps = get_info_v2(path)
    print(maps)
    return get_min_num(seeds, maps, 'seed', 'location')


def pairs(l: Iterable):
    i = 0
    while i < len(l) - 1:
        yield l[i], l[i + 1]
        i += 2


def get_min_location_part2(path: str):
    seeds, maps = get_info(path)
    new_seeds = []
    for seed_number, seed_offset in pairs(seeds):
        new_seeds.append((seed_number, seed_number + seed_offset - 1))

    new_maps = {
        (el_dst, el_src): tuple([
            (threesome[1], threesome[0], threesome[2])
            for threesome in threesomes
        ])
        for (el_src, el_dst), threesomes in maps.items()
    }

    return get_min_num(new_seeds, new_maps, from_el='location', to_el='seed')
    location = 0
    while True:
        seed_num = get_min_num([location], new_maps, 'location', 'seed')
        print(location, seed_num)
        pass
        for min_seed, max_seed in new_seeds:
            if min_seed <= seed_num <= max_seed:
                return location
        location += 1


if __name__ == '__main__':
    part1_example_result = get_min_location_part1_v2('inputs/seed.example.in')
    print(part1_example_result)  # 35
    #
    # part1_result = get_min_location_part1('inputs/seed.in')
    # print(part1_result)  # 227653707

    # part2_example_result = get_min_location_part2('inputs/seed.example.in')
    # print(part2_example_result)

    # part2_result = get_min_location_part2('inputs/seed.in')
    # print(part2_result)
