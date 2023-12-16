# I am so happy to solve it all by myself
# And I did have an insight of using transposed matrix instead of going through columns
# Wheeeeeeeeeeeeeee

with open('13.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

    patterns = []
    pattern = None
    lines.append('')  # A hack to add the last pattern to the array
    for line in lines:
        if not pattern:
            pattern = []
        if line:
            pattern.append(line)
        else:
            patterns.append(pattern)
            pattern = None

    # Part 1
    def compare_rows(i, j, pattern):
        if i < 0 or j >= len(pattern):  # We have reached the end and previous rows are reflected
            return True
        if pattern[i] != pattern[j]:
            return False
        return compare_rows(i - 1, j + 1, pattern)

    # Part 2
    def compare_rows_smudged(i, j, pattern, fixed):
        if i < 0 or j >= len(pattern):  # We have reached the end and previous rows are reflected
            return fixed  # We take it as a reflection line only if we have something fixed
        if pattern[i] != pattern[j]:
            diff = sum([0 if pair[0] == pair[1] else 1 for pair in list(zip(pattern[i], pattern[j]))])
            if diff == 1 and not fixed:
                fixed = True
                return compare_rows_smudged(i - 1, j + 1, pattern, fixed)
            return False
        return compare_rows_smudged(i - 1, j + 1, pattern, fixed)

    def check_horizontal_reflection(pattern):
        for possible_line in range(1, len(pattern)):
            # if compare_rows(possible_line - 1, possible_line, pattern):  # Part 1
            if compare_rows_smudged(possible_line - 1, possible_line, pattern, False):  # Part 2
                return possible_line
        return None

    result = 0

    for pattern in patterns:
        # Checking horizontal reflection
        horizontal_reflection_line = check_horizontal_reflection(pattern)

        if horizontal_reflection_line:
            result += 100 * horizontal_reflection_line
            continue

        # Checking vertical reflection
        # Let's transpose this pattern and go check for horizontal reflection
        pattern = [''.join(r) for r in list(zip(*pattern))]
        vertical_reflection_line = check_horizontal_reflection(pattern)
        if vertical_reflection_line:
            result += vertical_reflection_line

    print(result)
