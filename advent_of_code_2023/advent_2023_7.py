from functools import cmp_to_key

with open('7.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]
    hands = []
    result = 0

    def get_hand_type(cards_stack, jokers=False):
        three_of_a_kind = False
        pair = False
        if jokers:
            # If there is any J in a hand, replace it with the most winning cards
            jokers_q = cards_stack.pop('J', 0)
            if jokers_q == 5:
                return 1  # Five of a kind
            cards_stack[list(cards_stack.keys())[0]] += jokers_q
        for card, q in cards_stack.items():
            if q == 5:
                return 1  # Five of a kind
            if q == 4:
                return 2  # Four of a kind
            if q == 3:
                three_of_a_kind = True
                continue
            if q == 2 and three_of_a_kind:
                return 3  # Fullhouse
            if q == 2 and pair:
                return 5  # Two pair
            if q == 2:
                pair = True
                continue
            if q == 1 and three_of_a_kind:
                return 4  # Three of a kind
            if q == 1 and pair:
                return 6  # One pair
            return 7  # High card

    def sort_rank_part_1(hand_1, hand_2):
        order = 'AKQJT98765432'
        return sort_rank(hand_1, hand_2, order)

    def sort_rank_part_2(hand_1, hand_2):
        order = 'AKQT98765432J'
        return sort_rank(hand_1, hand_2, order)

    def sort_rank(hand_1, hand_2, order):
        # Weakest hand gets the lower rank
        if hand_1['hand_type'] < hand_2['hand_type']:
            return 1
        if hand_1['hand_type'] > hand_2['hand_type']:
            return -1
        for i in range(len(hand_1['hand'])):
            return 1 if order.find(hand_1['hand'][i]) < order.find(hand_2['hand'][i]) else -1

    for line in lines:
        cards, bid = line.split()[0], int(line.split()[1])
        hand = {'hand': cards, 'bid': bid}
        hands.append(hand)

        cards_stack = {card: cards.count(card) for card in cards}
        cards_stack_sorted = dict(sorted(cards_stack.items(), key=lambda x: x[1], reverse=True))

        # Part 1
        # hand['hand_type'] = get_hand_type(cards_stack_sorted)

        # Part 2
        hand['hand_type'] = get_hand_type(cards_stack_sorted, jokers=True)

    # Part 1
    # hands_sorted = sorted(hands, key=cmp_to_key(sort_rank_part_1))

    # Part 2
    hands_sorted = sorted(hands, key=cmp_to_key(sort_rank_part_2))

    for i in range(len(hands_sorted)):
        result += (i + 1) * hands_sorted[i]['bid']

    print(result)
