/* plot.js — tiny canvas plotting library for the 6.041 notes.
   Palette + mark rules follow the dataviz method: fixed categorical order,
   thin marks, recessive grid, stem plots for PMFs, one axis, hover tooltip. */
(function (global) {
  "use strict";
  const PAL = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"];
  const INK = "#0b0b0b", MUTED = "#898781", GRID = "#e1e0d9", AXIS = "#c3c2b7";
  const FONT = "12px system-ui, 'Segoe UI', sans-serif";
  const FONT_SM = "11px system-ui, 'Segoe UI', sans-serif";

  function niceTicks(lo, hi, n) {
    if (!(hi > lo)) hi = lo + 1;
    const span = hi - lo, step0 = span / Math.max(2, n);
    const mag = Math.pow(10, Math.floor(Math.log10(step0)));
    let step = mag;
    for (const m of [1, 2, 2.5, 5, 10]) { if (step0 <= m * mag) { step = m * mag; break; } }
    const t0 = Math.ceil(lo / step) * step, out = [];
    for (let t = t0; t <= hi + 1e-9; t += step) out.push(Math.abs(t) < 1e-12 ? 0 : t);
    return out;
  }
  function fmt(v) {
    if (v === 0) return "0";
    const a = Math.abs(v);
    if (a >= 1000) return v.toLocaleString("en-US", { maximumFractionDigits: 0 });
    if (a >= 100) return v.toFixed(0);
    if (a >= 1) return +v.toFixed(2) + "";
    if (a >= 0.01) return +v.toFixed(3) + "";
    return v.toExponential(1);
  }

  class Plot {
    constructor(canvas, opts) {
      this.cv = typeof canvas === "string" ? document.querySelector(canvas) : canvas;
      this.o = Object.assign({ xlim: [0, 1], ylim: [0, 1], xlabel: "", ylabel: "",
        title: "", pad: { l: 52, r: 14, t: 22, b: 40 }, grid: true, height: 300 }, opts || {});
      this.series = [];   // for tooltip: {label,color,pts:[[x,y]..], kind}
      this._legend = null;
      this._hover = null;
      this._raf = null;
      const dpr = window.devicePixelRatio || 1;
      const wCSS = this.cv.clientWidth || this.cv.parentElement.clientWidth || 640;
      this.w = wCSS; this.h = this.o.height;
      this.cv.style.height = this.h + "px";
      this.cv.width = Math.round(wCSS * dpr); this.cv.height = Math.round(this.h * dpr);
      this.g = this.cv.getContext("2d");
      this.g.scale(dpr, dpr);
      this._ci = 0;
      this._bindHover();
    }
    color(c) { return c === undefined ? PAL[this._ci++ % PAL.length] : (typeof c === "number" ? PAL[c % PAL.length] : c); }
    X(x) { const [a, b] = this.o.xlim, { l, r } = this.o.pad; return l + (x - a) / (b - a) * (this.w - l - r); }
    Y(y) { const [a, b] = this.o.ylim, { t, b: bo } = this.o.pad; return this.h - bo - (y - a) / (b - a) * (this.h - t - bo); }

    frame() {
      const g = this.g, o = this.o, { l, r, t, b } = o.pad;
      g.clearRect(0, 0, this.w, this.h);
      const xt = o.xticks || niceTicks(o.xlim[0], o.xlim[1], 7);
      const yt = o.yticks || niceTicks(o.ylim[0], o.ylim[1], 5);
      if (o.grid) {
        g.strokeStyle = GRID; g.lineWidth = 1; g.beginPath();
        for (const v of yt) { const y = this.Y(v); g.moveTo(l, y); g.lineTo(this.w - r, y); }
        g.stroke();
      }
      g.strokeStyle = AXIS; g.lineWidth = 1.2; g.beginPath();
      g.moveTo(l, t); g.lineTo(l, this.h - b); g.lineTo(this.w - r, this.h - b); g.stroke();
      g.fillStyle = MUTED; g.font = FONT_SM; g.textAlign = "center"; g.textBaseline = "top";
      for (const v of xt) { const x = this.X(v); if (x >= l - 1 && x <= this.w - r + 1) { g.fillText(fmt(v), x, this.h - b + 5); } }
      g.textAlign = "right"; g.textBaseline = "middle";
      for (const v of yt) g.fillText(fmt(v), l - 6, this.Y(v));
      g.font = FONT; g.fillStyle = INK; g.textAlign = "center"; g.textBaseline = "bottom";
      if (o.xlabel) g.fillText(o.xlabel, l + (this.w - l - r) / 2, this.h - 4);
      if (o.ylabel) { g.save(); g.translate(12, t + (this.h - t - b) / 2); g.rotate(-Math.PI / 2); g.textBaseline = "top"; g.fillText(o.ylabel, 0, 0); g.restore(); }
      if (o.title) { g.textBaseline = "top"; g.fillStyle = INK; g.font = "600 " + FONT; g.fillText(o.title, l + (this.w - l - r) / 2, 2); }
      return this;
    }
    _clip() { const { l, r, t, b } = this.o.pad; this.g.save(); this.g.beginPath(); this.g.rect(l, t, this.w - l - r, this.h - t - b); this.g.clip(); }

    line(xs, ys, o) {
      o = o || {}; const c = this.color(o.color); const g = this.g;
      this._clip(); g.strokeStyle = c; g.lineWidth = o.width || 2;
      if (o.dash) g.setLineDash(o.dash);
      g.beginPath();
      let started = false;
      for (let i = 0; i < xs.length; i++) {
        if (!isFinite(ys[i])) { started = false; continue; }
        const x = this.X(xs[i]), y = this.Y(ys[i]);
        if (!started) { g.moveTo(x, y); started = true; } else g.lineTo(x, y);
      }
      g.stroke(); g.setLineDash([]); g.restore();
      if (o.label) this.series.push({ label: o.label, color: c, pts: xs.map((x, i) => [x, ys[i]]), kind: "line" });
      return c;
    }
    func(f, o) {
      o = o || {}; const n = o.n || 240, [a, b] = this.o.xlim, xs = [], ys = [];
      for (let i = 0; i <= n; i++) { const x = a + (b - a) * i / n; xs.push(x); ys.push(f(x)); }
      return this.line(xs, ys, o);
    }
    area(xs, ys, o) {
      o = o || {}; const c = this.color(o.color); const g = this.g; const y0 = this.Y(Math.max(this.o.ylim[0], 0));
      this._clip(); g.globalAlpha = o.alpha !== undefined ? o.alpha : 0.25; g.fillStyle = c;
      g.beginPath(); g.moveTo(this.X(xs[0]), y0);
      for (let i = 0; i < xs.length; i++) g.lineTo(this.X(xs[i]), this.Y(ys[i]));
      g.lineTo(this.X(xs[xs.length - 1]), y0); g.closePath(); g.fill();
      g.globalAlpha = 1; g.restore();
      return c;
    }
    stem(xs, ys, o) {   /* PMF: thin stems + ≥8px markers */
      o = o || {}; const c = this.color(o.color); const g = this.g; const y0 = this.Y(Math.max(this.o.ylim[0], 0));
      this._clip(); g.strokeStyle = c; g.lineWidth = o.width || 2;
      for (let i = 0; i < xs.length; i++) {
        const x = this.X(xs[i]); g.beginPath(); g.moveTo(x, y0); g.lineTo(x, this.Y(ys[i])); g.stroke();
      }
      g.fillStyle = c;
      for (let i = 0; i < xs.length; i++) {
        g.beginPath(); g.arc(this.X(xs[i]), this.Y(ys[i]), o.r || 4, 0, 7); g.fill();
      }
      g.restore();
      if (o.label) this.series.push({ label: o.label, color: c, pts: xs.map((x, i) => [x, ys[i]]), kind: "stem" });
      return c;
    }
    bars(xs, hs, o) {   /* histogram-style bars; 2px gap; 4px rounded top */
      o = o || {}; const c = this.color(o.color); const g = this.g;
      const bw = o.bw !== undefined ? Math.abs(this.X(xs[0] + o.bw) - this.X(xs[0])) :
        Math.max(4, (this.w - this.o.pad.l - this.o.pad.r) / (xs.length * 1.5));
      const y0 = this.Y(Math.max(this.o.ylim[0], 0));
      this._clip(); g.fillStyle = c; g.globalAlpha = o.alpha !== undefined ? o.alpha : 0.85;
      for (let i = 0; i < xs.length; i++) {
        const x = this.X(xs[i]) - bw / 2 + 1, y = this.Y(hs[i]);
        const rr = Math.min(4, bw / 2, Math.abs(y0 - y));
        g.beginPath();
        g.moveTo(x, y0); g.lineTo(x, y + rr); g.arcTo(x, y, x + rr, y, rr);
        g.lineTo(x + bw - 2 - rr, y); g.arcTo(x + bw - 2, y, x + bw - 2, y + rr, rr);
        g.lineTo(x + bw - 2, y0); g.closePath(); g.fill();
      }
      g.globalAlpha = 1; g.restore();
      if (o.label) this.series.push({ label: o.label, color: c, pts: xs.map((x, i) => [x, hs[i]]), kind: "bar" });
      return c;
    }
    step(xs, ys, o) {   /* CDF staircase: right-continuous, closed dot at left of each riser */
      o = o || {}; const c = this.color(o.color); const g = this.g;
      this._clip(); g.strokeStyle = c; g.lineWidth = o.width || 2; g.beginPath();
      let px = this.X(this.o.xlim[0]), py = this.Y(o.y0 !== undefined ? o.y0 : 0);
      g.moveTo(px, py);
      for (let i = 0; i < xs.length; i++) {
        const x = this.X(xs[i]), y = this.Y(ys[i]);
        g.lineTo(x, py); g.moveTo(x, y); g.lineTo(x, y); py = y; g.lineTo(x, y);
      }
      g.lineTo(this.X(this.o.xlim[1]), py); g.stroke();
      if (o.dots !== false) {
        for (let i = 0; i < xs.length; i++) {
          const x = this.X(xs[i]), y = this.Y(ys[i]);
          g.fillStyle = c; g.beginPath(); g.arc(x, y, 3.5, 0, 7); g.fill();           /* closed */
          const yPrev = this.Y(i === 0 ? (o.y0 || 0) : ys[i - 1]);
          g.fillStyle = "#fff"; g.beginPath(); g.arc(x, yPrev, 3.5, 0, 7); g.fill();  /* open */
          g.strokeStyle = c; g.lineWidth = 1.5; g.beginPath(); g.arc(x, yPrev, 3.5, 0, 7); g.stroke();
        }
      }
      g.restore();
      if (o.label) this.series.push({ label: o.label, color: c, pts: xs.map((x, i) => [x, ys[i]]), kind: "step" });
      return c;
    }
    points(xs, ys, o) {
      o = o || {}; const c = this.color(o.color); const g = this.g;
      this._clip(); g.fillStyle = c;
      for (let i = 0; i < xs.length; i++) { g.beginPath(); g.arc(this.X(xs[i]), this.Y(ys[i]), o.r || 4, 0, 7); g.fill(); }
      g.restore();
      if (o.label) this.series.push({ label: o.label, color: c, pts: xs.map((x, i) => [x, ys[i]]), kind: "pt" });
      return c;
    }
    vline(x, o) { o = o || {}; const g = this.g; this._clip(); g.strokeStyle = o.color || MUTED; g.lineWidth = o.width || 1.3; g.setLineDash(o.dash || [5, 4]); g.beginPath(); g.moveTo(this.X(x), this.Y(this.o.ylim[0])); g.lineTo(this.X(x), this.Y(this.o.ylim[1])); g.stroke(); g.setLineDash([]); g.restore(); }
    hline(y, o) { o = o || {}; const g = this.g; this._clip(); g.strokeStyle = o.color || MUTED; g.lineWidth = o.width || 1.3; g.setLineDash(o.dash || [5, 4]); g.beginPath(); g.moveTo(this.X(this.o.xlim[0]), this.Y(y)); g.lineTo(this.X(this.o.xlim[1]), this.Y(y)); g.stroke(); g.setLineDash([]); g.restore(); }
    text(s, x, y, o) { o = o || {}; const g = this.g; g.fillStyle = o.color || INK; g.font = o.font || FONT; g.textAlign = o.align || "center"; g.textBaseline = o.baseline || "bottom"; g.fillText(s, this.X(x), this.Y(y) - (o.dy || 4)); }
    legend(pos) {
      if (!this.series.length) return;
      const g = this.g, { l, r, t } = this.o.pad;
      g.font = FONT_SM;
      let wMax = 0; for (const s of this.series) wMax = Math.max(wMax, g.measureText(s.label).width);
      const bw = wMax + 34, bh = this.series.length * 17 + 8;
      let x0 = pos === "left" ? l + 8 : this.w - r - bw - 8, y0 = t + 6;
      g.fillStyle = "rgba(255,255,255,0.92)"; g.strokeStyle = GRID;
      g.beginPath(); g.rect(x0, y0, bw, bh); g.fill(); g.stroke();
      this.series.forEach((s, i) => {
        const y = y0 + 12 + i * 17;
        g.strokeStyle = s.color; g.lineWidth = s.kind === "line" ? 2.5 : 0;
        if (s.kind === "line" || s.kind === "step") { g.beginPath(); g.moveTo(x0 + 7, y); g.lineTo(x0 + 22, y); g.stroke(); }
        else { g.fillStyle = s.color; g.beginPath(); g.arc(x0 + 14, y, 4.5, 0, 7); g.fill(); }
        g.fillStyle = INK; g.textAlign = "left"; g.textBaseline = "middle"; g.fillText(s.label, x0 + 28, y);
      });
    }
    _bindHover() {
      const tip = document.createElement("div");
      tip.style.cssText = "position:fixed;pointer-events:none;background:rgba(20,20,20,0.88);color:#fff;" +
        "font:11.5px system-ui,sans-serif;padding:4px 8px;border-radius:4px;z-index:99;display:none;white-space:pre;";
      document.body.appendChild(tip);
      this.cv.addEventListener("mousemove", (ev) => {
        if (!this.series.length) return;
        const rc = this.cv.getBoundingClientRect();
        const mx = ev.clientX - rc.left, my = ev.clientY - rc.top;
        let best = null, bd = 24 * 24;
        for (const s of this.series) for (const [x, y] of s.pts) {
          const dx = this.X(x) - mx, dy = this.Y(y) - my, d = dx * dx + dy * dy;
          if (d < bd) { bd = d; best = { s, x, y }; }
        }
        if (best) {
          tip.style.display = "block";
          tip.style.left = (ev.clientX + 12) + "px"; tip.style.top = (ev.clientY - 10) + "px";
          tip.textContent = best.s.label + "\nx = " + fmt(best.x) + "   y = " + fmt(best.y);
        } else tip.style.display = "none";
      });
      this.cv.addEventListener("mouseleave", () => { tip.style.display = "none"; });
    }
  }

  global.Plot = Plot;
  global.PlotPalette = PAL;
})(window);
