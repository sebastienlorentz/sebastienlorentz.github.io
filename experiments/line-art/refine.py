import os
import shutil
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np

N=1000
NUM_VARIATIONS=1000
EPSILON=0.05
SHRINK=0.8   # perturbation strength shrinks by this factor each refinement level
pi=np.pi

# Lineage path: base seed followed by the chain of variation indices that
# produced the diagram we want to refine. e.g. [483, 7, 12].
PATH=[98,215,117,371]

def calc_endpoints(k,a,b,c,d):
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

def coeffs_for_path(path):
    """Reconstruct the coefficients for any diagram from its lineage path.

    path[0] is the base seed (reproducing generate_rough.py exactly); each
    subsequent index appends a perturbation seeded by the path prefix up to
    and including that index, so every node in the tree is reproducible from
    its integers alone. Index 0 at any level means "exact parent" (no offset).
    """
    np.random.seed(path[0])
    a=np.random.uniform(-5,5,(2,2,2))
    b=np.random.randint(0,6,(2,2,2))
    c=np.random.randint(-6,7,(2,2,2))   # small integer frequencies -> coherent curves
    d=np.random.uniform(-10,10,(2,2,2))
    for depth in range(1,len(path)):
        rng=np.random.default_rng(tuple(path[:depth+1]))
        scale=0.0 if path[depth]==0 else EPSILON*SHRINK**(depth-1)
        a=a+scale*rng.standard_normal(a.shape)
        d=d+scale*rng.standard_normal(d.shape)
        # b (powers) and c (frequencies) held fixed across all refinement.
    return a,b,c,d

OUTPUT_DIR="refined_"+"_".join(map(str,PATH))
if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
os.makedirs(OUTPUT_DIR,exist_ok=True)

k=np.arange(N)
fig,ax=plt.subplots()
ax.set_axis_off()

for i in range(NUM_VARIATIONS):
    a,b,c,d=coeffs_for_path(PATH+[i])

    x1,y1,x2,y2=calc_endpoints(k,a,b,c,d)
    segs=np.stack([np.column_stack([x1,y1]),np.column_stack([x2,y2])],axis=1)

    ax.cla()
    ax.set_axis_off()
    ax.add_collection(LineCollection(segs,colors='black',linewidths=0.5))
    ax.set_aspect('equal')
    ax.autoscale()
    fig.savefig(os.path.join(OUTPUT_DIR,f"var_{i}.png"),dpi=150)
    print(f"variation {i} done")

plt.close(fig)
