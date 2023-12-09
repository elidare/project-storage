with open('4.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]
    points = 0
    scratchcards = dict()

    for line in lines:
        card, numbers = line.split(':')[0], line.split(':')[1]
        card_number = card.split()[1]
        scratchcards[card_number] = 1 if card_number not in scratchcards else scratchcards[card_number] + 1
        numbers = [n.strip() for n in numbers.strip().split('|')]
        winning_numbers = set(numbers[0].split())
        given_numbers = set(numbers[1].split())
        intersection = winning_numbers.intersection(given_numbers)

        if len(intersection) > 0:
            # Part 1
            points += 2 ** (len(intersection) - 1)

            # Part 2
            for i in range(len(intersection)):
                add_card = str(int(card_number) + i + 1)
                scratchcards[add_card] = scratchcards[card_number] if add_card not in scratchcards else \
                    scratchcards[add_card] + scratchcards[card_number]

    # print(points)
    print(sum(scratchcards.values()))
