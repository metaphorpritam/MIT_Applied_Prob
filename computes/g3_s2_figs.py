# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib", "scipy"]
# ///
"""Figures for note G3 section 2 (Joint, marginal and conditional PDFs).

Sources: L09 slides 3-8 (raster p01-p02), rec09 P1/P3/P4, B&T 3.4-3.5.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "notes" / "_build"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from mpl_style import setup, diagram_ax, PAL, INK, MUTED, GRID_C, AXIS_C  # noqa: E402

plt, _ = setup()
import numpy as np  # noqa: E402
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon, Rectangle, Arc  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection  # noqa: E402

IMG = ROOT / "notes" / "img"
IMG.mkdir(parents=True, exist_ok=True)
BLUE, ORANGE, GREEN, GOLD, PINK, DGREEN, PURPLE, RED = PAL

CMAP = LinearSegmentedColormap.from_list("g3s2", ["#f4f7fc", "#c3d9f2", "#7fb0e4", "#2a78d6", "#17406f"])


def save(fig, name):
    p = IMG / f"g3_s2_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


# ================================================== Fig 2.1  joint region
def fig_jointregion():
    fig, (axA, axB) = plt.subplots(1, 2, figsize=(10.4, 4.5),
                                   gridspec_kw={"width_ratios": [1.15, 1.0]})

    n = 400
    xs = np.linspace(0, 1, n)
    ys = np.linspace(0, 1, n)
    XX, YY = np.meshgrid(xs, ys)
    ZZ = XX + YY
    im = axA.pcolormesh(XX, YY, ZZ, cmap=CMAP, shading="auto", vmin=0, vmax=2)
    axA.contour(XX, YY, ZZ, levels=[0.25, 0.5, 0.75, 1.25, 1.5, 1.75],
                colors="#ffffff", linewidths=0.7, alpha=0.6)
    tri = Polygon([(0, 0), (1, 0), (0, 1)], closed=True, facecolor="none",
                  edgecolor=ORANGE, linewidth=2.4, hatch="///", zorder=4)
    axA.add_patch(tri)
    axA.plot([0, 1], [1, 0], color=ORANGE, linewidth=2.4, zorder=5)
    axA.annotate("$S=\\{x+y\\leq 1\\}$\n$\\mathbf{P}((X,Y)\\in S)=1/3$",
                 xy=(0.30, 0.30), xytext=(0.70, 0.78), ha="center",
                 fontsize=9.5, color=INK, zorder=8,
                 bbox=dict(boxstyle="round,pad=0.34", fc="white", ec=ORANGE, lw=1.4),
                 arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.6))
    axA.set_xlim(0, 1); axA.set_ylim(0, 1)
    axA.set_aspect("equal")
    axA.grid(False)
    axA.set_xlabel("$x$"); axA.set_ylabel("$y$")
    axA.set_title("Joint density $f_{X,Y}(x,y)=x+y$ on the unit square")
    cb = fig.colorbar(im, ax=axA, fraction=0.046, pad=0.03)
    cb.set_label("density (probability per unit area)", fontsize=8.5)
    cb.ax.tick_params(labelsize=8)

    # ---- panel B: the delta-square blow-up
    diagram_ax(axB)
    axB.set_xlim(0.40, 0.78)
    axB.set_ylim(0.40, 0.92)
    d = 0.05
    x0 = y0 = 0.5
    xs2 = np.linspace(0.40, 0.78, 200)
    ys2 = np.linspace(0.40, 0.70, 160)
    XX2, YY2 = np.meshgrid(xs2, ys2)
    axB.pcolormesh(xs2, ys2, XX2 + YY2, cmap=CMAP, shading="auto", vmin=0, vmax=2)
    axB.add_patch(Rectangle((x0, y0), d, d, facecolor=ORANGE, alpha=0.55,
                            edgecolor=ORANGE, linewidth=2.0, zorder=4))
    axB.annotate("", xy=(x0, y0 - 0.022), xytext=(x0 + d, y0 - 0.022),
                 arrowprops=dict(arrowstyle="<->", color=INK, lw=1.3))
    axB.text(x0 + d / 2, y0 - 0.043, "$\\delta$", ha="center", fontsize=11, color=INK)
    axB.annotate("", xy=(x0 - 0.022, y0), xytext=(x0 - 0.022, y0 + d),
                 arrowprops=dict(arrowstyle="<->", color=INK, lw=1.3))
    axB.text(x0 - 0.048, y0 + d / 2, "$\\delta$", va="center", fontsize=11, color=INK)
    axB.plot([x0], [y0], "o", color=INK, markersize=5, zorder=5)
    axB.text(0.59, 0.855,
             "$\\mathbf{P}(x\\leq X\\leq x+\\delta,\\,y\\leq Y\\leq y+\\delta)$\n"
             "$\\approx f_{X,Y}(x,y)\\,\\delta^{2}$",
             ha="center", va="center", fontsize=9.5, color=INK,
             bbox=dict(boxstyle="round,pad=0.34", fc="white", ec=GRID_C))
    axB.text(0.59, 0.755,
             "$x=y=0.5,\\ \\delta=0.05$:   exact $=0.002625$,\n"
             "approximation $=0.002500$   (ratio $1.05$)",
             ha="center", va="center", fontsize=9, color=MUTED,
             bbox=dict(boxstyle="round,pad=0.30", fc="#fbfaf6", ec=GRID_C))
    axB.text(x0 - 0.055, y0 - 0.012, "$(x,y)$", ha="center", va="top",
             fontsize=10, color=INK)
    axB.set_title("Blow-up: the $\\delta^2$ interpretation")
    fig.tight_layout()
    save(fig, "jointregion")


# ================================================== Fig 2.2  marginal projection
def fig_marginal():
    fig = plt.figure(figsize=(10.4, 4.3))
    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    ax2 = fig.add_subplot(1, 2, 2)

    n = 41
    xs = np.linspace(0, 1, n)
    ys = np.linspace(0, 1, n)
    XX, YY = np.meshgrid(xs, ys)
    ZZ = XX + YY
    ax1.plot_surface(XX, YY, ZZ, cmap=CMAP, alpha=0.40, linewidth=0.2,
                     edgecolor="#8fb4e0", rstride=2, cstride=2, antialiased=True)
    x0 = 0.30
    yy = np.linspace(0, 1, 60)
    zz = x0 + yy
    verts = [[(x0, 0.0, 0.0)] + [(x0, yv, zv) for yv, zv in zip(yy, zz)] + [(x0, 1.0, 0.0)]]
    slab = Poly3DCollection(verts, facecolor=ORANGE, alpha=0.92, edgecolor=RED,
                            linewidth=1.4, zorder=10)
    ax1.add_collection3d(slab)
    ax1.set_xlabel("$x$", labelpad=-2)
    ax1.set_ylabel("$y$", labelpad=-2)
    ax1.set_zlabel("$f_{X,Y}$", labelpad=-4)
    ax1.set_zlim(0, 2)
    ax1.tick_params(labelsize=7, pad=-1)
    ax1.view_init(elev=24, azim=-58)
    ax1.set_title("Slab at $x=0.30$: area $=\\int f_{X,Y}(0.30,y)\\,dy$", pad=-2)

    m = xs + 0.5
    ax2.plot(xs, m, color=BLUE, linewidth=2.2, label="$f_X(x)=x+\\frac{1}{2}$")
    ax2.fill_between(xs, 0, m, color=BLUE, alpha=0.14)
    ax2.plot([x0], [x0 + 0.5], "o", color=ORANGE, markersize=8, zorder=5)
    ax2.annotate("$f_X(0.30)=0.80$\n(= area of the orange slab)",
                 xy=(x0, x0 + 0.5), xytext=(0.42, 0.55),
                 fontsize=9.5, color=ORANGE,
                 arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.5))
    ax2.set_xlim(0, 1); ax2.set_ylim(0, 1.75)
    ax2.set_xlabel("$x$"); ax2.set_ylabel("density")
    ax2.set_title("Marginal $f_X$ = the slab areas, one per $x$")
    ax2.legend(loc="upper left")
    fig.tight_layout()
    save(fig, "marginal")


# ================================================== Fig 2.3  THE slice picture
def _bump(XX, YY):
    return 0.40 + 3.2 * np.exp(-((XX - 0.62) ** 2 + (YY - 0.55) ** 2) / (2 * 0.15 ** 2))


def fig_slice():
    n = 33
    g = np.linspace(0, 1, n)
    XX, YY = np.meshgrid(g, g, indexing="ij")
    Z = _bump(XX, YY)
    dx = g[1] - g[0]
    Z = Z / (Z.sum() * dx * dx)              # normalize to a genuine joint pdf
    fX = Z.sum(axis=1) * dx                   # marginal of X

    fig = plt.figure(figsize=(11.6, 4.2))
    axes = [fig.add_subplot(1, 3, k, projection="3d") for k in (1, 2, 3)]
    for ax in axes:
        ax.set_box_aspect((1, 1, 0.62))
        ax.view_init(elev=26, azim=-62)
        ax.set_xlabel("$x$", labelpad=-6, fontsize=9)
        ax.set_ylabel("$y$", labelpad=-6, fontsize=9)
        ax.tick_params(labelsize=6.5, pad=-3)
        ax.set_xticks([0, 0.5, 1]); ax.set_yticks([0, 0.5, 1])
        ax.grid(False)

    i0 = 14                                   # index of the highlighted x
    x0 = g[i0]

    # (a) joint surface + the cut line
    axes[0].plot_wireframe(XX, YY, Z, rstride=1, cstride=1,
                           color=DGREEN, linewidth=0.45, alpha=0.85)
    axes[0].plot(np.full(n, x0), g, Z[i0, :], color=RED, linewidth=2.4, zorder=10)
    axes[0].set_zlim(0, Z.max() * 1.05)
    axes[0].set_zticks([0, 1, 2])
    axes[0].set_title("(a) joint density $f_{X,Y}$\nwith the cut at $x=%.2f$" % x0,
                      fontsize=10, pad=-4)

    # (b) the single fin standing on the cut
    axes[1].plot_wireframe(XX, YY, Z, rstride=2, cstride=2,
                           color="#bcd7c9", linewidth=0.35, alpha=0.7)
    verts = [[(x0, 0.0, 0.0)] + [(x0, yv, zv) for yv, zv in zip(g, Z[i0, :])] + [(x0, 1.0, 0.0)]]
    axes[1].add_collection3d(Poly3DCollection(verts, facecolor=ORANGE, alpha=0.8,
                                              edgecolor=RED, linewidth=1.4))
    axes[1].set_zlim(0, Z.max() * 1.05)
    axes[1].set_zticks([0, 1, 2])
    axes[1].set_title("(b) one slice; its AREA is\n$f_X(%.2f)=%.3f$" % (x0, fX[i0]),
                      fontsize=10, pad=-4)

    # (c) family of renormalized fins = conditional densities
    axes[2].plot_wireframe(XX, YY, np.zeros_like(Z), rstride=4, cstride=4,
                           color=GRID_C, linewidth=0.5)
    for i in range(2, n - 1, 5):
        cond = Z[i, :] / fX[i]
        v = [[(g[i], 0.0, 0.0)] + [(g[i], yv, zv) for yv, zv in zip(g, cond)] + [(g[i], 1.0, 0.0)]]
        axes[2].add_collection3d(Poly3DCollection(
            v, facecolor=BLUE, alpha=0.42, edgecolor=BLUE, linewidth=1.0))
    axes[2].set_zlim(0, 3.2)
    axes[2].set_zticks([0, 1, 2, 3])
    axes[2].set_title("(c) each slice divided by its own area:\n"
                      "$f_{Y|X}(y\\,|\\,x)$, one pdf per $x$", fontsize=10, pad=-4)

    fig.subplots_adjust(left=0.01, right=0.99, top=0.88, bottom=0.02, wspace=0.06)
    save(fig, "slice")


# ================================================== Fig 2.4  Buffon
def fig_buffon():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.6, 4.3),
                                   gridspec_kw={"width_ratios": [1.0, 1.05]})
    # --- geometry
    diagram_ax(ax1)
    ax1.set_xlim(-0.15, 3.5)
    ax1.set_ylim(-0.55, 2.55)
    for yv in (0.0, 1.0, 2.0):
        ax1.plot([-0.05, 3.15], [yv, yv], color=MUTED, linewidth=1.6)
    ax1.annotate("", xy=(3.30, 0.0), xytext=(3.30, 1.0),
                 arrowprops=dict(arrowstyle="<->", color=INK, lw=1.4))
    ax1.text(3.40, 0.5, "$d$", va="center", fontsize=12, color=INK)

    # needle crossing the line y=1
    theta = np.deg2rad(35)
    mid = np.array([1.25, 0.78])
    L = 1.5
    e = np.array([np.cos(theta), np.sin(theta)])
    p1, p2 = mid - (L / 2) * e, mid + (L / 2) * e
    ax1.plot([p1[0], p2[0]], [p1[1], p2[1]], color=INK, linewidth=4.5,
             solid_capstyle="round", zorder=5)
    ax1.plot([mid[0]], [mid[1]], "o", color=ORANGE, markersize=7, zorder=6)
    # perpendicular distance x from midpoint up to the nearest line y=1
    ax1.plot([mid[0], mid[0]], [mid[1], 1.0], color=ORANGE, linewidth=2.0,
             linestyle="--", zorder=6)
    ax1.text(mid[0] - 0.09, (mid[1] + 1.0) / 2, "$x$", ha="right", va="center",
             fontsize=12, color=ORANGE)
    # angle at the crossing point with the line y=1
    t_cross = (1.0 - mid[1]) / e[1]
    cross = mid + t_cross * e
    ax1.add_patch(Arc(cross, 0.85, 0.85, theta1=0, theta2=np.rad2deg(theta),
                      color=BLUE, linewidth=1.8))
    ax1.text(cross[0] + 0.50, 1.06, r"$\theta$", fontsize=13, color=BLUE)
    ax1.text(p2[0] + 0.10, p2[1] + 0.16, r"needle, length $\ell$", fontsize=10,
             color=INK, ha="left")
    ax1.text(1.55, -0.34,
             r"crosses  $\Leftrightarrow$  $x \leq \frac{\ell}{2}\sin\theta$",
             fontsize=11, color=INK, ha="center",
             bbox=dict(boxstyle="round,pad=0.32", fc="#fbfaf6", ec=GRID_C))
    ax1.set_title("Buffon's needle: the two random quantities")

    # --- event region in the (theta, x) rectangle, l/d = 0.5, d = 1
    d_, l_ = 1.0, 0.5
    th = np.linspace(0, np.pi / 2, 400)
    curve = (l_ / 2) * np.sin(th)
    ax2.add_patch(Rectangle((0, 0), np.pi / 2, d_ / 2, facecolor=GRID_C,
                            alpha=0.45, edgecolor=AXIS_C, linewidth=1.2))
    ax2.fill_between(th, 0, curve, color=ORANGE, alpha=0.55, zorder=3)
    ax2.plot(th, curve, color=RED, linewidth=2.2, zorder=4,
             label=r"$x=\frac{\ell}{2}\sin\theta$")
    ax2.set_xlim(0, np.pi / 2 * 1.02)
    ax2.set_ylim(0, d_ / 2 * 1.18)
    ax2.set_xticks([0, np.pi / 8, np.pi / 4, 3 * np.pi / 8, np.pi / 2])
    ax2.set_xticklabels(["0", r"$\pi/8$", r"$\pi/4$", r"$3\pi/8$", r"$\pi/2$"])
    ax2.set_xlabel(r"$\theta$")
    ax2.set_ylabel("$x$")
    ax2.text(0.42, 0.075, "CROSS", fontsize=10.5, color="#8a3c12", fontweight="bold")
    ax2.text(0.42, 0.40, "NO CROSS", fontsize=10.5, color=MUTED, fontweight="bold")
    ax2.text(np.pi / 4, 0.545,
             "joint density $f_{X,\\Theta}=\\frac{4}{\\pi d}$ (constant)\n"
             "$\\mathbf{P}(\\mathrm{cross})=\\frac{4}{\\pi d}\\cdot\\frac{\\ell}{2}"
             "=\\frac{2\\ell}{\\pi d}=0.3183$",
             ha="center", va="center", fontsize=9.5, color=INK,
             bbox=dict(boxstyle="round,pad=0.34", fc="white", ec=GRID_C))
    ax2.legend(loc="upper left", fontsize=9)
    ax2.set_title(r"Sample space $[0,\pi/2]\times[0,d/2]$, drawn for $\ell/d=1/2$")
    fig.tight_layout()
    save(fig, "buffon")


# ================================================== Fig 2.5  stick breaking
def fig_stick():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.2))
    # support triangle 0 <= y <= x <= 1
    ax1.add_patch(Polygon([(0, 0), (1, 0), (1, 1)], closed=True,
                          facecolor=BLUE, alpha=0.16, edgecolor=BLUE, linewidth=2.0))
    ax1.plot([0, 1], [0, 1], color=BLUE, linewidth=2.0)
    # density label sits left of the orange slice line, below the green one, so that
    # it covers neither.
    ax1.text(0.50, 0.11, "$f_{X,Y}(x,y)=\\frac{1}{\\ell x}$", fontsize=12, color=BLUE,
             ha="center", zorder=8,
             bbox=dict(boxstyle="round,pad=0.22", fc="white", ec="none", alpha=0.85))
    xv = 0.72
    ax1.plot([xv, xv], [0, xv], color=ORANGE, linewidth=2.6, zorder=5)
    ax1.annotate("slice at $X=x$:\n$Y$ uniform on $[0,x]$", xy=(xv, xv * 0.76),
                 xytext=(0.18, 0.92), fontsize=9.5, color=ORANGE, ha="left",
                 arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.5))
    yv = 0.30
    ax1.plot([yv, 1], [yv, yv], color=DGREEN, linewidth=2.6, zorder=5)
    # anchor the green leader on the LEFT end of its slice (x = y): it then stays
    # clear of the orange slice line instead of cutting across it.
    ax1.annotate("slice at $Y=y$:\n$x$ runs from $y$ to $\\ell$", xy=(yv + 0.02, yv + 0.01),
                 xytext=(0.045, 0.52), fontsize=9.5, color=DGREEN, ha="left",
                 arrowprops=dict(arrowstyle="->", color=DGREEN, lw=1.5))
    ax1.set_xlim(0, 1.08); ax1.set_ylim(0, 1.08)
    ax1.set_aspect("equal")
    ax1.set_xticks([0, 0.5, 1]); ax1.set_xticklabels(["0", "$\\ell/2$", "$\\ell$"])
    ax1.set_yticks([0, 0.5, 1]); ax1.set_yticklabels(["0", "$\\ell/2$", "$\\ell$"])
    ax1.set_xlabel("$x$ (first break)"); ax1.set_ylabel("$y$ (second break)")
    ax1.set_title("Support $\\{0\\leq y\\leq x\\leq \\ell\\}$ (L09 slides 7–8)")

    yy = np.linspace(1e-4, 1, 600)
    fy = np.log(1 / yy)
    ax2.plot(yy, fy, color=BLUE, linewidth=2.2,
             label="$f_Y(y)=\\frac{1}{\\ell}\\log\\frac{\\ell}{y}$")
    ax2.fill_between(yy, 0, fy, color=BLUE, alpha=0.13)
    ax2.axvline(0.25, color=ORANGE, linewidth=2.0, linestyle="--")
    ax2.text(0.275, 3.05, "$\\mathbb{E}[Y]=\\ell/4$", color=ORANGE, fontsize=11,
             fontweight="bold")
    xx = np.linspace(0, 1, 200)
    ax2.plot(xx, xx / 2, color=DGREEN, linewidth=2.0, linestyle="-.",
             label="$\\mathbb{E}[Y\\,|\\,X=x]=x/2$")
    ax2.set_xlim(0, 1); ax2.set_ylim(0, 4.0)
    ax2.set_xlabel("$y$  (resp. $x$), in units of $\\ell$")
    ax2.set_ylabel("density  /  conditional mean")
    ax2.legend(loc="upper right", fontsize=9)
    ax2.set_title("Marginal of $Y$ and the conditional mean of $Y$")
    fig.tight_layout()
    save(fig, "stick")


# ================================================== Fig 2.6  rec09 P1
def fig_oddint():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 3.9))
    lam = 1.0
    xx = np.linspace(0, 8, 900)
    ax1.plot(xx, lam * np.exp(-lam * xx), color=BLUE, linewidth=2.2,
             label="$f_X(x)=\\lambda e^{-\\lambda x}$,  $\\lambda=1$")
    labels = ["0.2325", "0.0315", "0.0043"]
    for k, n in enumerate((1, 3, 5)):
        seg = np.linspace(n, n + 1, 120)
        ax1.fill_between(seg, 0, lam * np.exp(-lam * seg), color=ORANGE, alpha=0.62,
                         zorder=3)
        ax1.text(n + 0.5, lam * np.exp(-lam * n) + 0.045, labels[k],
                 ha="center", fontsize=8.5, color="#8a3c12")
    for n in (0, 2, 4, 6):
        seg = np.linspace(n, n + 1, 120)
        ax1.fill_between(seg, 0, lam * np.exp(-lam * seg), color=GRID_C, alpha=0.75,
                         zorder=2)
    ax1.set_xlim(0, 8); ax1.set_ylim(0, 1.15)
    ax1.set_xticks(range(9))
    ax1.set_xlabel("$x$"); ax1.set_ylabel("$f_X(x)$")
    ax1.text(3.6, 0.75, "orange strips: $n$ odd\ntotal $=1/(e^{\\lambda}+1)=0.2689$",
             fontsize=9.5, color=INK,
             bbox=dict(boxstyle="round,pad=0.32", fc="white", ec=GRID_C))
    ax1.legend(loc="upper right", fontsize=9)
    ax1.set_title("Odd-numbered unit intervals under the exponential pdf")

    lams = np.linspace(0.02, 5, 500)
    ax2.plot(lams, 1 / (np.exp(lams) + 1), color=BLUE, linewidth=2.3,
             label="$\\mathbf{P}(n\\ \\mathrm{odd})=1/(e^{\\lambda}+1)$")
    ax2.axhline(0.5, color=MUTED, linewidth=1.2, linestyle=":")
    ax2.text(2.6, 0.522, "$1/2$: the $\\lambda\\to 0$ limit", fontsize=9, color=MUTED)
    for lv, tag in ((0.5, "0.3775"), (1.0, "0.2689"), (2.0, "0.1192")):
        ax2.plot([lv], [1 / (np.exp(lv) + 1)], "o", color=ORANGE, markersize=7, zorder=5)
        ax2.annotate(f"$\\lambda={lv:g}$: {tag}", xy=(lv, 1 / (np.exp(lv) + 1)),
                     xytext=(lv + 0.35, 1 / (np.exp(lv) + 1) + 0.055), fontsize=8.5,
                     color="#8a3c12",
                     arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.1))
    ax2.set_xlim(0, 5); ax2.set_ylim(0, 0.62)
    ax2.set_xlabel("$\\lambda$"); ax2.set_ylabel("probability")
    ax2.legend(loc="upper right", fontsize=9)
    ax2.set_title("The answer as a function of $\\lambda$")
    fig.tight_layout()
    save(fig, "oddint")


# ================================================== Fig 2.7  rec09 P3 triangle
def fig_tri():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.2))
    ax1.add_patch(Polygon([(0, 0), (1, 0), (0, 1)], closed=True,
                          facecolor=BLUE, alpha=0.16, edgecolor=BLUE, linewidth=2.0))
    ax1.text(0.16, 0.10, "$f_{X,Y}=2$", fontsize=13, color=BLUE, ha="center")
    for yv, col in ((0.25, ORANGE), (0.6, DGREEN)):
        ax1.plot([0, 1 - yv], [yv, yv], color=col, linewidth=3.0, zorder=5)
        ax1.plot([(1 - yv) / 2], [yv], "o", color=col, markersize=8, zorder=6)
        ax1.annotate(f"$y={yv}$: $X\\,|\\,Y=y$ uniform on $[0,{1-yv:.2f}]$\n"
                     f"$\\mathbb{{E}}[X|Y={yv}]={(1-yv)/2:.3f}$ (dot)",
                     xy=(1 - yv, yv), xytext=(0.40, yv + 0.16), fontsize=8.5, color=col,
                     arrowprops=dict(arrowstyle="->", color=col, lw=1.3))
    ax1.set_xlim(0, 1.12); ax1.set_ylim(0, 1.12)
    ax1.set_aspect("equal")
    ax1.set_xlabel("$x$"); ax1.set_ylabel("$y$")
    ax1.set_title("Uniform on the triangle $(0,0),(0,1),(1,0)$ (rec09 P3)")

    yy = np.linspace(0, 1, 300)
    ax2.plot(yy, 2 * (1 - yy), color=BLUE, linewidth=2.3, label="$f_Y(y)=2(1-y)$")
    ax2.fill_between(yy, 0, 2 * (1 - yy), color=BLUE, alpha=0.12)
    ax2.plot(yy, (1 - yy) / 2, color=ORANGE, linewidth=2.3, linestyle="--",
             label="$\\mathbb{E}[X\\,|\\,Y=y]=(1-y)/2$")
    ax2.axhline(1 / 3, color=DGREEN, linewidth=1.6, linestyle=":")
    # keep the label clear of the dotted 1/3 line: the line used to run through the
    # bottom of the glyphs and read as a strikethrough.
    ax2.text(0.36, 0.44, "$\\mathbb{E}[X]=\\mathbb{E}[Y]=1/3$", color=DGREEN,
             fontsize=10, fontweight="bold", ha="left", va="bottom",
             bbox=dict(boxstyle="round,pad=0.20", fc="white", ec="none", alpha=0.85))
    ax2.set_xlim(0, 1); ax2.set_ylim(0, 2.2)
    ax2.set_xlabel("$y$"); ax2.set_ylabel("density  /  conditional mean")
    ax2.legend(loc="upper right", fontsize=9)
    ax2.set_title("Marginal of $Y$, and the conditional mean of $X$")
    fig.tight_layout()
    save(fig, "tri")


# ================================================== Fig 2.8  broken stick
def fig_broken():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.4),
                                   gridspec_kw={"width_ratios": [1.0, 1.0]})
    # left: the stick and its three pieces
    diagram_ax(ax1)
    ax1.set_xlim(-0.08, 1.12)
    ax1.set_ylim(-0.62, 0.62)
    u, v = 0.28, 0.66
    ax1.add_patch(Rectangle((0, -0.05), u, 0.10, facecolor=BLUE, alpha=0.75,
                            edgecolor=INK, linewidth=1.0))
    ax1.add_patch(Rectangle((u, -0.05), v - u, 0.10, facecolor=ORANGE, alpha=0.8,
                            edgecolor=INK, linewidth=1.0))
    ax1.add_patch(Rectangle((v, -0.05), 1 - v, 0.10, facecolor=DGREEN, alpha=0.75,
                            edgecolor=INK, linewidth=1.0))
    for pos, lab in ((u, "$x$"), (v, "$y$")):
        ax1.plot([pos, pos], [-0.14, 0.14], color=INK, linewidth=1.6)
        ax1.text(pos, 0.19, lab, ha="center", fontsize=11, color=INK)
    ax1.text(u / 2, -0.22, "$x$", ha="center", fontsize=10, color=BLUE)
    ax1.text((u + v) / 2, -0.22, "$y-x$", ha="center", fontsize=10, color="#8a3c12")
    ax1.text((v + 1) / 2, -0.22, "$1-y$", ha="center", fontsize=10, color=DGREEN)
    ax1.text(0.5, 0.40, "unit stick broken at two uniform points\n"
                        "($x &lt; y$ shown)".replace("&lt;", "<"),
             ha="center", fontsize=10, color=INK)
    ax1.text(0.5, -0.45,
             "triangle possible  $\\Leftrightarrow$  every piece $&lt;\\ 1/2$".replace("&lt;", "<"),
             ha="center", fontsize=11, color=INK,
             bbox=dict(boxstyle="round,pad=0.32", fc="#fbfaf6", ec=GRID_C))

    # right: the unit square with the two favourable triangles
    ax2.add_patch(Rectangle((0, 0), 1, 1, facecolor=GRID_C, alpha=0.40,
                            edgecolor=AXIS_C, linewidth=1.2))
    ax2.add_patch(Polygon([(0, 0.5), (0.5, 0.5), (0.5, 1.0)], closed=True,
                          facecolor=ORANGE, alpha=0.62, edgecolor=RED, linewidth=1.8))
    ax2.add_patch(Polygon([(0.5, 0), (0.5, 0.5), (1.0, 0.5)], closed=True,
                          facecolor=ORANGE, alpha=0.62, edgecolor=RED, linewidth=1.8))
    ax2.plot([0, 1], [0, 1], color=MUTED, linewidth=1.2, linestyle="--")
    ax2.text(0.83, 0.90, "$y &gt; x$".replace("&gt;", ">"), fontsize=9.5, color=MUTED)
    ax2.text(0.87, 0.10, "$y &lt; x$".replace("&lt;", "<"), fontsize=9.5, color=MUTED)
    ax2.text(0.235, 0.68, "area\n$1/8$", ha="center", va="center", fontsize=10,
             color="#8a3c12", fontweight="bold")
    ax2.text(0.68, 0.235, "area\n$1/8$", ha="center", va="center", fontsize=10,
             color="#8a3c12", fontweight="bold")
    ax2.annotate("$x&lt;1/2,\\ y&gt;1/2,\\ y&lt;x+1/2$".replace("&lt;", "<").replace("&gt;", ">"),
                 xy=(0.10, 0.545), xytext=(0.02, 1.12), fontsize=9, color=RED,
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.3))
    ax2.set_xlim(-0.02, 1.02); ax2.set_ylim(-0.02, 1.24)
    ax2.set_aspect("equal")
    ax2.set_xticks([0, 0.5, 1]); ax2.set_yticks([0, 0.5, 1])
    ax2.set_xlabel("$x$ = first break point"); ax2.set_ylabel("$y$ = second break point")
    ax2.set_title("Favourable region: total area $=1/8+1/8=1/4$")
    ax1.set_title("The three pieces")
    fig.tight_layout()
    save(fig, "broken")


# ================================================== Fig 2.9  decision flowchart
def fig_flow():
    fig, ax = plt.subplots(figsize=(9.6, 6.6))
    diagram_ax(ax)
    ax.set_aspect("auto")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    def box(x, y, w, h, txt, fc, ec, fs=9.2, tc=INK):
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                    boxstyle="round,pad=0.9,rounding_size=2.2",
                                    linewidth=1.5, facecolor=fc, edgecolor=ec,
                                    zorder=2))
        ax.text(x, y, txt, ha="center", va="center", fontsize=fs, color=tc, zorder=3)

    def arrow(x1, y1, x2, y2, label="", lx=0, ly=0):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                                     arrowstyle="-|>", mutation_scale=14,
                                     linewidth=1.4, color=MUTED, zorder=1,
                                     shrinkA=2, shrinkB=3))
        if label:
            ax.text((x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly, label, fontsize=8.6,
                    color=MUTED, ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none"))

    box(50, 94, 62, 9, "You are given a model for two continuous r.v.'s.\n"
                       "What do you actually have?", "#eef3fb", BLUE, 9.6)

    box(17, 76, 30, 11, "a REGION $S$ and the words\n\"uniform on $S$\"",
        "#fdf3ec", ORANGE)
    box(50, 76, 28, 11, "a formula for\n$f_{X,Y}(x,y)$", "#eef3fb", BLUE)
    box(84, 76, 30, 11, "$f_X$ and a rule for\n$Y$ given $X=x$", "#edf7f2", DGREEN)

    arrow(35, 89.5, 20, 82)
    arrow(50, 89.5, 50, 82)
    arrow(65, 89.5, 81, 82)

    box(17, 60, 30, 10, "$f_{X,Y}=\\frac{1}{\\mathrm{area}(S)}$ on $S$,\n0 outside",
        "white", ORANGE)
    box(84, 60, 30, 10, "multiplication rule:\n$f_{X,Y}=f_X(x)\\,f_{Y|X}(y|x)$",
        "white", DGREEN)
    arrow(17, 70.5, 17, 65.2)
    arrow(84, 70.5, 84, 65.2)
    arrow(32.5, 60, 44, 68)
    arrow(68.5, 60, 57, 68)

    box(50, 46, 44, 10, "Now you have the joint PDF.  Two moves, and only two:",
        "#f6f4ee", AXIS_C, 9.6)
    arrow(50, 70.5, 50, 51.2)

    box(24, 30, 36, 13, "MARGINAL — integrate the other\nvariable OUT over the support:\n"
                        "$f_Y(y)=\\int f_{X,Y}(x,y)\\,dx$", "#eef3fb", BLUE)
    box(76, 30, 36, 13, "CONDITIONAL — fix $y$, slice,\nand renormalize:\n"
                        "$f_{X|Y}(x|y)=f_{X,Y}(x,y)/f_Y(y)$", "#fdf3ec", ORANGE)
    arrow(40, 41.2, 28, 37)
    arrow(60, 41.2, 72, 37)
    arrow(42.5, 30, 57.5, 30, "need $f_Y$ first", 0, 3.2)

    box(24, 12, 36, 11, "$\\mathbb{E}[g(X,Y)]=\\int\\int g\\,f_{X,Y}$;\n"
                        "check independence: $f_{X,Y}\\!=\\!f_Xf_Y$?", "white", BLUE)
    box(76, 12, 36, 11, "$\\mathbb{E}[X|Y=y]=\\int x f_{X|Y}(x|y)dx$;\n"
                        "then $\\mathbb{E}[X]=\\int \\mathbb{E}[X|Y=y]f_Y(y)dy$",
        "white", ORANGE)
    arrow(24, 23.2, 24, 17.8)
    arrow(76, 23.2, 76, 17.8)

    fig.tight_layout()
    save(fig, "flow")


if __name__ == "__main__":
    fig_jointregion()
    fig_marginal()
    fig_slice()
    fig_buffon()
    fig_stick()
    fig_oddint()
    fig_tri()
    fig_broken()
    fig_flow()
    print("all figures done")
