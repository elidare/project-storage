# Part 1
def is_safe(levels):
    asc = levels[0] < levels[1]
    desc = levels[0] > levels[1]

    for i in range(1, len(levels)):
        if abs(levels[i] - levels[i - 1]) < 1 or abs(levels[i] - levels[i - 1]) > 3:
            return False

        if asc and levels[i] < levels[i - 1] or desc and levels[i] > levels[i - 1]:
            return False

    return True


# Part 2
def maybe_safe(levels):
    if is_safe(levels):
        return True

    for i in range(len(levels)):
        l = levels[:]
        l.pop(i)
        if is_safe(l):
            return True

    return False


safe_amount = 0
maybe_safe_amount = 0

with open('2.txt', 'r') as f:
    while True:
        line = f.readline().strip()

        if not line:
            break

        levels = [int(i) for i in line.split()]

        if is_safe(levels):
            safe_amount += 1

        if maybe_safe(levels):
            maybe_safe_amount += 1

print(safe_amount)
print(maybe_safe_amount)
