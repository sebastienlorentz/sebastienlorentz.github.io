import numpy as np
import matplotlib.pyplot as plt
import shutil
import os

folder = 'weight_diagrams'
if os.path.exists(folder):
    shutil.rmtree(folder)
os.makedirs(folder)

# order must match how your code packs the state vector into the network
input_labels = ["x", "x_dot", "theta", "theta_dot"]

for epoch in range(0, 1001, 100):
    data = np.load(f"epoch_{epoch}_weights.npz")
    weights = [data["W1"], data["W2"], data["w3"].reshape(1, -1)]

    sizes = [weights[0].shape[1]] + [W.shape[0] for W in weights]
    ys = [np.linspace(0, 1, n) if n > 1 else [0.5] for n in sizes]

    plt.figure(figsize=(16, 12))
    for li, W in enumerate(weights):
        wmax = np.abs(W).max()                     # normalize per layer, not globally
        for j in range(W.shape[0]):
            for i in range(W.shape[1]):
                m = abs(W[j, i]) / wmax
                if li == 0:
                    m = m ** 0.6               # input layer is dominated by a couple of huge weights; lift the weaker ones
                plt.plot([li, li + 1], [ys[li][i], ys[li + 1][j]],
                         color="#D85A30" if W[j, i] > 0 else "#378ADD", lw=4 * m, alpha=m)

    for x, y in enumerate(ys):
        plt.scatter([x] * len(y), y, c="k", zorder=2)

    for i, lab in enumerate(input_labels):
        plt.text(-0.08, ys[0][i], lab, ha="right", va="center", fontsize=21)
    plt.text(3.35, ys[3][0], 'x_ddot', ha="right", va="center", fontsize=21)

    plt.xlim(-0.8, len(weights) + 0.2)
    plt.title(f"epoch {epoch}", fontsize=18)
    plt.axis("off")
    plt.savefig(f"{folder}/epoch_{epoch}_weights.png", dpi=130, bbox_inches="tight")
    print(f"saved {folder}/epoch_{epoch}_weights.png")
    plt.close()