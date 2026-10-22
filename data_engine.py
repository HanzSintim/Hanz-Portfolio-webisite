"""
Hanz Ofosuhene-Sintim — Portfolio Data & Analytics Engine (Python 3)
====================================================================
Provides structured domain models, algorithmic telemetry calculations,
bilingual (EN/FR) content dictionaries, and a Python reference implementation
of the E.Leclerc Self-Checkout greedy change-making & TVA calculation engine.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import math
from typing import Dict, List, Optional


@dataclass(frozen=True)
class SkillPetal:
    """Represents a petal/node in the radial & flower infographic diagrams."""
    code: str
    title_en: str
    title_fr: str
    score: int
    accent: str
    metrics_en: str
    metrics_fr: str
    tools: List[str]


@dataclass(frozen=True)
class EngineeringProject:
    """Represents a complete engineering system in the workstation showcase."""
    index: str
    slug: str
    title_en: str
    title_fr: str
    category: str
    primary_lang: str
    status_en: str
    status_fr: str
    repo_url: str
    summary_en: str
    summary_fr: str
    architecture_en: List[str]
    architecture_fr: List[str]
    tech_stack: List[str]
    code_Filename: str
    code_snippet: str
    metrics: Dict[str, str]


@dataclass(frozen=True)
class LeadershipRole:
    """Executive leadership and governance milestone."""
    badge: str
    role_en: str
    role_fr: str
    organization: str
    location: str
    period: str
    highlights_en: List[str]
    highlights_fr: List[str]


@dataclass(frozen=True)
class AcademicNode:
    """Academic corridor node linking Ghana (PRESEC / KNUST) and France (JUNIA Lille)."""
    code: str
    institution: str
    short_name: str
    degree_en: str
    degree_fr: str
    city: str
    country: str
    coordinates: str
    period: str
    focus_en: str
    focus_fr: str


def compute_euro_checkout_simulation(amount_eur: float, cash_tendered_eur: float) -> Dict[str, object]:
    """
    Python twin of the E.Leclerc Self-Checkout C++ engine:
    - Converts floating-point Euros into exact integer centimes via round()
    - Computes French 20% TVA breakdown (HT + TVA == TTC)
    - Executes the Greedy Change-Making Algorithm over the 12 official Euro denominations
    """
    total_cents = int(round(amount_eur * 100))
    tendered_cents = int(round(cash_tendered_eur * 100))
    total_ht_cents = int(round(total_cents / 1.20))
    tva_cents = total_cents - total_ht_cents

    denominations = [
        (5000, "50.00 € Bill"),
        (2000, "20.00 € Bill"),
        (1000, "10.00 € Bill"),
        (500, "5.00 € Bill"),
        (200, "2.00 € Coin"),
        (100, "1.00 € Coin"),
        (50, "0.50 € Coin"),
        (20, "0.20 € Coin"),
        (10, "0.10 € Coin"),
        (5, "0.05 € Coin"),
        (2, "0.02 € Coin"),
        (1, "0.01 € Coin"),
    ]

    change_cents = max(0, tendered_cents - total_cents)
    remaining = change_cents
    dispensed: List[Dict[str, object]] = []

    for denom_cents, label in denominations:
        count, remaining = divmod(remaining, denom_cents)
        if count > 0:
            dispensed.append({
                "denomination": label,
                "cents": denom_cents,
                "count": count,
                "subtotal_eur": f"{(count * denom_cents) / 100:.2f} €",
            })

    return {
        "total_ttc_eur": round(total_cents / 100.0, 2),
        "total_ht_eur": round(total_ht_cents / 100.0, 2),
        "tva_20_eur": round(tva_cents / 100.0, 2),
        "cash_tendered_eur": round(tendered_cents / 100.0, 2),
        "change_returned_eur": round(change_cents / 100.0, 2),
        "change_cents": change_cents,
        "nfc_eligible": total_cents <= 5000,
        "dispensed_denominations": dispensed,
    }


def get_skill_petals() -> List[SkillPetal]:
    """Returns the 6 core engineering petals for the LEAFE-inspired flower & radial infographics."""
    return [
        SkillPetal(
            code="01",
            title_en="Python 3 & Backend Architecture",
            title_fr="Python 3 & Architecture Backend",
            score=95,
            accent="#10b981",
            metrics_en="Flask WSGI · REST APIs · Data Modeling · Automation & CLI Tooling",
            metrics_fr="Flask WSGI · APIs REST · Modélisation de Données · Automatisation",
            tools=["Python 3.12", "Flask", "Jinja2", "Dataclasses", "REST / JSON", "Pytest"],
        ),
        SkillPetal(
            code="02",
            title_en="C / C++17 & POS Systems",
            title_fr="C / C++17 & Systèmes TPV",
            score=94,
            accent="#34d399",
            metrics_en="Polymorphic OOP · RTTI dynamic_cast · Greedy Algorithms · STL",
            metrics_fr="POO Polymorphe · RTTI dynamic_cast · Algorithmes Gloutons · STL",
            tools=["C++17", "C99", "GCC / G++", "GDB", "WSL2 Linux", "Make / CMake"],
        ),
        SkillPetal(
            code="03",
            title_en="Microelectronics & Embedded MCU",
            title_fr="Microélectronique & MCU Embarqués",
            score=91,
            accent="#059669",
            metrics_en="STM32 & ESP32 Dual-MCU · Cadence IC · Ultrasonic ToF · PWM Control",
            metrics_fr="Double-MCU STM32 & ESP32 · Cadence IC · Ultrasons ToF · Commande PWM",
            tools=["STM32", "ESP32", "MSP430", "Arduino AVR", "Cadence Virtuoso", "UART / I2C / SPI"],
        ),
        SkillPetal(
            code="04",
            title_en="Relational Data & 3NF Schemas",
            title_fr="Données Relationnelles & Schémas 3NF",
            score=92,
            accent="#6ee7b7",
            metrics_en="Conceptual ER Modeling · M:N Junction Resolution · 3NF Normalization",
            metrics_fr="Modélisation ER Conceptuelle · Résolution M:N · Normalisation 3NF",
            tools=["SQL", "3NF Schema Design", "ER Diagrams", "PostgreSQL / SQLite", "JSON Stores"],
        ),
        SkillPetal(
            code="05",
            title_en="PCB Hardware & Sensor Fusion",
            title_fr="Conception PCB & Fusion Capteurs",
            score=89,
            accent="#14b8a6",
            metrics_en="KiCad Schematic Capture · FeCl3 Etching · Hysteresis Relay Loops",
            metrics_fr="Saisie Schématique KiCad · Gravure FeCl3 · Boucles Relais à Hystérésis",
            tools=["KiCad PCB", "FeCl3 Etching", "H-Bridge PWM", "40kHz Ultrasonic", "16x2 LCD"],
        ),
        SkillPetal(
            code="06",
            title_en="Executive & Technical Leadership",
            title_fr="Leadership Exécutif & Technique",
            score=96,
            accent="#a7f3d0",
            metrics_en="ACES President (KNUST) · GHAFRA Nord Lead (Lille) · Cross-Functional R&D",
            metrics_fr="Président ACES (KNUST) · Responsable GHAFRA Nord (Lille) · R&D",
            tools=["Engineering Governance", "Agile R&D", "Bilingual EN/FR", "Supply Chain Ops"],
        ),
    ]


def get_engineering_projects() -> List[EngineeringProject]:
    """Returns the curated portfolio of Hanz Ofosuhene-Sintim's engineering projects."""
    return [
        EngineeringProject(
            index="01",
            slug="python-telemetry-portfolio-engine",
            title_en="Python 3 & Flask Telemetry Portfolio Engine",
            title_fr="Moteur de Portfolio & Télémétrie en Python 3 / Flask",
            category="python",
            primary_lang="Python 3.12 · Flask",
            status_en="Production · Live API & Static Compiler",
            status_fr="En Production · API Live & Compilateur Statique",
            repo_url="https://github.com/HanzSintim/Hanz-Portfolio-webisite",
            summary_en=(
                "Full-stack Python application and static site generator powering this portfolio. "
                "Combines typed Python dataclasses, algorithmic telemetry endpoints, bilingual (EN/FR) "
                "content negotiation, and a Python financial/POS simulation engine."
            ),
            summary_fr=(
                "Application Python full-stack et générateur statique propulsant ce portfolio. "
                "Combine dataclasses typées, points de terminaison REST de télémétrie, négociation "
                "bilingue (FR/EN) et simulateur algorithmique de caisse en Python."
            ),
            architecture_en=[
                "Typed Python 3 domain layer (SkillPetal, EngineeringProject, AcademicNode dataclasses)",
                "Flask WSGI REST API endpoints (/api/v1/profile, /api/v1/projects, /api/v1/pos-simulator)",
                "Hybrid Static Freezer (--build-static) compiling Jinja2 templates for zero-latency GitHub Pages hosting",
                "Algorithmic Euro centime & TVA 20% verification engine with divmod() greedy change optimization",
            ],
            architecture_fr=[
                "Couche domaine Python 3 typée (dataclasses SkillPetal, EngineeringProject, AcademicNode)",
                "Points de terminaison REST Flask WSGI (/api/v1/profile, /api/v1/projects, /api/v1/pos-simulator)",
                "Compilateur statique hybride (--build-static) générant le build GitHub Pages depuis Jinja2",
                "Moteur algorithmique Euro en centimes & TVA 20% avec rendu de monnaie glouton via divmod()",
            ],
            tech_stack=["Python 3.12", "Flask", "Jinja2", "Dataclasses", "REST JSON API", "HTML5 / CSS3 / ES6"],
            code_Filename="data_engine.py",
            code_snippet="""def compute_euro_checkout_simulation(amount_eur: float, cash_tendered_eur: float) -> dict:
    \"\"\"Exact integer-centime French TVA (20%) & Greedy Euro Change Dispenser in Python.\"\"\"
    total_cents = int(round(amount_eur * 100))
    tendered_cents = int(round(cash_tendered_eur * 100))
    total_ht_cents = int(round(total_cents / 1.20))
    tva_cents = total_cents - total_ht_cents

    denominations = [5000, 2000, 1000, 500, 200, 100, 50, 20, 10, 5, 2, 1]
    remaining = max(0, tendered_cents - total_cents)
    dispensed = {}
    for d in denominations:
        count, remaining = divmod(remaining, d)
        if count:
            dispensed[f"{d / 100:.2f} €"] = count
    return {"ttc": total_cents / 100, "ht": total_ht_cents / 100, "tva": tva_cents / 100, "change": dispensed}""",
            metrics={"Language": "Python 3.12", "API Routes": "5 REST Endpoints", "Precision": "100% Integer Centimes"},
        ),
        EngineeringProject(
            index="02",
            slug="leclerc-self-checkout-pos",
            title_en="E.Leclerc Self-Checkout Terminal (Caisse Libre-Service)",
            title_fr="Terminal Caisse Libre-Service E.Leclerc (C++17 POS)",
            category="cpp",
            primary_lang="C++17 · OOP & RTTI",
            status_en="Completed · 0 Warnings (-Wall -Wextra)",
            status_fr="Terminé · 0 Avertissement (-Wall -Wextra)",
            repo_url="https://github.com/HanzSintim/LECLERC-Self-Checkout",
            summary_en=(
                "French hypermarket self-checkout simulator engineered in C++17. Implements runtime "
                "polymorphism (virtual destructor + dynamic_cast) for load-cell bagging scale verification, "
                "a 12-denomination Euro cash validator with greedy change dispensing, and French PSD2 NFC/EMV card rules."
            ),
            summary_fr=(
                "Simulateur de caisse libre-service d'hypermarché français conçu en C++17. Implémente "
                "le polymorphisme d'exécution (dynamic_cast) pour la balance d'ensachage, un monnayeur Euro "
                "à 12 coupures avec algorithme glouton, et les règles bancaires NFC <= 50€ / Puce EMV + PIN."
            ),
            architecture_en=[
                "Polymorphic Product hierarchy (Physicalproducts & Digitalproduct) with RTTI dynamic_cast",
                "Load-cell bagging scale verification accumulating physical mass (kg) while bypassing digital licenses",
                "Hybrid Payment Terminal supporting Cash (Espèces), Card (CB/NFC <= 50€), and Split Payment (Paiement Mixte)",
                "Greedy Change-Making Algorithm over 12 Euro denominations (50€ down to 0.01€) + TVA 20% thermal receipt",
            ],
            architecture_fr=[
                "Hiérarchie polymorphe Product (Physicalproducts & Digitalproduct) avec RTTI dynamic_cast",
                "Balance de sécurité vérifiant la masse physique (kg) avec contournement pour licences numériques",
                "Terminal de paiement hybride : Espèces, Carte Bancaire (NFC <= 50€ ou EMV+PIN) et Paiement Mixte",
                "Algorithme glouton de rendu de monnaie sur 12 coupures Euro (50€ à 0.01€) + Ticket TVA 20%",
            ],
            tech_stack=["C++17", "Polymorphism & RTTI", "Greedy Algorithms", "STL Vectors", "IEEE-754 Mitigation", "GCC"],
            code_Filename="L'ECLERC.cpp",
            code_snippet="""// Runtime polymorphism via dynamic_cast on the E.Leclerc load-cell bagging scale
Physicalproducts *physPtr = dynamic_cast<Physicalproducts *>(p);
if (physPtr != nullptr) {
    float itemTotalWeightKg = physPtr->getweight() * ci.getquantity();
    totalBaggingWeightKg += itemTotalWeightKg;
}
// Greedy Change-Making Algorithm over the 12 official Euro denominations in centimes
const int euroDenomCents[12] = {5000, 2000, 1000, 500, 200, 100, 50, 20, 10, 5, 2, 1};
for (int d = 0; d < 12; ++d) {
    int count = remainderToDispense / euroDenomCents[d];
    remainderToDispense = remainderToDispense % euroDenomCents[d];
}""",
            metrics={"Language": "C++17", "Denominations": "12 Euro Bills/Coins", "NFC Ceiling": "50.00 € (PSD2)"},
        ),
        EngineeringProject(
            index="03",
            slug="autonomous-street-cleaning-robot",
            title_en="Autonomous Street-Cleaning Robot (Dual-MCU Architecture)",
            title_fr="Robot Autonome de Nettoyage Urbain (Architecture Double-MCU)",
            category="embedded",
            primary_lang="Embedded C · STM32 & ESP32",
            status_en="Active R&D · JUNIA ISEN Lille M1 Team",
            status_fr="R&D Active · Équipe M1 JUNIA ISEN Lille",
            repo_url="https://github.com/HanzSintim",
            summary_en=(
                "7-member M1 engineering R&D system at JUNIA Lille combining deterministic STM32 motor/actuator "
                "control with ESP32 wireless telemetry, UART AI vision debris detection, and an ultrasonic "
                "time-of-flight obstacle avoidance curtain."
            ),
            summary_fr=(
                "Projet R&D M1 à 7 ingénieurs chez JUNIA Lille combinant commande moteur temps-réel sur STM32, "
                "télémétrie sans fil sur ESP32, caméra IA de détection de déchets sur UART et rideau de sécurité "
                "ultrasonique à temps de vol (ToF)."
            ),
            architecture_en=[
                "Dual-MCU partitioning: STM32 handles hard real-time PWM H-bridge traction & brush actuation",
                "ESP32 co-processor manages Wi-Fi/BLE telemetry uplink and operator diagnostics dashboard",
                "External AI vision camera streams bounding-box coordinates over high-speed UART",
                "Multi-sensor ultrasonic ToF array enforces deterministic emergency braking",
            ],
            architecture_fr=[
                "Partitionnement Double-MCU : STM32 dédié au contrôle PWM temps-réel des moteurs et balais",
                "Co-processeur ESP32 gérant la télémétrie Wi-Fi/BLE et le tableau de bord opérateur",
                "Caméra IA externe transmettant les coordonnées de détection via bus UART haute vitesse",
                "Réseau de capteurs ultrasoniques ToF assurant le freinage d'urgence déterministe",
            ],
            tech_stack=["Embedded C", "STM32", "ESP32", "UART AI Vision", "PWM H-Bridge", "Ultrasonic ToF"],
            code_Filename="robot_control_loop.c",
            code_snippet="""// Deterministic safety check & UART AI vision debris alignment loop (STM32)
void Robot_ControlStep(const UltrasonicArray_t *tof, const VisionFrame_t *ai) {
    if (tof->front_distance_cm < SAFETY_STOP_THRESHOLD_CM) {
        PWM_SetDutyCycle(MOTOR_LEFT | MOTOR_RIGHT, 0); // Hard real-time emergency brake
        UART_SendTelemetry(ESP32_PORT, STATUS_OBSTACLE_HALT);
        return;
    }
    int16_t steering_err = ai->debris_centroid_x - FRAME_CENTER_X;
    PWM_ApplyDifferentialDrive(BASE_SPEED_PWM, KP_STEER * steering_err);
}""",
            metrics={"Architecture": "STM32 + ESP32", "Team Size": "7 M1 Engineers", "Lab": "JUNIA Lille, France"},
        ),
        EngineeringProject(
            index="04",
            slug="smart-logistics-3nf-database",
            title_en="Smart Logistics & Delivery 3NF Relational Data Model",
            title_fr="Modèle Relationnel 3NF de Logistique & Livraison Intelligente",
            category="data",
            primary_lang="SQL · Python · 3NF ER Modeling",
            status_en="Completed · Normalized to 3NF",
            status_fr="Terminé · Normalisé en 3NF",
            repo_url="https://github.com/HanzSintim/CoE_group22",
            summary_en=(
                "End-to-end relational database architecture for multi-hub parcel routing, fleet dispatch, "
                "and customer tracking. Resolves M:N cardinalities via composite-key associative junction "
                "tables and eliminates transitive dependencies through strict Third Normal Form (3NF)."
            ),
            summary_fr=(
                "Architecture de base de données relationnelle pour le routage multi-entrepôts et le suivi "
                "de flotte. Résout les cardinalités M:N par tables de jonction associatives et élimine les "
                "dépendances transitives via une normalisation stricte en 3NF."
            ),
            architecture_en=[
                "Conceptual Entity-Relationship (ER) schema covering Shipments, Hubs, Couriers, Vehicles &SLAs",
                "Resolution of M:N routing legs via Shipment_Route_Hop composite primary/foreign keys",
                "Full 1NF -> 2NF -> 3NF normalization eliminating partial and transitive functional dependencies",
                "Python verification scripts & indexed SQL analytical queries for hub bottleneck telemetry",
            ],
            architecture_fr=[
                "Schéma Entité-Association (EA) couvrant Colis, Entrepôts, Livreurs, Véhicules et SLA",
                "Résolution des relations M:N via tables associatives à clés primaires composites",
                "Normalisation 1NF -> 2NF -> 3NF éliminant toute redondance et dépendance transitive",
                "Scripts Python de validation et requêtes SQL indexées pour l'analyse des flux logistiques",
            ],
            tech_stack=["SQL", "3NF Normalization", "ER Modeling", "Python Data Validation", "Composite Keys"],
            code_Filename="schema_3nf.sql",
            code_snippet="""CREATE TABLE Shipment_Route_Hop (
    shipment_id      INT NOT NULL REFERENCES Shipment(shipment_id),
    hop_sequence     SMALLINT NOT NULL CHECK (hop_sequence >= 1),
    origin_hub_id    INT NOT NULL REFERENCES Logistics_Hub(hub_id),
    dest_hub_id      INT NOT NULL REFERENCES Logistics_Hub(hub_id),
    courier_id       INT NOT NULL REFERENCES Courier(courier_id),
    dispatched_at    TIMESTAMP NOT NULL,
    arrived_at       TIMESTAMP NULL,
    PRIMARY KEY (shipment_id, hop_sequence) -- 3NF Composite Associative Key
);""",
            metrics={"Normal Form": "Strict 3NF", "Cardinalities": "M:N Resolved", "Integrity": "Referential FK"},
        ),
        EngineeringProject(
            index="05",
            slug="automatic-water-tank-control",
            title_en="Automatic Water Tank Ultrasonic Monitoring & Relay Control",
            title_fr="Contrôle Automatique de Réservoir par Ultrasons & Hystérésis",
            category="embedded",
            primary_lang="Embedded C/C++ · AVR MCU",
            status_en="Completed · Hardware Validated",
            status_fr="Terminé · Validé sur Matériel",
            repo_url="https://github.com/HanzSintim",
            summary_en=(
                "Closed-loop liquid level controller utilizing non-contact 40 kHz ultrasonic time-of-flight "
                "ranging (d = v * t / 2), dual-threshold Schmitt hysteresis to prevent relay contact chatter, "
                "and real-time 16x2 LCD operator telemetry."
            ),
            summary_fr=(
                "Système d'asservissement de niveau d'eau sans contact par ultrasons 40 kHz (d = v * t / 2), "
                "commande de pompe à hystérésis double-seuil éliminant le broutage du relais, et affichage "
                "temps-réel sur écran LCD 16x2."
            ),
            architecture_en=[
                "40 kHz acoustic pulse-echo Time-of-Flight calculation with speed-of-sound scaling",
                "Dual-threshold hysteresis state machine (LOW_TRIGGER = 20%, HIGH_CUTOFF = 90%)",
                "Opto-isolated relay actuation protecting the microcontroller from inductive pump flyback",
                "Live 16x2 parallel LCD interface displaying fill percentage, distance (cm), and pump state",
            ],
            architecture_fr=[
                "Calcul précis de distance par temps de vol acoustique 40 kHz (d = v * t / 2)",
                "Machine à états à hystérésis double-seuil (Seuil Bas = 20%, Arrêt Haut = 90%)",
                "Actionnement relais opto-isolé protégeant le MCU contre les surtensions inductives",
                "Interface opérateur LCD 16x2 affichant le pourcentage de remplissage et l'état pompe",
            ],
            tech_stack=["Embedded C++", "Arduino AVR", "40kHz Ultrasonic ToF", "Hysteresis Control", "KiCad PCB"],
            code_Filename="water_tank_hysteresis.ino",
            code_snippet="""float measureWaterLevelPercent(long echoDurationUs, float tankHeightCm) {
    float distanceCm = (echoDurationUs * 0.0343f) / 2.0f; // Acoustic Time-of-Flight
    float fillCm = max(0.0f, tankHeightCm - distanceCm);
    return constrain((fillCm / tankHeightCm) * 100.0f, 0.0f, 100.0f);
}
// Dual-threshold hysteresis prevents rapid relay oscillation at boundary levels
if (!pumpActive && levelPct <= LOW_LEVEL_THRESHOLD_PCT)  pumpActive = true;
if (pumpActive  && levelPct >= HIGH_LEVEL_CUTOFF_PCT)    pumpActive = false;""",
            metrics={"Sensor": "40 kHz Ultrasonic", "Control Law": "Dual Hysteresis", "Display": "16x2 HD44780 LCD"},
        ),
        EngineeringProject(
            index="06",
            slug="agricconnect-data-ecosystem",
            title_en="AgricConnect & Relational Web Data Systems",
            title_fr="AgricConnect & Systèmes de Données Web Relationnels",
            category="python",
            primary_lang="Python · JS · Full-Stack Data",
            status_en="Collaborative Ecosystem · GitHub",
            status_fr="Écosystème Collaboratif · GitHub",
            repo_url="https://github.com/AgriKorn/AgricConnect",
            summary_en=(
                "Freshness-aware agricultural supply-chain marketplace connecting farmers, buyers, and "
                "logistics drivers, paired with structured web data-table ingestion pipelines."
            ),
            summary_fr=(
                "Plateforme logistique agricole sensible à la fraîcheur connectant producteurs, acheteurs "
                "et transporteurs, couplée à des tables de données dynamiques."
            ),
            architecture_en=[
                "Multi-actor marketplace matching perishable farm inventory with cold-chain transport routes",
                "Structured form-to-table validation and DOM state synchronization (Data-Table repo)",
                "Collaborative Git workflow across multi-developer engineering teams",
            ],
            architecture_fr=[
                "Mise en relation multi-acteurs entre stocks agricoles périssables et transporteurs",
                "Validation de formulaires structurés et synchronisation de tables de données (Data-Table)",
                "Flux de travail Git collaboratif au sein d'équipes d'ingénierie distribuées",
            ],
            tech_stack=["Python", "JavaScript ES6", "HTML5 / CSS3", "Supply-Chain Logistics", "Git"],
            code_Filename="freshness_scorer.py",
            code_snippet="""def compute_freshness_priority(harvest_hours_ago: float, transit_hours: float, temp_c: float) -> float:
    \"\"\"Ranks farm lots by remaining shelf-life urgency for dispatch prioritization.\"\"\"
    thermal_factor = math.exp(0.045 * max(0.0, temp_c - 4.0))
    effective_age = (harvest_hours_ago + transit_hours) * thermal_factor
    return round(max(0.0, 100.0 - effective_age * 1.25), 2)""",
            metrics={"Ecosystem": "AgriKorn / HanzSintim", "Focus": "Perishable Logistics", "Stack": "Python & Web"},
        ),
    ]


def get_leadership_roles() -> List[LeadershipRole]:
    """Returns executive leadership roles held across Ghana and France."""
    return [
        LeadershipRole(
            badge="PRESIDENT",
            role_en="Department President — ACES KNUST",
            role_fr="Président de Département — ACES KNUST",
            organization="Association of Computer Engineering Students (KNUST)",
            location="Kumasi, Ghana",
            period="2024 – 2025",
            highlights_en=[
                "Chief executive representative for 800+ Computer Engineering undergraduates at KNUST.",
                "Directed ACES Tech Week, Codefest hackathons, academic mentorship, and industry partnerships.",
                "Oversaw departmental software repositories (ACES Website, CareerHub, Techware automation).",
            ],
            highlights_fr=[
                "Président exécutif représentant plus de 800 étudiants en Génie Informatique à KNUST.",
                "Direction de l'ACES Tech Week, du hackathon Codefest, du mentorat académique et des partenariats.",
                "Supervision des dépôts logiciels du département (Site ACES, CareerHub, automatisation Techware).",
            ],
        ),
        LeadershipRole(
            badge="STRATEGY LEAD",
            role_en="Strategic Planning & Organizing Lead",
            role_fr="Responsable Planification Stratégique & Organisation",
            organization="GHAFRA Nord (Ghanaian Community in Northern France)",
            location="Lille, France",
            period="2025 – Present",
            highlights_en=[
                "Architects operational roadmaps, student integration programs, and institutional events across Lille & Hauts-de-France.",
                "Coordinates cross-cultural academic and professional networking between Ghanaian scholars and French institutions.",
            ],
            highlights_fr=[
                "Conception des feuilles de route opérationnelles, programmes d'accueil étudiant et événements à Lille.",
                "Coordination des réseaux académiques et professionnels franco-ghanéens dans les Hauts-de-France.",
            ],
        ),
        LeadershipRole(
            badge="CO-LEAD OPS",
            role_en="Co-Lead, Commercial & Hardware Operations",
            role_fr="Co-Responsable Opérations Commerciales & Matérielles",
            organization="H & D'S HUB",
            location="Ghana",
            period="2023 – Present",
            highlights_en=[
                "Managed international hardware procurement, pre-shipment device diagnostics, and unit-economics pricing.",
                "Streamlined inventory tracking and last-mile customer fulfillment workflows.",
            ],
            highlights_fr=[
                "Gestion des approvisionnements matériels, diagnostics techniques avant expédition et tarification.",
                "Optimisation du suivi des stocks et de la chaîne de distribution client.",
            ],
        ),
    ]


def get_academic_corridor() -> List[AcademicNode]:
    """Returns the 3-stage academic corridor from Accra & Kumasi (Ghana) to Lille (France)."""
    return [
        AcademicNode(
            code="FR-LILLE",
            institution="JUNIA — Grande École d'Ingénieurs (ISEN Lille)",
            short_name="JUNIA ISEN Lille",
            degree_en="M1 Microelectronics, Nanotechnology & Embedded Systems",
            degree_fr="M1 Microélectronique, Nanotechnologies & Systèmes Embarqués",
            city="Lille",
            country="France",
            coordinates="50.6292° N, 3.0573° E",
            period="2025 – Present",
            focus_en="IC Design (Cadence), STM32/ESP32 Embedded Systems, Smart Sensors, Autonomous Robotics & Nanotech.",
            focus_fr="Conception IC (Cadence), Systèmes Embarqués STM32/ESP32, Capteurs Intelligents, Robotique & Nanotech.",
        ),
        AcademicNode(
            code="GH-KUMASI",
            institution="Kwame Nkrumah University of Science and Technology (KNUST)",
            short_name="KNUST Kumasi",
            degree_en="BSc Computer Engineering (ACES President)",
            degree_fr="BSc Génie Informatique (Président ACES)",
            city="Kumasi",
            country="Ghana",
            coordinates="6.6745° N, 1.5716° W",
            period="2022 – 2025",
            focus_en="Computer Architecture, C/C++ OOP, Python Software Engineering, 3NF Database Systems & Embedded Labs.",
            focus_fr="Architecture des Ordinateurs, POO C/C++, Ingénierie Python, Bases de Données 3NF & Labs Embarqués.",
        ),
        AcademicNode(
            code="GH-ACCRA",
            institution="Presbyterian Boys' Secondary School (PRESEC-Legon)",
            short_name="PRESEC-Legon (Odadeɛ)",
            degree_en="General Science (Physics, Chemistry, Elective Mathematics)",
            degree_fr="Sciences Générales (Physique, Chimie, Mathématiques Approfondies)",
            city="Accra (Legon)",
            country="Ghana",
            coordinates="5.6506° N, 0.1862° W",
            period="Graduated 2022",
            focus_en="Rigorous analytical foundation in physical sciences, calculus, and competitive STEM problem-solving.",
            focus_fr="Socle analytique rigoureux en sciences physiques, calcul différentiel et résolution de problèmes STEM.",
        ),
    ]


def build_full_portfolio_payload() -> Dict[str, object]:
    """Assembles the complete JSON-serializable state for both Flask and the Static Generator."""
    petals = [asdict(p) for p in get_skill_petals()]
    projects = [asdict(p) for p in get_engineering_projects()]
    leadership = [asdict(r) for r in get_leadership_roles()]
    corridor = [asdict(c) for c in get_academic_corridor()]

    avg_proficiency = round(sum(p["score"] for p in petals) / len(petals), 1)
    sample_pos = compute_euro_checkout_simulation(47.97, 60.00)

    return {
        "engineer": {
            "name": "Hanz Ofosuhene-Sintim",
            "handle": "@HanzSintim",
            "github_url": "https://github.com/HanzSintim",
            "email": "hanz.ofosuhene-sintim@student.junia.com",
            "secondary_email": "hanzsintim@gmail.com",
            "location": "Lille, France 🇫🇷  ⇄  Kumasi / Accra, Ghana 🇬🇭",
            "headline_en": "Python & C++ Systems Architect · Microelectronics & Embedded Engineer",
            "headline_fr": "Architecte Systèmes Python & C++ · Ingénieur Microélectronique & Embarqué",
            "tagline_en": (
                "Start your change for the future — bridging high-level Python intelligence & relational "
                "data systems with deterministic C++17 POS engines and STM32/ESP32 silicon hardware."
            ),
            "tagline_fr": (
                "Préparer l'ingénierie de demain — allier l'intelligence logicielle Python & les bases "
                "de données 3NF à la précision du C++17 et des systèmes embarqués STM32/ESP32."
            ),
        },
        "telemetry_summary": {
            "average_proficiency_pct": avg_proficiency,
            "production_systems_count": len(projects),
            "core_languages": ["Python 3", "C++17", "Embedded C", "SQL (3NF)", "JavaScript ES6"],
            "active_corridor": "Accra / Kumasi (GH) -> Lille (FR)",
            "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        },
        "skill_petals": petals,
        "projects": projects,
        "leadership": leadership,
        "corridor": corridor,
        "sample_pos_simulation": sample_pos,
    }


if __name__ == "__main__":
    import json
    payload = build_full_portfolio_payload()
    print(json.dumps(payload["telemetry_summary"], indent=2))
