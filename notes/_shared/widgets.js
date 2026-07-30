/* widgets.js — declarative interactive-widget framework for the 6.041 notes.
   Widget.create({el, title, note, controls:[...], height, draw(state, canvas, out)})
   Control types:
     {type:'range', id, label, min, max, step, value, fmt}   slider + −/+ steppers + numeric box
     {type:'number', id, label, min, max, step, value}
     {type:'select', id, label, options:[{v,label}], value}
     {type:'check',  id, label, value}
     {type:'button', id, label, primary, onClick(state, api)}
     {type:'anim',   id, label, fps, tick(state, api)}       play/pause animation loop
   draw() is called on every change; `out` is a readout <div> for computed values. */
(function (global) {
  "use strict";
  function el(tag, cls, html) { const e = document.createElement(tag); if (cls) e.className = cls; if (html !== undefined) e.innerHTML = html; return e; }

  function create(cfg) {
    const host = typeof cfg.el === "string" ? document.querySelector(cfg.el) : cfg.el;
    if (!host) { console.error("Widget host not found:", cfg.el); return null; }
    host.classList.add("widget");
    const state = {};
    const api = { redraw, state, set(id, v) { state[id] = v; syncCtl(id); redraw(); } };
    const ctlEls = {};

    if (cfg.title) host.appendChild(el("div", "whead", cfg.title));
    const bar = el("div", "wcontrols"); host.appendChild(bar);
    const cwrap = el("div", "wcanvas"); host.appendChild(cwrap);
    const canvas = el("canvas", "plot"); cwrap.appendChild(canvas);
    canvas.style.height = (cfg.height || 300) + "px";
    const out = el("div", "wreadout"); host.appendChild(out);
    if (cfg.note) host.appendChild(el("div", "wnote", cfg.note));

    (cfg.controls || []).forEach((c) => {
      const w = el("div", "wctl"); bar.appendChild(w);
      if (c.type === "range" || c.type === "number") {
        state[c.id] = c.value;
        w.appendChild(el("label", "", c.label));
        let slider = null;
        if (c.type === "range") {
          slider = el("input"); slider.type = "range";
          slider.min = c.min; slider.max = c.max; slider.step = c.step || 1; slider.value = c.value;
          w.appendChild(slider);
        }
        const dec = el("span", "wstep", "−"), inc = el("span", "wstep", "+");
        const box = el("input", "wval"); box.type = "text"; box.value = c.value;
        if (c.type === "range") w.appendChild(dec);
        w.appendChild(box);
        if (c.type === "range") w.appendChild(inc);
        const stepv = +(c.step || 1);
        const clamp = (v) => Math.min(c.max, Math.max(c.min, v));
        const setv = (v) => {
          v = clamp(v); if (!isFinite(v)) v = c.value;
          const dec10 = (String(stepv).split(".")[1] || "").length;
          state[c.id] = +v.toFixed(Math.min(6, dec10 + 2));
          if (slider) slider.value = state[c.id];
          box.value = c.fmt ? c.fmt(state[c.id]) : state[c.id];
          redraw();
        };
        if (slider) slider.addEventListener("input", () => setv(+slider.value));
        box.addEventListener("change", () => setv(parseFloat(box.value)));
        dec.addEventListener("click", () => setv(state[c.id] - stepv));
        inc.addEventListener("click", () => setv(state[c.id] + stepv));
        ctlEls[c.id] = { sync() { if (slider) slider.value = state[c.id]; box.value = state[c.id]; } };
      } else if (c.type === "select") {
        state[c.id] = c.value !== undefined ? c.value : c.options[0].v;
        w.appendChild(el("label", "", c.label));
        const s = el("select");
        c.options.forEach((o) => { const op = el("option", "", o.label); op.value = o.v; s.appendChild(op); });
        s.value = state[c.id];
        s.addEventListener("change", () => { state[c.id] = s.value; redraw(); });
        w.appendChild(s);
        ctlEls[c.id] = { sync() { s.value = state[c.id]; } };
      } else if (c.type === "check") {
        state[c.id] = !!c.value;
        const cb = el("input"); cb.type = "checkbox"; cb.checked = state[c.id];
        cb.addEventListener("change", () => { state[c.id] = cb.checked; redraw(); });
        w.appendChild(cb); w.appendChild(el("label", "", c.label));
        ctlEls[c.id] = { sync() { cb.checked = state[c.id]; } };
      } else if (c.type === "button") {
        const b = el("button", c.primary ? "primary" : "", c.label);
        b.addEventListener("click", () => c.onClick(state, api));
        w.appendChild(b);
      } else if (c.type === "anim") {
        let running = false, last = 0;
        const b = el("button", "primary", c.label || "▶ animate");
        const loop = (ts) => {
          if (!running) return;
          if (ts - last >= 1000 / (c.fps || 8)) { last = ts; c.tick(state, api); }
          requestAnimationFrame(loop);
        };
        b.addEventListener("click", () => {
          running = !running;
          b.innerHTML = running ? "❚❚ pause" : (c.label || "▶ animate");
          if (running) requestAnimationFrame(loop);
        });
        api["stop_" + c.id] = () => { running = false; b.innerHTML = c.label || "▶ animate"; };
        w.appendChild(b);
      }
    });

    function syncCtl(id) { if (ctlEls[id]) ctlEls[id].sync(); }
    function redraw() {
      canvas.width = 0;                     // force fresh measure
      const p = cfg.draw(state, canvas, out, api);
      return p;
    }
    // initial + responsive redraw
    redraw();
    let t = null;
    new ResizeObserver(() => { clearTimeout(t); t = setTimeout(redraw, 120); }).observe(cwrap);
    return api;
  }

  global.Widget = { create };
})(window);
