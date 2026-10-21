"""Portfolio project seed data and JSON persistence helpers.

Provides the 5 accurate engineering projects with lifecycle statuses
("in_progress" vs "completed"), mineral domain tones, sequential system
block diagrams, milestone pipelines, engineering tradeoffs, and bilingual
teammate acknowledgments.
"""

import json
from pathlib import Path

PROJECTS_JSON_PATH = Path(__file__).resolve().parent / "projects.json"

SEED_PROJECTS = [
    {
        "slug": "autonomous-street-cleaning-robot",
        "status": "in_progress",
        "category": "Embedded & Hardware",
        "domain_tone": "copper",
        "title": "Autonomous Street-Cleaning Robot Prototype",
        "tech_stack": [
            "C/C++",
            "STM32 / ESP32",
            "External AI Camera Module",
            "Motor & Actuator Control",
            "Sensor Fusion",
        ],
        "block_diagram": [
            "External AI Camera & Obstacle Sensors",
            "STM32 / ESP32 MCU Control Unit",
            "PWM Motor & Sweeper Actuation",
            "Autonomous Street Navigation Loop",
        ],
        "milestones": [
            {
                "stage": "Stage 1: Architecture & Sensor Selection",
                "state": "done",
                "detail": (
                    "Defined dual-MCU partitioning (STM32 real-time motor loop "
                    "+ ESP32 telemetry), external AI camera interface, and "
                    "chassis power budget with the 7-member JUNIA Lille team."
                ),
            },
            {
                "stage": "Stage 2: MCU Control",
                "state": "active",
                "detail": (
                    "Implementing embedded C/C++ PWM motor drivers, rotary "
                    "sweeper actuation, and deterministic ultrasonic obstacle "
                    "interrupt routines."
                ),
            },
            {
                "stage": "Stage 3: Integration",
                "state": "upcoming",
                "detail": (
                    "Closed-loop vision-to-actuation fusion, emergency stop "
                    "watchdog validation, and outdoor pavement trials in Lille."
                ),
            },
        ],
        "tradeoffs": [
            (
                "Dual-MCU Partitioning (STM32 + ESP32) vs. Single SoC: "
                "Isolated hard real-time PWM motor control on STM32 while "
                "offloading wireless telemetry and camera framing to ESP32."
            ),
            (
                "External AI Camera Module vs. On-MCU Vision: Chosen to "
                "preserve deterministic MCU loop timing (<5 ms) and lower "
                "embedded RAM footprint."
            ),
        ],
        "team_acknowledgment": {
            "en": (
                "7-Member M1 Engineering R&D Team at JUNIA Lille — "
                "Collaborative hardware, embedded firmware, and vision "
                "integration (Add teammate names here)."
            ),
            "fr": (
                "Équipe R&D M1 de 7 élèves-ingénieurs à JUNIA Lille — "
                "Collaboration matériel, firmware embarqué et vision IA "
                "(Ajouter les noms des coéquipiers ici)."
            ),
        },
        "summary": (
            "Active M1 R&D project at JUNIA Lille: 7-member engineering "
            "team prototyping an autonomous street-cleaning robot for "
            "urban Lille streets."
        ),
        "highlights": [
            (
                "Prototyping an autonomous urban sweeper robot within a "
                "7-member engineering team at JUNIA Lille."
            ),
            (
                "Developing embedded C/C++ firmware across STM32 and ESP32 "
                "microcontrollers for motor control and telemetry."
            ),
            (
                "Integrating an external AI camera module with distance "
                "sensors for real-time obstacle and debris detection."
            ),
        ],
        "en": {
            "title": "Autonomous Street-Cleaning Robot Prototype",
            "category": "Embedded & Hardware",
            "status_label": "In Progress — Active R&D",
            "tech_stack": [
                "C/C++",
                "STM32 / ESP32",
                "External AI Camera Module",
                "Motor Control",
                "Sensor Fusion",
            ],
            "block_diagram": [
                "External AI Camera & Obstacle Sensors",
                "STM32 / ESP32 MCU Control Unit",
                "PWM Motor & Sweeper Actuation",
                "Autonomous Street Navigation Loop",
            ],
            "milestones": [
                {
                    "stage": "Stage 1: Architecture & Sensor Selection",
                    "state": "done",
                    "detail": (
                        "Defined dual-MCU partitioning (STM32 real-time motor "
                        "loop + ESP32 telemetry), external AI camera interface, "
                        "and power budget with the 7-member JUNIA Lille team."
                    ),
                },
                {
                    "stage": "Stage 2: MCU Control",
                    "state": "active",
                    "detail": (
                        "Implementing embedded C/C++ PWM motor drivers, rotary "
                        "sweeper actuation, and deterministic ultrasonic "
                        "obstacle interrupt routines."
                    ),
                },
                {
                    "stage": "Stage 3: Integration",
                    "state": "upcoming",
                    "detail": (
                        "Closed-loop vision-to-actuation fusion, emergency "
                        "stop watchdog validation, and urban trials in Lille."
                    ),
                },
            ],
            "tradeoffs": [
                (
                    "Dual-MCU Partitioning (STM32 + ESP32) vs. Single SoC: "
                    "Isolated hard real-time PWM motor control on STM32 while "
                    "offloading wireless telemetry and camera framing to ESP32."
                ),
                (
                    "External AI Camera Module vs. On-MCU Vision: Chosen to "
                    "preserve deterministic MCU loop timing (<5 ms) and lower "
                    "embedded SRAM footprint."
                ),
            ],
            "summary": (
                "Active M1 R&D project at JUNIA Lille: 7-member student "
                "engineering team prototyping an autonomous street-cleaning "
                "robot designed for Lille streets."
            ),
            "highlights": [
                (
                    "Co-engineering an autonomous street-cleaning robot "
                    "within a 7-member M1 R&D team at JUNIA Lille."
                ),
                (
                    "Writing C/C++ embedded control firmware on STM32/ESP32 "
                    "microcontrollers for locomotion and brush actuation."
                ),
                (
                    "Interfacing an external AI camera module and proximity "
                    "sensors for urban obstacle avoidance."
                ),
            ],
        },
        "fr": {
            "title": "Prototype de Robot Autonome de Nettoyage Urbain",
            "category": "Embarqué & Matériel",
            "status_label": "En cours — R&D Active",
            "tech_stack": [
                "C/C++",
                "STM32 / ESP32",
                "Module Caméra IA Externe",
                "Commande Moteur",
                "Fusion Capteurs",
            ],
            "block_diagram": [
                "Caméra IA Externe & Capteurs d'Obstacles",
                "Unité de Commande MCU STM32 / ESP32",
                "Pilotage PWM Moteurs & Balayage",
                "Boucle de Navigation Urbaine Autonome",
            ],
            "milestones": [
                {
                    "stage": "Étape 1 : Architecture & Sélection Capteurs",
                    "state": "done",
                    "detail": (
                        "Partitionnement bi-MCU (boucle temps réel STM32 + "
                        "télémétrie ESP32), caméra IA externe et bilan "
                        "énergétique définis avec l'équipe R&D de 7 à JUNIA."
                    ),
                },
                {
                    "stage": "Étape 2 : Commande MCU",
                    "state": "active",
                    "detail": (
                        "Développement du firmware C/C++ PWM, asservissement "
                        "des brosses rotatives et interruptions capteurs "
                        "ultrasons."
                    ),
                },
                {
                    "stage": "Étape 3 : Intégration",
                    "state": "upcoming",
                    "detail": (
                        "Fusion vision/commande en boucle fermée, chien de "
                        "garde matériel et essais urbains à Lille."
                    ),
                },
            ],
            "tradeoffs": [
                (
                    "Architecture bi-MCU (STM32 + ESP32) vs SoC unique : "
                    "Isolation de l'asservissement PWM temps réel sur STM32 et "
                    "délégation de la télémétrie/vision à l'ESP32."
                ),
                (
                    "Module Caméra IA Externe vs Inférence sur MCU : Préserve "
                    "une boucle de contrôle déterministe (<5 ms) et réduit "
                    "l'empreinte mémoire."
                ),
            ],
            "summary": (
                "Projet R&D M1 actif à JUNIA Lille : équipe de 7 étudiants "
                "ingénieurs concevant un robot autonome de nettoyage pour "
                "les rues de Lille."
            ),
            "highlights": [
                (
                    "Conception collaborative au sein d'une équipe R&D de "
                    "7 élèves-ingénieurs M1 à JUNIA Lille."
                ),
                (
                    "Développement du firmware C/C++ sur microcontrôleurs "
                    "STM32 et ESP32 pour la propulsion et l'asservissement."
                ),
                (
                    "Intégration d'un module caméra IA externe et de "
                    "capteurs de distance pour la détection d'obstacles."
                ),
            ],
        },
    },
    {
        "slug": "cpp-shopping-mall-system",
        "status": "completed",
        "category": "Software & Systems",
        "domain_tone": "navy",
        "title": "C++ Shopping Mall Management System",
        "tech_stack": [
            "C++",
            "OOP Architecture",
            "GCC / GDB (WSL)",
            "Data Structures",
            "Project Lead",
        ],
        "block_diagram": [
            "CLI & Operator Input Layer",
            "OOP Class Hierarchy (Tenant / Inventory)",
            "In-Memory Search & Indexing Engine",
            "Persistent Record Serialization",
        ],
        "milestones": [
            {
                "stage": "Stage 1: Architecture & Sensor Selection",
                "state": "done",
                "detail": "OOP domain modeling, abstract base classes, and interface contracts.",
            },
            {
                "stage": "Stage 2: MCU Control",
                "state": "done",
                "detail": "Core C++ implementation, STL indexing engine, and GDB memory verification.",
            },
            {
                "stage": "Stage 3: Integration",
                "state": "done",
                "detail": "Team module integration, deterministic file persistence, and QA sign-off.",
            },
        ],
        "tradeoffs": [
            (
                "Polymorphic Class Hierarchy vs. Flat Structs: Enabled clean "
                "extensibility across store categories and billing rules "
                "while enforcing strict encapsulation."
            ),
            (
                "In-Memory STL Indexing + File Serialization vs. External DB: "
                "Zero external runtime dependencies and sub-millisecond lookup "
                "under the WSL GCC/GDB toolchain."
            ),
        ],
        "team_acknowledgment": {
            "en": (
                "Project Lead — Hanz Ofosuhene-Sintim, in collaboration "
                "with Computer Engineering student team members "
                "(Add collaborator names here)."
            ),
            "fr": (
                "Chef de Projet — Hanz Ofosuhene-Sintim, en collaboration "
                "avec les membres de l'équipe d'ingénierie informatique "
                "(Ajouter les noms des collaborateurs ici)."
            ),
        },
        "summary": (
            "Object-oriented C++ system engineered to manage retail "
            "tenants, inventory records, and mall operations with modular "
            "class hierarchies."
        ),
        "highlights": [
            (
                "Architected modular C++ class hierarchies applying "
                "encapsulation, inheritance, and polymorphism."
            ),
            (
                "Compiled and debugged using the C/C++ GCC/GDB development "
                "toolchain under WSL/Linux."
            ),
            (
                "Served as Project Lead: partitioned software modules, "
                "reviewed interfaces, and integrated team deliverables."
            ),
        ],
        "en": {
            "title": "C++ Shopping Mall Management System",
            "category": "Software & Systems",
            "status_label": "Completed",
            "tech_stack": [
                "C++",
                "OOP Architecture",
                "GCC / GDB (WSL)",
                "Data Structures",
                "Project Lead",
            ],
            "block_diagram": [
                "CLI & Operator Input Layer",
                "OOP Class Hierarchy (Tenant / Inventory)",
                "In-Memory Search & Indexing Engine",
                "Persistent Record Serialization",
            ],
            "milestones": [
                {
                    "stage": "Stage 1: Architecture & Class Contracts",
                    "state": "done",
                    "detail": "OOP domain modeling, abstract base classes, and team interface contracts.",
                },
                {
                    "stage": "Stage 2: Core C++ & GDB Verification",
                    "state": "done",
                    "detail": "In-memory search/indexing engine and WSL GCC/GDB memory validation.",
                },
                {
                    "stage": "Stage 3: Integration",
                    "state": "done",
                    "detail": "Multi-developer module merge, persistent record serialization, and QA.",
                },
            ],
            "tradeoffs": [
                (
                    "Polymorphic Class Hierarchy vs. Flat Structs: Enabled "
                    "clean extensibility across store categories and billing "
                    "workflows while enforcing strict encapsulation."
                ),
                (
                    "In-Memory STL Indexing + File Serialization vs. External "
                    "DB: Guaranteed zero external runtime dependencies and "
                    "fast compilation under WSL GCC/GDB."
                ),
            ],
            "summary": (
                "Object-oriented C++ application engineered to manage "
                "shops, inventory records, and billing workflows across a "
                "multi-tenant shopping mall."
            ),
            "highlights": [
                (
                    "Designed the system architecture using C++ Object-"
                    "Oriented Programming (OOP) and modular class hierarchies."
                ),
                (
                    "Built and verified using the GCC/GDB C++ toolchain in "
                    "a WSL development environment."
                ),
                (
                    "Led the student engineering team: coordinated task "
                    "allocation and unified all C++ modules."
                ),
            ],
        },
        "fr": {
            "title": "Système C++ de Gestion de Centre Commercial",
            "category": "Logiciel & Systèmes",
            "status_label": "Terminé",
            "tech_stack": [
                "C++",
                "Architecture POO",
                "GCC / GDB (WSL)",
                "Structures de Données",
                "Chef de Projet",
            ],
            "block_diagram": [
                "Interface Opérateur & Saisie CLI",
                "Hiérarchie de Classes POO (Boutiques / Stocks)",
                "Moteur d'Indexation & Recherche Mémoire",
                "Sérialisation Persistante des Registres",
            ],
            "milestones": [
                {
                    "stage": "Étape 1 : Architecture & Contrats POO",
                    "state": "done",
                    "detail": "Modélisation objet, classes abstraites et interfaces d'équipe.",
                },
                {
                    "stage": "Étape 2 : Noyau C++ & Débogage GDB",
                    "state": "done",
                    "detail": "Moteur d'indexation mémoire et validation sous WSL GCC/GDB.",
                },
                {
                    "stage": "Étape 3 : Intégration",
                    "state": "done",
                    "detail": "Fusion des modules, sérialisation persistante et recette finale.",
                },
            ],
            "tradeoffs": [
                (
                    "Hiérarchie Polymorphe POO vs Structures Plates : "
                    "Extensibilité propre des catégories de boutiques et "
                    "encapsulation stricte des états."
                ),
                (
                    "Indexation STL en Mémoire + Sérialisation Fichier : "
                    "Aucune dépendance externe et exécution immédiate sous "
                    "WSL GCC/GDB."
                ),
            ],
            "summary": (
                "Application C++ orientée objet conçue pour gérer les "
                "enseignes, les stocks et les opérations d'un centre "
                "commercial."
            ),
            "highlights": [
                (
                    "Modélisation de l'architecture système en C++ orienté "
                    "objet avec hiérarchies de classes modulaires."
                ),
                (
                    "Compilation et débogage via la chaîne d'outils C/C++ "
                    "GCC/GDB sous environnement WSL."
                ),
                (
                    "Direction de l'équipe projet : découpage fonctionnel, "
                    "revue de code et intégration finale."
                ),
            ],
        },
    },
    {
        "slug": "smart-logistics-database-schema",
        "status": "completed",
        "category": "Software & Systems",
        "domain_tone": "forest",
        "title": "Smart Logistics & Delivery System Data Modeling",
        "tech_stack": [
            "System Data Modeling",
            "ER Diagrams",
            "Associative Tables",
            "Relational Schema Normalization",
        ],
        "block_diagram": [
            "Logistics Domain Requirements Analysis",
            "Conceptual Entity-Relationship (ER) Diagram",
            "M:N Resolution via Associative Tables",
            "Normalized 3NF Relational Schema",
        ],
        "milestones": [
            {
                "stage": "Stage 1: Architecture & Entity Capture",
                "state": "done",
                "detail": "Mapped orders, fleets, hubs, and courier cardinalities.",
            },
            {
                "stage": "Stage 2: Associative Table Resolution",
                "state": "done",
                "detail": "Decomposed M:N relationships into composite-key bridge tables.",
            },
            {
                "stage": "Stage 3: 3NF Normalization",
                "state": "done",
                "detail": "Eliminated transitive dependencies and verified referential integrity.",
            },
        ],
        "tradeoffs": [
            (
                "Strict 3NF Normalization vs. Denormalized Read Tables: "
                "Prioritized zero update anomalies and strict foreign-key "
                "integrity across shipment state transitions."
            ),
            (
                "Explicit Associative Bridge Tables with Audit Attributes: "
                "Allowed tracking per-leg timestamps and courier handoffs "
                "across multi-hop deliveries."
            ),
        ],
        "team_acknowledgment": {
            "en": (
                "Collaborative System Data Modeling Team — Engineered with "
                "fellow Computer Engineering teammates "
                "(Add teammate names here)."
            ),
            "fr": (
                "Équipe Collaborative de Modélisation de Données — Conçu "
                "avec mes coéquipiers en génie informatique "
                "(Ajouter les noms des coéquipiers ici)."
            ),
        },
        "summary": (
            "System data modeling architecture for a logistics platform: "
            "engineered the full ER diagram, associative tables, and "
            "normalized relational schema."
        ),
        "highlights": [
            (
                "Engineered the complete Entity-Relationship (ER) diagram "
                "mapping orders, fleets, hubs, and delivery lifecycles."
            ),
            (
                "Resolved complex many-to-many (M:N) relationships using "
                "dedicated associative bridge tables."
            ),
            (
                "Normalized the relational database schema to eliminate "
                "redundancy and enforce referential integrity."
            ),
        ],
        "en": {
            "title": "Smart Logistics & Delivery System Data Modeling",
            "category": "Software & Systems",
            "status_label": "Completed",
            "tech_stack": [
                "System Data Modeling",
                "ER Diagrams",
                "Associative Tables",
                "Relational Schema Normalization",
            ],
            "block_diagram": [
                "Logistics Domain Requirements Analysis",
                "Conceptual Entity-Relationship (ER) Diagram",
                "M:N Resolution via Associative Tables",
                "Normalized 3NF Relational Schema",
            ],
            "milestones": [
                {
                    "stage": "Stage 1: Architecture & Entity Capture",
                    "state": "done",
                    "detail": "Mapped orders, fleets, hubs, and courier cardinalities.",
                },
                {
                    "stage": "Stage 2: Associative Table Resolution",
                    "state": "done",
                    "detail": "Decomposed M:N relationships into composite-key bridge tables.",
                },
                {
                    "stage": "Stage 3: 3NF Normalization",
                    "state": "done",
                    "detail": "Eliminated transitive dependencies and verified referential integrity.",
                },
            ],
            "tradeoffs": [
                (
                    "Strict 3NF Normalization vs. Denormalized Read Tables: "
                    "Prioritized zero update anomalies and strict foreign-key "
                    "integrity across shipment state transitions."
                ),
                (
                    "Explicit Associative Bridge Tables with Audit Attributes: "
                    "Enabled tracking per-leg timestamps and courier handoffs "
                    "across multi-hop deliveries."
                ),
            ],
            "summary": (
                "Comprehensive system data modeling for a smart logistics "
                "and delivery network, from conceptual ER architecture to "
                "normalized relational schema."
            ),
            "highlights": [
                (
                    "Designed the end-to-end Entity-Relationship (ER) "
                    "diagram capturing customers, couriers, and shipments."
                ),
                (
                    "Resolved many-to-many relationships through structured "
                    "associative tables with composite keys."
                ),
                (
                    "Normalized the relational schema (up to 3NF) to ensure "
                    "strict data consistency across delivery states."
                ),
            ],
        },
        "fr": {
            "title": (
                "Modélisation de Données — Système Logistique & Livraison"
            ),
            "category": "Logiciel & Systèmes",
            "status_label": "Terminé",
            "tech_stack": [
                "Modélisation de Données",
                "Diagrammes E-A (ER)",
                "Tables Associatives",
                "Normalisation Schéma Relationnel",
            ],
            "block_diagram": [
                "Analyse Fonctionnelle des Flux Logistiques",
                "Diagramme Entité-Association (ER) Conceptuel",
                "Résolution N:M par Tables Associatives",
                "Schéma Relationnel Normalisé (3NF)",
            ],
            "milestones": [
                {
                    "stage": "Étape 1 : Architecture & Entités",
                    "state": "done",
                    "detail": "Cartographie des commandes, flottes, dépôts et livreurs.",
                },
                {
                    "stage": "Étape 2 : Tables Associatives",
                    "state": "done",
                    "detail": "Résolution des relations N:M par clés composites.",
                },
                {
                    "stage": "Étape 3 : Normalisation 3NF",
                    "state": "done",
                    "detail": "Élimination des dépendances transitives et intégrité référentielle.",
                },
            ],
            "tradeoffs": [
                (
                    "Normalisation 3NF Stricte vs Dénormalisation : "
                    "Priorité à l'absence d'anomalies de mise à jour et à "
                    "l'intégrité référentielle des expéditions."
                ),
                (
                    "Tables Associatives Enrichies d'Attributs d'Audit : "
                    "Traçabilité complète des horodatages et transferts "
                    "multi-étapes."
                ),
            ],
            "summary": (
                "Architecture de modélisation de données pour un système "
                "de logistique et livraison : diagramme ER complet, tables "
                "associatives et normalisation relationnelle."
            ),
            "highlights": [
                (
                    "Conception intégrale du diagramme Entité-Association "
                    "(ER) modélisant commandes, livreurs et expéditions."
                ),
                (
                    "Résolution des relations plusieurs-à-plusieurs (N:M) "
                    "via des tables associatives dédiées."
                ),
                (
                    "Normalisation du schéma relationnel pour éliminer les "
                    "redondances et garantir l'intégrité référentielle."
                ),
            ],
        },
    },
    {
        "slug": "automatic-water-tank-control",
        "status": "completed",
        "category": "Embedded & Hardware",
        "domain_tone": "copper",
        "title": "Automatic Water Tank Level Monitoring & Control System",
        "tech_stack": [
            "Arduino MCU",
            "Ultrasonic Sensor",
            "Closed-Loop Relay Control",
            "16x2 LCD Telemetry",
        ],
        "block_diagram": [
            "Ultrasonic Sensor Input",
            "Arduino MCU Processing",
            "Relay & Pump Actuation",
            "16x2 LCD Telemetry",
        ],
        "milestones": [
            {
                "stage": "Stage 1: Architecture & Sensor Selection",
                "state": "done",
                "detail": "Selected non-contact ultrasonic time-of-flight sensing and relay isolation.",
            },
            {
                "stage": "Stage 2: MCU Control",
                "state": "done",
                "detail": "Programmed hysteresis control loop and echo pulse filtering on Arduino MCU.",
            },
            {
                "stage": "Stage 3: Integration",
                "state": "done",
                "detail": "Bench calibration with pump relay switching and live 16x2 LCD operator telemetry.",
            },
        ],
        "tradeoffs": [
            (
                "Non-Contact Ultrasonic Sensing vs. Submersible Float Probes: "
                "Eliminated electrode corrosion and mineral fouling inside "
                "the water reservoir."
            ),
            (
                "Dual-Threshold Hysteresis Band vs. Single Setpoint: "
                "Prevented relay chatter and pump motor wear caused by "
                "surface ripples."
            ),
        ],
        "team_acknowledgment": {
            "en": (
                "Embedded Hardware & Control Build — Developed with lab "
                "project partners (Add partner names here)."
            ),
            "fr": (
                "Réalisation Embarquée & Asservissement — Développé avec "
                "les partenaires de laboratoire (Ajouter les noms ici)."
            ),
        },
        "summary": (
            "Closed-loop embedded control system using an Arduino MCU, "
            "ultrasonic distance telemetry, automated relay switching, "
            "and real-time LCD status feedback."
        ),
        "highlights": [
            (
                "Interfaced an ultrasonic time-of-flight sensor for "
                "non-contact reservoir level measurement."
            ),
            (
                "Implemented hysteresis-based closed-loop relay control "
                "to prevent pump rapid-cycling."
            ),
            (
                "Rendered live water percentage and pump status on an "
                "embedded LCD operator interface."
            ),
        ],
        "en": {
            "title": "Automatic Water Tank Level Monitoring & Control System",
            "category": "Embedded & Hardware",
            "status_label": "Completed",
            "tech_stack": [
                "Arduino MCU",
                "Ultrasonic Sensor",
                "Closed-Loop Relay Control",
                "16x2 LCD Telemetry",
            ],
            "block_diagram": [
                "Ultrasonic Sensor Input",
                "Arduino MCU Processing",
                "Relay & Pump Actuation",
                "16x2 LCD Telemetry",
            ],
            "milestones": [
                {
                    "stage": "Stage 1: Architecture & Sensor Selection",
                    "state": "done",
                    "detail": "Selected non-contact ultrasonic time-of-flight sensing and relay isolation.",
                },
                {
                    "stage": "Stage 2: MCU Control",
                    "state": "done",
                    "detail": "Programmed hysteresis control loop and echo pulse filtering on Arduino MCU.",
                },
                {
                    "stage": "Stage 3: Integration",
                    "state": "done",
                    "detail": "Bench calibration with pump relay switching and live 16x2 LCD telemetry.",
                },
            ],
            "tradeoffs": [
                (
                    "Non-Contact Ultrasonic Sensing vs. Submersible Float "
                    "Probes: Eliminated electrode corrosion and mineral "
                    "fouling inside the water reservoir."
                ),
                (
                    "Dual-Threshold Hysteresis Band vs. Single Setpoint: "
                    "Prevented relay chatter and pump motor wear caused by "
                    "water surface ripples."
                ),
            ],
            "summary": (
                "Automated water reservoir monitoring and pump control "
                "system built around an Arduino microcontroller, ultrasonic "
                "sensing, and real-time LCD telemetry."
            ),
            "highlights": [
                (
                    "Measured real-time water depth using non-contact "
                    "ultrasonic acoustic pulse timing."
                ),
                (
                    "Engineered closed-loop relay actuation with upper and "
                    "lower threshold hysteresis."
                ),
                (
                    "Displayed continuous tank volume telemetry and pump "
                    "state on a 16x2 LCD screen."
                ),
            ],
        },
        "fr": {
            "title": (
                "Système Automatisé de Supervision & Contrôle de Réservoir"
            ),
            "category": "Embarqué & Matériel",
            "status_label": "Terminé",
            "tech_stack": [
                "Arduino MCU",
                "Capteur Ultrason",
                "Commande Relais Boucle Fermée",
                "Télémétrie LCD 16x2",
            ],
            "block_diagram": [
                "Acquisition Capteur Ultrason",
                "Traitement MCU Arduino",
                "Commutation Relais & Pompe",
                "Télémétrie Écran LCD 16x2",
            ],
            "milestones": [
                {
                    "stage": "Étape 1 : Architecture & Choix Capteur",
                    "state": "done",
                    "detail": "Mesure acoustique sans contact et isolation du relais de puissance.",
                },
                {
                    "stage": "Étape 2 : Commande MCU",
                    "state": "done",
                    "detail": "Boucle d'hystérésis et filtrage d'écho sur Arduino.",
                },
                {
                    "stage": "Étape 3 : Intégration",
                    "state": "done",
                    "detail": "Calibration sur banc et affichage temps réel sur LCD 16x2.",
                },
            ],
            "tradeoffs": [
                (
                    "Capteur Ultrason Sans Contact vs Sondes Immergées : "
                    "Élimine l'oxydation des électrodes et l'encrassement "
                    "dans le réservoir."
                ),
                (
                    "Régulation par Bande d'Hystérésis vs Seuil Unique : "
                    "Empêche les commutations rapides du relais dues aux "
                    "ondulations de surface."
                ),
            ],
            "summary": (
                "Système embarqué de surveillance et régulation de niveau "
                "d'eau utilisant un microcontrôleur Arduino, un capteur "
                "ultrason, un relais en boucle fermée et un affichage LCD."
            ),
            "highlights": [
                (
                    "Mesure sans contact de la hauteur d'eau par capteur "
                    "de distance à ultrasons."
                ),
                (
                    "Asservissement en boucle fermée du relais de pompe "
                    "avec seuils d'hystérésis."
                ),
                (
                    "Affichage temps réel du niveau et de l'état de la "
                    "pompe sur écran LCD 16x2."
                ),
            ],
        },
    },
    {
        "slug": "bilingual-engineering-portfolio",
        "status": "in_progress",
        "category": "Software & Systems",
        "domain_tone": "forest",
        "title": "Full-Stack Bilingual Engineering Portfolio & REST API",
        "tech_stack": [
            "Python 3",
            "Flask",
            "Jinja2",
            "Header-Based i18n",
            "JSON Persistence",
        ],
        "block_diagram": [
            "HTTP Request & Accept-Language / Cookie i18n",
            "Flask Routing & Context Processor Engine",
            "projects.json Persistent Data Store",
            "2D App-Shell & SVG Mind-Map UI",
        ],
        "milestones": [
            {
                "stage": "Stage 1: Architecture & Sensor Selection",
                "state": "done",
                "detail": (
                    "Engineered Flask routing, header + cookie FR/EN "
                    "localization engine, and JSON persistence layer."
                ),
            },
            {
                "stage": "Stage 2: MCU Control",
                "state": "active",
                "detail": (
                    "Building the tactile App-Shell, 3-view SVG Bézier radial "
                    "mind-map, Spotlight Command Palette, and R&D workbench."
                ),
            },
            {
                "stage": "Stage 3: Integration",
                "state": "upcoming",
                "detail": (
                    "Live API telemetry latency console, production WSGI "
                    "hardening, and continuous asset pipeline."
                ),
            },
        ],
        "tradeoffs": [
            (
                "Flat-File JSON Persistence (`projects.json`) vs. RDBMS: "
                "Zero-config Git-auditable storage with instant localhost "
                "Project Studio mutations and sub-2ms `/api/projects` reads."
            ),
            (
                "Server-Rendered Jinja2 + Vanilla JS vs. Heavy SPA Bundle: "
                "Eliminated build-step overhead and client hydration delay "
                "while keeping kinetic SVG and command-palette interactivity."
            ),
        ],
        "team_acknowledgment": {
            "en": (
                "Lead Architect & Developer — Hanz Ofosuhene-Sintim "
                "(Individual Full-Stack Engineering Project)."
            ),
            "fr": (
                "Architecte & Développeur Principal — Hanz Ofosuhene-Sintim "
                "(Projet Individuel d'Ingénierie Full-Stack)."
            ),
        },
        "summary": (
            "Modular bilingual (FR/EN) engineering dashboard and JSON REST "
            "API built with Python 3, Flask, Jinja2, smart i18n detection, "
            "and local Project Studio persistence."
        ),
        "highlights": [
            (
                "Engineered a smart FR/EN localization engine combining "
                "Accept-Language negotiation with 1-year cookie overrides."
            ),
            (
                "Built a JSON-backed persistence layer and local Project "
                "Studio for live status switching and project creation."
            ),
            (
                "Designed an architectural Gallery Alabaster / OLED Black "
                "App-Shell with an interactive 3-view SVG mind-map."
            ),
        ],
        "en": {
            "title": "Full-Stack Bilingual Engineering Portfolio & REST API",
            "category": "Software & Systems",
            "status_label": "In Progress — Active R&D",
            "tech_stack": [
                "Python 3",
                "Flask",
                "Jinja2",
                "Header-Based i18n",
                "JSON Persistence",
            ],
            "block_diagram": [
                "HTTP Request & Accept-Language / Cookie i18n",
                "Flask Routing & Context Processor Engine",
                "projects.json Persistent Data Store",
                "2D App-Shell & SVG Mind-Map UI",
            ],
            "milestones": [
                {
                    "stage": "Stage 1: Architecture & Sensor Selection",
                    "state": "done",
                    "detail": (
                        "Engineered Flask routing, header + cookie FR/EN "
                        "localization engine, and JSON persistence layer."
                    ),
                },
                {
                    "stage": "Stage 2: MCU Control",
                    "state": "active",
                    "detail": (
                        "Building the tactile App-Shell, 3-view SVG Bézier "
                        "radial mind-map, Spotlight Command Palette, and "
                        "R&D workbench."
                    ),
                },
                {
                    "stage": "Stage 3: Integration",
                    "state": "upcoming",
                    "detail": (
                        "Live API telemetry latency console, production WSGI "
                        "hardening, and continuous asset pipeline."
                    ),
                },
            ],
            "tradeoffs": [
                (
                    "Flat-File JSON Persistence (`projects.json`) vs. RDBMS: "
                    "Zero-config Git-auditable storage with instant localhost "
                    "Project Studio mutations and sub-2ms `/api/projects` reads."
                ),
                (
                    "Server-Rendered Jinja2 + Vanilla JS vs. Heavy SPA Bundle: "
                    "Eliminated build-step overhead and client hydration delay "
                    "while keeping kinetic SVG and command-palette interactivity."
                ),
            ],
            "summary": (
                "Full-stack bilingual (FR/EN) engineering portfolio and "
                "REST API built with Python 3, Flask, Jinja2, header-based "
                "i18n localization, and JSON persistence."
            ),
            "highlights": [
                (
                    "Implemented automatic FR/EN language negotiation via "
                    "HTTP headers and persistent cookie overrides."
                ),
                (
                    "Architected a local JSON persistence store supporting "
                    "live project creation, status toggling, and team edits."
                ),
                (
                    "Crafted a responsive 2D App-Shell with a 3-view SVG "
                    "mind-map and interactive case-study drawer."
                ),
            ],
        },
        "fr": {
            "title": "Portfolio d'Ingénierie Bilingue Full-Stack & API REST",
            "category": "Logiciel & Systèmes",
            "status_label": "En cours — R&D Active",
            "tech_stack": [
                "Python 3",
                "Flask",
                "Jinja2",
                "i18n par En-têtes HTTP",
                "Persistance JSON",
            ],
            "block_diagram": [
                "Requête HTTP & Négociation i18n / Cookie",
                "Moteur de Routage Flask & Context Processor",
                "Stockage Persistant projects.json",
                "Interface App-Shell 2D & Mind-Map SVG",
            ],
            "milestones": [
                {
                    "stage": "Étape 1 : Architecture & Sélection Capteurs",
                    "state": "done",
                    "detail": (
                        "Moteur Flask, négociation linguistique FR/EN par "
                        "en-têtes/cookie et persistance JSON."
                    ),
                },
                {
                    "stage": "Étape 2 : Commande MCU",
                    "state": "active",
                    "detail": (
                        "App-Shell tactile, mind-map radial SVG à 3 vues, "
                        "palette Spotlight et établi R&D."
                    ),
                },
                {
                    "stage": "Étape 3 : Intégration",
                    "state": "upcoming",
                    "detail": (
                        "Console de télémétrie API en direct, durcissement "
                        "WSGI et déploiement continu."
                    ),
                },
            ],
            "tradeoffs": [
                (
                    "Persistance JSON (`projects.json`) vs SGBD Relationnel : "
                    "Stockage versionnable sous Git sans serveur tiers, avec "
                    "édition instantanée via Project Studio."
                ),
                (
                    "Rendu Jinja2 + JS Natif vs SPA Lourde : Zéro latence "
                    "d'hydratation tout en offrant un mind-map SVG cinétique "
                    "et une palette de commande globale."
                ),
            ],
            "summary": (
                "Portfolio d'ingénierie bilingue (FR/EN) et API REST "
                "développé avec Python 3, Flask, Jinja2, détection i18n "
                "intelligente et persistance JSON."
            ),
            "highlights": [
                (
                    "Développement d'un moteur de localisation FR/EN "
                    "combinant négociation HTTP et persistance par cookie."
                ),
                (
                    "Mise en place d'une couche de persistance JSON avec "
                    "Project Studio local pour l'édition en direct."
                ),
                (
                    "Conception d'un App-Shell Gallery Alabaster / OLED "
                    "Black avec mind-map SVG interactif à 3 vues."
                ),
            ],
        },
    },
]


def save_projects(projects):
    """Persist the given list of project dictionaries to `projects.json`."""
    with open(PROJECTS_JSON_PATH, "w", encoding="utf-8") as file_obj:
        json.dump(projects, file_obj, indent=2, ensure_ascii=False)


def load_projects():
    """Load projects from `projects.json`, seeding from `SEED_PROJECTS`."""
    if not PROJECTS_JSON_PATH.exists():
        save_projects(SEED_PROJECTS)
        return list(SEED_PROJECTS)

    try:
        with open(PROJECTS_JSON_PATH, "r", encoding="utf-8") as file_obj:
            data = json.load(file_obj)
            if isinstance(data, list) and data:
                return data
    except (OSError, json.JSONDecodeError):
        pass

    save_projects(SEED_PROJECTS)
    return list(SEED_PROJECTS)


PROJECTS = load_projects()
