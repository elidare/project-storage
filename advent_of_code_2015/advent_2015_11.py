with open('11.txt', 'r') as f:
    pswd = f.readline()


def get_next_secure_pswd(input):
    ABC = 'abcdefghijklmnopqrstuvwxyz'

    def get_next_pswd(current):
        wrapped = 0
        next_ = ''

        for i in range(len(current)):
            if current[-1 - i] == ABC[-1]:  # z-letter
                next_ += ABC[0]
                wrapped += 1
            else:
                next_ += ABC[ABC.find(current[-1 - i]) + 1]
                break
        # Part that wasn't incremented + all the incremented letters reversed, because we were going backwards
        return current[:len(current) - wrapped - 1] + next_[::-1]

    def check_pswd(pswd):
        if any(map(pswd.count, list('iol'))):
            return False

        has_straight = False
        for i in range(len(pswd)):
            combination = pswd[i:i + 3]
            if len(combination) == 3 and ABC.count(combination) > 0:
                has_straight = True
                break

        doubles = set()
        for i in range(1, len(pswd)):
            if pswd[i - 1] == pswd[i]:
                doubles.add(pswd[i])

        return has_straight and len(doubles) >= 2

    current_password = get_next_pswd(input)
    while not check_pswd(current_password):
        current_password = get_next_pswd(current_password)

    return current_password


print(get_next_secure_pswd(pswd))
