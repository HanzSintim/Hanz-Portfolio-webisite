/**
 * Hanz Ofosuhene-Sintim — Interactive Portfolio Engine (ES6)
 * Powers:
 *  - Bilingual EN <-> FR instant switching
 *  - Laptop Workstation 6-Project Switcher
 *  - Live Python/JS E.Leclerc Euro Change & TVA 20% Simulator
 *  - Dual-Corridor Hardware Clock (Lille CET & Accra GMT)
 */

(function () {
  "use strict";

  let currentLang = "en";
  let activeProjectIndex = 0;

  const projectsData = window.PORTFOLIO_DATA ? window.PORTFOLIO_DATA.projects : [];

  // 1. Bilingual Language Toggle
  function applyLanguage(lang) {
    currentLang = lang;
    document.documentElement.setAttribute("lang", lang);

    const nodes = document.querySelectorAll("[data-en][data-fr]");
    nodes.forEach((el) => {
      const text = el.getAttribute(`data-${lang}`);
      if (text) {
        el.textContent = text;
      }
    });

    const langBtn = document.getElementById("langToggleBtn");
    if (langBtn) {
      langBtn.textContent = lang === "en" ? "FR 🇫🇷 / EN" : "EN 🇬🇧 / FR";
    }

    renderActiveProject(activeProjectIndex);
  }

  // 2. Laptop Workstation Project Switcher
  function renderActiveProject(index) {
    if (!projectsData || !projectsData.length) return;
    activeProjectIndex = index;
    const proj = projectsData[index];

    const buttons = document.querySelectorAll(".project-select-btn");
    buttons.forEach((btn, idx) => {
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
    const urlBarEl = document.getElementById("screenUrlBar");

    if (titleEl) titleEl.textContent = currentLang === "fr" ? proj.title_fr : proj.title_en;
    if (statusEl) statusEl.textContent = currentLang === "fr" ? proj.status_fr : proj.status_en;
    if (summaryEl) summaryEl.textContent = currentLang === "fr" ? proj.summary_fr : proj.summary_en;
    if (urlBarEl) urlBarEl.textContent = `https://github.com/HanzSintim/${proj.slug}`;
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
          <div class="screen-metric-box">
            <div class="m-key">${k}</div>
            <div class="m-val">${v}</div>
          </div>`
        )
        .join("");
    }
  }

  // 3. E.Leclerc Euro Change & TVA 20% Calculator (Python API + Client Fallback)
  function computeLocalEuroPos(amountEur, tenderedEur) {
    const totalCents = Math.round(amountEur * 100);
    const tenderedCents = Math.round(tenderedEur * 100);
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
      if (count > 0) {
        dispensed.push({ count, denomination: label });
      }
    }

    return {
      total_ttc_eur: (totalCents / 100).toFixed(2),
      total_ht_eur: (totalHtCents / 100).toFixed(2),
      tva_20_eur: (tvaCents / 100).toFixed(2),
      change_returned_eur: (changeCents / 100).toFixed(2),
      nfc_eligible: totalCents <= 5000,
      dispensed_denominations: dispensed,
    };
  }

  function updatePosSimulator() {
    const amountInput = document.getElementById("posAmountInput");
    const tenderedInput = document.getElementById("posTenderedInput");
    const summaryOut = document.getElementById("posSummaryOutput");
    const denomOut = document.getElementById("posDenomOutput");

    if (!amountInput || !tenderedInput || !summaryOut || !denomOut) return;

    const amount = Math.max(0.01, parseFloat(amountInput.value) || 47.97);
    const tendered = Math.max(amount, parseFloat(tenderedInput.value) || 60.0);

    const res = computeLocalEuroPos(amount, tendered);
    const nfcBadge = res.nfc_eligible
      ? "NFC Sans Contact OK (<= 50€)"
      : "EMV Chip + 4-Digit PIN Required (> 50€)";

    summaryOut.textContent = `HT: ${res.total_ht_eur} € | TVA (20%): ${res.tva_20_eur} € | Change: ${res.change_returned_eur} € | ${nfcBadge}`;

    if (res.dispensed_denominations.length === 0) {
      denomOut.innerHTML = `<span class="denom-pill">Exact Amount (0.00 € Change)</span>`;
    } else {
      denomOut.innerHTML = res.dispensed_denominations
        .map((d) => `<span class="denom-pill">${d.count} × ${d.denomination}</span>`)
        .join("");
    }
  }

  // 4. Dual-Corridor Clock (Lille CET & Accra GMT)
  function updateClocks() {
    const clockEl = document.getElementById("corridorLiveClock");
    if (!clockEl) return;
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
      }).format(now);
      clockEl.textContent = `Lille (CET): ${lille}  ⇄  Kumasi/Accra (GMT): ${accra}`;
    } catch (e) {
      // Fallback
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    const langBtn = document.getElementById("langToggleBtn");
    if (langBtn) {
      langBtn.addEventListener("click", () => {
        applyLanguage(currentLang === "en" ? "fr" : "en");
      });
    }

    const projBtns = document.querySelectorAll(".project-select-btn");
    projBtns.forEach((btn, idx) => {
      btn.addEventListener("click", () => renderActiveProject(idx));
    });

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
