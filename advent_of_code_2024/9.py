import time


MASK = '.'

with open('9.txt', 'r') as f:
    disk = f.readline().strip()


def part_1():
    start_time = time.time()
    # Let's convert the disk just like in the example
    # so that is rearranged as 0..111....22222
    blocks = list()
    for i in range(0, len(disk), 2):
        blocks += [str(i // 2)] * int(disk[i])
        if i + 1 < len(disk):
            blocks += [MASK] * int(disk[i + 1])

    # Now let's just go through the array and switch numbers and dots
    i = 0
    while i < len(blocks):
        # If the last one is a dot, cut it off
        if blocks[-1] == MASK:
            blocks = blocks[:-1]
            continue
        # Switch
        if blocks[i] == MASK:
            blocks[i] = blocks[-1]
            blocks = blocks[:-1]
        i += 1

    count = 0
    for i in range(len(blocks)):
        count += i * int(blocks[i])

    print("--- %s seconds ---" % (time.time() - start_time))
    return count


def part_2():
    start_time = time.time()
    # Let's do the list slightly different
    # [['0', '0'], ['.', '.', '.'], ...]
    blocks = list()
    for i in range(0, len(disk), 2):
        if disk[i] != '0':
            blocks.append([str(i // 2)] * int(disk[i]))
        if i + 1 < len(disk) and disk[i + 1] != '0':
            blocks.append([MASK] * int(disk[i + 1]))

    # Let's go backwards and try to find the suitable place
    # Oh that will take hell of a time
    index = len(blocks) - 1
    while True:
        if index == 0:
            break

        last_file = blocks[index]
        if last_file[0] != MASK:  # We move file only if it is actually a file
            for j in range(len(blocks)):
                # If we met the file we want to move, break
                if index == j:
                    break
                # We are searching only for dots of appropriate length
                if ''.join(blocks[j]).find(MASK) == -1 or len(blocks[j]) < len(last_file):
                    continue

                if len(blocks[j]) == len(last_file):
                    blocks[j], blocks[index] = last_file, blocks[j]
                    break
                else:  # If len(blocks[j]) > len(last_file)
                    diff = len(blocks[j]) - len(last_file)
                    blocks[j], blocks[index] = last_file, blocks[j][:len(last_file)]
                    blocks[j + 1:j + 1] = [[MASK] * diff]  # Inserting the diff of the '.'
                    index += 1  # Insert fixing
                    break

        index -= 1

    count = 0
    full_index = 0
    for b in blocks:
        for n in b:
            if n != MASK:
                count += int(n) * full_index
            full_index += 1

    print("--- %s seconds ---" % (time.time() - start_time))
    return count


print('Result:', part_1())  # 6.063064098358154 seconds
print('Result:', part_2())  # 10.766049861907959 seconds
