import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import MDS
from adjustText import adjust_text

def plot_from_distance_matrix(distance_matrix, labels=None):
    mds = MDS(dissimilarity="precomputed", random_state=0)
    coords = mds.fit_transform(distance_matrix)

    plt.figure(figsize=(8, 6))
    plt.scatter(coords[:, 0], coords[:, 1], s=80, c='skyblue', edgecolors='k')

    texts = []
    for i, (x, y) in enumerate(coords):
        if labels is not None:
            texts.append(plt.text(x, y, labels[i], fontsize=10))
        else:
            texts.append(plt.text(x, y, str(i), fontsize=10))

    adjust_text(texts, arrowprops=dict(arrowstyle="->", color='gray'))
    plt.title("MDS Plot with Adjusted Labels")
    plt.show()

if __name__ == "__main__":
    distance_matrix = np.array([
        [0, 2, 3, 4],
        [2, 0, 5, 6],
        [3, 5, 0, 7],
        [4, 6, 7, 0]
    ])
    labels = ["A", "B", "C", "D"]
    plot_from_distance_matrix(distance_matrix, labels)
