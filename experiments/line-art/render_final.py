import os
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from fractions import Fraction
import numpy as np

# Coefficients come from clean_coeffs.py -- run that first on your final PATH.
CLEAN_FILE="clean_coeffs.npz"

# N only samples the curves more finely (density); it does not change the shape.
N=1500
pi=np.pi

# High-res render settings.
FIGSIZE=(12,12)
DPI=600
LINEWIDTH=0.4
ALPHA=0.95  # line transparency; lower = softer build-up of tone in dense areas

# Animation settings (segments drawn progressively).
# Drawing speed = ANIM_SEG_PER_FRAME * ANIM_FPS segments per second; lower = slower.
ANIM_SEG_PER_FRAME=4
ANIM_FPS=25
ANIM_FIGSIZE=(8,8)
ANIM_DPI=100

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

# ------------------------- LaTeX formula builder (renders fractions) -------------------------

def _texnum(v):
    f=Fraction(float(v)).limit_denominator(1000)
    if f.denominator==1:
        return str(f.numerator)
    s="-" if f<0 else ""
    return f"{s}\\frac{{{abs(f.numerator)}}}{{{f.denominator}}}"

def _term(coef,func,c,d,b):
    """One a*trig(...)^b term, returned as (sign, body) for clean joining."""
    sign="-" if coef<0 else "+"
    mag=_texnum(abs(coef))
    if b==0:                       # trig(...)^0 == 1, so the term is just the constant
        return sign,mag
    phase="" if Fraction(float(d)).limit_denominator(1000)==0 else f" + {_texnum(d)}\\pi"
    arg=f"\\frac{{{_texnum(c)}\\pi k}}{{{N}}}{phase}"
    power="" if b==1 else f"^{{{b}}}"
    return sign,f"{mag}\\,\\{func}\\!\\left({arg}\\right){power}"

def _coordinate(a,b,c,d,r,L):
    """LaTeX for one coordinate; drops zero terms and tidies signs."""
    parts=[_term(a[r,ti,L],fn,c[r,ti,L],d[r,ti,L],b[r,ti,L])
           for ti,fn in ((0,"sin"),(1,"cos"))
           if Fraction(float(a[r,ti,L])).limit_denominator(1000)!=0]
    if not parts:
        return "0"
    s0,t0=parts[0]
    out=("-"+t0) if s0=="-" else t0
    for s,t in parts[1:]:
        out+=f" {s} {t}"
    return out.replace("+ -","- ")  # tidy "+ -frac" from negative phases

def build_latex(a,b,c,d):
    x1=_coordinate(a,b,c,d,0,0); y1=_coordinate(a,b,c,d,1,0)
    x2=_coordinate(a,b,c,d,0,1); y2=_coordinate(a,b,c,d,1,1)
    p1=f"\\left( {x1},\\ \\ {y1} \\right)"
    p2=f"\\left( {x2},\\ \\ {y2} \\right)"
    return p1,p2

# ------------------------------- run -------------------------------

data=np.load(CLEAN_FILE)
a,b,c,d=data['a'],data['b'],data['c'],data['d']
PATH=[int(x) for x in data['path']]

OUTPUT_DIR="final_"+"_".join(map(str,PATH))
os.makedirs(OUTPUT_DIR,exist_ok=True)
stem=os.path.join(OUTPUT_DIR,"diagram_"+"_".join(map(str,PATH)))

# 1) High-res diagram
k=np.arange(N)
x1,y1,x2,y2=calc_endpoints(k,a,b,c,d)
segs=np.stack([np.column_stack([x1,y1]),np.column_stack([x2,y2])],axis=1)
fig,ax=plt.subplots(figsize=FIGSIZE)
ax.set_axis_off()
ax.add_collection(LineCollection(segs,colors='black',linewidths=LINEWIDTH,alpha=ALPHA))
ax.set_aspect('equal')
ax.autoscale()
fig.savefig(stem+".png",dpi=DPI,bbox_inches='tight',pad_inches=0.1)
plt.close(fig)

# 2) LaTeX formula + rendered preview in the reference style
p1,p2=build_latex(a,b,c,d)
with open(stem+"_formula.tex","w") as f:
    f.write(f"% Endpoints of the k-th line segment, k = 1,2,...,{N}\n")
    f.write("\\[\n"+p1+"\n\\]\n\\[\n"+p2+"\n\\]\n")

ffig=plt.figure(figsize=(16,4))
ffig.text(0.5,0.95,f"For $k = 1,2,3,\\ldots,{N}$ the endpoints of the $k$-th line segment are:",
          ha='center',va='top',fontsize=14)
ffig.text(0.5,0.60,f"${p1}$",ha='center',va='center',fontsize=15)
ffig.text(0.5,0.25,f"and  ${p2}$",ha='center',va='center',fontsize=15)
ffig.savefig(stem+"_formula.png",dpi=200,bbox_inches='tight',pad_inches=0.3)
plt.close(ffig)

# 3) Animation: segments drawn one by one (GIF, loops continuously)
from matplotlib.animation import FuncAnimation,PillowWriter

class GifWriter(PillowWriter):
    def finish(self):  # loop=0 makes the GIF repeat indefinitely
        self._frames[0].save(self.outfile,save_all=True,append_images=self._frames[1:],
                             duration=int(1000/self.fps),loop=0)

afig,aax=plt.subplots(figsize=ANIM_FIGSIZE)
aax.set_axis_off()
aax.set_aspect('equal')
aax.add_collection(LineCollection(segs,colors='none'))  # set the view to the full diagram
aax.autoscale()
lc=LineCollection([],colors='black',linewidths=LINEWIDTH,alpha=ALPHA)
aax.add_collection(lc)

def update(n):
    lc.set_segments(segs[:n])
    return (lc,)
anim=FuncAnimation(afig,update,frames=range(0,N+1,ANIM_SEG_PER_FRAME),blit=True)
anim.save(stem+"_anim.gif",writer=GifWriter(fps=ANIM_FPS),dpi=ANIM_DPI)
plt.close(afig)

print("wrote files to "+OUTPUT_DIR)
