import numpy as np
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
data_dir = base_dir / "data"
data_dir.mkdir(exist_ok=True)
    

# Load or initialize hand matrix
def load_hand_matrix():
    file_path = data_dir / "hand_matrix.npy"

    try :
        hand_matrix = np.load(file_path, allow_pickle=True)
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

        np.save(file_path, hand_matrix)

    return hand_matrix

# Load or initialize equity matrix
def load_equity_matrix():  
    file_path = data_dir / "equity_matrix.npy"

    try :
        equity_matrix = np.load(file_path, allow_pickle=True)
        print("equity_matrix loaded from file.")
    except Exception as e :
        print(e)
        equity_matrix = None

    if equity_matrix is None:

        equity_matrix = np.empty((13, 13), dtype=object)

        for i in range(13):
            for j in range(13):
                equity_matrix[i][j] = np.empty((169, 33), dtype=float)
        np.save(file_path, equity_matrix)

    return equity_matrix

