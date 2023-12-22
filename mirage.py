def lines(path: str):
    with open(path) as file:
        while line := file.readline():
            yield line.strip()


def seqs(path: str):
    for line in lines(path):
        yield list(map(int, line.strip().split()))


def get_seqs(seq: list) -> list[list]:
    all_zeros = False
    seqs = [seq]
    while not all_zeros:
        all_zeros = True
        cur_seq_idx = len(seqs)
        deltas = []

        for i in range(len(seqs[cur_seq_idx - 1]) - 1):
            delta = seqs[cur_seq_idx - 1][i + 1] - seqs[cur_seq_idx - 1][i]
            all_zeros = all_zeros and delta == 0
            deltas.append(delta)
        seqs.append(deltas)
    return seqs


def get_next(seq: list):
    seqs = get_seqs(seq)

    d = 0
    while seqs:
        d += seqs.pop(-1)[-1]
    return d


def part_1(path: str):
    return sum(map(get_next, seqs(path)))


def get_previous(seq: list):
    seqs = get_seqs(seq)

    d = 0
    while seqs:
        d = seqs.pop(-1)[0] - d
    return d


def part_2(path: str):
    return sum(map(get_previous, seqs(path)))


if __name__ == '__main__':
    res_part1_example = part_1('inputs/mirage.example.in')
    print(res_part1_example)

    res_part1 = part_1('inputs/mirage.in')
    print(res_part1)

    res_part2_example = part_2('inputs/mirage.example.in')
    print(res_part2_example)

    res_part2 = part_2('inputs/mirage.in')
    print(res_part2)
