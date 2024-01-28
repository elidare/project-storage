# Part 1 was finally easy enough to do it all by myself!
# And Part 2 is a hard one :(
# Although I have read the detailed explanations from the following comment,
# and now I can code it!
# https://www.reddit.com/r/adventofcode/comments/18pnycy/comment/khlrstp/?utm_source=share&utm_medium=web2x&context=3
import numpy as np


with open('24.txt', 'r') as f:
    stone_data = [line.strip() for line in f.readlines()]
    stones_lines = list()

    for s in stone_data:
        p, v = s.split('@')
        px, py, pz = [int(_.strip()) for _ in p.strip().split(',')]
        vx, vy, vz = [int(_.strip()) for _ in v.strip().split(',')]

        stones_lines.append({
            'px': px, 'py': py, 'pz': pz,
            'vx': vx, 'vy': vy, 'vz': vz,
        })

    def part_one():
        # test_area = (7, 27)
        test_area = (200000000000000, 400000000000000)
        intersections = 0

        for s in stones_lines:
            m = s['vy'] / s['vx']
            c = s['py'] - s['px'] * m
            # y = a * x + b
            s['m'] = m
            s['c'] = c

        for i in range(len(stones_lines)):
            for j in range(i + 1, len(stones_lines)):
                line_1, line_2 = stones_lines[i], stones_lines[j]
                if line_1['m'] == line_2['m']:
                    # The lines are the same or they are parallel
                    continue

                x = (line_1['c'] - line_2['c']) / (line_2['m'] - line_1['m'])
                y = line_1['m'] * x + line_1['c']

                if line_1['vx'] < 0 and x > line_1['px'] or \
                    line_1['vx'] > 0 and x < line_1['px'] or \
                    line_2['vx'] < 0 and x > line_2['px'] or \
                    line_2['vx'] > 0 and x < line_2['px']:
                    # An intersection happened in the past
                    continue

                if test_area[0] <= x <= test_area[1] and test_area[0] <= y <= test_area[1]:
                    intersections += 1

        return intersections

    def part_two():
        # For the Cramer equation we would need 4 hailstones
        s0, s1, s2, s3 = stones_lines[1:5]
        # The number are too big, so the answer floats for 1-2.
        # Equations for hailstones 1 to 4 gave the answer that was accepted.

        # Coefficients look like (Thank you reddit!)
        # vy0 - vy1   vx1 - vx0   0           py1 - py0   px0 - px1   0         = px0*vy0 - py0*vx0 - px1*vy1 + py1*vx1
        # vz0 - vz1   0           vx1 - vx0   pz1 - pz0   0           px0 - px1 = px0*vz0 - pz0*vx0 - px1*vz1 + pz1*vx1
        # vy0 - vy2   vx2 - vx0   0           py2 - py0   px0 - px2   0         = px0*vy0 - py0*vx0 - px2*vy2 + py2*vx2
        # vz0 - vz2   0           vx2 - vx0   pz2 - pz0   0           px0 - px2 = px0*vz0 - pz0*vx0 - px2*vz2 + pz2*vx2
        # vy0 - vy3   vx3 - vx0   0           py3 - py0   px0 - px3   0         = px0*vy0 - py0*vx0 - px3*vy3 + py3*vx3
        # vz0 - vz3   0           vx3 - vx0   pz3 - pz0   0           px0 - px3 = px0*vz0 - pz0*vx0 - px3*vz3 + pz3*vx3

        px0, px1, px2, px3 = s0['px'], s1['px'], s2['px'], s3['px']
        vx0, vx1, vx2, vx3 = s0['vx'], s1['vx'], s2['vx'], s3['vx']
        py0, py1, py2, py3 = s0['py'], s1['py'], s2['py'], s3['py']
        vy0, vy1, vy2, vy3 = s0['vy'], s1['vy'], s2['vy'], s3['vy']
        pz0, pz1, pz2, pz3 = s0['pz'], s1['pz'], s2['pz'], s3['pz']
        vz0, vz1, vz2, vz3 = s0['vz'], s1['vz'], s2['vz'], s3['vz']

        # Let's just use numpy
        a = np.array([[vy0 - vy1, vx1 - vx0, 0, py1 - py0, px0 - px1, 0],
                     [vz0 - vz1, 0, vx1 - vx0, pz1 - pz0, 0, px0 - px1],
                     [vy0 - vy2, vx2 - vx0, 0, py2 - py0, px0 - px2, 0],
                     [vz0 - vz2, 0, vx2 - vx0, pz2 - pz0, 0, px0 - px2],
                     [vy0 - vy3, vx3 - vx0, 0, py3 - py0, px0 - px3, 0],
                     [vz0 - vz3, 0, vx3 - vx0, pz3 - pz0, 0, px0 - px3]])
        b = np.array([px0*vy0 - py0*vx0 - px1*vy1 + py1*vx1, px0*vz0 - pz0*vx0 - px1*vz1 + pz1*vx1,
                      px0*vy0 - py0*vx0 - px2*vy2 + py2*vx2, px0*vz0 - pz0*vx0 - px2*vz2 + pz2*vx2,
                      px0*vy0 - py0*vx0 - px3*vy3 + py3*vx3, px0*vz0 - pz0*vx0 - px3*vz3 + pz3*vx3])

        pxr, pyr, pzr, vxr, vyr, vzr = [round(x) for x in np.linalg.solve(a, b)]

        return pxr + pyr + pzr

    print(part_one())
    print(part_two())



