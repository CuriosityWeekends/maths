'''
This a python script to generate distanes to each router from a random point
In a fixed environment(position of routers is fixed)

Update:
Added algorithm to approximate distance between each router.. ;)
'''

import random
import numpy as np

r_1 = np.array([0,10])
r_2 = np.array([20,0])
r_3 = np.array([25,0])

def find_distances(o):
    global r_1, r_2, r_3
    d1 = np.linalg.norm(r_1 - o)
    d2 = np.linalg.norm(r_2 - o)
    d3 = np.linalg.norm(r_3 - o)
    return d1, d2, d3

def distance_between_routers(r_1, r_2, r_3):
    r_12 = [np.linalg.norm(r_1-r_2), np.linalg.norm(r_1+r_2)]
    r_13 = [np.linalg.norm(r_1-r_3), np.linalg.norm(r_1+r_3)]
    r_23 = [np.linalg.norm(r_3-r_2), np.linalg.norm(r_3+r_2)]
    return r_12, r_13, r_23
i = 0
best_r_12 = [0, 1000]
best_r_13 = [0, 1000]
best_r_23 = [0, 1000]
while True:
    i += 1
    x = random.randint(-30, 30)
    y = random.randint(-30, 30)
    o = np.array([x, y])

    d1, d2, d3 = find_distances(o)
    print(f'''##O{i} (Distance to routers from orgin{i})
          R1: {d1}
          R2: {d2}
          R3: {d3}''')
    #print(o) #It is to be not available
    r_12, r_13, r_23 = distance_between_routers(d1, d2, d3)

    print(f'''###Distance between each Routers
          R1 --> R2: (|{d1} - {d2}|) `{r_12[0]} <> {r_12[1]}` (|{d1} + {d2}|)
          R1 --> R3: (|{d1} - {d3}|) `{r_13[0]} <> {r_13[1]}` (|{d1} + {d3}|)
          R2 --> R3: (|{d2} - {d3}|) `{r_23[0]} <> {r_23[1]}` (|{d2} + {d3}|)''')
    change = ''
    if r_12[0] > best_r_12[0]:
        best_r_12[0] = r_12[0]
        change += 'a'
    if r_12[1] < best_r_12[1]:
        best_r_12[1] = r_12[1]
        change += 'b'
    if r_13[0] > best_r_13[0]:
        best_r_13[0] = r_13[0]
        change += 'c'
    if r_13[1] < best_r_13[1]:
        best_r_13[1] = r_13[1]
        change += 'd'
    if r_23[0] > best_r_23[0]:
        best_r_23[0] = r_23[0]
        change += 'e'
    if r_23[1] < best_r_23[1]:
        best_r_23[1] = r_23[1]
        change += 'f'
    if change != '':
        print(f'''##Total Conclusion With All data
              {"*" if "a" in change else ""}R1{"*" if "b" in change else ""} --> R2: `{best_r_12[0]} <> {best_r_12[1]}`
              {"*" if "c" in change else ""}R1{"*" if "d" in change else ""} --> R3: `{best_r_13[0]} <> {best_r_13[1]}`
              {"*" if "e" in change else ""}R2{"*" if "f" in change else ""} --> R3: `{best_r_23[0]} <> {best_r_23[1]}`''')
    if input(": ") == "stop":
        break