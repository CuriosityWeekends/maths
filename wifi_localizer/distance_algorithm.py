import random
import numpy as np
from example1_env import routers, find_distances, distance_between_routers


def updated_distances(point, distances=None):
    dists = find_distances(point)
    current = distance_between_routers(dists)
    if distances is None:
        return current
    for key in distances:
        dmin = max(distances[key][0], current[key][0])
        dmax = min(distances[key][1], current[key][1])
        distances[key] = (dmin, dmax)
    return distances
# Side note, i just noticed that i didn't use the distance_between_routers function from the env
# nvm, i am using it here now lol, and it looks cleaner this way

if __name__ == "__main__":
    distances = None
    while True:
        x = random.randint(-30, 30)
        y = random.randint(-30, 30)
        point = np.array([x, y])

        distances = updated_distances(point, distances)

        print(f"## Point: {point}")
        for (i, j), (dmin, dmax) in distances.items():
            print(f"R{i+1} --> R{j+1}: `{dmin:.4f} <> {dmax:.4f}`")

        change = input("Continue? (type 'stop' to exit): ")
        if change.lower() == "stop":
            break