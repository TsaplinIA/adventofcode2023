maps = {
    (0, 1): [(0, 3, 4)],
    (1, 2): [(3, -2, 2), (5, +2, 4)]
}


def map_join(first_map: list, second_map: list):
    map3_list = []
    borders = set()
    for a, a_delta, a_count in first_map:
        borders.add(a+a_delta)
        borders.add(a+a_delta+a_count)
    for b, b_delta, b_count in second_map:
        borders.add(b)
        borders.add(b+b_count)

    borders = sorted(borders)

    segments = []
    for i in range(len(borders)-1):
        segments.append((borders[i], borders[i+1]))

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


map_join(*maps.items())
