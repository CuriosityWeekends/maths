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
            coverage += (x_vals >= dmin) & (x_vals <= dmax) # Counts coverage in each interval

        results[pair] = (x_vals, coverage)

    return results

def _best_distances(coverage_results):
    """
    This should find the "brightest" spot in the coverage heatmap.
    """
    best_distances = {}

    for pair, (x_vals, coverage) in coverage_results.items():
        best_index = np.argmax(coverage)     # index of maximum coverage
        best_distance = x_vals[best_index]   # distance at that index
        best_distances[pair] = best_distance

    return best_distances

def best_distance_from_ranges(ranges):
    all_pairs = set()
    for scan in ranges:
        all_pairs.update(scan.keys())
    pairs = list(all_pairs)
    results = {}

    for pair in pairs:
        intervals = [d[pair] for d in ranges if pair in d]
        if not intervals:
            results[pair] = None
            continue
        
        changes = []
        for dmin, dmax in intervals:
            changes.append((dmin, +1))
            changes.append((dmax, -1))
        
        changes.sort(key=lambda x: (x[0], -x[1]))
        coverage = 0
        max_coverage = 0
        best_segment = None
        prev_x = None

        for x, change in changes:
            if prev_x is not None and coverage == max_coverage and coverage > 0:
                best_segment = (prev_x, x)

            coverage += change
            prev_x = x
            if coverage > max_coverage:
                max_coverage = coverage
                best_segment = None
        
        if best_segment:
            best_distance = (best_segment[0] + best_segment[1]) / 2
        else:
            best_distance = None
        
        results[pair] = best_distance
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

if __name__ == "__main__":
    all_distances = []
    best_ranges = None

    for _ in range(10000):  # Iteration count
        x = random.randint(-25, 25)
        y = random.randint(-25, 25)
        point = np.array([x, y])

        best_ranges = updated_distances(point, best_ranges)
        all_distances.append(distance_between_routers(find_distances(point)))

    print("Best ranges found:")
    for pair, (dmin, dmax) in best_ranges.items():
        print(f"Routers {pair}: {dmin} <> {dmax}")

    print("Most probable distances:")
    best_distances = best_distance_from_ranges(all_distances)
    for pair, distance in best_distances.items():
        print(f"Routers {pair}: {distance}")
    
    coverage = compute_coverage(all_distances, bins=50000)
    plot_heatmap(coverage)