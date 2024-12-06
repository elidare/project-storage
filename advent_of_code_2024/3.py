import re


multiplications = 0
multiplications_enabled = 0
DONT = "don't()"
DO = "do()"

with (open('3.txt', 'r') as f):
    while True:
        line = f.readline().strip()

        if not line:
            break

        # Part 1
        for m in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", line):
            multiplications += int(m[0]) * int(m[1])

        # Part 2
        # Thank you reddit that you teach me how to use regexps and
        # not cause another problem
        enabled = True
        for a, b, do, dont in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)|(do\(\))|(don't\(\))", line):
            if do:
                enabled = True
            if dont:
                enabled = False
            if a and b and enabled:
                multiplications_enabled += int(a) * int(b)


print(multiplications)
print(multiplications_enabled)
