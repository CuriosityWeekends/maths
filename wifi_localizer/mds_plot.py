import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse.csgraph import floyd_warshall
from sklearn.manifold import MDS
from adjustText import adjust_text
from scipy.spatial import distance_matrix as DM

def plot_from_distance_matrix(distance_matrix, labels=None):
    mds = MDS(dissimilarity="precomputed", random_state=8)
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
    plt.grid(True)
    plt.show()

    #euclid_dists = DM(coords, coords)
    #print("Pairwise distances between points after MDS:")
    #print(np.round(euclid_dists, 3))
    #return coords, euclid_dists

def compute_full_distance_matrix(partial_distances):
    '''
    To complete the metrix with only the known relations.
    '''
    D = partial_distances.astype(float)
    D[D == 0] = np.inf
    np.fill_diagonal(D, 0)
    # Compute shortest paths to fill in missing distances
    D_filled = floyd_warshall(D, directed=False)
    return D_filled

if __name__ == "__main__":
    distance_matrix = np.array([
        [0, 4, 3, 5],   #C -4- D
        [4, 0, 5, 3],   #3|    3|
        [3, 5, 0, 4],   #A -4- B
        [5, 3, 4, 0]
    ])
    labels = ["A", "B", "C", "D"]
    plot_from_distance_matrix(compute_full_distance_matrix(distance_matrix), labels)
