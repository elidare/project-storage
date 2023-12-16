# And this also I've done by myself!

with open('14.txt', 'r') as f:
    platform = [line.strip() for line in f.readlines()]
    ROUNDED_ROCK = 'O'
    CUBE_SHAPED_ROCK = '#'
    NORTH = 'north'
    SOUTH = 'south'
    WEST = 'west'
    EAST = 'east'

    def count_load(platform):
        load = 0
        for i in range(len(platform)):
            load += platform[i].count(ROUNDED_ROCK) * (len(platform) - i)
        return load

    def tilt_platform(platform, direction):
        # Let's transpose it to work with rows, or switch North to West
        if direction in (NORTH, SOUTH):
            platform = [''.join(r) for r in list(zip(*platform))]

        platform_moved = []
        # Move all the rocks to the West
        for row in platform:
            # Split by the cube-shaped rocks, so they will stay untouched
            moved_row = CUBE_SHAPED_ROCK.join(
                [''.join(sorted(s, reverse=(direction in (NORTH, WEST)))) for s in row.split(CUBE_SHAPED_ROCK)]
            )
            platform_moved.append(moved_row)

        # And transpose the result back again to the North
        if direction in (NORTH, SOUTH):
            platform_moved = [''.join(r) for r in list(zip(*platform_moved))]

        return platform_moved

    def make_cycle(platform):
        platform = tilt_platform(platform, NORTH)
        platform = tilt_platform(platform, WEST)
        platform = tilt_platform(platform, SOUTH)
        platform = tilt_platform(platform, EAST)
        return platform

    # Part 1 - Tilt it to the North
    # platform = tilt_platform(platform, NORTH)
    # Now count the load of rocks
    # print(count_load(platform))

    # Part 2 - make several cycles
    loads = []
    MAGIC_NUMBER = 7
    while True:
        platform = make_cycle(platform)
        # I see that loads eventually got repeated every 7th time, let's fiddle with it
        loads.append(count_load(platform))
        if len(loads) >= MAGIC_NUMBER * 2:
            # Take the last 14 items of the loads and compare them 7 by 7
            repeated = loads[-1 * MAGIC_NUMBER:] == loads[-2 * MAGIC_NUMBER:-1 * MAGIC_NUMBER]
            if repeated:
                break

    index = (len(loads) - 2 * MAGIC_NUMBER) + (1000000000 - (len(loads) - 2 * MAGIC_NUMBER)) % 7 - 1
    print(loads[index])  # Print the load after the 1000000000 cycle
