import os
import shutil
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np

N=1000
NUM_DIAGRAMS=1000
OUTPUT_DIR="rough"
pi=np.pi

def calc_endpoints(k):
    k=k/N
    x1=(a[0,0,0]*np.sin(c[0,0,0]*pi*k+d[0,0,0]*pi)**b[0,0,0]
        +a[0,1,0]*np.cos(c[0,1,0]*pi*k+d[0,1,0]*pi)**b[0,1,0])
    y1=(a[1,0,0]*np.sin(c[1,0,0]*pi*k+d[1,0,0]*pi)**b[1,0,0]
        +a[1,1,0]*np.cos(c[1,1,0]*pi*k+d[1,1,0]*pi)**b[1,1,0])

    x2=(a[0,0,1]*np.sin(c[0,0,1]*pi*k+d[0,0,1]*pi)**b[0,0,1]
        +a[0,1,1]*np.cos(c[0,1,1]*pi*k+d[0,1,1]*pi)**b[0,1,1])
    y2=(a[1,0,1]*np.sin(c[1,0,1]*pi*k+d[1,0,1]*pi)**b[1,0,1]
        +a[1,1,1]*np.cos(c[1,1,1]*pi*k+d[1,1,1]*pi)**b[1,1,1])
    return x1,y1,x2,y2

if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
os.makedirs(OUTPUT_DIR,exist_ok=True)

k=np.arange(N)
fig,ax=plt.subplots()
ax.set_axis_off()

for seed in range(0,NUM_DIAGRAMS):
    np.random.seed(seed)
    a=np.random.uniform(-5,5,(2,2,2))
    b=np.random.randint(0,6,(2,2,2))
    c=np.random.randint(-6,7,(2,2,2))   # small integer frequencies -> coherent curves
    d=np.random.uniform(-10,10,(2,2,2))

    x1,y1,x2,y2=calc_endpoints(k)
    segs=np.stack([np.column_stack([x1,y1]),np.column_stack([x2,y2])],axis=1)

    ax.cla()
    ax.set_axis_off()
    ax.add_collection(LineCollection(segs,colors='black',linewidths=0.5))
    ax.set_aspect('equal')
    ax.autoscale()
    fig.savefig(os.path.join(OUTPUT_DIR,f"diagram_seed_{seed}.png"),dpi=150)
    print(f"diagram {seed} done")

plt.close(fig)

