import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import LineCollection

#manually define connections
#n_nodes=5
#connections=[
#    [1,2],
#    [1,3],
#    [1,4],
#    [2,3],
#    [2,4],
#    [4,5]
#]

#or generate random connections for testing
n_nodes = 10
all_pairs = [[i, j] for i in range(1, n_nodes+1) for j in range(i+1, n_nodes+1)]
connections = random.sample(all_pairs, k=random.randint(n_nodes-1, len(all_pairs)))


nodes=[]

#need adjusting depending on number of nodes
center_force=0.5
repel_force=20
link_force=3
link_length=3
dt=0.01

plane_size=10

centerx=0
centery=0

class Node:
    def __init__(self,index):
        self.index=index
        self.x=random.uniform(-plane_size/2,plane_size/2)
        self.y=random.uniform(-plane_size/2,plane_size/2)
        self.xdot=0
        self.ydot=0

    def distance(self,node):
        return math.sqrt((self.x-node.x)**2+(self.y-node.y)**2)

    def move(self, force):
        self.xdot = (self.xdot + force[0] * dt) * 0.9
        self.ydot = (self.ydot + force[1] * dt) * 0.9
        self.x += self.xdot * dt
        self.y += self.ydot * dt

    def calc_force(self, other):
        force_x = 0.0
        force_y = 0.0
        epsilon = 1e-5

        dx_center = centerx - self.x
        dy_center = centery - self.y

        force_x += dx_center * center_force
        force_y += dy_center * center_force

        if self.index == other.index:
            return force_x, force_y

        dx = self.x - other.x
        dy = self.y - other.y
        distance = np.hypot(dx, dy) + epsilon

        repel_magnitude = repel_force / (distance ** 2)
        force_x += (dx / distance) * repel_magnitude
        force_y += (dy / distance) * repel_magnitude

        is_connected = (
            [self.index, other.index] in connections or
            [other.index, self.index] in connections
        )

        if is_connected:
            displacement = distance - link_length
            spring_magnitude = link_force * displacement
            force_x -= dx * spring_magnitude
            force_y -= dy * spring_magnitude

        return [force_x, force_y]


for i in range(n_nodes):
    nodes.append(Node(i+1))

node_map = {obj.index: obj for obj in nodes}

fig, ax = plt.subplots()
ax.set_xlim(-plane_size/2, plane_size/2)
ax.set_ylim(-plane_size/2, plane_size/2)
ax.set_aspect('equal')

scatter = ax.scatter([n.x for n in nodes], [n.y for n in nodes],
                     s=200, c='grey', edgecolors='black', zorder=3)

line_collection = LineCollection([], colors='gray', linewidths=1.5, linestyles='dashed', zorder=2)
ax.add_collection(line_collection)


def update(frame):
    for node in nodes:
        fx, fy = 0.0, 0.0
        for other in nodes:
            dfx, dfy = node.calc_force(other)
            fx += dfx
            fy += dfy
        node.move([fx, fy])

    scatter.set_offsets([[n.x, n.y] for n in nodes])

    current_lines = []
    for start_idx, end_idx in connections:
        node_a = node_map[start_idx]
        node_b = node_map[end_idx]
        current_lines.append([(node_a.x, node_a.y), (node_b.x, node_b.y)])
    line_collection.set_segments(current_lines)

    return [scatter, line_collection]


initial_lines = [[(node_map[a].x, node_map[a].y), (node_map[b].x, node_map[b].y)]
                 for a, b in connections]
line_collection.set_segments(initial_lines)
plt.savefig('initial_layout.png', dpi=150, bbox_inches='tight')

ani = animation.FuncAnimation(
    fig=fig,
    func=update,
    frames=10000,
    interval=25,
    blit=True
)

fig.canvas.mpl_connect('close_event', lambda _: fig.savefig('final_layout.png', dpi=150, bbox_inches='tight'))

plt.show()