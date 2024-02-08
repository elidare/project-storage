with open('18.txt', 'r') as f:
    grid = [list(a.strip()) for a in f.readlines()]
    m = len(grid)
    n = len(grid[0])
    ON = '#'
    OFF = '.'
    TIMES = 100


def part_one():
    def switch():
        # Make snapshot of the current state
        grid_snapshot = [list(''.join(r)) for r in grid]
        for i in range(m):
            for j in range(n):
                neighbors_on = 0
                for di, dj in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    k, l = i + di, j + dj
                    if 0 <= k < m and 0 <= l < n and grid_snapshot[k][l] == ON:
                        neighbors_on += 1

                if grid_snapshot[i][j] == ON:
                    grid[i][j] = ON if 2 <= neighbors_on <= 3 else OFF
                else:
                    grid[i][j] = ON if neighbors_on == 3 else OFF

    for _ in range(TIMES):
        switch()

    return sum([''.join(r).count(ON) for r in grid])


def part_two():
    # Turn on corner lights
    for i, j in [(0, 0), (m - 1, 0), (0, n - 1), (m - 1, n - 1)]:
        grid[i][j] = ON

    def switch():
        # Make snapshot of the current state
        grid_snapshot = [list(''.join(r)) for r in grid]
        for i in range(m):
            for j in range(n):
                neighbors_on = 0
                for di, dj in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    k, l = i + di, j + dj
                    if 0 <= k < m and 0 <= l < n and grid_snapshot[k][l] == ON:
                        neighbors_on += 1
                # Fixme
                if grid_snapshot[i][j] == ON:
                    grid[i][j] = ON if 2 <= neighbors_on <= 3 else OFF
                else:
                    grid[i][j] = ON if neighbors_on == 3 else OFF

                # Explicitly declaring corner lights ON
                if (i, j) in [(0, 0), (m - 1, 0), (0, n - 1), (m - 1, n - 1)]:
                    grid[i][j] = ON

    for _ in range(TIMES):
        switch()

    return sum([''.join(r).count(ON) for r in grid])


print(part_one())
print(part_two())
