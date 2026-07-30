# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""Figures for G7 section 5 (synthesis + COURSE FINALE).

Fig 5.1  g7_s5_whichmethod  - decision flowchart: which classical method?
Fig 5.2  g7_s5_twoworlds    - posterior + credible interval  vs  20 confidence
                              intervals around a fixed theta
Fig 5.3  g7_s5_alphabeta    - the alpha/beta trade-off has no free lunch
Fig 5.4  g7_s5_arc          - THE COURSE ARC: G1 -> G7 concept map
"""
import io
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, "d:/Python-UV/MIT_Applied_Prob/notes/_build")
from mpl_style import PAL, INK, MUTED, GRID_C, diagram_ax, setup  # noqa: E402

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
plt, _ = setup()
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch  # noqa: E402

IMG = "d:/Python-UV/MIT_Applied_Prob/notes/img/"


def box(ax, x, y, w, h, text, fc="white", ec=None, fs=8.0, weight="normal",
        tc=None, va="center", pad=0.02):
    ec = ec or GRID_C
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle=f"round,pad={pad},rounding_size=0.12",
                                facecolor=fc, edgecolor=ec, linewidth=1.2,
                                zorder=2, mutation_aspect=1))
    yy = y if va == "center" else y + h / 2 - 0.18
    ax.text(x, yy, text, ha="center", va=va, fontsize=fs,
            color=tc or INK, zorder=3, linespacing=1.55, fontweight=weight)


def arrow(ax, x0, y0, x1, y1, color=None, lw=1.2, rad=0.0):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>",
                                 mutation_scale=11, color=color or MUTED,
                                 linewidth=lw, zorder=1,
                                 connectionstyle=f"arc3,rad={rad}",
                                 shrinkA=1, shrinkB=3))


# ==================================================================== Fig 5.1
fig, ax = plt.subplots(figsize=(10.6, 6.4))
diagram_ax(ax)
ax.set_aspect("auto")
ax.set_xlim(-0.4, 20.4)
ax.set_ylim(-0.3, 12.6)

box(ax, 10.0, 11.5, 15.0, 1.15,
    "$\\theta$ is an unknown CONSTANT, no prior available.  What do you owe?",
    fc="#f2f4f8", fs=10.0, weight="bold")

mids = [
    (2.6, "A single number\nfor $\\theta$", PAL[0]),
    (7.4, "A number PLUS\nan honest range", PAL[2]),
    (12.6, "A relation between\ntwo measured\nvariables", PAL[3]),
    (17.4, "A decision between\nhypotheses", PAL[1]),
]
for x, t, c in mids:
    box(ax, x, 8.9, 4.1, 1.5, t, fc="#fbfbfa", ec=c, fs=8.6)
    arrow(ax, 10.0, 10.85, x, 9.75)

# Each leaf is drawn line-block by line-block at explicit heights, so that the
# tall mathtext fractions cannot overprint the caption above or the prose below
# (matplotlib spaces the lines of a multi-line string by font size alone, and
# ignores how tall a \frac actually is).  MATH_FS is shared by all four boxes.
MATH_FS = 9.0
BODY_FS = 7.3
leaves = [
    (2.6, PAL[0], "MAXIMUM LIKELIHOOD",
     [(5.55, "$\\hat\\theta_{ML}=\\arg\\max_\\theta\\;p_X(x;\\theta)$")],
     "maximize $\\log$ of the\nlikelihood; check bias,\nthen consistency",
     "B&T \u00a79.1 / L23 slide 3,\nL24 slide 2  (G7 \u00a72)"),
    (7.4, PAL[2], "SAMPLE MEAN + CI",
     [(5.90, "$\\hat\\Theta_n=\\frac{1}{n}\\sum_i X_i$"),
      (4.95, "$\\hat\\Theta_n\\pm z\\,\\hat\\sigma/\\sqrt{n}$")],
     "unbiased, consistent;\n$z=1.96$ at $95\\%$;\nestimate $\\sigma$ with $\\hat S_n$",
     "B&T \u00a79.1 / L23 slides 5-7\n(G7 \u00a71)"),
    (12.6, PAL[3], "LINEAR REGRESSION",
     [(5.90, "$\\hat\\theta_1=\\dfrac{\\sum(x_i-\\bar x)(y_i-\\bar y)}"
             "{\\sum(x_i-\\bar x)^2}$"),
      (4.95, "$\\hat\\theta_0=\\bar y-\\hat\\theta_1\\bar x$")],
     "least squares; equals ML\nunder i.i.d. normal noise",
     "B&T \u00a79.2 / L24 slides 3-4\n(G7 \u00a73)"),
    (17.4, PAL[1], "LIKELIHOOD RATIO TEST",
     [(5.95, "reject $H_0$ iff", BODY_FS),
      (4.95, "$\\dfrac{p_X(x;H_1)}{p_X(x;H_0)}>\\xi$")],
     "fix $\\alpha=\\mathbf{P}(\\text{reject }H_0;H_0)$,\n"
     "then $\\xi$; $\\beta$ is whatever\nit turns out to be",
     "B&T \u00a79.3 / L24 slides 7-8,\nL25 slide 2  (G7 \u00a74)"),
]
for x, c, head, math_lines, body, srcline in leaves:
    box(ax, x, 4.35, 4.35, 5.5, "", fc="white", ec=c)
    arrow(ax, x, 8.1, x, 7.35, color=c)
    ax.text(x, 6.62, head, ha="center", va="center", fontsize=BODY_FS + 0.5,
            color=INK, zorder=4)
    for entry in math_lines:
        y, s = entry[0], entry[1]
        fs = entry[2] if len(entry) > 2 else MATH_FS
        ax.text(x, y, s, ha="center", va="center", fontsize=fs,
                color=INK, zorder=4)
    ax.text(x, 3.55, body, ha="center", va="center", fontsize=BODY_FS,
            color=INK, zorder=4, linespacing=1.75)
    ax.text(x, 2.20, srcline, ha="center", va="center", fontsize=BODY_FS,
            color=MUTED, zorder=4, linespacing=1.75)

ax.text(10.0, 0.55, "If a prior for $\\theta$ is available and defensible, you are in G6 "
        "instead: posterior \u2192 MAP / LMS / linear LMS.",
        ha="center", va="bottom", fontsize=8.2, color=MUTED, style="italic")
ax.set_title("Which classical method?", fontsize=11.5, color=INK, pad=6)
fig.savefig(IMG + "g7_s5_whichmethod.png", dpi=150)
plt.close(fig)
print("wrote g7_s5_whichmethod.png")

# ==================================================================== Fig 5.2
fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.4, 4.4),
                               gridspec_kw=dict(width_ratios=[1.0, 1.15],
                                                wspace=0.28))

# --- left: Bayesian.  prior N(0, 5^2), n = 10 obs of N(theta, 2^2), xbar = 5
mu0, s0, n_e, sig, xbar = 0.0, 5.0, 10, 2.0, 5.0
w = (1 / s0 ** 2) / (1 / s0 ** 2 + n_e / sig ** 2)
pm = w * mu0 + (1 - w) * xbar
ps = np.sqrt(1.0 / (1 / s0 ** 2 + n_e / sig ** 2))
t = np.linspace(-2.0, 10.0, 600)
axL.plot(t, stats.norm.pdf(t, mu0, s0), color=MUTED, lw=1.4, ls="--",
         label="prior  $N(0,5^2)$")
axL.plot(t, stats.norm.pdf(t, pm, ps), color=PAL[0], lw=2.2,
         label="posterior, given data")
lo, hi = pm - 1.959964 * ps, pm + 1.959964 * ps
m = (t >= lo) & (t <= hi)
axL.fill_between(t[m], 0, stats.norm.pdf(t[m], pm, ps), color=PAL[0], alpha=0.16)
axL.plot([lo, hi], [0.018, 0.018], color=PAL[0], lw=3, solid_capstyle="butt")
axL.set_ylim(0, 0.92)   # headroom so the annotation clears the posterior peak
axL.set_xlabel(r"$\theta$   — the unknown is the random thing")
axL.set_ylabel("density")
axL.set_title("BAYESIAN: data fixed, $\\Theta$ random", fontsize=10)
axL.annotate(f"$95\\%$ credible interval\n"
             f"$\\mathbf{{P}}(\\Theta\\in[{lo:.2f},\\,{hi:.2f}]\\mid X=x)=0.95$",
             xy=(-1.85, 0.90), ha="left", va="top", fontsize=8.4, color=INK)
axL.legend(loc="upper left", fontsize=7.6, bbox_to_anchor=(0.0, 0.86))

# --- right: classical. 20 replications, 95% CIs around a FIXED theta
theta, sigma, n_obs = 5.0, 2.0, 25
half = 1.959964 * sigma / np.sqrt(n_obs)
demo = np.random.default_rng(4).normal(theta, sigma, size=(20, n_obs)).mean(axis=1)
axR.axvline(theta, color=INK, lw=1.6, zorder=1)
axR.text(theta + 0.06, 22.6, r"the true $\theta=5$ (fixed, not random)",
         fontsize=8.4, color=INK, va="center")
for i, mh in enumerate(demo):
    y = 20 - i
    miss = abs(mh - theta) > half
    c = PAL[7] if miss else PAL[2]
    axR.plot([mh - half, mh + half], [y, y], color=c, lw=2.0,
             solid_capstyle="butt", zorder=2)
    axR.plot([mh], [y], "o", color=c, ms=3.4, zorder=3)
axR.plot([], [], color=PAL[2], lw=2.0, label="covers $\\theta$  (19 of 20)")
axR.plot([], [], color=PAL[7], lw=2.0, label="misses  (1 of 20)")
axR.set_ylim(-3.4, 23.4)
axR.set_xlim(3.3, 7.0)
axR.set_yticks([])
axR.set_xlabel(r"$\hat\Theta_n\pm 1.96\,\sigma/\sqrt{n}$   — the interval is the random thing")
axR.set_title("CLASSICAL: $\\theta$ fixed, the interval random", fontsize=10)
axR.legend(loc="lower right", fontsize=8)
axR.grid(axis="y", visible=False)

fig.savefig(IMG + "g7_s5_twoworlds.png", dpi=150)
plt.close(fig)
print("wrote g7_s5_twoworlds.png")

# ==================================================================== Fig 5.3
fig, (axA, axB) = plt.subplots(1, 2, figsize=(10.0, 4.2),
                               gridspec_kw=dict(wspace=0.28))
n_g = 10
sqn = np.sqrt(n_g)
al = np.linspace(1e-4, 0.999, 600)
xi = stats.norm.ppf(1 - al) * sqn
be = stats.norm.cdf((xi - n_g) / sqn)

axA.plot(al, be, color=PAL[1], lw=2.2)
for a0, lab in ((0.20, None), (0.05, None), (0.01, None)):
    x0 = stats.norm.ppf(1 - a0) * sqn
    b0 = float(stats.norm.cdf((x0 - n_g) / sqn))
    axA.plot([a0], [b0], "o", color=PAL[0], ms=6, zorder=4)
    axA.annotate(f"$\\alpha={a0}$\n$\\beta={b0:.4f}$", xy=(a0, b0),
                 xytext=(a0 + 0.075, b0 + 0.055), fontsize=8.2, color=INK)
axA.set_xlabel(r"$\alpha$ = $\mathbf{P}$(reject $H_0$ ; $H_0$)  — false alarm")
axA.set_ylabel(r"$\beta$ = $\mathbf{P}$(accept $H_0$ ; $H_1$)  — missed detection")
axA.set_title(r"One $n$: every $\alpha$ you save costs $\beta$", fontsize=10)
axA.set_xlim(-0.02, 0.72)
axA.set_ylim(-0.02, 0.62)

for n, c in ((10, PAL[1]), (40, PAL[3]), (160, PAL[2])):
    s = np.sqrt(n)
    x = stats.norm.ppf(1 - al) * s
    bb = stats.norm.cdf((x - n) / s)
    bb = np.where(bb < 1e-30, np.nan, bb)
    axB.semilogy(al, bb, color=c, lw=2.0, label=f"$n={n}$")
axB.axvline(0.05, color=MUTED, lw=1.0, ls=":")
for n, c, b in ((10, PAL[1], 6.458e-2), (40, PAL[3], 1.436e-6),
                (160, PAL[2], 1.823e-28)):
    axB.plot([0.05], [b], "o", color=c, ms=6.5, zorder=6,
             markeredgecolor="white", markeredgewidth=0.8)
axB.annotate(r"at $\alpha=0.05$ (dotted):  $\beta$ falls" "\n"
             r"from $6.46\times10^{-2}$ ($n=10$) to" "\n"
             r"$1.82\times10^{-28}$ ($n=160$)",
             xy=(0.34, 3e-13), fontsize=8.4, color=INK)
axB.set_xlabel(r"$\alpha$")
axB.set_ylabel(r"$\beta$  (log scale)")
axB.set_title("More data is the only free lunch", fontsize=10)
axB.set_ylim(1e-30, 2.0)
axB.legend(loc="lower right", fontsize=8.5)
fig.suptitle("$H_0$: $X_i\\sim N(0,1)$ versus $H_1$: $X_i\\sim N(1,1)$, "
             "reject when $\\sum_i X_i>\\xi'$",
             fontsize=10.5, color=INK, y=1.02)
fig.savefig(IMG + "g7_s5_alphabeta.png", dpi=150)
plt.close(fig)
print("wrote g7_s5_alphabeta.png")

# ==================================================================== Fig 5.4
fig, ax = plt.subplots(figsize=(15.0, 9.0))
diagram_ax(ax)
ax.set_aspect("auto")
ax.set_xlim(-0.6, 28.6)
ax.set_ylim(-0.4, 17.0)

PHASE = [(2.0, 3.9, "PHASE 1 \u00b7 MODELS", "#eef3fb", PAL[0]),
         (8.0, 7.9, "PHASE 2 \u00b7 RANDOM VARIABLES", "#eefaf5", PAL[2]),
         (16.0, 7.9, "PHASE 3 \u00b7 PROCESSES IN TIME", "#fdf6e7", PAL[3]),
         (24.0, 7.9, "PHASE 4 \u00b7 WHAT THE DATA SAYS", "#fdf1ea", PAL[1])]
for x, w, t, fc, ec in PHASE:
    box(ax, x, 15.6, w, 1.0, t, fc=fc, ec=ec, fs=9.5, weight="bold", tc=ec)

NOTES = [
    (2.0, "G1", "Probability models", "#eef3fb", PAL[0],
     "sample space + axioms\nconditioning, Bayes\nindependence\ncounting"),
    (6.0, "G2", "Discrete r.v.'s", "#eefaf5", PAL[2],
     "PMFs, the four families\n$\\mathbb{E}$, linearity, $\\operatorname{var}$\n"
     "joint PMFs\n$\\operatorname{var}(M_n)=\\sigma^2/n$"),
    (10.0, "G3", "Continuous r.v.'s", "#eefaf5", PAL[2],
     "PDFs, CDFs, normal\njoint + continuous Bayes\nderived distributions\n"
     "convolution, cov, $\\rho$"),
    (14.0, "G4", "Conditioning\n& processes", "#fdf6e7", PAL[3],
     "$\\mathbb{E}[X\\mid Y]$ as a r.v.\niterated expectations\nrandom sums\n"
     "Bernoulli / Poisson"),
    (18.0, "G5", "Markov chains", "#fdf6e7", PAL[3],
     "$n$-step: $R(n)=P^n$\nrecurrent / transient\nbalance eqns for $\\pi$\n"
     "absorption probs & times"),
    (22.0, "G6", "Limits &\nBayesian inference", "#fdf1ea", PAL[1],
     "Markov, Chebyshev\nWLLN, CLT\nposterior, MAP\nLMS, linear LMS"),
    (26.0, "G7", "Classical\ninference", "#fdf1ea", PAL[1],
     "bias, consistency, CIs\nmaximum likelihood\nlinear regression\n"
     "LRT, $\\alpha$ vs $\\beta$"),
]
for x, tag, name, fc, ec, body in NOTES:
    box(ax, x, 11.6, 3.3, 5.0, "", fc=fc, ec=ec)
    ax.text(x, 13.7, tag, ha="center", va="center", fontsize=13,
            fontweight="bold", color=ec, zorder=4)
    ax.text(x, 12.85, name, ha="center", va="center", fontsize=8.6,
            fontweight="bold", color=INK, zorder=4)
    ax.text(x, 10.7, body, ha="center", va="center", fontsize=7.2,
            color=MUTED, zorder=4, linespacing=1.65)
for x in (2.0, 6.0, 10.0, 14.0, 18.0, 22.0):
    arrow(ax, x + 1.75, 11.6, x + 2.25, 11.6, lw=1.4)

ax.text(14.0, 16.6,
        "outcomes  \u2192  numbers  \u2192  numbers that evolve  \u2192  "
        "numbers that tell you about the model",
        ha="center", va="center", fontsize=10.5, color=INK, style="italic")

# the three cross-cutting threads, drawn as straight lanes beneath the row
ax.text(0.0, 8.62, "THREE THREADS RUN THROUGH ALL SEVEN NOTES  \u2193", ha="left",
        va="center", fontsize=8.6, fontweight="bold", color=INK)
LANES = [(2.0, 26.0, 7.75, PAL[0], (6.0, 10.0, 14.0, 18.0, 22.0),
          "condition and renormalize:   $\\mathbf{P}(A\\mid B)$ (G1 \u00a72)   "
          "$\\rightarrow$   posterior $f_{\\Theta\\mid X}$ (G6 \u00a73)   $\\rightarrow$   "
          "likelihood ratio $p_X(x;H_1)/p_X(x;H_0)$ (G7 \u00a74)"),
         (6.0, 26.0, 6.55, PAL[2], (10.0, 14.0, 18.0, 22.0),
          "averages concentrate:   $\\operatorname{var}(M_n)=\\sigma^2/n$ (G2 \u00a73)   "
          "$\\rightarrow$   WLLN & CLT (G6 \u00a71\u2013\u00a72)   $\\rightarrow$   consistency and "
          "$\\hat\\Theta_n\\pm z\\hat\\sigma/\\sqrt{n}$ (G7 \u00a71)"),
         (14.0, 22.0, 5.35, PAL[3], (18.0,),
          "conditional expectation:   $\\mathbb{E}[X\\mid Y]$ as a random variable "
          "(G4 \u00a71)   $\\rightarrow$   LMS estimator $\\mathbb{E}[\\Theta\\mid X]$ (G6 \u00a74)")]
for x0, x1, y, c, mids_x, lab in LANES:
    ax.plot([x0, x0], [9.05, y], color=c, lw=1.0, ls=":", zorder=1)
    ax.plot([x1, x1], [9.05, y], color=c, lw=1.0, ls=":", zorder=1)
    ax.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle="-|>",
                                 mutation_scale=12, color=c, linewidth=1.6,
                                 zorder=1, shrinkA=0, shrinkB=0))
    for mx in mids_x:
        ax.plot([mx], [y], "o", color=c, ms=3.2, zorder=2)
    ax.text(x0 + 0.25, y + 0.42, lab, ha="left", va="bottom", fontsize=7.8,
            color=c, zorder=5,
            bbox=dict(boxstyle="round,pad=0.16", facecolor="white",
                      edgecolor="none"))

box(ax, 14.0, 2.3, 27.4, 4.2, "", fc="#fafaf7", ec=GRID_C)
ax.text(14.0, 3.98, "TWO IDEAS AND ONE FACT CARRY THE WHOLE COURSE",
        ha="center", va="center", fontsize=9.6, fontweight="bold", color=INK)
LINES = [
    (3.05, "1.  ADDITIVITY OVER A PARTITION.  Total probability (G1 \u00a72) "
           "$\\rightarrow$ total expectation (G4 \u00a71) $\\rightarrow$ balance "
           "equations (G5 \u00a73) $\\rightarrow$ the Bayes denominator (G6 \u00a73)."),
    (2.12, "2.  RENORMALIZE INSIDE THE CONDITIONING EVENT.  Conditional "
           "probability (G1 \u00a72) $\\rightarrow$ conditional PDFs (G3 \u00a73) "
           "$\\rightarrow$ posteriors (G6 \u00a73) $\\rightarrow$ likelihood ratios "
           "(G7 \u00a74)."),
    (1.19, "3.  AVERAGES CONCENTRATE.  $\\operatorname{var}(M_n)=\\sigma^2/n$ "
           "(G2 \u00a73) $\\rightarrow$ WLLN and CLT (G6 \u00a71\u2013\u00a72) "
           "$\\rightarrow$ consistency, confidence intervals, and every "
           "significance level in G7."),
]
for y, s in LINES:
    ax.text(1.0, y, s, ha="left", va="center", fontsize=8.0, color=INK)
ax.text(14.0, 0.35, "Everything else in seven notes is one of these three, "
        "applied to a particular decomposition.",
        ha="center", va="center", fontsize=8.4, color=MUTED, style="italic")

ax.set_title("The whole course, G1 \u2192 G7", fontsize=13,
             color=INK, pad=10)
fig.savefig(IMG + "g7_s5_arc.png", dpi=150)
plt.close(fig)
print("wrote g7_s5_arc.png")
