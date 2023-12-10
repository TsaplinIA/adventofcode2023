import re


def get_info(path: str):
    node_map = {}
    with open(path) as file:
        rl = file.readline().strip()
        for C, L, R in re.findall(r'((?:\w+){3}) = \(((?:\w+){3}), ((?:\w+){3})\)', file.read()):
            node_map[C] = {
                'L': L,
                'R': R,
            }
    return rl, node_map


def step_counter(loop: str, node_map: dict):
    current_node = 'AAA'
    step_count = 0
    while current_node != 'ZZZ':
        current_node = node_map[current_node][loop[step_count % len(loop)]]
        step_count += 1
    return step_count


if __name__ == '__main__':
    part1_example_result = step_counter(*get_info('inputs/haunted_wasteland.example.in'))
    print(part1_example_result)  # 6

    part1_result = step_counter(*get_info('inputs/haunted_wasteland.in'))
    print(part1_result)
