# https://github.com/mgtezak/Advent_of_Code/blob/master/2023/Day_21.py
# https://github.com/CalSimmon/advent-of-code/blob/main/2023/day_21/solution.py

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
        return 0


    # print(part_one())
    print(part_two())
