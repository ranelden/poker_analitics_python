from treys import Card, Deck, Evaluator
from hand_parser import canonical_hand_parser_pseudo_random

def tirage_simulator(hero_cards, villain_cards):
    #initialiser les objets importante
    deck = Deck()
    evaluator = Evaluator()

    #choix de la main de hero et villain 
    temp_hand_hero, temp_hand_villain = canonical_hand_parser_pseudo_random(hero_cards, villain_cards)
    hand_hero = [Card.new(temp_hand_hero[0]), Card.new(temp_hand_hero[1])]
    hand_villain = [Card.new(temp_hand_villain[0]), Card.new(temp_hand_villain[1])]

    #prepare le paquet
    deck.cards.remove(hand_hero[0])
    deck.cards.remove(hand_hero[1])
    deck.cards.remove(hand_villain[0])
    deck.cards.remove(hand_villain[1])

    #creation du board
    board = deck.draw(5)

    #evalutation des differente mains
    hero_score = 7462 - evaluator.evaluate(board, hand_hero)
    villain_score = 7462 - evaluator.evaluate(board, hand_villain)

    if hero_score > villain_score : result = 1
    elif hero_score < villain_score : result = 0
    elif hero_score == villain_score : result = 0.5
    
    delta_score = hero_score - villain_score
    
    return result, hero_score, villain_score, delta_score
