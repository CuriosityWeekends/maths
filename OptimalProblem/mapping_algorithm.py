import numpy as np
import random
import matplotlib.pyplot as plt
from distance_algorithm import find_distances, distance_between_routers, updated_distances

def compute_coverage(all_distances, bins=500):
    """
    Bins is the no of intervals to divide the distance range into.
    Compute coverage arrays for each router pair.
    Essentally counts how many times each distance range is covered.
    Returns a dict: {pair: (x_vals, coverage)}.
    """
    pairs = list(all_distances[0].keys())
    results = {}

    for pair in pairs:
        mins = [d[pair][0] for d in all_distances]
        maxs = [d[pair][1] for d in all_distances]

        x_vals = np.linspace(min(mins), max(maxs), bins) # Empty array of x values
        coverage = np.zeros_like(x_vals)

        for dmin, dmax in zip(mins, maxs):
            coverage += (x_vals >= dmin) & (x_vals <= dmax) # Count coverage in each interval

        results[pair] = (x_vals, coverage)

    return results


def plot_heatmap(coverage_dict):
    pairs = list(coverage_dict.keys())
    fig, axes = plt.subplots(len(pairs), 1, figsize=(10, 3*len(pairs)))

    if len(pairs) == 1:
        axes = [axes]

    for ax, pair in zip(axes, pairs):
        x_vals, coverage = coverage_dict[pair]
        ax.imshow(
            coverage[np.newaxis, :],
            extent=[x_vals[0], x_vals[-1], 0, 1],
            aspect="auto",
            cmap="viridis"
        )
        ax.set_title(f"Heatmap for Routers {pair}")
        ax.set_yticks([])
        ax.set_xlabel("Distance")

    plt.tight_layout()
    plt.show()
