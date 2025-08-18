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

