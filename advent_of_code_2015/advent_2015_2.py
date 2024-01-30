with open('2.txt', 'r') as f:
    gifts = [l.strip() for l in f.readlines()]

    def part_one():
        total_paper = 0
        for gift in gifts:
            l, w, h = [int(m) for m in gift.split('x')]
            min_side = min(l * w, w * h, h * l)
            total_paper += 2 * l * w + 2 * w * h + 2 * h * l + min_side

        return total_paper

    def part_two():
        total_ribbon = 0
        for gift in gifts:
            l, w, h = [int(m) for m in gift.split('x')]
            min_perimeter = min(2 * (l + w), 2 * (w + h), 2 * (h + l))
            total_ribbon += min_perimeter + l * w * h

        return total_ribbon


    print(part_one())
    print(part_two())
