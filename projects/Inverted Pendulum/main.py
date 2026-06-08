import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from math import cos, sin, pi
import os
import shutil


folder = 'videos'
if os.path.exists(folder):
    shutil.rmtree(folder)
os.makedirs(folder)

epoch_length = 3000

dt = 0.01
g = 10
L = 1
cart_width = 1.0
cart_height = 0.5

n_inp = 4
n_hid1 = 36
n_hid2 = 36

data_split = 0.85

np.random.seed(2)

data = np.load('expert_data.npz')
data_states = data['X']
data_action = data['Y']

states_train = data_states[:int(len(data_states) * data_split)]
actions_train = data_action[:int(len(data_action) * data_split)]
states_test = data_states[int(len(data_states) * data_split):]
actions_test = data_action[int(len(data_action) * data_split):]


class PendulumSim:
    def __init__(self):
        self.reset()

    def reset(self, theta0=0.1):
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


def run_epoch(sim, policy, epoch_length, theta0=0.1):
    sim.reset(theta0)
    states = []
    for _ in range(epoch_length):
        state = (sim.x, sim.x_dot, sim.theta, sim.theta_dot)
        x_ddot = policy(state)
        sim.step(x_ddot)
        states.append(state)
    return states


W1 = np.random.randn(n_hid1, n_inp) * np.sqrt(1 / n_inp)
W2 = np.random.randn(n_hid2, n_hid1) * np.sqrt(1 / n_hid1)
w3 = np.random.randn(n_hid2) * np.sqrt(1 / n_hid2)
b1 = np.zeros(n_hid1)
b2 = np.zeros(n_hid2)
b3 = 0.0


def forward(X):
    Z1 = X @ W1.T + b1
    A1 = np.tanh(Z1)
    Z2 = A1 @ W2.T + b2
    A2 = np.tanh(Z2)
    P = A2 @ w3 + b3
    cache = (X, A1, A2)
    return P, cache


def policy(state):
    x = np.array([state[0], state[1], wrap(state[2]), state[3]], dtype=float)
    P, _ = forward(x.reshape(1, 4))
    return float(P[0])


def animate_epoch(states, name="epoch"):
    render_fps = 30
    step_n = max(1, int(1 / (render_fps * dt)))
    render_states = states[::step_n]

    fig, ax = plt.subplots()
    ax.set_xlim(-6, 6)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')
    ax.axhline(0, color='gray', linewidth=1)
    cart = plt.Rectangle((0, 0), cart_width, cart_height, color='steelblue')
    ax.add_patch(cart)
    line, = ax.plot([0, 0], [0, 1], color='black', linewidth=1.5)

    def update(frame):
        x, x_dot, theta, theta_dot = render_states[frame]
        pivot_y = cart_height / 2
        pen_x = x + L * sin(theta)
        pen_y = pivot_y + L * cos(theta)
        line.set_data([x, pen_x], [pivot_y, pen_y])
        cart.set_xy([x - cart_width / 2, 0])
        return cart, line

    ani = animation.FuncAnimation(fig, update, frames=len(render_states),
                                  interval=1000 / render_fps, blit=True)
    ani.save(f'videos/{name}.mp4', writer='ffmpeg', fps=render_fps,
             extra_args=['-vcodec', 'libx264', '-crf', '28'])
    plt.close(fig)


def mse_loss(P, Y):
    return np.mean((Y - P) ** 2)


def backward(cache, P, Y):
    X, A1, A2 = cache
    B = len(Y)

    dP = 2 * (P - Y) / B

    gw3 = A2.T @ dP
    gb3 = dP.sum()
    dA2 = np.outer(dP, w3)

    dZ2 = dA2 * (1 - A2 ** 2)

    gW2 = dZ2.T @ A1
    gb2 = dZ2.sum(axis=0)
    dA1 = dZ2 @ W2

    dZ1 = dA1 * (1 - A1 ** 2)

    gW1 = dZ1.T @ X
    gb1 = dZ1.sum(axis=0)

    return gW1, gb1, gW2, gb2, gw3, gb3


def update(grads, lr):
    global W1, b1, W2, b2, w3, b3
    gW1, gb1, gW2, gb2, gw3, gb3 = grads
    W1 -= lr * gW1
    b1 -= lr * gb1
    W2 -= lr * gW2
    b2 -= lr * gb2
    w3 -= lr * gw3
    b3 -= lr * gb3


def train(epochs=1000, batch_size=64, lr=0.01):
    global states_train, actions_train

    # live loss plot with dual axes (train left, val right)
    plt.ion()
    fig_loss, ax_train = plt.subplots()
    ax_val = ax_train.twinx()
    ax_train.set_xlabel('Epoch')
    ax_train.set_ylabel('Train Loss', color='blue')
    ax_val.set_ylabel('Val Loss', color='orange')
    train_line, = ax_train.plot([], [], 'b-', label='train')
    val_line, = ax_val.plot([], [], color='orange', label='val')
    train_losses = []
    val_losses = []

    for epoch in range(epochs):
        perm = np.random.permutation(len(states_train))
        states_train = states_train[perm]
        actions_train = actions_train[perm]

        epoch_loss = 0
        n_batches = 0
        for i in range(0, len(states_train), batch_size):
            batch_states = states_train[i:i + batch_size]
            batch_actions = actions_train[i:i + batch_size]
            P, cache = forward(batch_states)
            loss = mse_loss(P, batch_actions)
            epoch_loss += loss
            n_batches += 1
            grads = backward(cache, P, batch_actions)
            update(grads, lr)

        avg_train_loss = epoch_loss / n_batches
        Pv, _ = forward(states_test)
        val_loss = mse_loss(Pv, actions_test)

        train_losses.append(avg_train_loss)
        val_losses.append(val_loss)

        print(f'{epoch}  train={round(avg_train_loss,5)}  val={round(val_loss,5)}')

        if epoch % 10 == 0:
            train_line.set_data(range(len(train_losses)), train_losses)
            val_line.set_data(range(len(val_losses)), val_losses)
            ax_train.relim()
            ax_train.autoscale_view()
            ax_val.relim()
            ax_val.autoscale_view()
            plt.pause(0.001)

        if epoch % 100 == 0:
            sim = PendulumSim()
            states = run_epoch(sim, policy, epoch_length=epoch_length, theta0=pi)
            animate_epoch(states, name=f"epoch_{epoch}")
            np.savez(f"epoch_{epoch}_weights", W1=W1, b1=b1, W2=W2, b2=b2, w3=w3, b3=b3)




train(epochs=1000, batch_size=64, lr=0.01)
sim = PendulumSim()
states = run_epoch(sim, policy, epoch_length=epoch_length, theta0=pi)
animate_epoch(states, name="trained")
np.savez("final_weights", W1=W1, b1=b1, W2=W2, b2=b2, w3=w3, b3=b3)
plt.ioff()
plt.show()