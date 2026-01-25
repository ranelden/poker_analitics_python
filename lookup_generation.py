import numpy as np
import json
import random
from datetime import datetime
from pathlib import Path
from treys import Card, Evaluator, Deck
import os
import matplotlib.pyplot as plt

os.makedirs("data", exist_ok=True)

# Load or initialize hand matrix
def load_hand_matrix():
    try :
        hand_matrix = np.load("data/hand_matrix.npy", allow_pickle=True)
        print("Hand matrix loaded from file.")
    except Exception as e :
        print(e)
        hand_matrix = None

    if hand_matrix is None:

        carte = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

        hand_matrix = np.empty((13, 13), dtype=object)

        for i in range(13):
            hand_matrix[i][i] = f"{carte[i]}{carte[i]}"

        for i in range(13):
            for j in range(i + 1, 13):
                hand_matrix[i][j] = f"{carte[i]}{carte[j]}s"
                hand_matrix[j][i] = f"{carte[i]}{carte[j]}o"

        np.save("data/hand_matrix.npy", hand_matrix)

        return hand_matrix

# Load or initialize equity matrix
def load_equity_matrix():   
    try :
        equity_matrix = np.load("data/equity_matrix.npy", allow_pickle=True)
        print("equity_matrix loaded from file.")
    except Exception as e :
        print(e)
        equity_matrix = None

    if equity_matrix is None:

        equity_matrix = np.empty((13, 13), dtype=object)

        for i in range(13):
            for j in range(13):
                equity_matrix[i][j] = np.empty((169, 22), dtype=float)
        np.save("data/equity_matrix.npy", equity_matrix)

    return equity_matrix

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

# Simulate equity calculations
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

def monte_carlo_experience(hero_cards, villain_cards, num_simulations=1000): # study the variation of num_simulations and closeness of true

    stats_matrix = np.empty((num_simulations, 4))
    #colonnes : equity, hero_score, villain_score, delta_score

    #generation de stats
    count = 0
    sum_equity = 0
    for i in stats_matrix: 
        i[0], i[1], i[2], i[3] = tirage_simulator(hero_cards, villain_cards)
        count += 1
        sum_equity += i[0]
        print(f"Simulation for {hero_cards} vs {villain_cards} : {count/num_simulations*100:.2f}%  completed : {sum_equity/count:.5f}", flush=True, end="\r")
    print(end="\n")
    #recuperation de la moyenne empyrique, et ou l equité
    equity = np.mean(stats_matrix[:,0])

    #hero stats global
    score_moyen_hero = np.mean(stats_matrix[:,1])
    variance_hero = np.var(stats_matrix[:,1])
    ecart_type_hero = np.std(stats_matrix[:,1])

    #hero stats victory/defeat
    score_moyen_hero_victory = np.mean(stats_matrix[stats_matrix[:,0]==1][:,1])
    score_moyen_hero_defeat = np.mean(stats_matrix[stats_matrix[:,0]==0][:,1])
    variance_hero_victory = np.var(stats_matrix[stats_matrix[:,0]==1][:,1])
    variance_hero_defeat = np.var(stats_matrix[stats_matrix[:,0]==0][:,1])
    ecart_type_hero_victory = np.std(stats_matrix[stats_matrix[:,0]==1][:,1])
    ecart_type_hero_defeat = np.std(stats_matrix[stats_matrix[:,0]==0][:,1])

    #delta stats
    delta_score_moyen = np.mean(stats_matrix[:,3])
    delta_score_moyen_victory = np.mean(stats_matrix[stats_matrix[:,0]==1][:,3])
    delta_score_moyen_defeat = np.mean(stats_matrix[stats_matrix[:,0]==0][:,3])

    #boxplot data min et max
    min_score_hero = np.min(stats_matrix[:,1])
    max_score_hero = np.max(stats_matrix[:,1]) 
    min_score_hero_victory = np.min(stats_matrix[stats_matrix[:,0]==1][:,1])
    max_score_hero_victory = np.max(stats_matrix[stats_matrix[:,0]==1][:,1])
    min_score_hero_defeat = np.min(stats_matrix[stats_matrix[:,0]==0][:,1])
    max_score_hero_defeat = np.max(stats_matrix[stats_matrix[:,0]==0][:,1])
    min_delta_score = np.min(stats_matrix[:,3])
    max_delta_score = np.max(stats_matrix[:,3])
    #boxplot data Q1, mediane, Q3
    Q1_score, mediane_score, Q3_score = np.percentile(stats_matrix[:,1], [25, 50, 75])
    Q1_score_victory, mediane_score_victory, Q3_score_victory = np.percentile(stats_matrix[stats_matrix[:,0]==1][:,1], [25, 50, 75])
    Q1_score_defeat, mediane_score_defeat, Q3_score_defeat = np.percentile(stats_matrix[stats_matrix[:,0]==0][:,1], [25, 50, 75])
    Q1_delta_score, mediane_delta_score, Q3_delta_score = np.percentile(stats_matrix[:,3], [25, 50, 75])
    
    return np.array([
        equity,
        score_moyen_hero,
        variance_hero,
        ecart_type_hero,
        score_moyen_hero_victory,
        score_moyen_hero_defeat,
        variance_hero_victory,
        variance_hero_defeat,
        ecart_type_hero_victory,
        ecart_type_hero_defeat,
        delta_score_moyen,
        delta_score_moyen_victory,
        delta_score_moyen_defeat,
        min_score_hero,
        max_score_hero,
        min_score_hero_victory,
        max_score_hero_victory,
        min_score_hero_defeat,
        max_score_hero_defeat,
        min_delta_score,
        max_delta_score,
        Q1_score,
        mediane_score,
        Q3_score,
        Q1_score_victory,
        mediane_score_victory,
        Q3_score_victory,
        Q1_score_defeat,
        mediane_score_defeat,
        Q3_score_defeat,
        Q1_delta_score,
        mediane_delta_score,
        Q3_delta_score
    ])

def equity_generation_for_canonical_hand_every_showdown(hero_card, hand_matrix, equity_matrix_slice_for_one_hand):
    
    # VÉRIFICATION 1 : C'est bien une matrice numpy
    if not isinstance(equity_matrix_slice_for_one_hand, np.ndarray):
        raise TypeError(f"equity_matrix_slice_for_one_hand doit être np.ndarray, pas {type(equity_matrix_slice_for_one_hand)}")
    
    # VÉRIFICATION 2 : Shape correct
    if equity_matrix_slice_for_one_hand.shape != (169, 22):
        raise ValueError(f"equity_matrix_slice_for_one_hand doit être (169, 22), pas {equity_matrix_slice_for_one_hand.shape}")
    
    if not isinstance(hand_matrix, np.ndarray):
        raise TypeError(f"hand_matrix doit être np.ndarray, pas {type(hand_matrix)}")   
    if hand_matrix.shape != (13, 13):
        raise ValueError(f"hand_matrix doit être (13, 13), pas {hand_matrix.shape}")

    for i in range(13):
        for j in range(13):
            villain_card = hand_matrix[i][j]
            equity_matrix_slice_for_one_hand[i*13+j] = monte_carlo_experience(hero_card, villain_card, num_simulations=10)    

    
    


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    equity_matrix = load_equity_matrix()
    hand_matrix = load_hand_matrix()

    equity_generation_for_canonical_hand_every_showdown("AA", hand_matrix, equity_matrix[0][0])

    

    
    
