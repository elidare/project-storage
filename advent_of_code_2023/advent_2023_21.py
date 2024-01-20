# Part 1 I did by myself somehow.
# Part 2 I gave up, I just gave up.

from collections import deque
import numpy as np


with open('21.txt', 'r') as f:
    garden_map = [list(line.strip()) for line in f.readlines()]
    ROCK = '#'
    PLOT = '.'
    START = 'S'
    MAX_STEPS_1 = 6  # 64
    MAX_STEPS_2 = 26501365
    map_length_y = len(garden_map)
    map_length_x = len(garden_map[0])

    for y in range(map_length_y):
        for x in range(map_length_x):
            if garden_map[y][x] == START:
                start_plot = (y, x)
                garden_map[y][x] = PLOT
                break

    def part_one():
        provisional_plots = [start_plot]
        for step in range(MAX_STEPS_1):
            plots = []
            for plot_y, plot_x in provisional_plots:
                if plot_y - 1 >= 0 and garden_map[plot_y - 1][plot_x] != ROCK and \
                        (plot_y - 1, plot_x) not in plots:
                    plots.append((plot_y - 1, plot_x))
                if plot_y + 1 < map_length_y and garden_map[plot_y + 1][plot_x] != ROCK and \
                        (plot_y + 1, plot_x) not in plots:
                    plots.append((plot_y + 1, plot_x))
                if plot_y - 1 >= 0 and garden_map[plot_y][plot_x - 1] != ROCK and \
                        (plot_y, plot_x - 1) not in plots:
                    plots.append((plot_y, plot_x - 1))
                if plot_y + 1 < map_length_x and garden_map[plot_y][plot_x + 1] != ROCK and \
                        (plot_y, plot_x + 1) not in plots:
                    plots.append((plot_y, plot_x + 1))
                provisional_plots = list(set(plots))

        return len(provisional_plots)

    def part_two():
        # I gave up and used this solution https://github.com/mgtezak/Advent_of_Code/blob/master/2023/Day_21.py
        # Wouldn't say I could have done it myself... at least I've tried to understand it...
        x_final, remainder = divmod(MAX_STEPS_2, map_length_x)
        border_crossings = [remainder, remainder + map_length_x, remainder + 2 * map_length_x]

        visited = set()
        queue = deque([(map_length_x // 2, map_length_x // 2)])
        total = [0, 0]  # [even, odd]

        Y = []
        for step in range(1, border_crossings[-1] + 1):
            for _ in range(len(queue)):
                x, y = queue.popleft()
                for i, j in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if (i, j) in visited or garden_map[i % map_length_y][j % map_length_x] == '#':
                        continue

                    visited.add((i, j))
                    queue.append((i, j))
                    total[step % 2] += 1

            if step in border_crossings:
                Y.append(total[step % 2])

        X = [0, 1, 2]
        coefficients = np.polyfit(X, Y, deg=2)  # get coefficients for quadratic equation y = a*x^2 + bx + c
        y_final = np.polyval(coefficients, x_final)  # using coefficients, get y value at x_final
        return y_final.round().astype(int)

    print(part_one())
    print(part_two())
