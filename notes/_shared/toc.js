/* toc.js — builds the fixed-sidebar TOC from #main h2/h3, with scrollspy,
   collapsible h2 groups, and a filter box. Runs on DOMContentLoaded. */
(function () {
  "use strict";
  function slug(s) { return s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 60); }

  document.addEventListener("DOMContentLoaded", function () {
    const toc = document.getElementById("toc");
    const main = document.getElementById("main");
    if (!toc || !main) return;
    const heads = main.querySelectorAll("h2, h3");
    const items = [];
    let curLi2 = null, curUl3 = null;
    heads.forEach((h) => {
      if (!h.id) h.id = slug(h.textContent) || "sec" + items.length;
      const li = document.createElement("li");
      li.className = h.tagName === "H2" ? "lvl2" : "lvl3";
      const a = document.createElement("a");
      a.href = "#" + h.id;
      a.textContent = h.textContent.replace(/\s+/g, " ").trim();
      li.appendChild(a);
      if (h.tagName === "H2") {
        const caret = document.createElement("span");
        caret.className = "caret"; caret.textContent = "▾";
        caret.addEventListener("click", (e) => {
          e.preventDefault(); e.stopPropagation();
          li.classList.toggle("collapsed");
          caret.textContent = li.classList.contains("collapsed") ? "▸" : "▾";
        });
        a.appendChild(caret);
        curUl3 = document.createElement("ul");
        curUl3.style.cssText = "list-style:none;margin:0;padding:0;";
        li.appendChild(curUl3);
        toc.appendChild(li);
        curLi2 = li;
      } else if (curUl3) {
        curUl3.appendChild(li);
      } else {
        toc.appendChild(li);
      }
      items.push({ h, a, li });
    });

    // scrollspy
    let ticking = false;
    function spy() {
      ticking = false;
      let active = items[0];
      for (const it of items) {
        if (it.h.getBoundingClientRect().top <= 90) active = it; else break;
      }
      items.forEach((it) => it.a.classList.toggle("active", it === active));
      if (active) {
        const sb = document.getElementById("sidebar");
        const r = active.a.getBoundingClientRect(), sr = sb.getBoundingClientRect();
        if (r.top < sr.top + 60 || r.bottom > sr.bottom - 60)
          active.a.scrollIntoView({ block: "center", behavior: "smooth" });
      }
    }
    window.addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(spy); } });
    spy();

    // filter
    const f = document.getElementById("tocfilter");
    if (f) f.addEventListener("input", () => {
      const q = f.value.trim().toLowerCase();
      items.forEach((it) => {
        const hit = !q || it.a.textContent.toLowerCase().includes(q);
        it.li.style.display = hit ? "" : "none";
        if (hit && q && it.li.className === "lvl3") {
          let p = it.li.parentElement.closest("li"); if (p) p.style.display = "";
        }
      });
    });

    // mobile toggle
    const tg = document.getElementById("sbtoggle");
    if (tg) tg.addEventListener("click", () => document.getElementById("sidebar").classList.toggle("open"));

    // dark mode toggle (persisted; overrides OS preference both ways).
    // Inserted right after the breadcrumb at the TOP of the sidebar so it is
    // always visible without scrolling the (long) TOC.
    const nav = document.querySelector("#sidebar .crumb") || document.querySelector("#sidebar .navlinks");
    if (nav) {
      const btn = document.createElement("button");
      btn.id = "themetoggle";
      const current = () => document.documentElement.dataset.theme ||
        (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
      const label = () => { btn.textContent = current() === "dark" ? "☀ light mode" : "🌙 dark mode"; };
      btn.addEventListener("click", () => {
        const next = current() === "dark" ? "light" : "dark";
        document.documentElement.dataset.theme = next;
        try { localStorage.setItem("theme6041", next); } catch (e) {}
        label();
      });
      label();
      if (nav.classList.contains("crumb")) nav.insertAdjacentElement("afterend", btn);
      else nav.appendChild(btn);
    }
  });
  // apply saved theme ASAP (before DOMContentLoaded to reduce flash)
  try {
    const saved = localStorage.getItem("theme6041");
    if (saved) document.documentElement.dataset.theme = saved;
  } catch (e) {}
})();
