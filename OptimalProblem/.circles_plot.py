import matplotlib.pyplot as plt
import numpy as np
import math
from itertools import cycle

plt.ion()
fig = plt.figure()
fig.set_size_inches(12, 10)

def plot_router_positions(distance_dict, router_labels=None, pause_time=0.1):
    plt.clf()
    def get_distance(node1, node2):
        return distance_dict.get((node1,node2), distance_dict.get((node2,node1), None))

    def draw_circle(center, radius, color='gray', alpha=0.3, linestyle='--'):
        circle = plt.Circle(center, radius, edgecolor=color, facecolor='none',
                                linestyle=linestyle, alpha=alpha, linewidth=1.5)
        plt.gca().add_patch(circle)
    
    def circle_intersections(center1, radius1, center2, radius2, eps=0.1):
        x0, y0 = center1
        x1, y1 = center2
        dx, dy = x1 - x0, y1 - y0
        center_distance = math.hypot(dx, dy)
        if center_distance > radius1 + radius2 + eps or center_distance < abs(radius1 - radius2) - eps or center_distance < eps:
            return []
        a = (radius1**2 - radius2**2 + center_distance**2) / (2 * center_distance)
        h = math.sqrt(max(radius1**2 - a**2, 0))
        xm, ym = x0 + a * dx / center_distance, y0 + a * dy / center_distance
        rx, ry = -dy * h / center_distance, dx * h / center_distance
        pointA, pointB = (xm + rx, ym + ry), (xm - rx, ym - ry)
        return [pointA] if h < eps else [pointA, pointB]

    def plot_points(points, **kwargs):
        if points:
            xs, ys = zip(*points)
            plt.scatter(xs, ys, **kwargs)

    all_nodes = sorted(set([i for pair in distance_dict.keys() for i in pair]))
    positions = {0: (0,0), 1: (get_distance(0,1), 0)}
    placed_nodes = [0,1]
    color_cycle = cycle(['red','green','blue','purple','brown','cyan'])

    plt.plot([positions[0][0], positions[1][0]], [positions[0][1], positions[1][1]], 'ko-', label='Baseline')

    for node in all_nodes:
        label = router_labels.get(node, str(node)) if router_labels else str(node)
        if node in placed_nodes:
            plt.scatter(*positions[node], color='black', s=120)
            plt.text(positions[node][0], positions[node][1]+0.5, label, ha='center', va='bottom', fontsize=12, fontweight='bold')
            continue

        available_anchors, anchor_colors = [], {}
        for anchor, color in zip(placed_nodes, color_cycle):
            dist_to_node = get_distance(anchor, node)
            if dist_to_node is not None:
                draw_circle(positions[anchor], dist_to_node, color=color)
                available_anchors.append(anchor)
                anchor_colors[anchor] = color

        candidate_points = [
            pt
            for i in range(len(available_anchors))
            for j in range(i+1, len(available_anchors))
            for pt in circle_intersections(
                positions[available_anchors[i]], get_distance(available_anchors[i], node),
                positions[available_anchors[j]], get_distance(available_anchors[j], node)
            )
        ]

        consistent_points = [
            pt for pt in candidate_points
            if all(abs(math.hypot(pt[0]-positions[a][0], pt[1]-positions[a][1]) - get_distance(a, node)) < 1e-1 for a in available_anchors)
        ]

        plot_points(candidate_points, color='orange', s=40, alpha=0.6, label='Candidates' if node==2 else "")
        for x, y in consistent_points:
            plt.scatter(x, y, facecolors='none', edgecolors='blue', s=120, linewidths=1.5, label='Consistent' if node==2 else "")
            plt.text(x, y+0.5, label, ha='center', va='bottom', fontsize=11, fontweight='bold')
            for a in available_anchors:
                plt.plot([x, positions[a][0]], [y, positions[a][1]], color=anchor_colors[a], linestyle=':', alpha=0.7)

        if consistent_points:
            chosen_point, marker_color, marker_style = max(consistent_points, key=lambda pt: pt[1]), 'blue', 'o'
        elif candidate_points:
            chosen_point, marker_color, marker_style = candidate_points[0], 'red', 'x'
            plt.text(chosen_point[0], chosen_point[1]+0.5, f"{label}?", ha='center', va='bottom', fontsize=11, fontweight='bold', color='red')
        else:
            continue

        positions[node] = chosen_point
        placed_nodes.append(node)
        plt.scatter(*chosen_point, color=marker_color, s=100, marker=marker_style)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.title("Router placement with all routers displayed (uncertain ones marked)", fontsize=14)
    plt.xlabel("X-axis distance")
    plt.ylabel("Y-axis distance")
    plt.legend()
    plt.draw()
    plt.pause(pause_time)
    return positions

if __name__ == "__main__":
    d = {
        (0, 5): 10, (0, 1): 20, (0, 2): 25, (0, 3): 10, (0, 4): 20,
        (5, 1): 22.36, (5, 2): 26.93, (5, 3): 14.14, (5, 4): 22.36,
        (1, 2): 5.0, (1, 3): 30.0, (1, 4): 40.0, (2, 3): 35.0, (2, 4): 45.0, (3, 4): 10.0,
    }

    labels = {0:'Server', 1:'RouterA', 2:'RouterB', 3:'RouterC', 4:'RouterD', 5:'RouterE'}
    positions = plot_router_positions(d, router_labels=labels, pause_time=0)
