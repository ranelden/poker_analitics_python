from src.data_visualisation.data_visualisation import plot_poker_surface_3d_for_hero_hand
from src.load_data_matrixes import load_equity_matrix, load_hand_matrix
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

base_dir = Path(__file__).resolve().parent

equity_matrix = load_equity_matrix()
equity_matrix_slice = equity_matrix[6][4]
hand_matrix = load_hand_matrix()
hand_name = hand_matrix[6][4]

fig, ax1, ax2 = plot_poker_surface_3d_for_hero_hand(equity_matrix_slice, base_dir, hand_name)

plt.show()