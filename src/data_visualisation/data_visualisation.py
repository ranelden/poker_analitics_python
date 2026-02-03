import pickle
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def plot_poker_surface_3d_for_hero_hand(equity_matrix_slice, base_dir, hand_name):

    data_dir = base_dir / "data" / "visualisation" / "hand_surface_3d"
    data_dir.mkdir(exist_ok=True)

    # Define file paths
    file_name_png = f'poker_surface_3d_{hand_name}.png'
    file_path = data_dir / file_name_png
    file_name_plt = f'poker_surface_3d_{hand_name}.plt'
    file_path_plt = data_dir / file_name_plt
 
    # Check if cached plot exists
    if file_path_plt.exists():
        print("Loading cached plot...")
        try :
            with open(file_path_plt, 'rb') as f:
                fig = pickle.load(f)
            ax1 = fig.axes[0]
            ax2 = fig.axes[1]

            if not file_path.exists():
                plt.savefig(file_path, dpi=300, bbox_inches='tight')

            return fig, ax1, ax2
        except Exception as e :
            print(f"Error loading cached plot: {e}")
            pass

    Z = equity_matrix_slice[:, 0].reshape((13, 13))
    X, Y = np.meshgrid(range(Z.shape[0]), range(Z.shape[1]))


    # create the label for the heatmap
    rangs = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

    labels = []
    for i, rang1 in enumerate(rangs):
        row = []
        for j, rang2 in enumerate(rangs):
            if i == j:
                label = f"{rang1}{rang2}"      # Paires: AA, KK, etc.
            elif i < j:
                label = f"{rang1}{rang2}s"     # Suited: AKs, AQs, etc.
            else:
                label = f"{rangs[j]}{rang1}o"  # Offsuit: AKo, KQo, etc.
            row.append(label)
        labels.append(row)

    labels = np.array(labels)

    fig = plt.figure(figsize=(16, 7))
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')

    surf = ax1.plot_surface(X, Y, Z, 
                            cmap='viridis',        # Colormap
                            edgecolor='black',     # Couleur des lignes de grille
                            linewidth=0.5,         # Épaisseur des lignes
                            antialiased=True,      # Lissage
                            alpha=0.9)             # Transparence

    cbar = fig.colorbar(surf, ax=ax1, shrink=0.5, aspect=10)
    cbar.set_label('Valeur', rotation=270, labelpad=15)

    ax1.set_xlim(0, 12)
    ax1.set_ylim(0, 12)
    ax1.set_zlim(0, 1) 

    ax1.set_xlabel('Colonne', fontsize=10, labelpad=10)
    ax1.set_ylabel('Ligne', fontsize=10, labelpad=10)
    ax1.set_zlabel('Valeur', fontsize=10, labelpad=10)

    # Titre
    ax1.set_title(f'Surface 3D des valeurs {hand_name}', fontsize=14, fontweight='bold', pad=20)

    # Angle de vue
    ax1.view_init(elev=25, azim=45)

    # Grille
    ax1.grid(True, alpha=0.3)

    # === MATRICE TEXTUELLE ===
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.axis('off')

    # Créer le texte des cellules avec labels et valeurs
    cellText = []
    for i in range(13):
        row = []
        for j in range(13):
            row.append(f"{labels[i,j]}\n{Z[i,j]:.3f}")
        cellText.append(row)

    # Créer le tableau
    table = ax2.table(
        cellText=cellText,
        cellLoc='center',
        loc='center',
        cellColours=plt.cm.viridis(Z)  # Couleurs selon les valeurs
    )

    # Personnaliser le tableau
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 2)  # Ajuster hauteur des cellules

    # Titre de la matrice
    ax2.set_title('Matrice canonique des mains de poker', 
                fontsize=12, fontweight='bold', pad=20)

    # === Ajustements finaux ===
    plt.tight_layout()

    # Sauvegarder la figure
    with open(file_path_plt, 'wb') as f:
        pickle.dump(fig, f)
    #sauvegarder en png aussi
    plt.savefig(file_path, dpi=300, bbox_inches='tight')

    return fig, ax1, ax2

