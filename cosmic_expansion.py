def elements(path: str):
    with open(path) as file:
        line_idx = 0
        while line := file.readline():
            for char_idx, char in enumerate(line.strip()):
                yield line_idx, char_idx, char
            line_idx += 1


def get_sum_of_deltas(path: str, scale: int):
    rows = []
    cols = []
    for line_idx, char_idx, char in elements(path):
        current = 1 if char != '.' else scale
        if char_idx < len(cols):
            cols[char_idx] = min(cols[char_idx], current)
        else:
            cols.append(current)

        if line_idx < len(rows):
            rows[line_idx] = min(rows[line_idx], current)
        else:
            rows.append(current)

    for r_idx in range(1, len(rows)):
        rows[r_idx] += rows[r_idx - 1]
    for c_idx in range(1, len(cols)):
        cols[c_idx] += cols[c_idx - 1]

    galaxies = []
    sum_of_deltas = 0
    for line_idx, char_idx, char in elements(path):
        if char == '.':
            continue
        sum_of_deltas += sum(map(lambda galaxy: abs(rows[line_idx] - rows[galaxy[0]]), galaxies))
        sum_of_deltas += sum(map(lambda galaxy: abs(cols[char_idx] - cols[galaxy[1]]), galaxies))
        galaxies.append((line_idx, char_idx))
    return sum_of_deltas


if __name__ == '__main__':
    res_part1_example = get_sum_of_deltas('inputs/cosmic_expansion.example.in', 2)
    print(res_part1_example)  # 374

    res_part1 = get_sum_of_deltas('inputs/cosmic_expansion.in', 2)
    print(res_part1)  # 9177603

    res_part2_example = get_sum_of_deltas('inputs/cosmic_expansion.example.in', 1_000_000)
    print(res_part2_example)  # 82000210

    res_part2 = get_sum_of_deltas('inputs/cosmic_expansion.in', 1_000_000)
    print(res_part2)  # 632003913611
