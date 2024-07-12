# I remember some MD5 puzzle from the 2015 advent Day 5

import hashlib


def part_one():
    START_HASH = '00000'
    PSWD_LEN = 8
    password = ''

    with open('5.txt', 'r') as f:
        room = f.readline().strip()

        i = 0
        while len(password) < PSWD_LEN:
            hash = hashlib.md5((room + str(i)).encode()).hexdigest()
            if hash.startswith(START_HASH):
                password += hash[5]
                print(i, password)
            i += 1

    return password


def part_two():
    START_HASH = '00000'
    PSWD_HIDDEN = '_'
    password = [PSWD_HIDDEN] * 8
    ORD_0, ORD_7 = ord('0'), ord('7')  # I was a bit lazy to think of int-ing hex numbers with low effort

    with open('5.txt', 'r') as f:
        room = f.readline().strip()

        i = 0
        while PSWD_HIDDEN in password:
            hash = hashlib.md5((room + str(i)).encode()).hexdigest()
            if hash.startswith(START_HASH):
                position = hash[5]
                if ORD_0 <= ord(position) <= ORD_7 and password[int(position)] == PSWD_HIDDEN:
                    password[int(hash[5])] = hash[6]
                    print(''.join(password))
            i += 1

    return ''.join(password)


print(part_one())
print(part_two())
