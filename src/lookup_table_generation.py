import numpy as np
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from load_data_matrixes import load_hand_matrix, load_equity_matrix
from tirage_simulator import tirage_simulator

def monte_carlo_experience(hero_cards, villain_cards, num_simulations=10000): # study the variation of num_simulations and closeness of true
    
    print(f"Starting Monte Carlo simulation for {hero_cards} vs {villain_cards} ")

    stats_matrix = np.empty((num_simulations, 4))
    #colonnes : equity, hero_score, villain_score, delta_score

    #generation de stats
    count = 0
    sum_equity = 0
    for i in stats_matrix: 
        i[0], i[1], i[2], i[3] = tirage_simulator(hero_cards, villain_cards)
        count += 1
        sum_equity += i[0]
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
    
    print(f"Completed Monte Carlo simulation for {hero_cards} vs {villain_cards} ")

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

def equity_generation_for_canonical_hand_every_showdown(hero_card, hand_matrix, equity_matrix_slice_for_one_hand, full_equity_matrix):
    # useless function with multi processing available
    # VÉRIFICATION 1 : C'est bien une matrice numpy
    if not isinstance(equity_matrix_slice_for_one_hand, np.ndarray):
        raise TypeError(f"equity_matrix_slice_for_one_hand doit être np.ndarray, pas {type(equity_matrix_slice_for_one_hand)}")
    
    # VÉRIFICATION 2 : Shape correct
    if equity_matrix_slice_for_one_hand.shape != (169, 33):
        raise ValueError(f"equity_matrix_slice_for_one_hand doit être (169, 33), pas {equity_matrix_slice_for_one_hand.shape}")

    if not isinstance(hand_matrix, np.ndarray):
        raise TypeError(f"hand_matrix doit être np.ndarray, pas {type(hand_matrix)}")   
    if hand_matrix.shape != (13, 13):
        raise ValueError(f"hand_matrix doit être (13, 13), pas {hand_matrix.shape}")

    for i in range(13):
        for j in range(13):
            if equity_matrix_slice_for_one_hand[i*13+j][0] != 0:
                print(f"Equity already computed for {hero_card} vs {hand_matrix[i][j]}, skipping...")
                continue  # skip already computed hands
            villain_card = hand_matrix[i][j]
            equity_matrix_slice_for_one_hand[i*13+j] = monte_carlo_experience(hero_card, villain_card)  

            np.save("data/equity_matrix.npy", full_equity_matrix)   

def worker_for_one_row(hero_card, villain_row, row_index):
        results =  []

        for col_index, villain_card in enumerate(villain_row):
            result = monte_carlo_experience(hero_card, villain_card)
            results.append(result)

        return results, row_index

def equity_generation_for_canonical_hand_every_showdown_with_multi_processing(hero_card, hand_matrix, equity_matrix_slice_for_one_hand, full_equity_matrix):
    
    # VÉRIFICATION 1 : C'est bien une matrice numpy
    if not isinstance(equity_matrix_slice_for_one_hand, np.ndarray):
        raise TypeError(f"equity_matrix_slice_for_one_hand doit être np.ndarray, pas {type(equity_matrix_slice_for_one_hand)}")
    
    # VÉRIFICATION 2 : Shape correct
    if equity_matrix_slice_for_one_hand.shape != (169, 33):
        raise ValueError(f"equity_matrix_slice_for_one_hand doit être (169, 33), pas {equity_matrix_slice_for_one_hand.shape}")

    if not isinstance(hand_matrix, np.ndarray):
        raise TypeError(f"hand_matrix doit être np.ndarray, pas {type(hand_matrix)}")   
    if hand_matrix.shape != (13, 13):
        raise ValueError(f"hand_matrix doit être (13, 13), pas {hand_matrix.shape}")
    
    max_workers = 13
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        
        futures = []
        for row_index in range(13):
            villain_row = hand_matrix[row_index]
            future = executor.submit(worker_for_one_row, hero_card, villain_row, row_index)
            futures.append(future)

        for future in as_completed(futures):
            results, row_index = future.result()
            for col_index, result in enumerate(results):
                equity_matrix_slice_for_one_hand[row_index*13 + col_index] = result

        np.save("data/equity_matrix.npy", full_equity_matrix)
    
def equity_generation_for_every_hand (hand_matrix, equity_matrix):
    for i in range(13):
        for j in range(13):
            
            equity_colomn = equity_matrix[i][j][:,0]

            has_zero = np.any(equity_colomn == 0)
            if not has_zero:
                print(f"Equity already computed for {hand_matrix[i][j]}, skipping...")
                continue  # skip already computed hands

            hero_card = hand_matrix[i][j]
            print(f"Starting equity generation for {hero_card}...")
            equity_generation_for_canonical_hand_every_showdown_with_multi_processing(hero_card, hand_matrix, equity_matrix[i][j], equity_matrix)
            print(f"Completed equity generation for {hero_card}.")

if __name__ == "__main__":

    os.makedirs("../data", exist_ok=True)

    equity_matrix = load_equity_matrix()
    hand_matrix = load_hand_matrix()

    try : 
        equity_generation_for_every_hand(hand_matrix, equity_matrix)

    except KeyboardInterrupt :
        print("Process interrupted by user. ")
        

    
    
