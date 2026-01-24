import numpy as np
import json
import random
from datetime import datetime
from pathlib import Path
from treys import Card, Evaluator, Deck
import os

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
                equity_matrix[i][j] = np.empty((13, 13), dtype=float)
        np.save("data/equity_matrix.npy", equity_matrix)

def canonical_hand_parser_pseudo_random(canonical_hand):
    colors = ['s', 'h', 'd', 'c']
    hero_hand = []

    if len(canonical_hand) == 3:

        if canonical_hand[2]=='s':
            color = random.choice(colors)
            hero_hand.append(canonical_hand[0]+color[0])
            hero_hand.append(canonical_hand[1]+color[0])

        if canonical_hand[2]=='o':
            color_1 = random.choice(colors)
            color_2 = random.choice([c for c in colors if c != color_1])
            hero_hand.append(canonical_hand[0]+color_1)
            hero_hand.append(canonical_hand[1]+color_2)

    elif len(canonical_hand) == 2:
        color_1, color_2 = random.sample(colors, 2)
        hero_hand.append(canonical_hand[0]+color_1)
        hero_hand.append(canonical_hand[1]+color_2)

    else: 
        raise ValueError("please put canonical card hand with upper case card and lower case type (\'o\' or \'s\') expect for pocket paire ex : AA")

    return hero_hand


# Simulate equity calculations
def tirage_simulator(hero_cards):
    #initialiser les objets importante
    deck = Deck()
    evaluator = Evaluator()

    #choix de la main de hero
    temp_hand_hero = canonical_hand_parser_pseudo_random(hero_cards)
    hand_hero = [Card.new(temp_hand_hero[0]), Card.new(temp_hand_hero[1])]

    #prepare le paquet
    deck.cards.remove(hand_hero[0])
    deck.cards.remove(hand_hero[1])

    #creation du board
    hand_villain = deck.draw(2)
    board = deck.draw(5)

    #evalutation des differente mains
    hero_score = evaluator.evaluate(board, hand_hero)
    villain_score = evaluator.evaluate(board, hand_villain)

    test = Card.print_pretty_cards([hand_hero[0], hand_hero[1], hand_villain[0], hand_villain[1]] + board)

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    #load_hand_matrix()
    #load_equity_matrix()

    
    tirage_simulator("AA")
