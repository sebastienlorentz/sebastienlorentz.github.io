import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from math import cos, sin, pi
from scipy.linalg import solve_continuous_are

dt = 0.027
g = 10
L = 1
cart_width = 1.0
cart_height = 0.5

swingup_k=0.15
swingup_kx = 0.2
swingup_kxd = 0.3

n_rollouts   = 300
rollout_steps = 500
action_noise = 0.3

balanced_keep = 0.4

class PendulumSim:
    def __init__(self):
        self.reset()

    def reset(self, theta0=pi):
        self.x = 0.0
        self.x_dot = 0.0
        self.theta = theta0
        self.theta_dot = 0.0

    def step(self, x_ddot):
        self.x_dot += x_ddot * dt
        self.x += self.x_dot * dt
        theta_ddot = g / L * sin(self.theta) - x_ddot / L * cos(self.theta)
        self.theta_dot += theta_ddot * dt
        self.theta += self.theta_dot * dt
        return self.x, self.x_dot, self.theta, self.theta_dot


def wrap(theta):
    return (theta + pi) % (2 * pi) - pi


A = np.array([[0,1,0,0],[0,0,0,0],[0,0,0,1],[0,0,g/L,0]])
B = np.array([[0],[1],[0],[-1/L]])
Q = np.diag([1, 1, 10, 1])
R = np.array([[0.1]])
P = solve_continuous_are(A, B, Q, R)
K = (np.linalg.inv(R) @ B.T @ P)[0]

def lqr_action(state):
    u = -K @ np.array([state[0], state[1], wrap(state[2]), state[3]])
    return float(u)


def swingup_action(state):
    x, x_dot, theta, theta_dot = state
    E=0.5 * L**2 * theta_dot**2 + g * L * cos(theta)
    E_top=g*L
    return swingup_k*(E-E_top)*np.sign(theta_dot*cos(theta)) - swingup_kx*x - swingup_kxd*x_dot



def expert(state):
    x, x_dot, theta, theta_dot = state
    if abs(wrap(theta)) < 0.4 and abs(theta_dot) < 3:
        return lqr_action(state)
    return swingup_action(state)


def visualize(controller, theta0=pi, n_steps=2000, speed=1):
    sim = PendulumSim()
    sim.reset(theta0)

    fig, ax = plt.subplots()
    ax.set_xlim(-6, 6)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')
    ax.axhline(0, color='gray', linewidth=1)
    cart = plt.Rectangle((0, 0), cart_width, cart_height, color='steelblue')
    ax.add_patch(cart)
    line, = ax.plot([0, 0], [0, 1], color='black', linewidth=1.5)
    title = ax.set_title('')

    def update(frame):
        for _ in range(speed):
            state = (sim.x, sim.x_dot, sim.theta, sim.theta_dot)
            sim.step(controller(state))
        pivot_y = cart_height / 2
        pen_x = sim.x + L * sin(sim.theta)
        pen_y = pivot_y + L * cos(sim.theta)
        line.set_data([sim.x, pen_x], [pivot_y, pen_y])
        cart.set_xy([sim.x - cart_width / 2, 0])
        title.set_text(f'θ={wrap(sim.theta):+.2f}  dθ/dṫ={sim.theta_dot:+.2f}  x={sim.x:+.2f}')
        return cart, line, title

    ani = animation.FuncAnimation(fig, update, frames=n_steps // speed,
                                  interval=1000 * dt * speed)
    plt.show()
    return ani


def generate_dataset(path='expert_data.npz'):
    X, Y = [], []
    sim = PendulumSim()
    for _ in range(n_rollouts):
        # varied starts: any angle + modest initial spin (covers swing-up, catch, and balance;
        # random theta_dot avoids the dead-hang where the pump has no direction)
        sim.reset(np.random.uniform(-pi, pi))
        sim.theta_dot = np.random.uniform(-5, 5)
        for _ in range(rollout_steps):
            state = (sim.x, sim.x_dot, sim.theta, sim.theta_dot)
            a = expert(state)                                  # label = expert's intended action HERE
            balanced = abs(wrap(state[2])) < 0.4 and abs(state[3]) < 3
            if not balanced or np.random.rand() < balanced_keep:
                X.append([state[0], state[1], wrap(state[2]), state[3]])   # store WRAPPED angle
                Y.append(a)
            sim.step(a + np.random.uniform(-action_noise, action_noise))   # explore with noise
    X, Y = np.array(X), np.array(Y)
    perm = np.random.permutation(len(X))                       # shuffle so batches mix trajectories
    X, Y = X[perm], Y[perm]
    np.savez(path, X=X, Y=Y)
    print(f'saved {len(X)} samples to {path}')
    return X, Y


#visualize(expert, theta0=pi+0.1, n_steps=2000, speed=1)
generate_dataset()
