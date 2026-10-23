/**
 * Hanz Ofosuhene-Sintim — Interactive Portfolio Client Engine
 * ===========================================================
 * Powers:
 * 1. 3D Mouse-Parallax Hero Halo & Floating Widgets
 * 2. Kinetic Typewriter Headline (EN / FR)
 * 3. 3-in-1 Live Showreel Sandbox (E.Leclerc POS, STM32 Robot, 40kHz Water Tank)
 * 4. Interactive Tech Dock & Service Pillar Project Filtering
 * 5. Code & Architecture Modal Drawer
 * 6. Dual Theme Switcher (Midnight Neon <-> Aarav Frosted Periwinkle Glass)
 */

(function () {
  "use strict";

  const rawJsonEl = document.getElementById("portfolioDataJson");
  const PORTFOLIO_DATA = rawJsonEl ? JSON.parse(rawJsonEl.textContent) : { projects: [] };

  let currentLang = "en";
  let waterPumpState = false; // Hysteresis memory state for Simulator 3

  // -------------------------------------------------------------------------
  // 1. CURSOR SPOTLIGHT & 3D PARALLAX HERO STAGE
  // -------------------------------------------------------------------------
  const cursorGlow = document.getElementById("cursorGlow");
  const heroStage = document.getElementById("heroStage");
  const heroHalo = document.getElementById("heroHalo");
  const parallaxWidgets = document.querySelectorAll("[data-parallax]");

  window.addEventListener("mousemove", (e) => {
    if (cursorGlow) {
      cursorGlow.style.left = `${e.clientX}px`;
      cursorGlow.style.top = `${e.clientY}px`;
    }

    if (heroStage && heroHalo) {
      const rect = heroStage.getBoundingClientRect();
      if (rect.top < window.innerHeight && rect.bottom > 0) {
        const relX = (e.clientX - (rect.left + rect.width / 2)) / (rect.width / 2);
        const relY = (e.clientY - (rect.top + rect.height / 2)) / (rect.height / 2);

        heroHalo.style.transform = `rotateY(${relX * 8}deg) rotateX(${-relY * 8}deg)`;

        parallaxWidgets.forEach((widget) => {
          const factor = parseFloat(widget.getAttribute("data-parallax") || "12");
          widget.style.transform = `translate3d(${relX * factor}px, ${relY * factor}px, 0)`;
        });
      }
    }
  });

  // -------------------------------------------------------------------------
  // 2. KINETIC TYPEWRITER SUBTITLE
  // -------------------------------------------------------------------------
  const typewriterEl = document.getElementById("heroTypewriter");
  const phrasesMap = {
    en: [
      "Python 3 & Flask Systems.",
      "C++17 Retail POS Engines.",
      "STM32 & ESP32 Robotics.",
      "Strict 3NF SQL Databases.",
      "Microelectronics & Silicon.",
    ],
    fr: [
      "des backends Python 3 & Flask.",
      "des caisses C++17 temps-réel.",
      "des robots STM32 & ESP32.",
      "des bases relationnelles 3NF.",
      "des circuits microélectroniques.",
    ],
  };

  let phraseIdx = 0;
  let charIdx = 0;
  let deleting = false;

  function tickTypewriter() {
    if (!typewriterEl) return;
    const list = phrasesMap[currentLang] || phrasesMap.en;
    const target = list[phraseIdx % list.length];

    if (!deleting) {
      charIdx++;
      typewriterEl.textContent = target.slice(0, charIdx);
      if (charIdx >= target.length) {
        deleting = true;
        setTimeout(tickTypewriter, 1750);
        return;
      }
      setTimeout(tickTypewriter, 52);
    } else {
      charIdx--;
      typewriterEl.textContent = target.slice(0, Math.max(0, charIdx));
      if (charIdx <= 0) {
        deleting = false;
        phraseIdx = (phraseIdx + 1) % list.length;
        setTimeout(tickTypewriter, 260);
        return;
      }
      setTimeout(tickTypewriter, 28);
    }
  }
  setTimeout(tickTypewriter, 700);

  // -------------------------------------------------------------------------
  // 3. INTERACTIVE SHOWREEL SANDBOX (3 LIVE SIMULATORS)
  // -------------------------------------------------------------------------
  const simTabs = document.querySelectorAll(".showreel-tab-btn");
  const simPanels = document.querySelectorAll(".sim-panel");

  simTabs.forEach((btn) => {
    btn.addEventListener("click", () => {
      const targetId = btn.getAttribute("data-sim-target");
      simTabs.forEach((b) => b.classList.remove("active"));
      simPanels.forEach((p) => p.classList.remove("active"));
      btn.classList.add("active");
      const panel = document.getElementById(targetId);
      if (panel) panel.classList.add("active");
    });
  });

  // --- SIMULATOR 01: E.LECLERC GREEDY EURO CHANGE & TVA 20% ---
  const posAmountSlider = document.getElementById("posAmountSlider");
  const posTenderedSlider = document.getElementById("posTenderedSlider");
  const posAmountLabel = document.getElementById("posAmountLabel");
  const posTenderedLabel = document.getElementById("posTenderedLabel");
  const posHtVal = document.getElementById("posHtVal");
  const posTvaVal = document.getElementById("posTvaVal");
  const posTtcVal = document.getElementById("posTtcVal");
  const posChangeVal = document.getElementById("posChangeVal");
  const posNfcBadge = document.getElementById("posNfcBadge");
  const posDenomContainer = document.getElementById("posDenomContainer");

  const EURO_DENOMS = [
    { cents: 5000, label: "50€ Bill", isBill: true },
    { cents: 2000, label: "20€ Bill", isBill: true },
    { cents: 1000, label: "10€ Bill", isBill: true },
    { cents: 500, label: "5€ Bill", isBill: true },
    { cents: 200, label: "2€ Coin", isBill: false },
    { cents: 100, label: "1€ Coin", isBill: false },
    { cents: 50, label: "0.50€ Coin", isBill: false },
    { cents: 20, label: "0.20€ Coin", isBill: false },
    { cents: 10, label: "0.10€ Coin", isBill: false },
    { cents: 5, label: "0.05€ Coin", isBill: false },
    { cents: 2, label: "0.02€ Coin", isBill: false },
    { cents: 1, label: "0.01€ Coin", isBill: false },
  ];

  function updatePosSimulator() {
    if (!posAmountSlider || !posTenderedSlider) return;
    let amount = parseFloat(posAmountSlider.value);
    let tendered = parseFloat(posTenderedSlider.value);
    if (tendered < amount) {
      tendered = Math.ceil(amount);
      posTenderedSlider.value = String(tendered);
    }

    const totalCents = Math.round(amount * 100);
    const tenderedCents = Math.round(tendered * 100);
    const htCents = Math.round(totalCents / 1.2);
    const tvaCents = totalCents - htCents;
    const changeCents = Math.max(0, tenderedCents - totalCents);

    posAmountLabel.textContent = `${(totalCents / 100).toFixed(2)} €`;
    posTenderedLabel.textContent = `${(tenderedCents / 100).toFixed(2)} €`;
    posHtVal.textContent = `${(htCents / 100).toFixed(2)} €`;
    posTvaVal.textContent = `${(tvaCents / 100).toFixed(2)} €`;
    posTtcVal.textContent = `${(totalCents / 100).toFixed(2)} €`;
    posChangeVal.textContent = `${(changeCents / 100).toFixed(2)} €`;

    if (posNfcBadge) {
      if (totalCents <= 5000) {
        posNfcBadge.textContent = "NFC <= 50€ ELIGIBLE";
        posNfcBadge.style.background = "rgba(16, 185, 129, 0.2)";
        posNfcBadge.style.color = "#34d399";
      } else {
        posNfcBadge.textContent = "EMV CHIP + PIN REQUIRED (>50€)";
        posNfcBadge.style.background = "rgba(245, 158, 11, 0.22)";
        posNfcBadge.style.color = "#fbbf24";
      }
    }

    if (posDenomContainer) {
      posDenomContainer.innerHTML = "";
      let rem = changeCents;
      if (rem === 0) {
        const exactChip = document.createElement("span");
        exactChip.className = "denom-chip";
        exactChip.textContent = "Exact Amount — 0.00 € Change";
        posDenomContainer.appendChild(exactChip);
      } else {
        EURO_DENOMS.forEach((d) => {
          const count = Math.floor(rem / d.cents);
          rem = rem % d.cents;
          if (count > 0) {
            const chip = document.createElement("span");
            chip.className = `denom-chip ${d.isBill ? "bill" : ""}`;
            chip.textContent = `${d.label} × ${count}`;
            posDenomContainer.appendChild(chip);
          }
        });
      }
    }
  }

  if (posAmountSlider && posTenderedSlider) {
    posAmountSlider.addEventListener("input", updatePosSimulator);
    posTenderedSlider.addEventListener("input", updatePosSimulator);
    updatePosSimulator();
  }

  // --- SIMULATOR 02: STM32 + ESP32 URBAN CLEANING ROBOT ---
  const robotDistSlider = document.getElementById("robotDistSlider");
  const robotSteerSlider = document.getElementById("robotSteerSlider");
  const robotDistLabel = document.getElementById("robotDistLabel");
  const robotSteerLabel = document.getElementById("robotSteerLabel");
  const robotLeftPwm = document.getElementById("robotLeftPwm");
  const robotRightPwm = document.getElementById("robotRightPwm");
  const robotBrushState = document.getElementById("robotBrushState");
  const robotStateBadge = document.getElementById("robotStateBadge");
  const robotTelemetryLog = document.getElementById("robotTelemetryLog");

  function updateRobotSimulator() {
    if (!robotDistSlider || !robotSteerSlider) return;
    const distCm = parseInt(robotDistSlider.value, 10);
    const steerPx = parseInt(robotSteerSlider.value, 10);

    robotDistLabel.textContent = `${distCm} cm`;
    robotSteerLabel.textContent = `${steerPx >= 0 ? "+" : ""}${steerPx} px`;

    if (distCm < 30) {
      robotLeftPwm.textContent = "0% (BRAKE)";
      robotRightPwm.textContent = "0% (BRAKE)";
      robotBrushState.textContent = "HALTED";
      robotBrushState.style.color = "#fb7185";
      robotStateBadge.textContent = "OBSTACLE EMERGENCY STOP";
      robotStateBadge.style.background = "rgba(244, 63, 94, 0.25)";
      robotStateBadge.style.color = "#fb7185";
      robotTelemetryLog.textContent = `[STM32_ISR] CRITICAL ToF=${distCm}cm (<30cm) -> PWM_SetDutyCycle(0) | UART->ESP32: OBSTACLE_HALT`;
    } else {
      const basePwm = 70;
      const delta = Math.round(steerPx * 0.25);
      const left = Math.min(100, Math.max(20, basePwm + delta));
      const right = Math.min(100, Math.max(20, basePwm - delta));
      robotLeftPwm.textContent = `${left}%`;
      robotRightPwm.textContent = `${right}%`;
      robotBrushState.textContent = "ACTIVE 90%";
      robotBrushState.style.color = "#a3e635";
      robotStateBadge.textContent = "NOMINAL AI SWEEP";
      robotStateBadge.style.background = "rgba(16, 185, 129, 0.2)";
      robotStateBadge.style.color = "#34d399";
      robotTelemetryLog.textContent = `[STM32_ISR] ToF=${distCm}cm (SAFE) | AI_ERR=${steerPx}px | DIFF_DRIVE(L=${left}%, R=${right}%)`;
    }
  }

  if (robotDistSlider && robotSteerSlider) {
    robotDistSlider.addEventListener("input", updateRobotSimulator);
    robotSteerSlider.addEventListener("input", updateRobotSimulator);
    updateRobotSimulator();
  }

  // --- SIMULATOR 03: 40kHz ULTRASONIC WATER TANK HYSTERESIS ---
  const waterLevelSlider = document.getElementById("waterLevelSlider");
  const waterLevelLabel = document.getElementById("waterLevelLabel");
  const waterPctKpi = document.getElementById("waterPctKpi");
  const waterEchoKpi = document.getElementById("waterEchoKpi");
  const waterRelayKpi = document.getElementById("waterRelayKpi");
  const waterLcdKpi = document.getElementById("waterLcdKpi");
  const waterPumpBadge = document.getElementById("waterPumpBadge");
  const waterVisualBar = document.getElementById("waterVisualBar");

  function updateWaterSimulator() {
    if (!waterLevelSlider) return;
    const pct = parseInt(waterLevelSlider.value, 10);
    const tankHeightCm = 200.0;
    const distFromSensorCm = Math.round(((100 - pct) / 100.0) * tankHeightCm);
    const echoUs = Math.round((distFromSensorCm * 2.0) / 0.0343);

    // Schmitt Trigger Dual-Threshold Hysteresis (Low <= 20% turns ON, High >= 90% turns OFF)
    if (!waterPumpState && pct <= 20) {
      waterPumpState = true;
    } else if (waterPumpState && pct >= 90) {
      waterPumpState = false;
    }

    waterLevelLabel.textContent = `${pct}% (${distFromSensorCm} cm from top sensor)`;
    waterPctKpi.textContent = `${pct}%`;
    waterEchoKpi.textContent = `${echoUs} µs`;
    waterVisualBar.style.width = `${pct}%`;

    const paddedPct = String(pct).padStart(3, "0");
    if (waterPumpState) {
      waterRelayKpi.textContent = "CLOSED (ON)";
      waterRelayKpi.style.color = "#a3e635";
      waterLcdKpi.textContent = `LVL:${paddedPct}% P:ON `;
      waterPumpBadge.textContent = "PUMP ACTIVE (FILLING)";
      waterPumpBadge.style.background = "rgba(163, 230, 53, 0.22)";
      waterPumpBadge.style.color = "#a3e635";
    } else {
      waterRelayKpi.textContent = "OPEN (OFF)";
      waterRelayKpi.style.color = "#38bdf8";
      waterLcdKpi.textContent = `LVL:${paddedPct}% P:OFF`;
      waterPumpBadge.textContent = "PUMP OFF (HYSTERESIS HOLD)";
      waterPumpBadge.style.background = "rgba(56, 189, 248, 0.2)";
      waterPumpBadge.style.color = "#38bdf8";
    }
  }

  if (waterLevelSlider) {
    waterLevelSlider.addEventListener("input", updateWaterSimulator);
    updateWaterSimulator();
  }

  // -------------------------------------------------------------------------
  // 4. PROJECT CATEGORY FILTERING & TECH DOCK / SERVICE JUMP LINKS
  // -------------------------------------------------------------------------
  const filterButtons = document.querySelectorAll(".filter-pill-btn");
  const projectCards = document.querySelectorAll(".project-showcase-card");

  function applyProjectFilter(category) {
    filterButtons.forEach((btn) => {
      btn.classList.toggle("active", btn.getAttribute("data-filter") === category);
    });

    projectCards.forEach((card) => {
      const cardCat = card.getAttribute("data-category");
      if (category === "all" || cardCat === category) {
        card.style.display = "flex";
      } else {
        card.style.display = "none";
      }
    });
  }

  filterButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      applyProjectFilter(btn.getAttribute("data-filter") || "all");
    });
  });

  document.querySelectorAll("[data-filter-jump]").forEach((tile) => {
    tile.addEventListener("click", () => {
      const cat = tile.getAttribute("data-filter-jump") || "all";
      applyProjectFilter(cat);
      const projSection = document.getElementById("projects");
      if (projSection) {
        projSection.scrollIntoView({ behavior: "smooth" });
      }
    });
  });

  // Process Step Cards interactive highlight
  const processCards = document.querySelectorAll(".process-step-card");
  processCards.forEach((card) => {
    card.addEventListener("click", () => {
      processCards.forEach((c) => c.classList.remove("active"));
      card.classList.add("active");
    });
  });

  // -------------------------------------------------------------------------
  // 5. PROJECT CODE & ARCHITECTURE MODAL INSPECTOR
  // -------------------------------------------------------------------------
  const projectModal = document.getElementById("projectModal");
  const modalCloseBtn = document.getElementById("modalCloseBtn");
  const modalLangPill = document.getElementById("modalLangPill");
  const modalTitle = document.getElementById("modalTitle");
  const modalSummary = document.getElementById("modalSummary");
  const modalArchList = document.getElementById("modalArchList");
  const modalCodeFilename = document.getElementById("modalCodeFilename");
  const modalCodeBlock = document.getElementById("modalCodeBlock");
  const modalRepoLink = document.getElementById("modalRepoLink");

  document.querySelectorAll("[data-open-modal]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const idx = parseInt(btn.getAttribute("data-open-modal") || "0", 10);
      const proj = (PORTFOLIO_DATA.projects || [])[idx];
      if (!proj || !projectModal) return;

      modalLangPill.textContent = `${proj.primary_lang} · ${currentLang === "fr" ? proj.status_fr : proj.status_en}`;
      modalTitle.textContent = currentLang === "fr" ? proj.title_fr : proj.title_en;
      modalSummary.textContent = currentLang === "fr" ? proj.summary_fr : proj.summary_en;
      modalCodeFilename.textContent = proj.code_Filename;
      modalCodeBlock.textContent = proj.code_snippet;
      modalRepoLink.href = proj.repo_url;

      modalArchList.innerHTML = "";
      const archItems = currentLang === "fr" ? proj.architecture_fr : proj.architecture_en;
      (archItems || []).forEach((item) => {
        const li = document.createElement("li");
        li.textContent = item;
        li.style.marginBottom = "6px";
        modalArchList.appendChild(li);
      });

      projectModal.classList.add("open");
    });
  });

  if (modalCloseBtn && projectModal) {
    modalCloseBtn.addEventListener("click", () => projectModal.classList.remove("open"));
    projectModal.addEventListener("click", (e) => {
      if (e.target === projectModal) projectModal.classList.remove("open");
    });
  }

  // -------------------------------------------------------------------------
  // 6. THEME SWITCHER (Midnight Neon <-> Aarav Frosted Periwinkle Glass) & EN/FR
  // -------------------------------------------------------------------------
  const themeToggleBtn = document.getElementById("themeToggleBtn");
  const themeIcon = document.getElementById("themeIcon");
  const themeLabel = document.getElementById("themeLabel");

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener("click", () => {
      const htmlEl = document.documentElement;
      const current = htmlEl.getAttribute("data-theme") || "dark";
      const next = current === "dark" ? "light" : "dark";
      htmlEl.setAttribute("data-theme", next);

      if (next === "light") {
        themeIcon.textContent = "🌙";
        themeLabel.textContent = "Midnight Neon";
      } else {
        themeIcon.textContent = "☀️";
        themeLabel.textContent = "Glass Light";
      }
    });
  }

  const langToggleBtn = document.getElementById("langToggleBtn");
  const langLabel = document.getElementById("langLabel");

  if (langToggleBtn) {
    langToggleBtn.addEventListener("click", () => {
      currentLang = currentLang === "en" ? "fr" : "en";
      langLabel.textContent = currentLang.toUpperCase();

      document.querySelectorAll("[data-i18n-en]").forEach((el) => {
        const text = el.getAttribute(currentLang === "fr" ? "data-i18n-fr" : "data-i18n-en");
        if (text) el.textContent = text;
      });
    });
  }
})();
