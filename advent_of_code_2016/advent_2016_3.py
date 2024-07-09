def part_one():
    valid_triangles = 0

    with open('3.txt', 'r') as f:
        triangles = [[int(t) for t in l.strip().split()] for l in f.readlines()]

        for t in triangles:
            t = sorted(t)

            if t[0] + t[1] > t[2]:
                valid_triangles += 1

    return valid_triangles


def part_two():
    valid_triangles = 0

    with open('3.txt', 'r') as f:
        triangles = [[int(t) for t in l.strip().split()] for l in f.readlines()]
        # Transpose columns into rows
        triangles = [list(c) for c in list(zip(*triangles))]

        for column in triangles:
            for i in range(0, len(column), 3):
                triangle = sorted([column[i], column[i + 1], column[i + 2]])
                if triangle[0] + triangle[1] > triangle[2]:
                    valid_triangles += 1

    return valid_triangles


print(part_one())
print(part_two())
