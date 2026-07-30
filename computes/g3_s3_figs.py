# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""Figures for G3 §3 — The four faces of Bayes' rule."""
import io
import sys
from pathlib import Path

import numpy as np
from scipy import stats, special

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "notes" / "_build"))
from mpl_style import setup, PAL, INK, MUTED, GRID_C  # noqa: E402

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
plt, _ = setup()
IMG = Path(__file__).resolve().parents[1] / "notes" / "img"
IMG.mkdir(parents=True, exist_ok=True)


def save(fig, name):
    p = IMG / f"g3_s3_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


# ===================================================================== #
# Fig 3.1 — the 2x2 Bayes map
# ===================================================================== #
def fig_bayesmap():
    fig, ax = plt.subplots(figsize=(10.6, 6.15))
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0, 6.15)
    ax.axis("off")
    ax.grid(False)

    cells = [
        # (col, row, header, formula, denominator, example, color)
        (0, 1, "unknown DISCRETE  |  evidence DISCRETE",
         r"$p_{X|Y}(x\,|\,y)=\dfrac{p_X(x)\,p_{Y|X}(y\,|\,x)}{p_Y(y)}$",
         r"$p_Y(y)=\sum_{x} p_X(x)\,p_{Y|X}(y\,|\,x)$",
         "G1 §2.4 radar:  plane / blip", 0),
        (1, 1, "unknown DISCRETE  |  evidence CONTINUOUS",
         r"$p_{X|Y}(x\,|\,y)=\dfrac{p_X(x)\,f_{Y|X}(y\,|\,x)}{f_Y(y)}$",
         r"$f_Y(y)=\sum_{x} p_X(x)\,f_{Y|X}(y\,|\,x)$",
         "rec11 P1:  $X=\\pm1$ + Laplacian noise", 1),
        (0, 0, "unknown CONTINUOUS  |  evidence DISCRETE",
         r"$f_{X|Y}(x\,|\,y)=\dfrac{f_X(x)\,p_{Y|X}(y\,|\,x)}{p_Y(y)}$",
         r"$p_Y(y)=\int f_X(x)\,p_{Y|X}(y\,|\,x)\,dx$",
         "rec11 P2:  coin bias $\\to$ Beta;  photon count", 2),
        (1, 0, "unknown CONTINUOUS  |  evidence CONTINUOUS",
         r"$f_{X|Y}(x\,|\,y)=\dfrac{f_X(x)\,f_{Y|X}(y\,|\,x)}{f_Y(y)}$",
         r"$f_Y(y)=\int f_X(x)\,f_{Y|X}(y\,|\,x)\,dx$",
         "B&T Ex. 3.19:  bulb lifetime $\\to$ rate $\\lambda$", 3),
    ]
    x0, y0, w, h, gx, gy = 1.15, 0.88, 4.45, 2.20, 0.30, 0.26
    for (c, r, head, form, den, ex, ci) in cells:
        xx = x0 + c * (w + gx)
        yy = y0 + r * (h + gy)
        ax.add_patch(plt.Rectangle((xx, yy), w, h, facecolor="white",
                                   edgecolor=PAL[ci], linewidth=1.8, zorder=2))
        ax.add_patch(plt.Rectangle((xx, yy + h - 0.40), w, 0.40, facecolor=PAL[ci],
                                   edgecolor=PAL[ci], linewidth=1.8, alpha=0.16, zorder=2))
        ax.text(xx + w / 2, yy + h - 0.20, head, ha="center", va="center",
                fontsize=8.6, color=PAL[ci], weight="bold", zorder=3)
        ax.text(xx + w / 2, yy + h - 0.86, form, ha="center", va="center",
                fontsize=13, color=INK, zorder=3)
        ax.text(xx + w / 2, yy + 0.72, den, ha="center", va="center",
                fontsize=11, color=MUTED, zorder=3)
        ax.text(xx + w / 2, yy + 0.25, ex, ha="center", va="center",
                fontsize=8.8, color=INK, style="italic", zorder=3)

    # axis labels for the grid
    ax.text(x0 + w / 2, y0 + 2 * h + gy + 0.16, "evidence $Y$ is DISCRETE",
            ha="center", va="bottom", fontsize=10.5, weight="bold", color=INK)
    ax.text(x0 + w + gx + w / 2, y0 + 2 * h + gy + 0.16, "evidence $Y$ is CONTINUOUS",
            ha="center", va="bottom", fontsize=10.5, weight="bold", color=INK)
    ax.text(x0 - 0.42, y0 + h + gy + h / 2, "unknown $X$ is DISCRETE\n(PMF prior $p_X$)",
            ha="center", va="center", fontsize=10.5, weight="bold", color=INK, rotation=90)
    ax.text(x0 - 0.42, y0 + h / 2, "unknown $X$ is CONTINUOUS\n(PDF prior $f_X$)",
            ha="center", va="center", fontsize=10.5, weight="bold", color=INK, rotation=90)

    ax.text(5.3, 0.34,
            "ONE rule:   posterior  $\\propto$  prior $\\times$ likelihood;   "
            "the denominator is whatever makes it integrate/sum to 1.\n"
            "Sum where the variable is discrete, integrate where it is continuous; "
            "use $p$ for PMFs and $f$ for PDFs.",
            ha="center", va="center", fontsize=9.4, color=INK,
            bbox=dict(boxstyle="round,pad=0.45", facecolor="#f6f5ef", edgecolor=GRID_C))
    ax.set_title("The four faces of Bayes' rule  (L10 slides 2–3)", fontsize=12, pad=10)
    save(fig, "bayesmap")


# ===================================================================== #
# Fig — (C|C) light bulb
# ===================================================================== #
def denom(y):
    return (2.0 / y ** 2) * ((y + 1) * np.exp(-y) - (1.5 * y + 1) * np.exp(-1.5 * y))


def fig_lightbulb():
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 3.9))
    lam = np.linspace(1.0, 1.5, 400)

    ax = axes[0]
    ax.plot(lam, np.full_like(lam, 2.0), color=MUTED, lw=2.2, ls="--",
            label="prior $f_\\Lambda(\\lambda)=2$")
    for i, y in enumerate((0.5, 2.0, 5.0)):
        ax.plot(lam, 2 * lam * np.exp(-lam * y) / denom(y), color=PAL[i], lw=2.2,
                label=f"posterior, observed $y={y}$")
    ax.set_xlim(0.98, 1.52)
    ax.set_ylim(0, 5.2)
    ax.set_xlabel("$\\lambda$  (failure rate of the bulb)")
    ax.set_ylabel("density")
    ax.set_title("(a) $f_{\\Lambda|Y}(\\lambda\\,|\\,y)$ on $[1,\\,3/2]$")
    ax.legend(loc="upper center", fontsize=8.2)

    ax = axes[1]
    ys = np.linspace(0.05, 12, 300)
    means = [np.trapezoid(lam * 2 * lam * np.exp(-lam * y) / denom(y), lam) for y in ys]
    ax.plot(ys, means, color=PAL[4], lw=2.4)
    ax.axhline(1.25, color=MUTED, ls="--", lw=1.4)
    ax.text(11.6, 1.258, "prior mean $1.25$", ha="right", va="bottom", fontsize=9, color=MUTED)
    for y, c, off in zip((0.5, 2.0, 5.0), PAL[:3], ((8, 10), (10, -34), (10, 10))):
        m = np.trapezoid(lam * 2 * lam * np.exp(-lam * y) / denom(y), lam)
        ax.plot([y], [m], "o", color=c, ms=7, zorder=5)
        ax.annotate(f"$y={y}$\n{m:.4f}", (y, m), textcoords="offset points",
                    xytext=off, fontsize=8.4, color=c)
    ax.set_xlim(0, 12)
    ax.set_ylim(1.0, 1.32)
    ax.set_xlabel("observed lifetime $y$")
    ax.set_ylabel("$\\mathbb{E}[\\Lambda\\,|\\,Y=y]$")
    ax.set_title("(b) posterior mean falls as the bulb lasts longer")
    fig.tight_layout()
    save(fig, "lightbulb")


# ===================================================================== #
# Fig — (D|C) Laplacian conditional densities + decision threshold
# ===================================================================== #
def fig_laplace():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.9))
    z = np.linspace(-5, 5, 1200)

    def lap(u, lam):
        return 0.5 * lam * np.exp(-lam * np.abs(u))

    ax = axes[0]
    lam, p = 1.0, 0.5
    ax.plot(z, lap(z + 1, lam), color=PAL[1], lw=2.2, label="$f_{Z|X}(z\\,|\\,-1)$")
    ax.plot(z, lap(z - 1, lam), color=PAL[0], lw=2.2, label="$f_{Z|X}(z\\,|\\,+1)$")
    zs = 0.0
    ax.axvline(zs, color=INK, lw=1.4, ls=":")
    ax.fill_between(z[z <= zs], 0, lap(z[z <= zs] - 1, lam), color=PAL[0], alpha=0.30)
    ax.fill_between(z[z >= zs], 0, lap(z[z >= zs] + 1, lam), color=PAL[1], alpha=0.30)
    ax.set_xlim(-5, 5)
    ax.set_ylim(0, 0.74)
    ax.set_xlabel("$z$  (observed $Z=X+Y$)")
    ax.set_ylabel("density")
    ax.set_title("(a) $p=1/2$, $\\lambda=1$:  threshold $z^*=0$")
    ax.annotate("$z^*=0$", (0, 0.545), ha="center", va="bottom", fontsize=9.5, color=INK)
    ax.annotate("miss  ($X=+1$ judged $-1$)", (-1.9, 0.055), textcoords="offset points",
                xytext=(0, 30), fontsize=8.3, color=PAL[0], ha="center",
                bbox=dict(boxstyle="round,pad=0.22", facecolor="white",
                          edgecolor=GRID_C, linewidth=0.7),
                arrowprops=dict(arrowstyle="->", color=PAL[0], lw=1.0), zorder=6)
    ax.annotate("false alarm", (1.9, 0.055), textcoords="offset points",
                xytext=(6, 34), fontsize=8.3, color=PAL[1], ha="center",
                bbox=dict(boxstyle="round,pad=0.22", facecolor="white",
                          edgecolor=GRID_C, linewidth=0.7),
                arrowprops=dict(arrowstyle="->", color=PAL[1], lw=1.0), zorder=6)
    ax.text(-4.9, 0.725, "$\\mathbf{P}(\\mathrm{error})=e^{-\\lambda}\\sqrt{p(1-p)}=0.183940$",
            fontsize=9.2, color=INK, ha="left", va="top",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=GRID_C))
    ax.legend(loc="upper right", fontsize=8.6)

    ax = axes[1]
    lam, p = 2.0, 0.3
    ax.plot(z, 0.7 * lap(z + 1, lam), color=PAL[1], lw=2.2,
            label="$(1-p)\\,f_{Z|X}(z\\,|\\,-1)$")
    ax.plot(z, 0.3 * lap(z - 1, lam), color=PAL[0], lw=2.2,
            label="$p\\,f_{Z|X}(z\\,|\\,+1)$")
    zs = np.log(0.7 / 0.3) / (2 * lam)
    ax.axvline(zs, color=INK, lw=1.4, ls=":")
    ax.fill_between(z[z <= zs], 0, 0.3 * lap(z[z <= zs] - 1, lam), color=PAL[0], alpha=0.30)
    ax.fill_between(z[z >= zs], 0, 0.7 * lap(z[z >= zs] + 1, lam), color=PAL[1], alpha=0.30)
    ax.set_xlim(-3.2, 3.2)
    ax.set_ylim(0, 0.95)
    ax.set_xlabel("$z$  (observed $Z=X+Y$)")
    ax.set_ylabel("weighted density")
    ax.set_title("(b) $p=0.3$, $\\lambda=2$:  threshold shifts right")
    ax.annotate(f"$z^*={zs:.6f}$", (zs, 0.30), ha="left", va="center",
                fontsize=9, color=INK, xytext=(zs + 0.42, 0.45),
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.0))
    ax.text(-3.05, 0.93, "$\\mathbf{P}(\\mathrm{error})=e^{-2}\\sqrt{0.3\\cdot0.7}=0.062018$",
            fontsize=9.2, color=INK, ha="left", va="top",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=GRID_C))
    ax.legend(loc="upper right", fontsize=8.4)
    fig.tight_layout()
    save(fig, "laplace")


# ===================================================================== #
# Fig — posterior vs observation, Laplacian vs Gaussian
# ===================================================================== #
def fig_posterior():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.9))
    z = np.linspace(-4, 4, 1600)
    d = np.abs(z + 1) - np.abs(z - 1)

    ax = axes[0]
    for i, lam in enumerate((0.3, 1.0, 3.0)):
        ax.plot(z, 0.5 / (0.5 + 0.5 * np.exp(-lam * d)), color=PAL[i], lw=2.2,
                label=f"$\\lambda={lam}$")
    ax.axhline(0.5, color=MUTED, ls="--", lw=1.2)
    ax.axvline(-1, color=GRID_C, lw=1.6)
    ax.axvline(1, color=GRID_C, lw=1.6)
    ax.set_xlim(-4, 4)
    ax.set_ylim(-0.03, 1.03)
    ax.set_xlabel("$z$")
    ax.set_ylabel("$\\mathbf{P}(X=1\\,|\\,Z=z)$")
    ax.set_title("(a) Laplacian noise, $p=1/2$: flat outside $[-1,1]$")
    ax.text(2.6, 0.30, "plateau:\nno further\nevidence", fontsize=8.5, color=MUTED, ha="center")
    ax.legend(loc="lower right", fontsize=8.6)

    ax = axes[1]
    ax.plot(z, 0.5 / (0.5 + 0.5 * np.exp(-1.0 * d)), color=PAL[0], lw=2.4,
            label="Laplacian, $\\lambda=1$")
    ax.plot(z, np.exp(z) / (np.exp(z) + np.exp(-z)), color=PAL[3], lw=2.4, ls="--",
            label="normal noise, $\\sigma=1$ (B&T Ex. 3.20)")
    ax.axhline(0.5, color=MUTED, ls="--", lw=1.2)
    ax.set_xlim(-4, 4)
    ax.set_ylim(-0.03, 1.03)
    ax.set_xlabel("$z$")
    ax.set_ylabel("$\\mathbf{P}(X=1\\,|\\,Z=z)$")
    ax.set_title("(b) heavy tails saturate, light tails do not")
    ax.text(2.3, 0.850, "Laplacian plateau $0.880797$", fontsize=8.6, color=PAL[0],
            ha="center", va="top")
    ax.text(2.9, 0.968, "normal: $\\to 1$", fontsize=8.8, color=PAL[3],
            ha="center", va="top")
    ax.legend(loc="lower right", fontsize=8.4)
    fig.tight_layout()
    save(fig, "posterior")


# ===================================================================== #
# Fig — Beta prior -> posterior
# ===================================================================== #
def fig_beta():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.9))
    q = np.linspace(0, 1, 600)

    ax = axes[0]
    ax.plot(q, 6 * q * (1 - q), color=MUTED, lw=2.4, ls="--",
            label="prior $6q(1-q)$ = Beta(2,2)")
    ax.plot(q, 12 * q ** 2 * (1 - q), color=PAL[0], lw=2.4,
            label="$f_{Q|X}(q|1)=12q^2(1-q)$ = Beta(3,2)")
    ax.plot(q, 12 * q * (1 - q) ** 2, color=PAL[1], lw=2.4,
            label="$f_{Q|X}(q|0)=12q(1-q)^2$ = Beta(2,3)")
    for m, c in ((0.5, MUTED), (0.6, PAL[0]), (0.4, PAL[1])):
        ax.plot([m], [0], "^", color=c, ms=8, clip_on=False, zorder=6)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 2.70)
    ax.set_xlabel("$q$  (success probability)")
    ax.set_ylabel("density")
    ax.set_title("(a) rec11 P2: one toss moves the mean by $\\pm0.1$")
    ax.text(0.5, 0.09, "triangles = posterior means $0.4$, $0.5$, $0.6$",
            fontsize=8.2, color=MUTED, ha="center")
    ax.legend(loc="upper center", fontsize=8.0)

    ax = axes[1]
    ax.plot(q, stats.beta(2, 2).pdf(q), color=MUTED, lw=2.2, ls="--", label="prior Beta(2,2)")
    for i, (n, k) in enumerate(((4, 3), (10, 7), (40, 28))):
        a, b = 2 + k, 2 + n - k
        ax.plot(q, stats.beta(a, b).pdf(q), color=PAL[i], lw=2.2,
                label=f"$n={n},k={k}$ $\\to$ Beta({a},{b})")
    ax.axvline(0.7, color=INK, lw=1.3, ls=":")
    ax.text(0.70, 6.55, "sample frequency $k/n=0.7$", fontsize=8.4, color=INK,
            va="bottom", ha="center",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                      edgecolor=GRID_C, linewidth=0.7))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 7.3)
    ax.set_xlabel("$q$")
    ax.set_ylabel("density")
    ax.set_title("(b) more data $\\Rightarrow$ narrower, and mean $\\to k/n$")
    ax.legend(loc="upper left", fontsize=8.0)
    fig.tight_layout()
    save(fig, "beta")


# ===================================================================== #
# Fig — light beam / photon count (C|D, L10 slide 3 example)
# ===================================================================== #
def fig_photon():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.9))

    ax = axes[0]
    x = np.linspace(0, 9, 700)
    ax.plot(x, np.exp(-x), color=MUTED, lw=2.4, ls="--", label="prior $f_X(x)=e^{-x}$")
    for i, y in enumerate((0, 1, 3, 8)):
        pdf = 2 ** (y + 1) * x ** y * np.exp(-2 * x) / special.factorial(y)
        ax.plot(x, pdf, color=PAL[i], lw=2.2, label=f"$y={y}$ photons")
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 2.1)
    ax.set_xlabel("$x$  (beam intensity)")
    ax.set_ylabel("density")
    ax.set_title("(a) posterior $f_{X|Y}(x|y)=\\dfrac{2^{y+1}x^{y}e^{-2x}}{y!}$")
    ax.legend(loc="upper right", fontsize=8.2)

    ax = axes[1]
    ks = np.arange(0, 11)
    pm = 2.0 ** (-(ks + 1))
    ml, sl, bl = ax.stem(ks, pm, linefmt="-", markerfmt="o", basefmt=" ")
    plt.setp(sl, color=PAL[2], linewidth=1.8)
    plt.setp(ml, color=PAL[2], markersize=7)
    ax.set_xlim(-0.6, 10.6)
    ax.set_ylim(0, 0.57)
    ax.set_xticks(ks)
    ax.set_xlabel("$y$  (photon count)")
    ax.set_ylabel("$p_Y(y)$")
    ax.set_title("(b) the marginal count is geometric: $p_Y(y)=(1/2)^{y+1}$")
    ax.text(6.2, 0.42, "denominator of Bayes' rule,\nand it sums to 1",
            fontsize=9, color=MUTED, ha="center",
            bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=GRID_C))
    fig.tight_layout()
    save(fig, "photon")


fig_bayesmap()
fig_lightbulb()
fig_laplace()
fig_posterior()
fig_beta()
fig_photon()
print("done")
