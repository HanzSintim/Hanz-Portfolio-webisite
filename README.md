# Hanz Ofosuhene-Sintim — Python 3, C++17 & Embedded Systems Portfolio

[![Python 3.12 + Flask](https://img.shields.io/badge/PYTHON-3.12%20%C2%B7%20Flask%20WSGI-00E676?style=for-the-badge&logo=python&logoColor=04140d)](https://github.com/HanzSintim/Hanz-Portfolio-webisite)
[![C++17 & POS Systems](https://img.shields.io/badge/C%2B%2B17-Polymorphic%20POS%20%C2%B7%20RTTI-10B981?style=for-the-badge&logo=cplusplus&logoColor=white)](https://github.com/HanzSintim/LECLERC-Self-Checkout)
[![Embedded Silicon](https://img.shields.io/badge/SILICON-STM32%20%C2%B7%20ESP32%20%C2%B7%20Cadence-059669?style=for-the-badge)](https://github.com/HanzSintim)
[![Bilingual EN/FR](https://img.shields.io/badge/i18n-EN%20%E2%87%84%20FR%20Bilingual-34D399?style=for-the-badge)](https://hanzsintim.github.io/Hanz-Portfolio-webisite/)

> **"Start your change for the future"** — Bridging high-level **Python 3** intelligence & **3NF relational data systems** with deterministic **C++17 POS engines** and **STM32/ESP32 microelectronic hardware**.

---

## 1. Visual & Architectural Design System (*Alpine Mist + LEAFE Emerald-Obsidian*)

This portfolio is engineered with a dual-mode **Python 3 / Flask** backend (`app.py` + `data_engine.py`) and an interactive **Alpine Mist & LEAFE Emerald-Obsidian** frontend (`templates/index.html`, `static/css/emerald_obsidian.css`, `static/js/portfolio_engine.js`):

1. **Zone 1 — Misty Alpine-to-Obsidian Hero & 6-Node Capability Matrix:**
   - Layered SVG alpine ridges transitioning from alabaster mist into deep obsidian-emerald (`#060d0a`), accented by sweeping cubic Bézier trajectories and floating glassmorphic telemetry orbs (`PY 3.12`, `C++17`, `STM32`, `3NF`).
2. **Zone 2 — LEAFE Teardrop & Organic Portal Showcase:**
   - Asymmetric obsidian cards with diagonal emerald ribbons and teardrop-masked portals highlighting **Python 3 Backend/Data Architecture** and **C++17 / Embedded Silicon**.
3. **Zone 3 — Interactive 3D Laptop Workstation & Live Euro POS Simulator:**
   - Inspect all **6 production engineering systems** inside a 3D workstation monitor, complete with a live **Python/C++ E.Leclerc Greedy Change-Making & French TVA (20%) Calculator**.
4. **Zone 4 — Executive Dossier & 6-Petal Radial Flower Infographic:**
   - Highlights executive leadership (**ACES Department President @ KNUST**, **GHAFRA Nord Strategic Planning Lead @ Lille**, **H & D'S HUB Co-Lead**) alongside a quantitative **6-Petal Radial Flower Diagram** (`92.8%` average proficiency).
5. **Zone 5 — Global Engineering Corridor Map (`Ghana ⇄ France`):**
   - Custom dark-emerald vector map tracing the academic & R&D corridor from **PRESEC-Legon (Accra)** and **KNUST (Kumasi)** to **JUNIA ISEN (Lille, France)**.

---

## 2. Python 3 Architecture & REST API Endpoints

| File / Endpoint | Role & Specification |
| :--- | :--- |
| `data_engine.py` | Pure Python 3 domain & analytics module (`SkillPetal`, `EngineeringProject`, `LeadershipRole`, `AcademicNode` dataclasses + `compute_euro_checkout_simulation()`). |
| `app.py` | Flask WSGI application server + CLI static site compiler (`python app.py --build-static`). |
| `GET /` | Renders the interactive bilingual (`EN` / `FR`) portfolio page. |
| `GET /api/v1/profile` | Returns engineer identity, telemetry summary, and executive leadership roles in JSON. |
| `GET /api/v1/projects` | Returns all 6 engineering systems (supports `?category=python\|cpp\|embedded\|data`). |
| `GET /api/v1/infographics` | Returns the 6-petal radial proficiency vector and quantitative scores. |
| `GET /api/v1/corridor` | Returns the 3-node Ghana $\longleftrightarrow$ France academic corridor coordinates. |
| `GET /api/v1/pos-simulator` | Executes the Python integer-centime French TVA (20%) & 12-denomination Euro greedy change algorithm (`?amount=47.97&tendered=60.00`). |

---

## 3. Running Locally (Python Flask Server) or Compiling for GitHub Pages

```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch the live Python Flask server on http://127.0.0.1:5000
python app.py

# 3. Compile static HTML + JSON API snapshots for GitHub Pages hosting
python app.py --build-static
```
