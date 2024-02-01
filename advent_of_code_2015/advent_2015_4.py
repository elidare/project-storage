import hashlib


with open('4.txt', 'r') as f:
    input = f.readline().strip()

    def get_number(start):
        # Let's try bruteforce
        i = 0
        while not hashlib.md5((input + str(i)).encode()).hexdigest().startswith(start):
            i += 1

        return i

    print(get_number('00000'))
    print(get_number('000000'))
