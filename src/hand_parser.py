import random

def parse_canonical_hand(canonical_hand, taken_cards):
    # there might be an error there, i haven t made clear test on every possibility
    colors = ['s', 'h', 'd', 'c']

    while True:
        hand = []

        if len(canonical_hand) == 3:
            r1, r2, t = canonical_hand

            if t == 's':
                c = random.choice(colors)
                hand = [r1 + c, r2 + c]

            elif t == 'o':
                c1 = random.choice(colors)
                c2 = random.choice([c for c in colors if c != c1])
                hand = [r1 + c1, r2 + c2]

        elif len(canonical_hand) == 2:
            r = canonical_hand[0]
            c1, c2 = random.sample(colors, 2)
            hand = [r + c1, r + c2]

        else:
            raise ValueError("invalid canonical hand")

        # CHECK COLLISION EXACTE
        if not any(card in taken_cards for card in hand):
            taken_cards.update(hand)
            return hand

def canonical_hand_parser_pseudo_random(canonical_hand_hero, canonical_hand_villain):
    taken_cards = set()

    hero_hand = parse_canonical_hand(canonical_hand_hero, taken_cards)
    villain_hand = parse_canonical_hand(canonical_hand_villain, taken_cards)

    return hero_hand, villain_hand