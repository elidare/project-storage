# Trying to copy-paste Day 17, but it's not working
# because I need the longest, not the shortest path

# Let's try recursion!
# Both parts are done using following solutions
# Thank you reddit!
# https://www.reddit.com/r/adventofcode/comments/18oy4pc/comment/keob34r/

import sys


sys.setrecursionlimit(10000)

with open('23.txt', 'r') as f:
    grid = [line.strip() for line in f.readlines()]
    m = len(grid)
    n = len(grid[0])
    PATH = '.'
    FOREST = '#'
    SLOPES = {'>': [0, 1], '<': [0, -1], '^': [-1, 0], 'v': [1, 0]}

    start = (0, grid[0].find(PATH))
    end = (m - 1, grid[m - 1].find(PATH))
    directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]

    def part_one():
        def next_step(current, path, steps):
            if current == end:
                return steps
            longest_steps = -1
            x, y = current[0], current[1]
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy

                if new_x < 0 or new_y < 0 or new_x >= m or new_y >= n:
                    continue

                next_tile = grid[new_x][new_y]

                if next_tile in SLOPES:
                    dxx, dyy = SLOPES[next_tile][0], SLOPES[next_tile][1]
                    if dx * dxx == -1 or dy * dyy == -1:
                        continue

                if next_tile == FOREST:
                    continue

                if (new_x, new_y) in path:
                    continue

                new_path = set(path)
                new_path.add((new_x, new_y))
                new_steps = next_step((new_x, new_y), new_path, steps + 1)
                longest_steps = max(longest_steps, new_steps)
            return longest_steps

        path = set()
        path.add(start)
        return next_step(start, path, 0)

    def part_two():
        def adjust_pos(x, y, dir):
            dx, dy = SLOPES[dir]
            return x + dx, y + dy

        def reverse_dir(cur_dir):
            idx = 'v>^<'.index(cur_dir)
            return '^<v>'[idx]

        def possible_dirs(x, y, current_direction):
            next_dirs = []
            backtrack = reverse_dir(current_direction)
            for dir in 'v>^<':
                if dir == backtrack:
                    continue  # can't backtrack

                new_x, new_y = adjust_pos(x, y, dir)
                if new_x < 0 or new_y < 0 or new_x >= m or new_y >= n:
                    continue

                tile = grid[new_x][new_y]

                if tile != FOREST:
                    next_dirs.append(dir)
            return next_dirs

        def find_nodes():
            visited = set()
            nodes = {}
            queue = [(start, 'v')]  # position, direction

            while queue:
                from_node, current_direction = queue.pop()
                if (from_node, current_direction) in visited:
                    continue

                visited.add((from_node, current_direction))
                x, y = from_node
                steps = 0

                while True:
                    steps += 1
                    x, y = adjust_pos(x, y, current_direction)
                    next_dirs = possible_dirs(x, y, current_direction)

                    if len(next_dirs) > 1 or (x, y) == end:
                        to_node = (x, y)

                        if from_node not in nodes:
                            nodes[from_node] = []
                        nodes[from_node].append((to_node, steps))
                        if to_node not in nodes:
                            nodes[to_node] = []
                        nodes[to_node].append((from_node, steps))
                        visited.add((to_node, reverse_dir(current_direction)))
                        for dir in next_dirs:
                            if (to_node, dir) not in visited:
                                queue.append((to_node, dir))
                        break
                    current_direction = next_dirs[0]

            return nodes

        def take_a_hike(nodes):
            cache = {}
            longest_walk = 0
            visited = set()
            visited.add(start)
            queue = [(start, 0, frozenset(visited))]
            while len(queue) > 0:
                current_node, steps, visited = queue.pop()
                if current_node == end:
                    if steps > longest_walk:
                        print(steps)
                        longest_walk = steps
                    continue
                if cache.get((current_node, visited), -1) >= steps:
                    continue  # already have same or longer path
                cache[(current_node, visited)] = steps
                new_visited = set(visited)
                new_visited.add(current_node)
                new_visited = frozenset(new_visited)
                for next_node, steps_to_node in nodes[current_node]:
                    if next_node in new_visited:
                        continue  # in my set of visited nodes
                    new_steps = steps + steps_to_node
                    if cache.get((next_node, new_visited), 0) >= new_steps:
                        continue  # already have same or longer path
                    queue.append((next_node, new_steps, new_visited))
            return longest_walk

        nodes = find_nodes()
        return take_a_hike(nodes)

    print('Steps:', part_one())
    print('Steps:', part_two())


