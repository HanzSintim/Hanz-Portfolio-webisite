/**
 * Hanz Ofosuhene-Sintim — High-Reactivity Interactive Portfolio Engine
 * Features:
 *  1. 60fps HTML5 Canvas Neural/Silicon Constellation reacting to mouse cursor
 *  2. Radial Cursor Spotlight (--mouse-x, --mouse-y) & 3D Card Tilt Physics
 *  3. 4-Atmosphere Chameleon Theme Switcher (Aurora, Editorial Light, Cyber, Silicon Gold)
 *  4. Animated Typewriter Role Cycling & Bilingual (EN <-> FR) Engine
 *  5. Live Interactive CLI Terminal (hanz@junia-lille:~$)
 *  6. Filterable 3D Workstation + Live Python/C++ E.Leclerc Euro POS Simulator
 *  7. Interactive SVG Radar/Petal Highlighter & Ghana <-> France Corridor Map Pins
 */

(function () {
  "use strict";

  let currentLang = "en";
  let activeProjectIndex = 0;
  const projectsData = window.PORTFOLIO_DATA ? window.PORTFOLIO_DATA.projects : [];
  const petalsData = window.PORTFOLIO_DATA ? window.PORTFOLIO_DATA.skill_petals : [];

  // =========================================================================
  // 1. TOAST NOTIFICATION HELPER
  // =========================================================================
  function showToast(msg) {
    const toast = document.getElementById("toastBanner");
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add("show");
    clearTimeout(window._toastTimer);
    window._toastTimer = setTimeout(() => toast.classList.remove("show"), 2800);
  }

  // =========================================================================
  // 2. 60FPS INTERACTIVE CONSTELLATION CANVAS
  // =========================================================================
  function initConstellationCanvas() {
    const canvas = document.getElementById("constellationCanvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const mouse = { x: -9999, y: -9999 };
    window.addEventListener("mousemove", (e) => {
      mouse.x = e.clientX;
      mouse.y = e.clientY;
    });
    window.addEventListener("resize", () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    });

    const count = Math.min(55, Math.floor((width * height) / 24000));
    const nodes = Array.from({ length: count }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.55,
      vy: (Math.random() - 0.5) * 0.55,
      r: Math.random() * 1.8 + 1.1,
    }));

    function draw() {
      ctx.clearRect(0, 0, width, height);
      const isLight = document.documentElement.getAttribute("data-theme") === "editorial";
      const dotColor = isLight ? "rgba(37, 99, 235, 0.45)" : "rgba(99, 102, 241, 0.55)";
      const lineBase = isLight ? "37, 99, 235" : "56, 189, 248";

      for (let i = 0; i < nodes.length; i++) {
        const n = nodes[i];
        n.x += n.vx;
        n.y += n.vy;

        if (n.x < 0 || n.x > width) n.vx *= -1;
        if (n.y < 0 || n.y > height) n.vy *= -1;

        // Gentle mouse repulsion/attraction
        const dxm = mouse.x - n.x;
        const dym = mouse.y - n.y;
        const distMouse = Math.hypot(dxm, dym);
        if (distMouse < 160) {
          ctx.beginPath();
          ctx.moveTo(n.x, n.y);
          ctx.lineTo(mouse.x, mouse.y);
          ctx.strokeStyle = `rgba(${lineBase}, ${(1 - distMouse / 160) * 0.42})`;
          ctx.lineWidth = 1;
          ctx.stroke();
        }

        ctx.beginPath();
        ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
        ctx.fillStyle = dotColor;
        ctx.fill();

        for (let j = i + 1; j < nodes.length; j++) {
          const m = nodes[j];
          const d = Math.hypot(n.x - m.x, n.y - m.y);
          if (d < 130) {
            ctx.beginPath();
            ctx.moveTo(n.x, n.y);
            ctx.lineTo(m.x, m.y);
            ctx.strokeStyle = `rgba(${lineBase}, ${(1 - d / 130) * 0.2})`;
            ctx.lineWidth = 0.8;
            ctx.stroke();
          }
        }
      }
      requestAnimationFrame(draw);
    }
    draw();
  }

  // =========================================================================
  // 3. SPOTLIGHT CURSOR TRACKING & SUBTLE 3D TILT ON BENTO CARDS
  // =========================================================================
  function initSpotlightAndTilt() {
    const cards = document.querySelectorAll(".bento-card");
    cards.forEach((card) => {
      card.addEventListener("mousemove", (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        card.style.setProperty("--mouse-x", `${x}px`);
        card.style.setProperty("--mouse-y", `${y}px`);

        if (card.hasAttribute("data-tilt")) {
          const rotY = ((x / rect.width) - 0.5) * 4.5;
          const rotX = ((y / rect.height) - 0.5) * -4.5;
          card.style.transform = `perspective(900px) rotateX(${rotX.toFixed(2)}deg) rotateY(${rotY.toFixed(2)}deg)`;
        }
      });

      card.addEventListener("mouseleave", () => {
        if (card.hasAttribute("data-tilt")) {
          card.style.transform = "perspective(900px) rotateX(0deg) rotateY(0deg)";
        }
      });
    });
  }

  // =========================================================================
  // 4. 4-THEME CHAMELEON ENGINE
  // =========================================================================
  function initThemeSwitcher() {
    const themeBtns = document.querySelectorAll("[data-set-theme]");
    const saved = localStorage.getItem("hanz_theme") || "aurora";
    document.documentElement.setAttribute("data-theme", saved);

    themeBtns.forEach((btn) => {
      btn.classList.toggle("active", btn.getAttribute("data-set-theme") === saved);
      btn.addEventListener("click", () => {
        const nextTheme = btn.getAttribute("data-set-theme");
        document.documentElement.setAttribute("data-theme", nextTheme);
        localStorage.setItem("hanz_theme", nextTheme);
        themeBtns.forEach((b) => b.classList.toggle("active", b === btn));
        showToast(`Theme switched to ${nextTheme.toUpperCase()}`);
      });
    });
  }

  // =========================================================================
  // 5. ANIMATED TYPEWRITER ROLE SWITCHER
  // =========================================================================
  function initTypewriter() {
    const el = document.getElementById("typewriterText");
    if (!el) return;

    const rolesEn = [
      "Python 3 & Flask Systems Architect",
      "C++17 POS & Embedded Firmware Engineer",
      "M1 Microelectronics & Nanotech @ JUNIA Lille",
      "BSc Computer Engineering @ KNUST (ACES President)",
      "3NF Relational Data & API Designer",
    ];
    const rolesFr = [
      "Architecte Systèmes Python 3 & Flask",
      "Ingénieur C++17 TPV & Systèmes Embarqués",
      "M1 Microélectronique & Nanotech @ JUNIA Lille",
      "BSc Génie Informatique @ KNUST (Président ACES)",
      "Concepteur d'APIs REST & Bases de Données 3NF",
    ];

    let roleIdx = 0;
    let charIdx = 0;
    let deleting = false;

    function tick() {
      const list = currentLang === "fr" ? rolesFr : rolesEn;
      const word = list[roleIdx % list.length];

      if (!deleting) {
        charIdx++;
        el.textContent = word.slice(0, charIdx);
        if (charIdx >= word.length) {
          deleting = true;
          setTimeout(tick, 2000);
          return;
        }
        setTimeout(tick, 45);
      } else {
        charIdx--;
        el.textContent = word.slice(0, charIdx);
        if (charIdx <= 0) {
          deleting = false;
          roleIdx = (roleIdx + 1) % list.length;
          setTimeout(tick, 260);
          return;
        }
        setTimeout(tick, 24);
      }
    }
    tick();
  }

  // =========================================================================
  // 6. INTERACTIVE CLI TERMINAL EMULATOR (hanz@junia-lille:~$)
  // =========================================================================
  function initTerminal() {
    const outBox = document.getElementById("termOutputBox");
    const inputEl = document.getElementById("termCommandInput");
    const chipBtns = document.querySelectorAll("[data-term-cmd]");
    if (!outBox || !inputEl) return;

    function appendLine(html, isCmd = false) {
      const div = document.createElement("div");
      div.style.marginBottom = "0.35rem";
      div.innerHTML = isCmd
        ? `<span style="color:#10b981;font-weight:700;">hanz@junia-lille:~$</span> <span style="color:#f8fafc;">${html}</span>`
        : html;
      outBox.appendChild(div);
      outBox.scrollTop = outBox.scrollHeight;
    }

    function runCommand(raw) {
      const cmd = raw.trim().toLowerCase();
      if (!cmd) return;
      appendLine(raw, true);

      if (cmd === "help") {
        appendLine(
          `<span style="color:#38bdf8;">Available commands:</span> <code>python</code>, <code>leclerc</code>, <code>projects</code>, <code>corridor</code>, <code>leadership</code>, <code>theme</code>, <code>contact</code>, <code>clear</code>`
        );
      } else if (cmd === "python" || cmd === "skills") {
        appendLine(
          `<span style="color:#a5b4fc;">[Python 3.12 Stack]</span> Flask WSGI · Typed @dataclass Models · REST JSON Telemetry · SQL 3NF Schemas · 95% Proficiency.`
        );
      } else if (cmd === "leclerc" || cmd === "pos") {
        appendLine(
          `<span style="color:#fbbf24;">[E.Leclerc C++17 POS]</span> RTTI dynamic_cast Bagging Scale + 12-Denomination Euro Greedy Dispenser + PSD2 NFC (&lt;= 50€). Jumping to simulator...`
        );
        renderActiveProject(1);
      } else if (cmd === "projects") {
        appendLine(
          `01. Python Telemetry Portfolio | 02. E.Leclerc C++17 POS | 03. STM32+ESP32 Autonomous Robot | 04. Smart Logistics 3NF DB | 05. Ultrasonic Water Tank | 06. AgricConnect`
        );
      } else if (cmd === "corridor") {
        appendLine(
          `🇬🇭 ACCRA (PRESEC '22) ➔ 🇬🇭 KUMASI (KNUST BSc CompEng / ACES President) ➔ 🇫🇷 LILLE (JUNIA ISEN M1 Microelectronics &amp; Embedded)`
        );
      } else if (cmd === "leadership") {
        appendLine(
          `★ ACES Department President (KNUST) | ★ GHAFRA Nord Strategic Planning Lead (Lille) | ★ H &amp; D'S HUB Co-Lead`
        );
      } else if (cmd === "contact") {
        appendLine(
          `Email: <a href="mailto:hanz.ofosuhene-sintim@student.junia.com" style="color:#38bdf8;">hanz.ofosuhene-sintim@student.junia.com</a> | GitHub: @HanzSintim`
        );
      } else if (cmd === "theme") {
        const themes = ["aurora", "editorial", "cyber", "silicon"];
        const curr = document.documentElement.getAttribute("data-theme") || "aurora";
        const next = themes[(themes.indexOf(curr) + 1) % themes.length];
        document.documentElement.setAttribute("data-theme", next);
        appendLine(`Switched active visual theme to <strong style="color:#f59e0b;">${next.toUpperCase()}</strong>.`);
      } else if (cmd === "clear") {
        outBox.innerHTML = "";
      } else {
        appendLine(`Command not recognized: <code>${cmd}</code>. Type <code>help</code> for options.`);
      }
    }

    inputEl.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        runCommand(inputEl.value);
        inputEl.value = "";
      }
    });

    chipBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        runCommand(btn.getAttribute("data-term-cmd"));
      });
    });
  }

  // =========================================================================
  // 7. WORKSTATION PROJECT SWITCHER & CATEGORY FILTER
  // =========================================================================
  function renderActiveProject(index) {
    if (!projectsData || !projectsData.length) return;
    activeProjectIndex = index;
    const proj = projectsData[index];

    document.querySelectorAll(".project-rail-item").forEach((btn, idx) => {
      btn.classList.toggle("active", idx === index);
    });

    const titleEl = document.getElementById("screenProjTitle");
    const statusEl = document.getElementById("screenProjStatus");
    const summaryEl = document.getElementById("screenProjSummary");
    const archListEl = document.getElementById("screenProjArch");
    const metricsRowEl = document.getElementById("screenProjMetrics");
    const repoLinkEl = document.getElementById("screenProjRepo");
    const codeFileEl = document.getElementById("screenCodeFilename");
    const codePreEl = document.getElementById("screenCodePre");

    if (titleEl) titleEl.textContent = currentLang === "fr" ? proj.title_fr : proj.title_en;
    if (statusEl) statusEl.textContent = currentLang === "fr" ? proj.status_fr : proj.status_en;
    if (summaryEl) summaryEl.textContent = currentLang === "fr" ? proj.summary_fr : proj.summary_en;
    if (repoLinkEl) repoLinkEl.href = proj.repo_url;
    if (codeFileEl) codeFileEl.textContent = proj.code_Filename;
    if (codePreEl) codePreEl.textContent = proj.code_snippet;

    if (archListEl) {
      const archItems = currentLang === "fr" ? proj.architecture_fr : proj.architecture_en;
      archListEl.innerHTML = archItems.map((item) => `<li>${item}</li>`).join("");
    }

    if (metricsRowEl && proj.metrics) {
      metricsRowEl.innerHTML = Object.entries(proj.metrics)
        .map(
          ([k, v]) => `
          <div class="metric-mini-tile" style="padding:0.65rem 0.8rem;">
            <div style="font-family:var(--font-mono);font-size:0.65rem;color:var(--text-secondary);">${k}</div>
            <div style="font-family:var(--font-mono);font-size:0.82rem;font-weight:800;color:var(--accent-2);margin-top:0.15rem;">${v}</div>
          </div>`
        )
        .join("");
    }
  }

  function initProjectFilters() {
    const filterBtns = document.querySelectorAll("[data-filter-cat]");
    const railItems = document.querySelectorAll(".project-rail-item");

    filterBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        const cat = btn.getAttribute("data-filter-cat");
        filterBtns.forEach((b) => b.classList.toggle("active", b === btn));

        let firstVisible = -1;
        railItems.forEach((item, idx) => {
          const itemCat = item.getAttribute("data-proj-cat");
          const show = cat === "all" || itemCat === cat;
          item.style.display = show ? "flex" : "none";
          if (show && firstVisible === -1) firstVisible = idx;
        });

        if (firstVisible !== -1) renderActiveProject(firstVisible);
      });
    });
  }

  // =========================================================================
  // 8. LIVE E.LECLERC EURO POS GREEDY CHANGE & TVA 20% SIMULATOR
  // =========================================================================
  function updatePosSimulator() {
    const amountInput = document.getElementById("posAmountInput");
    const tenderedInput = document.getElementById("posTenderedInput");
    const summaryOut = document.getElementById("posSummaryOutput");
    const denomOut = document.getElementById("posDenomOutput");
    if (!amountInput || !tenderedInput || !summaryOut || !denomOut) return;

    const amount = Math.max(0.01, parseFloat(amountInput.value) || 47.97);
    const tendered = Math.max(amount, parseFloat(tenderedInput.value) || 60.0);

    const totalCents = Math.round(amount * 100);
    const tenderedCents = Math.round(tendered * 100);
    const totalHtCents = Math.round(totalCents / 1.2);
    const tvaCents = totalCents - totalHtCents;

    const denoms = [
      [5000, "50.00 € Bill"],
      [2000, "20.00 € Bill"],
      [1000, "10.00 € Bill"],
      [500, "5.00 € Bill"],
      [200, "2.00 € Coin"],
      [100, "1.00 € Coin"],
      [50, "0.50 € Coin"],
      [20, "0.20 € Coin"],
      [10, "0.10 € Coin"],
      [5, "0.05 € Coin"],
      [2, "0.02 € Coin"],
      [1, "0.01 € Coin"],
    ];

    let changeCents = Math.max(0, tenderedCents - totalCents);
    let rem = changeCents;
    const dispensed = [];

    for (const [cents, label] of denoms) {
      const count = Math.floor(rem / cents);
      rem = rem % cents;
      if (count > 0) dispensed.push({ count, label });
    }

    const nfcState =
      totalCents <= 5000 ? "NFC Contactless OK (<= 50€)" : "EMV Chip + 4-Digit PIN Required (> 50€)";
    summaryOut.textContent = `HT: ${(totalHtCents / 100).toFixed(2)} €  ·  TVA (20%): ${(tvaCents / 100).toFixed(2)} €  ·  Change: ${(changeCents / 100).toFixed(2)} €  ·  ${nfcState}`;

    denomOut.innerHTML =
      dispensed.length === 0
        ? `<span class="denom-badge">Exact Tender (0.00 € Change)</span>`
        : dispensed.map((d) => `<span class="denom-badge">${d.count} × ${d.label}</span>`).join("");
  }

  // =========================================================================
  // 9. INTERACTIVE RADAR PETALS & CORRIDOR MAP PINS
  // =========================================================================
  function initRadarAndMapReactivity() {
    const petalCards = document.querySelectorAll(".petal-focus-card");
    const svgPetals = document.querySelectorAll("[data-svg-petal]");

    petalCards.forEach((card, idx) => {
      card.addEventListener("mouseenter", () => {
        petalCards.forEach((c, i) => c.classList.toggle("active", i === idx));
        svgPetals.forEach((g, i) => {
          g.style.transform = i === idx ? "scale(1.12)" : "scale(1)";
        });
      });
    });

    const mapPins = document.querySelectorAll("[data-corridor-pin]");
    const corridorCards = document.querySelectorAll("[data-corridor-card]");
    mapPins.forEach((pin) => {
      pin.addEventListener("click", () => {
        const code = pin.getAttribute("data-corridor-pin");
        corridorCards.forEach((card) => {
          card.classList.toggle("active", card.getAttribute("data-corridor-card") === code);
        });
        showToast(`Focused Corridor Node: ${code}`);
      });
    });
  }

  // =========================================================================
  // 10. DUAL-CONTINENT HARDWARE CLOCKS & BILINGUAL SWITCHER
  // =========================================================================
  function updateClocks() {
    const lilleEl = document.getElementById("clockLille");
    const accraEl = document.getElementById("clockAccra");
    const navSubEl = document.getElementById("corridorLiveClock");
    try {
      const now = new Date();
      const lille = new Intl.DateTimeFormat("en-GB", {
        timeZone: "Europe/Paris",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      }).format(now);
      const accra = new Intl.DateTimeFormat("en-GB", {
        timeZone: "Africa/Accra",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      }).format(now);

      if (lilleEl) lilleEl.textContent = `${lille} CET`;
      if (accraEl) accraEl.textContent = `${accra} GMT`;
      if (navSubEl) navSubEl.textContent = `Lille ${lille} ⇄ Ghana ${accra}`;
    } catch (e) {}
  }

  function applyLanguage(lang) {
    currentLang = lang;
    document.documentElement.setAttribute("lang", lang);
    document.querySelectorAll("[data-en][data-fr]").forEach((el) => {
      el.textContent = el.getAttribute(`data-${lang}`);
    });
    const langBtn = document.getElementById("langToggleBtn");
    if (langBtn) langBtn.textContent = lang === "en" ? "FR 🇫🇷" : "EN 🇬🇧";
    renderActiveProject(activeProjectIndex);
    showToast(lang === "fr" ? "Langue : Français 🇫🇷" : "Language: English 🇬🇧");
  }

  document.addEventListener("DOMContentLoaded", () => {
    initConstellationCanvas();
    initSpotlightAndTilt();
    initThemeSwitcher();
    initTypewriter();
    initTerminal();
    initProjectFilters();
    initRadarAndMapReactivity();

    document.querySelectorAll(".project-rail-item").forEach((btn, idx) => {
      btn.addEventListener("click", () => renderActiveProject(idx));
    });

    const langBtn = document.getElementById("langToggleBtn");
    if (langBtn) {
      langBtn.addEventListener("click", () => applyLanguage(currentLang === "en" ? "fr" : "en"));
    }

    const copyEmailBtn = document.getElementById("copyEmailBtn");
    if (copyEmailBtn) {
      copyEmailBtn.addEventListener("click", () => {
        navigator.clipboard.writeText("hanz.ofosuhene-sintim@student.junia.com");
        showToast("Copied email: hanz.ofosuhene-sintim@student.junia.com ✨");
      });
    }

    const copyCodeBtn = document.getElementById("copyCodeBtn");
    if (copyCodeBtn) {
      copyCodeBtn.addEventListener("click", () => {
        const code = document.getElementById("screenCodePre");
        if (code) {
          navigator.clipboard.writeText(code.textContent);
          showToast("Copied source snippet to clipboard! 💻");
        }
      });
    }

    const amountInput = document.getElementById("posAmountInput");
    const tenderedInput = document.getElementById("posTenderedInput");
    if (amountInput && tenderedInput) {
      amountInput.addEventListener("input", updatePosSimulator);
      tenderedInput.addEventListener("input", updatePosSimulator);
      updatePosSimulator();
    }

    renderActiveProject(0);
    updateClocks();
    setInterval(updateClocks, 1000);
  });
})();
