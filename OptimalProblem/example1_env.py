import numpy as np

routers = np.array([
    [0, 10],
    [20, 0],
    [25, 0],
]) #Since we have only 3 routers, we can use a fixed array (for simplicity)

def find_distances(point, routers=routers):
    """
    Distances from point to each router.
    """
    return np.linalg.norm(routers - point, axis=1)

def distance_between_routers(distances: list) -> dict: 
    """
    Get min/max distance ranges between routers.
    distances: array of distances from routers to one another.
    Returns: dict {(i,j): (dmin, dmax)}
    """
    n = len(distances)
    results = {}
    for i in range(n):
        for j in range(i+1, n):
            dmin = abs(distances[i] - distances[j])
            dmax = distances[i] + distances[j]
            results[(i, j)] = (dmin, dmax)
    return results