from fractions import Fraction
import numpy as np

# --- Must match refine.py so the lineage reconstructs identically ---
EPSILON=0.05
SHRINK=0.8
pi=np.pi

# Final lineage path (from refine.py) of the diagram you want to clean.
PATH=[98,215,117,371]

# Rounding: smaller denominator = "nicer" but further from the original.
# High-power terms are touchier, so they get a larger cap (more accuracy).
MAX_DEN=20
MAX_DEN_HIGH_POWER=50
HIGH_POWER=3

OUT_FILE="clean_coeffs.npz"

def coeffs_for_path(path):
    """Reconstruct coefficients from a lineage path (identical to refine.py)."""
    np.random.seed(path[0])
    a=np.random.uniform(-5,5,(2,2,2))
    b=np.random.randint(0,6,(2,2,2))
    c=np.random.randint(-6,7,(2,2,2))
    d=np.random.uniform(-10,10,(2,2,2))
    for depth in range(1,len(path)):
        rng=np.random.default_rng(tuple(path[:depth+1]))
        scale=0.0 if path[depth]==0 else EPSILON*SHRINK**(depth-1)
        a=a+scale*rng.standard_normal(a.shape)
        d=d+scale*rng.standard_normal(d.shape)
    return a,b,c,d

def endpoints(a,b,c,d,t):
    """The four coordinates over a normalized parameter t in [0,1)."""
    trig=(np.sin,np.cos)
    def coord(r,L):
        return sum(a[r,ti,L]*trig[ti](c[r,ti,L]*pi*t+d[r,ti,L]*pi)**b[r,ti,L] for ti in (0,1))
    return coord(0,0),coord(1,0),coord(0,1),coord(1,1)

def frac(x,cap):
    return Fraction(float(x)).limit_denominator(cap)

a,b,c,d=coeffs_for_path(PATH)
a2,b2,c2,d2=a.copy(),b.copy().astype(int),c.copy().astype(int),d.copy()

for r in (0,1):
    for ti,fn in ((0,np.sin),(1,np.cos)):
        for L in (0,1):
            freq=int(c[r,ti,L]); pw=int(b[r,ti,L])
            cap=MAX_DEN_HIGH_POWER if pw>=HIGH_POWER else MAX_DEN
            if freq==0:
                # k-independent term -> collapse to a single constant fraction (power 0).
                const=a[r,ti,L]*fn(d[r,ti,L]*pi)**pw
                a2[r,ti,L]=float(frac(const,cap)); b2[r,ti,L]=0; c2[r,ti,L]=0; d2[r,ti,L]=0.0
            else:
                phase=(d[r,ti,L]+1)%2-1          # reduce phase mod 2 into (-1,1]
                a2[r,ti,L]=float(frac(a[r,ti,L],cap))
                d2[r,ti,L]=float(frac(phase,cap))

# --- report how much the shape moved ---
t=np.arange(1000)/1000
orig=np.array(endpoints(a,b,c,d,t))
clean=np.array(endpoints(a2,b2,c2,d2,t))
span=np.ptp(orig,axis=1).max()                  # rough size of the figure
max_dev=np.abs(orig-clean).max()
print(f"max coordinate shift: {max_dev:.4f}  ({100*max_dev/span:.2f}% of figure size)\n")
for r,row in ((0,"x1/x2"),(1,"y1/y2")):
    for ti,t_ in ((0,"sin"),(1,"cos")):
        for L in (0,1):
            print(f"[{r},{ti},{L}] {t_}: amp {a[r,ti,L]:+.4f}->{frac(a2[r,ti,L],99)}"
                  f"  phase {d[r,ti,L]:+.4f}->{frac(d2[r,ti,L],99)}  pow {b[r,ti,L]}->{b2[r,ti,L]}")

np.savez(OUT_FILE,a=a2,b=b2,c=c2,d=d2,path=np.array(PATH))
print(f"\nwrote {OUT_FILE}  (now run render_final.py)")
