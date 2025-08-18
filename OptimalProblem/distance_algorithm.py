import random
import numpy as np
import example1_env as env

n = len(env.routers)
distances = {(i,j): [0, float("inf")] for i in range(n) for j in range(i+1,n)}

def updated_distances(point, distances=distances):
    dists = env.find_distances(point)
    for i in range(n):
        for j in range(i+1, n):
            dmin = abs(dists[i] - dists[j])
            dmax = dists[i] + dists[j]
            if dmin > distances[(i, j)][0]:
                distances[(i, j)][0] = dmin
            if dmax < distances[(i, j)][1]:
                distances[(i, j)][1] = dmax
    return distances
# Side note, i just noticed that i didn't use the distance_between_routers function from the env

if __name__ == "__main__":
    while True:
        x = random.randint(-30, 30)
        y = random.randint(-30, 30)
        point = np.array([x, y])

        distances = updated_distances(point)

        print(f"## Point: {point}")
        for (i, j), (dmin, dmax) in distances.items():
            print(f"R{i+1} --> R{j+1}: `{dmin:.4f} <> {dmax:.4f}`")

        change = input("Continue? (type 'stop' to exit): ")
        if change.lower() == "stop":
            break