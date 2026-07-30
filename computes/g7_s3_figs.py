# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Figures for G7 §3 — linear regression. Writes notes/img/g7_s3_*.png."""
import io
import sys
import numpy as np

sys.path.insert(0, "d:/Python-UV/MIT_Applied_Prob/notes/_build")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)

from mpl_style import setup, diagram_ax, PAL, INK, MUTED, GRID_C, AXIS_C  # noqa: E402

plt, _ = setup()
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch  # noqa: E402

OUT = "d:/Python-UV/MIT_Applied_Prob/notes/img/"

XS = np.array([1, 2, 3, 4, 5, 6, 7, 8], float)
YS = np.array([63, 61, 72, 74, 79, 87, 86, 98], float)
T0, T1 = 55.0, 5.0


# ==========================================================================
# Fig 3.1 — residual geometry (regenerates the L24 slide 3 diagram)
# ==========================================================================
def fig_residual():
    fig, ax = plt.subplots(figsize=(6.6, 4.3))
    x = np.array([1.0, 2.2, 3.5, 4.6, 6.0, 7.2])
    y = np.array([1.55, 3.35, 2.30, 2.62, 3.75, 4.05])
    b1, b0 = np.polyfit(x, y, 1)
    xl = np.array([0.0, 8.0])
    ax.plot(xl, b0 + b1 * xl, color=PAL[0], lw=2.2, zorder=3)
    for xi, yi in zip(x, y):
        ax.plot([xi, xi], [yi, b0 + b1 * xi], color=MUTED, lw=1.1, ls=(0, (3, 2)), zorder=2)
    ax.plot(x, y, "x", color=PAL[1], ms=9, mew=2.2, zorder=4)

    i = 1                                   # the highlighted point (x_i, y_i)
    xi, yi, fi = x[i], y[i], b0 + b1 * x[i]
    ax.annotate("", xy=(xi + 0.22, yi), xytext=(xi + 0.22, fi),
                arrowprops=dict(arrowstyle="<->", color=PAL[3], lw=2.0), zorder=5)
    ax.annotate(r"$(x_i,\,y_i)$", xy=(xi, yi), xytext=(xi - 1.05, yi + 0.38),
                color=INK, fontsize=10,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.9))
    ax.annotate("residual\n" + r"$y_i-\hat\theta_0-\hat\theta_1 x_i$",
                xy=(xi + 0.28, (yi + fi) / 2), xytext=(3.5, 4.55),
                ha="center", va="center", color=INK, fontsize=10,
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0,
                                connectionstyle="arc3,rad=0.15"))
    ax.text(7.95, b0 + b1 * 7.95 - 0.30, r"$y=\hat\theta_0+\hat\theta_1 x$",
            color=PAL[0], fontsize=11, ha="right", va="top")
    ax.plot([0.3, 0.3], [0, b0 + 0.02], lw=0)   # keep intercept visible
    ax.annotate("", xy=(0, b0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="<->", color=MUTED, lw=1.2))
    ax.text(0.12, b0 / 2, r"$\hat\theta_0$", color=MUTED, fontsize=10, va="center")
    ax.set_xlim(-0.35, 8.4)
    ax.set_ylim(0, 5.3)
    ax.set_xlabel("$x$ (the fixed explanatory value)")
    ax.set_ylabel("$y$ (the noisy response)")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    ax.spines["left"].set_color(AXIS_C)
    ax.spines["bottom"].set_color(AXIS_C)
    ax.set_title("Least squares minimizes the sum of the SQUARED vertical gaps")
    fig.savefig(OUT + "g7_s3_residual.png")
    plt.close(fig)
    print("wrote g7_s3_residual.png")


# ==========================================================================
# Fig 3.2 — the normal equations: SSE bowl, its contours, the two lines
# ==========================================================================
def fig_normaleq():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.3))

    ax = axes[0]
    t0 = np.linspace(35, 75, 260)
    t1 = np.linspace(2.0, 8.0, 260)
    T0g, T1g = np.meshgrid(t0, t1)
    SSE = np.zeros_like(T0g)
    for xi, yi in zip(XS, YS):
        SSE += (yi - T0g - T1g * xi) ** 2
    lv = [60 + d for d in (25, 100, 250, 550, 1050, 1800)]
    ax.contourf(T0g, T1g, SSE, levels=[0] + lv + [1e9],
                colors=["#dceaf8", "#e6f0fa", "#eef5fc", "#f4f8fd",
                        "#f9fbfe", "#fdfdff", "white", "white"], zorder=0)
    cs = ax.contour(T0g, T1g, SSE, levels=lv, colors=[AXIS_C], linewidths=0.9, zorder=1)
    # Inline contour labels, placed by hand on the transverse (lower) arcs.
    # The two normal-equation lines run almost exactly along the ellipses' long
    # axes, so the ends of every ellipse are occupied; the arc directly below
    # the optimum is the only clear ground, and it is also clear of the green
    # marker and of the annotation leader line (which leaves to the upper right).
    ax.clabel(cs, [lv[1], lv[3]], fmt="SSE = %.0f", fontsize=7.5, colors=[MUTED],
              manual=[(55.0, 4.30), (55.0, 3.36)])
    # normal equation E0:  n*t0 + (sum x) t1 = sum y  ->  8 t0 + 36 t1 = 620
    ax.plot(t0, (620 - 8 * t0) / 36, color=PAL[0], lw=2.0,
            label=r"$(\mathrm{E}_0)$   $8\theta_0+36\theta_1=620$")
    # normal equation E1: (sum x) t0 + (sum x^2) t1 = sum xy -> 36 t0 + 204 t1 = 3000
    ax.plot(t0, (3000 - 36 * t0) / 204, color=PAL[1], lw=2.0,
            label=r"$(\mathrm{E}_1)$   $36\theta_0+204\theta_1=3000$")
    ax.plot([55], [5], "o", color=PAL[5], ms=9, zorder=5)
    ax.annotate(r"$(\hat\theta_0,\hat\theta_1)=(55,\,5)$" + "\n" + r"$\mathrm{SSE}=60$",
                xy=(55, 5), xytext=(60.5, 6.6), fontsize=9.5, color=INK,
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))
    ax.set_xlim(35, 75)
    ax.set_ylim(2.0, 8.0)
    ax.set_xlabel(r"intercept $\theta_0$")
    ax.set_ylabel(r"slope $\theta_1$")
    ax.set_title("SSE contours and the two normal equations")
    ax.legend(loc="lower left", fontsize=8.5)

    ax = axes[1]
    tt0 = np.linspace(40, 70, 400)
    s_t0 = np.array([np.sum((YS - a - 5 * XS) ** 2) for a in tt0])
    tt1 = np.linspace(3.0, 7.0, 400)
    s_t1 = np.array([np.sum((YS - 55 - b * XS) ** 2) for b in tt1])
    ax.plot(tt0, s_t0, color=PAL[0], lw=2.0, label=r"$\mathrm{SSE}(\theta_0,\ \theta_1=5)$")
    ax2 = ax.twiny()
    ax2.plot(tt1, s_t1, color=PAL[1], lw=2.0, label=r"$\mathrm{SSE}(\theta_0=55,\ \theta_1)$")
    ax2.set_xlim(3.0, 7.0)
    ax2.set_xlabel(r"slope $\theta_1$  (orange curve)", color=PAL[1])
    ax2.tick_params(axis="x", colors=PAL[1])
    ax2.grid(False)
    ax.axhline(60, color=MUTED, ls=(0, (4, 3)), lw=1.1)
    ax.text(41, 95, r"minimum $\mathrm{SSE}=60$", color=MUTED, fontsize=9)
    ax.plot([55], [60], "o", color=PAL[0], ms=7, zorder=5)
    ax2.plot([5], [60], "o", color=PAL[1], ms=7, zorder=5)
    ax.set_xlim(40, 70)
    ax.set_ylim(0, 1500)
    ax.set_xlabel(r"intercept $\theta_0$  (blue curve)", color=PAL[0])
    ax.tick_params(axis="x", colors=PAL[0])
    ax.set_ylabel("SSE")
    ax.set_title("Each one-dimensional slice is an upward parabola", pad=34)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper center", fontsize=8.5)
    fig.tight_layout()
    fig.savefig(OUT + "g7_s3_normaleq.png")
    plt.close(fig)
    print("wrote g7_s3_normaleq.png")


# ==========================================================================
# Fig 3.3 — the worked example
# ==========================================================================
def fig_worked():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.2))
    ax = axes[0]
    xl = np.array([0.4, 9.2])
    ax.plot(xl, T0 + T1 * xl, color=PAL[0], lw=2.2,
            label=r"fit  $y=55+5x$")
    for xi, yi in zip(XS, YS):
        ax.plot([xi, xi], [yi, T0 + T1 * xi], color=PAL[3], lw=1.6, zorder=2)
    ax.plot(XS, YS, "o", color=PAL[1], ms=7, zorder=4, label="data $(x_i,y_i)$")
    ax.plot([4.5], [77.5], "*", color=PAL[5], ms=15, zorder=5,
            label=r"$(\bar x,\bar y)=(4.5,\,77.5)$")
    for xi, yi in zip(XS, YS):
        r = yi - (T0 + T1 * xi)
        # anchor each label at the data-point end of its segment and push it
        # OUTWARD (up for r > 0, down for r < 0), so it never sits on the fit line
        ax.annotate(f"{r:+.0f}", xy=(xi, yi),
                    xytext=(8, 7 if r > 0 else -7), textcoords="offset points",
                    fontsize=8.5, color=PAL[3], va="center", ha="left")
    ax.set_xlim(0.4, 9.2)
    ax.set_ylim(55, 103)
    ax.set_xlabel("$x$ = weekly problem-set hours")
    ax.set_ylabel("$y$ = final exam score")
    ax.set_title(r"$\hat\theta_1=210/42=5$,   $\hat\theta_0=77.5-5(4.5)=55$")
    ax.legend(loc="upper left", fontsize=8.5)

    ax = axes[1]
    resid = YS - (T0 + T1 * XS)
    ax.axhline(0, color=AXIS_C, lw=1.4)
    ax.vlines(XS, 0, resid, color=PAL[3], lw=1.6)
    ax.plot(XS, resid, "o", color=PAL[3], ms=7)
    ax.set_xlim(0.4, 9.2)
    ax.set_ylim(-7.4, 5.6)
    ax.set_xlabel("$x$")
    ax.set_ylabel("residual  $y_i-\\hat\\theta_0-\\hat\\theta_1 x_i$")
    ax.set_title(r"Residuals: $\sum r_i=0$,  $\sum x_i r_i=0$,  $\mathrm{SSE}=60$")
    ax.text(4.5, -7.0, "no trend, no fan shape, no curve = nothing left for a line to explain",
            fontsize=8.5, color=MUTED, va="bottom", ha="center")
    fig.tight_layout()
    fig.savefig(OUT + "g7_s3_worked.png")
    plt.close(fig)
    print("wrote g7_s3_worked.png")


# ==========================================================================
# Fig 3.4 — B&T Example 9.9, leaning tower of Pisa
# ==========================================================================
def fig_pisa():
    yr = np.arange(1975, 1988)
    lean = np.array([2.9642, 2.9644, 2.9656, 2.9667, 2.9673, 2.9688, 2.9696,
                     2.9698, 2.9713, 2.9717, 2.9725, 2.9742, 2.9757])
    b1, b0 = np.polyfit(yr, lean, 1)
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.0))
    ax = axes[0]
    xl = np.array([1974.0, 1988.0])
    ax.plot(xl, b0 + b1 * xl, color=PAL[0], lw=2.0,
            label=r"$y=1.123338+0.00093187\,x$")
    ax.plot(yr, lean, "o", color=PAL[1], ms=6, label="measured lean")
    ax.set_xlim(1974, 1988)
    ax.set_ylim(2.9625, 2.9772)
    ax.set_xlabel("year $x$")
    ax.set_ylabel("lean $y$ (metres)")
    ax.set_title(r"B&T Example 9.9   ($R^2=0.988$)")
    ax.legend(loc="upper left", fontsize=8.5)

    ax = axes[1]
    r = (lean - (b0 + b1 * yr)) * 1000.0
    ax.axhline(0, color=AXIS_C, lw=1.4)
    ax.vlines(yr, 0, r, color=PAL[3], lw=1.6)
    ax.plot(yr, r, "o", color=PAL[3], ms=6)
    ax.set_xlim(1974, 1988)
    ax.set_xlabel("year $x$")
    ax.set_ylabel("residual (millimetres)")
    ax.set_title("Residuals: sub-millimetre and patternless")
    ax.set_ylim(-0.95, 0.95)
    ax.text(1974.35, -0.90, "largest 0.74 mm; 9 sign runs in 13 points\n"
                            "(pure noise would average 7) — no curve left",
            fontsize=8.5, color=MUTED, va="bottom")
    fig.tight_layout()
    fig.savefig(OUT + "g7_s3_pisa.png")
    plt.close(fig)
    print("wrote g7_s3_pisa.png")


# ==========================================================================
# Fig 3.5 — decision flowchart: which regression?
# ==========================================================================
def box(ax, x, y, w, h, text, fc, ec, fs=9.0, weight="normal"):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.012,rounding_size=0.03",
                                facecolor=fc, edgecolor=ec, lw=1.3, zorder=2))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=INK,
            zorder=3, fontweight=weight, linespacing=1.35)


def diamond(ax, x, y, w, h, text, fs=8.8):
    ax.add_patch(plt.Polygon([[x, y + h / 2], [x + w / 2, y], [x, y - h / 2], [x - w / 2, y]],
                             facecolor="#fdf6e3", edgecolor=PAL[3], lw=1.3, zorder=2))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=INK,
            zorder=3, linespacing=1.3)


def arrow(ax, p, q, label=None, lx=0, ly=0, color=None):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=13,
                                 color=color or MUTED, lw=1.2, zorder=1,
                                 shrinkA=2, shrinkB=3))
    if label:
        ax.text((p[0] + q[0]) / 2 + lx, (p[1] + q[1]) / 2 + ly, label,
                fontsize=8.2, color=MUTED, ha="center", va="center", zorder=4,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))


def fig_flow():
    fig, ax = plt.subplots(figsize=(9.6, 7.4))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    ax.grid(False)

    box(ax, 32, 95, 46, 7,
        "data pairs $(x_i,y_i)$, $i=1,\\dots,n$;\nyou want to predict $y$ from $x$",
        "#eef4fc", PAL[0], fs=9.5, weight="bold")
    diamond(ax, 32, 82, 40, 12, "do you have a genuine PRIOR\ndistribution for the coefficients?")
    box(ax, 80, 82, 34, 9,
        "BAYESIAN linear regression\nMAP formulas, B&T §9.2\n(shrinks toward the prior mean)",
        "#f7f0fb", PAL[6], fs=8.6)
    arrow(ax, (32, 91.5), (32, 88), None)
    arrow(ax, (52, 82), (63, 82), "yes", ly=2.4)

    diamond(ax, 32, 66, 40, 12, "on a scatter plot, is the trend\nroughly a straight line?")
    arrow(ax, (32, 76), (32, 72), "no", lx=3.2)
    box(ax, 80, 66, 34, 11,
        "change the variable, not the method:\nfit $y\\approx\\theta_0+\\theta_1 h(x)$\n"
        "(e.g. $h(x)=x^2$ or $\\ln x$)\nstill LINEAR least squares in $\\theta$",
        "#eef9f4", PAL[2], fs=8.6)
    arrow(ax, (52, 66), (63, 66), "no", ly=2.4)

    diamond(ax, 32, 50, 40, 12, "one explanatory variable,\nor several?")
    arrow(ax, (32, 60), (32, 56), "yes", lx=3.6)
    box(ax, 80, 50, 34, 9,
        "MULTIPLE regression\n$\\min\\sum(y_i-\\theta_0-\\theta_1x_i-\\theta_2z_i)^2$\n"
        "watch for multicollinearity",
        "#eef9f4", PAL[2], fs=8.6)
    arrow(ax, (52, 50), (63, 50), "several", ly=2.4)

    diamond(ax, 32, 34, 40, 12, "do the residuals have\nroughly constant spread?")
    arrow(ax, (32, 44), (32, 40), "one", lx=3.2)
    box(ax, 80, 34, 34, 9,
        "WEIGHTED least squares\n$\\min\\sum\\alpha_i(y_i-\\theta_0-\\theta_1x_i)^2$\n"
        "with $\\alpha_i$ small where $\\sigma_i$ is large",
        "#fdf1ec", PAL[1], fs=8.6)
    arrow(ax, (52, 34), (63, 34), "no (heteroskedastic)", lx=-1.5, ly=2.6)

    box(ax, 32, 18, 52, 16,
        "SIMPLE linear regression — closed form\n\n"
        "$\\hat\\theta_1=\\dfrac{\\sum(x_i-\\bar x)(y_i-\\bar y)}{\\sum(x_i-\\bar x)^2}$,"
        "   $\\hat\\theta_0=\\bar y-\\hat\\theta_1\\bar x$",
        "#eef4fc", PAL[0], fs=9.4, weight="bold")
    arrow(ax, (32, 28), (32, 26.2), "yes", lx=3.4, ly=0.9)

    box(ax, 32, 3.4, 62, 6.2,
        "then report: $\\hat\\sigma=\\sqrt{\\mathrm{SSE}/(n-2)}$, confidence intervals for "
        "$\\theta_0,\\theta_1$, $R^2$,\nand a residual plot — and do NOT claim causation",
        "#fbfbf8", AXIS_C, fs=8.8)
    arrow(ax, (32, 10.0), (32, 6.8))

    ax.set_title("Which regression? (L24 slides 3–6 · B&T §9.2)",
                 fontsize=11.5, fontweight="600", pad=6)
    fig.savefig(OUT + "g7_s3_flow.png")
    plt.close(fig)
    print("wrote g7_s3_flow.png")


# ==========================================================================
# Fig 3.6 — three ways regression misleads
# ==========================================================================
def fig_pitfalls():
    fig, axes = plt.subplots(1, 3, figsize=(12.6, 3.9))
    rng = np.random.default_rng(41)

    # (a) extrapolation
    ax = axes[0]
    xa = np.linspace(1, 8, 14)
    ya = 40 + 30 * np.log(xa) + rng.normal(0, 1.6, xa.size)
    b1, b0 = np.polyfit(xa, ya, 1)
    xhi = 18.0
    xf = np.linspace(1, xhi, 200)
    ax.plot(xf, b0 + b1 * xf, color=PAL[0], lw=2.0, label="fitted line")
    ax.plot(xf, 40 + 30 * np.log(xf), color=PAL[2], lw=2.0, ls=(0, (5, 3)),
            label="true relation")
    ax.plot(xa, ya, "o", color=PAL[1], ms=5, label="data")
    ax.axvspan(1, 8, color=PAL[0], alpha=0.07)
    ax.text(4.5, 41, "data range", fontsize=8.5, color=MUTED, ha="center")
    gap = (b0 + b1 * 15.0) - (40 + 30 * np.log(15.0))
    ax.annotate(f"at $x=15$ the line is\n{gap:.0f} above the truth",
                xy=(15.0, 0.5 * ((b0 + b1 * 15.0) + (40 + 30 * np.log(15.0)))),
                xytext=(2.0, 175), fontsize=8.5, color=INK, ha="left",
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0,
                                connectionstyle="arc3,rad=-0.2"))
    ax.annotate("", xy=(15.0, b0 + b1 * 15.0), xytext=(15.0, 40 + 30 * np.log(15.0)),
                arrowprops=dict(arrowstyle="<->", color=PAL[3], lw=1.8))
    ax.set_xlim(1, xhi)
    ax.set_ylim(35, 205)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title("(a) Extrapolation")
    ax.legend(loc="lower right", fontsize=8)

    # (b) heteroskedasticity
    ax = axes[1]
    xb = np.linspace(1, 10, 60)
    yb = 5 + 2 * xb + rng.normal(0, 0.35 * xb ** 1.4, xb.size)
    b1b, b0b = np.polyfit(xb, yb, 1)
    ax.plot(xb, b0b + b1b * xb, color=PAL[0], lw=2.0)
    ax.plot(xb, yb, "o", color=PAL[1], ms=4.5)
    ax.fill_between(xb, 5 + 2 * xb - 2 * 0.35 * xb ** 1.4, 5 + 2 * xb + 2 * 0.35 * xb ** 1.4,
                    color=PAL[1], alpha=0.10)
    ax.set_xlim(0.5, 10.5)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title("(b) Heteroskedasticity")
    ax.text(1.0, 36, "spread grows with $x$:\nthe right-hand points\ndominate the fit",
            fontsize=8.5, color=MUTED, va="top")

    # (c) one high-leverage point (Practice 3.13 data)
    ax = axes[2]
    x2 = np.append(XS, 15.0)
    y2 = np.append(YS, 60.0)
    b1c, b0c = np.polyfit(x2, y2, 1)
    xl = np.array([0.4, 16.0])
    ax.plot(xl, T0 + T1 * xl, color=PAL[2], lw=2.0, ls=(0, (5, 3)),
            label=r"8 points: $y=55+5x$")
    ax.plot(xl, b0c + b1c * xl, color=PAL[7], lw=2.0,
            label=r"9 points: $y=73.67+0.33x$")
    ax.plot(XS, YS, "o", color=PAL[1], ms=6, label="original data")
    ax.plot([15], [60], "D", color=PAL[7], ms=9, label="one added point")
    ax.set_xlim(0.4, 16.0)
    ax.set_ylim(50, 140)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title("(c) A single high-leverage point")
    ax.legend(loc="upper left", fontsize=7.6)
    fig.tight_layout()
    fig.savefig(OUT + "g7_s3_pitfalls.png")
    plt.close(fig)
    print("wrote g7_s3_pitfalls.png")


fig_residual()
fig_normaleq()
fig_worked()
fig_pisa()
fig_flow()
fig_pitfalls()
print("done")
