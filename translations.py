"""Bilingual (FR / EN) UI localization dictionary for the Bento dashboard."""

UI_TEXT = {
    "fr": {
        "lang_code": "fr",
        "lang_label": "Français",
        "meta_title": (
            "Hanz Ofosuhene-Sintim | Ingénieur Systèmes Embarqués"
        ),
        "sidebar": {
            "brand_name": "Hanz Ofosuhene-Sintim",
            "brand_status": "M1 Systèmes Embarqués · JUNIA Lille",
            "nav_label": "Navigation principale",
            "home": "Accueil",
            "about": "À propos",
            "projects": "Projets",
            "experience": "Expériences",
            "education": "Formation",
            "contact": "CV & Contact",
            "api_json": "API JSON",
        },
        "topbar": {
            "search_placeholder": (
                "Rechercher sur le portfolio (C++, KiCad, STM32)..."
            ),
            "search_aria": "Rechercher des projets ou compétences",
            "search_clear": "Effacer",
            "theme_toggle_label": "Basculer le thème Light / Dark",
            "theme_light": "Light",
            "theme_dark": "Dark",
            "lang_switch_tooltip": "Switch language to English (EN)",
            "profile_name": "Hanz Ofosuhene-Sintim",
            "profile_role": "Électronique & Embarqué",
        },
        "hero": {
            "eyebrow": "INGÉNIEUR ÉLECTRONIQUE & SYSTÈMES EMBARQUÉS",
            "greeting": "Bonjour",
            "name_intro": "Je suis Hanz Ofosuhene-Sintim.",
            "subtitle": (
                "M1 Electronics & Embedded Systems at JUNIA Lille | "
                "BSc Computer Engineering at KNUST"
            ),
            "description": (
                "Conception de systèmes embarqués (STM32, ESP32, Arduino), "
                "architecture C/C++ sous chaîne GCC/GDB (WSL), modélisation "
                "de schémas relationnels ER et leadership exécutif."
            ),
            "cta": "Explorer l'orbite interactive →",
            "secondary_cta": "Catalogue projets",
            "photo_caption": (
                "Hanz Ofosuhene-Sintim · Systèmes Embarqués & Architecture"
            ),
        },
        "telemetry": {
            "eyebrow": "TÉLÉMÉTRIE & FOCUS ACTUEL",
            "title": "R&D M1 JUNIA Lille",
            "focus_project": (
                "Robot Autonome de Nettoyage Urbain (Équipe R&D de 7)"
            ),
            "focus_stack": "STM32 · ESP32 · C/C++ · Caméra IA Externe",
            "stat_active_label": "En cours (R&D)",
            "stat_completed_label": "Terminés",
            "stat_total_label": "Systèmes",
            "cv_btn": "CV & Contact",
            "api_btn": "API JSON Brute",
        },
        "mindmap": {
            "badge": "ORBITE RADIALE INTERACTIVE · 3 VUES",
            "title": "Cartographie Radiale & Flux Système",
            "subtitle": (
                "Cliquez sur une capsule orbitale pour pulser son flux "
                "SVG, inspecter les détails et filtrer le dashboard."
            ),
            "reset_filter": "Réinitialiser le filtre",
            "prev_view": "Vue précédente",
            "next_view": "Vue suivante",
            "hub_title": "Hanz Ofosuhene-Sintim",
            "hub_subtitle": "M1 JUNIA · BSc KNUST",
            "detail_default_title": (
                "Sélectionnez un nœud en orbite autour du portrait"
            ),
            "detail_default_text": (
                "Chaque capsule déclenche une impulsion de données SVG "
                "et filtre dynamiquement les projets ou ouvre la section."
            ),
            "detail_action_btn": "Ouvrir / Filtrer →",
            "views": [
                {
                    "id": "overview",
                    "label": "1 · Vue Globale",
                    "nodes": [
                        {
                            "tone": "copper",
                            "code": "COMP",
                            "title": "Compétences Clés",
                            "subtitle": "MCU, C++, ER & Python",
                            "detail": (
                                "Matrice de compétences : STM32, ESP32, "
                                "C/C++ GCC/GDB (WSL), Modélisation ER et "
                                "KiCad."
                            ),
                            "href": "#skills-bento",
                            "filter": "",
                        },
                        {
                            "tone": "navy",
                            "code": "BIO",
                            "title": "À propos & Profil",
                            "subtitle": "Parcours Ghana-France",
                            "detail": (
                                "Ingénieur Systèmes Embarqués & "
                                "Informatique bilingue FR/EN."
                            ),
                            "href": "/about",
                            "filter": "",
                        },
                        {
                            "tone": "forest",
                            "code": "PROJ",
                            "title": "Projets & R&D (5)",
                            "subtitle": "2 En cours · 3 Terminés",
                            "detail": (
                                "5 projets d'ingénierie avec schémas-blocs "
                                "et remerciements d'équipe."
                            ),
                            "href": "#projects-bento",
                            "filter": "",
                        },
                        {
                            "tone": "bronze",
                            "code": "LEAD",
                            "title": "Leadership Exécutif",
                            "subtitle": "ACES · GHAFRA · H&D",
                            "detail": (
                                "Président ACES KNUST (Tech Week, Codefest "
                                "2026), GHAFRA Nord Lille & H & D'S HUB."
                            ),
                            "href": "#leadership-bento",
                            "filter": "",
                        },
                        {
                            "tone": "zinc",
                            "code": "EDU",
                            "title": "Formation",
                            "subtitle": "JUNIA Lille & KNUST",
                            "detail": (
                                "M1 Electronics & Embedded Systems à JUNIA "
                                "Lille | BSc Computer Engineering à KNUST."
                            ),
                            "href": "/about#education",
                            "filter": "",
                        },
                        {
                            "tone": "steel",
                            "code": "CV",
                            "title": "CV & Contact",
                            "subtitle": "Opportunités & API",
                            "detail": (
                                "Contact direct pour collaborations R&D, "
                                "stages systèmes embarqués et API JSON."
                            ),
                            "href": "/about#contact",
                            "filter": "",
                        },
                    ],
                },
                {
                    "id": "stack",
                    "label": "2 · Stack Matériel-Logiciel",
                    "nodes": [
                        {
                            "tone": "copper",
                            "code": "MCU",
                            "title": "Microcontrôleurs",
                            "subtitle": "STM32 · ESP32 · Arduino",
                            "detail": (
                                "Programmation embarquée temps réel sur "
                                "STM32, ESP32, MSP430 et Arduino."
                            ),
                            "href": "#projects-bento",
                            "filter": "stm32 esp32 arduino",
                        },
                        {
                            "tone": "navy",
                            "code": "C++",
                            "title": "C/C++ & WSL / GDB",
                            "subtitle": "POO & Chaîne GCC/GDB",
                            "detail": (
                                "Hiérarchies de classes POO, structures "
                                "de données et débogage GCC/GDB sous WSL."
                            ),
                            "href": "#projects-bento",
                            "filter": "c++",
                        },
                        {
                            "tone": "forest",
                            "code": "DATA",
                            "title": "Modélisation & ER",
                            "subtitle": "Tables Associatives 3NF",
                            "detail": (
                                "Diagrammes Entité-Association (ER), "
                                "résolution N:M et schémas normalisés 3NF."
                            ),
                            "href": "#projects-bento",
                            "filter": "er schema",
                        },
                        {
                            "tone": "steel",
                            "code": "API",
                            "title": "Python & Flask API",
                            "subtitle": "Jinja2 · i18n · JSON",
                            "detail": (
                                "Architecture backend Python 3, Flask, "
                                "détection i18n et persistance JSON."
                            ),
                            "href": "#projects-bento",
                            "filter": "python flask",
                        },
                        {
                            "tone": "copper",
                            "code": "SENS",
                            "title": "Capteurs & Caméra IA",
                            "subtitle": "Ultrasons · Relais · PWM",
                            "detail": (
                                "Intégration de caméra IA externe, "
                                "télémétrie ultrason et commande moteur."
                            ),
                            "href": "#projects-bento",
                            "filter": "ultrasonic camera sensor",
                        },
                        {
                            "tone": "bronze",
                            "code": "HW",
                            "title": "KiCad & Prototypage",
                            "subtitle": "Schémas & Intégration",
                            "detail": (
                                "Saisie de schémas électroniques, conception "
                                "PCB sous KiCad et tests matériels."
                            ),
                            "href": "#skills-bento",
                            "filter": "embedded",
                        },
                    ],
                },
                {
                    "id": "leadership",
                    "label": "3 · Leadership & Parcours",
                    "nodes": [
                        {
                            "tone": "bronze",
                            "code": "ACES",
                            "title": "Président ACES",
                            "subtitle": "Tech Week · Codefest 2026",
                            "detail": (
                                "Président du Département ACES (KNUST) : "
                                "Tech Week, Codefest 2026, Faculty Games "
                                "& expansion médias numériques."
                            ),
                            "href": "#leadership-bento",
                            "filter": "",
                        },
                        {
                            "tone": "steel",
                            "code": "GHAFRA",
                            "title": "GHAFRA Nord Lille",
                            "subtitle": "Stratégie & Organisation",
                            "detail": (
                                "Leadership en planification stratégique "
                                "et organisation communautaire à Lille."
                            ),
                            "href": "#leadership-bento",
                            "filter": "",
                        },
                        {
                            "tone": "copper",
                            "code": "HUB",
                            "title": "H & D'S HUB",
                            "subtitle": "Import & Revente Mobile",
                            "detail": (
                                "Direction commerciale de H & D'S HUB et "
                                "entreprise d'import/revente mobile."
                            ),
                            "href": "#leadership-bento",
                            "filter": "",
                        },
                        {
                            "tone": "zinc",
                            "code": "JUNIA",
                            "title": "JUNIA Lille (M1)",
                            "subtitle": "R&D Robotique Urbaine",
                            "detail": (
                                "Cycle Ingénieur M1 Électronique & "
                                "Systèmes Embarqués à JUNIA Lille."
                            ),
                            "href": "#projects-bento",
                            "filter": "junia",
                        },
                        {
                            "tone": "navy",
                            "code": "KNUST",
                            "title": "KNUST (BSc)",
                            "subtitle": "Computer Engineering",
                            "detail": (
                                "BSc Computer Engineering à KNUST et "
                                "direction d'équipes logicielles C++."
                            ),
                            "href": "#projects-bento",
                            "filter": "c++",
                        },
                        {
                            "tone": "forest",
                            "code": "I18N",
                            "title": "Ingénierie FR / EN",
                            "subtitle": "Collaboration Bilingue",
                            "detail": (
                                "Exécution technique bilingue français / "
                                "anglais entre la France et le Ghana."
                            ),
                            "href": "/about#contact",
                            "filter": "",
                        },
                    ],
                },
            ],
        },
        "status": {
            "completed": "Terminé",
            "in_progress": "En cours — R&D Active",
            "filter_all": "Tous",
            "filter_completed": "Terminé",
            "filter_in_progress": "En cours (R&D)",
            "toggle_btn": "Basculer le statut",
        },
        "studio": {
            "new_project_btn": "+ Nouveau Projet",
            "modal_title": "Project Studio — Créer un Projet",
            "modal_subtitle": (
                "Ajout direct persisté dans projects.json (Mode Localhost)."
            ),
            "title_en": "Titre du projet (EN)",
            "title_fr": "Titre du projet (FR)",
            "category": "Catégorie",
            "status": "Statut du cycle de vie",
            "tone": "Couleur d'accent",
            "tech_stack": "Stack technique (séparée par des virgules)",
            "block_diagram": "Schéma-bloc (3-4 étapes séparées par |)",
            "summary_en": "Résumé technique (EN)",
            "summary_fr": "Résumé technique (FR)",
            "highlights_en": "Points clés EN (séparés par |)",
            "highlights_fr": "Points clés FR (séparés par |)",
            "team_ack": "Remerciements d'équipe & collaborateurs",
            "save_btn": "Enregistrer dans projects.json",
            "cancel_btn": "Annuler",
        },
        "drawer": {
            "badge": "ÉTUDE DE CAS D'INGÉNIERIE",
            "close_aria": "Fermer le panneau d'étude de cas",
            "block_diagram_title": "Architecture & Schéma-Bloc Système",
            "highlights_title": "Réalisations & Points Clés Techniques",
            "tech_stack_title": "Technologies & Outils",
            "team_title": "Équipe & Collaborateurs (Remerciements)",
            "team_edit_label": (
                "Modifier les noms des coéquipiers (Localhost) :"
            ),
            "team_save_btn": "Mettre à jour l'équipe",
            "open_case_study": "Ouvrir l'étude de cas détaillée",
        },
        "bento": {
            "projects_title": "Projets & R&D Active",
            "projects_subtitle": (
                "Cliquez sur + pour inspecter le schéma-bloc et l'équipe."
            ),
            "view_all_projects": "Catalogue (5) →",
            "skills_title": "Matrice de Compétences",
            "skills_subtitle": (
                "Capsules techniques par domaine fonctionnel."
            ),
            "leadership_title": "Leadership & Opérations",
            "leadership_subtitle": (
                "Gouvernance exécutive, stratégie et entrepreneuriat."
            ),
            "leadership_more": "Voir tout le parcours →",
            "no_search_results": (
                "Aucun élément ne correspond à votre filtre actuel."
            ),
            "domains": {
                "copper": {
                    "title": "MCU, Capteurs & Embarqué",
                    "code": "EMB",
                },
                "navy": {
                    "title": "C/C++, POO & GCC/GDB (WSL)",
                    "code": "C++",
                },
                "forest": {
                    "title": "Modélisation ER & Python/Flask",
                    "code": "DATA",
                },
                "bronze": {
                    "title": "Leadership & Entrepreneuriat",
                    "code": "LEAD",
                },
                "zinc": {
                    "title": "Formation & Recherche R&D",
                    "code": "EDU",
                },
                "steel": {
                    "title": "Ingénierie Bilingue & Contact",
                    "code": "CV",
                },
            },
        },
        "projects_page": {
            "title": "Catalogue des Projets d'Ingénierie",
            "subtitle": (
                "Systèmes embarqués, architectures C++, modélisation ER "
                "et développements R&D en cours."
            ),
            "filter_all": "Toutes catégories",
            "filter_embedded": "Embarqué & Matériel",
            "filter_software": "Logiciel & Systèmes",
            "empty": "Aucun projet trouvé pour ce filtre.",
        },
        "about_page": {
            "title": "Parcours, Leadership & Architecture",
            "education_title": "Formation Académique",
            "skills_title": "Compétences Techniques & Outils",
            "leadership_title": (
                "Leadership Exécutif, Organisation & Entrepreneuriat"
            ),
            "contact_title": "CV & Contact Direct",
            "contact_text": (
                "Disponible pour échanger autour des systèmes embarqués, "
                "de la robotique autonome et des opportunités d'ingénierie."
            ),
            "aces_role": (
                "Président du Département ACES — KNUST (Association of "
                "Computer Engineering Students)"
            ),
            "aces_points": [
                (
                    "Direction exécutive complète de l'association des "
                    "étudiants en génie informatique et représentation "
                    "officielle auprès de la faculté."
                ),
                (
                    "Pilotage des grands événements techniques et "
                    "académiques : Tech Week, Codefest 2026 et Faculty Games."
                ),
                (
                    "Expansion stratégique des médias numériques (Digital "
                    "Media Expansion) et rayonnement du département."
                ),
            ],
            "ghafra_role": (
                "Leadership en Planification Stratégique & Organisation — "
                "GHAFRA Nord (Lille, France)"
            ),
            "ghafra_points": [
                (
                    "Coordination opérationnelle, planification stratégique "
                    "et mobilisation communautaire au sein de GHAFRA Nord "
                    "à Lille."
                ),
                (
                    "Structuration logistique d'événements et accompagnement "
                    "des étudiants et professionnels."
                ),
            ],
            "venture_role": (
                "Fondateur & Opérations Commerciales — H & D'S HUB & "
                "Import/Revente de Matériel Mobile"
            ),
            "venture_points": [
                (
                    "Création et gestion de H & D'S HUB ainsi que d'une "
                    "activité d'importation et de revente d'appareils "
                    "mobiles."
                ),
                (
                    "Maîtrise de la chaîne d'approvisionnement matérielle, "
                    "du diagnostic qualité et de la négociation commerciale."
                ),
            ],
        },
        "footer": {
            "tagline": (
                "Gallery Alabaster & True OLED Black Architecture · "
                "Python & Flask · Hanz Ofosuhene-Sintim"
            ),
        },
    },
    "en": {
        "lang_code": "en",
        "lang_label": "English",
        "meta_title": (
            "Hanz Ofosuhene-Sintim | Embedded Systems Engineer"
        ),
        "sidebar": {
            "brand_name": "Hanz Ofosuhene-Sintim",
            "brand_status": "M1 Embedded Systems · JUNIA Lille",
            "nav_label": "Primary navigation",
            "home": "Home",
            "about": "About",
            "projects": "Projects",
            "experience": "Experience",
            "education": "Education",
            "contact": "CV & Contact",
            "api_json": "Raw JSON API",
        },
        "topbar": {
            "search_placeholder": (
                "Search portfolio (C++, KiCad, STM32)..."
            ),
            "search_aria": "Search projects or skills",
            "search_clear": "Clear",
            "theme_toggle_label": "Toggle Light / Dark theme",
            "theme_light": "Light",
            "theme_dark": "Dark",
            "lang_switch_tooltip": "Basculer la langue en Français (FR)",
            "profile_name": "Hanz Ofosuhene-Sintim",
            "profile_role": "Electronics & Embedded",
        },
        "hero": {
            "eyebrow": "ELECTRONICS & EMBEDDED SYSTEMS ENGINEER",
            "greeting": "Hello",
            "name_intro": "I'm Hanz Ofosuhene-Sintim.",
            "subtitle": (
                "M1 Electronics & Embedded Systems at JUNIA Lille | "
                "BSc Computer Engineering at KNUST"
            ),
            "description": (
                "Prototyping embedded hardware systems (STM32, ESP32, "
                "Arduino), engineering modular C/C++ architectures with the "
                "GCC/GDB WSL toolchain, and modeling relational ER schemas."
            ),
            "cta": "Explore interactive orbit →",
            "secondary_cta": "Project catalog",
            "photo_caption": (
                "Hanz Ofosuhene-Sintim · Embedded Systems & Architecture"
            ),
        },
        "telemetry": {
            "eyebrow": "LIVE TELEMETRY & CURRENT FOCUS",
            "title": "Active M1 R&D · JUNIA Lille",
            "focus_project": (
                "Autonomous Street-Cleaning Robot (7-Member R&D Team)"
            ),
            "focus_stack": "STM32 · ESP32 · C/C++ · External AI Camera",
            "stat_active_label": "Active R&D",
            "stat_completed_label": "Completed",
            "stat_total_label": "Total Builds",
            "cv_btn": "CV & Contact",
            "api_btn": "Raw JSON API",
        },
        "mindmap": {
            "badge": "RADIAL ORBIT ARCHITECTURE · 3 VIEWS",
            "title": "Interactive Radial Orbit & Signal Trace",
            "subtitle": (
                "Click any orbiting capsule pill to pulse its kinetic SVG "
                "signal wire, inspect details, and filter the workspace."
            ),
            "reset_filter": "Reset project filter",
            "prev_view": "Previous view",
            "next_view": "Next view",
            "hub_title": "Hanz Ofosuhene-Sintim",
            "hub_subtitle": "M1 JUNIA · BSc KNUST",
            "detail_default_title": (
                "Click any capsule pill orbiting the center portrait"
            ),
            "detail_default_text": (
                "Each capsule triggers a high-contrast kinetic SVG signal "
                "pulse and filters matching engineering builds below."
            ),
            "detail_action_btn": "Open / Filter →",
            "views": [
                {
                    "id": "overview",
                    "label": "1 · Portfolio Overview",
                    "nodes": [
                        {
                            "tone": "copper",
                            "code": "SKILLS",
                            "title": "Core Competencies",
                            "subtitle": "MCU, C++, ER & Python",
                            "detail": (
                                "Full technical matrix: STM32, ESP32, "
                                "C/C++ GCC/GDB (WSL), ER Data Modeling & "
                                "KiCad."
                            ),
                            "href": "#skills-bento",
                            "filter": "",
                        },
                        {
                            "tone": "navy",
                            "code": "ABOUT",
                            "title": "About & Identity",
                            "subtitle": "Ghana-France Trajectory",
                            "detail": (
                                "Bilingual FR/EN Embedded Systems & "
                                "Computer Engineer."
                            ),
                            "href": "/about",
                            "filter": "",
                        },
                        {
                            "tone": "forest",
                            "code": "PROJ",
                            "title": "Projects & R&D (5)",
                            "subtitle": "2 Active R&D · 3 Completed",
                            "detail": (
                                "5 engineering builds with visual system "
                                "block diagrams and team acknowledgments."
                            ),
                            "href": "#projects-bento",
                            "filter": "",
                        },
                        {
                            "tone": "bronze",
                            "code": "LEAD",
                            "title": "Executive Leadership",
                            "subtitle": "ACES · GHAFRA · H&D",
                            "detail": (
                                "ACES Dept. President at KNUST (Tech Week, "
                                "Codefest 2026), GHAFRA Nord Lille & "
                                "H & D'S HUB."
                            ),
                            "href": "#leadership-bento",
                            "filter": "",
                        },
                        {
                            "tone": "zinc",
                            "code": "EDU",
                            "title": "Education",
                            "subtitle": "JUNIA Lille & KNUST",
                            "detail": (
                                "M1 Electronics & Embedded Systems at JUNIA "
                                "Lille | BSc Computer Engineering at KNUST."
                            ),
                            "href": "/about#education",
                            "filter": "",
                        },
                        {
                            "tone": "steel",
                            "code": "CV",
                            "title": "CV & Contact",
                            "subtitle": "Opportunities & API",
                            "detail": (
                                "Direct contact for R&D collaboration, "
                                "embedded systems roles, and JSON API."
                            ),
                            "href": "/about#contact",
                            "filter": "",
                        },
                    ],
                },
                {
                    "id": "stack",
                    "label": "2 · System & HW-SW Stack",
                    "nodes": [
                        {
                            "tone": "copper",
                            "code": "MCU",
                            "title": "Microcontrollers",
                            "subtitle": "STM32 · ESP32 · Arduino",
                            "detail": (
                                "Real-time embedded control across STM32, "
                                "ESP32, MSP430, and Arduino MCUs."
                            ),
                            "href": "#projects-bento",
                            "filter": "stm32 esp32 arduino",
                        },
                        {
                            "tone": "navy",
                            "code": "C++",
                            "title": "C/C++ & WSL / GDB",
                            "subtitle": "OOP & GCC/GDB Toolchain",
                            "detail": (
                                "Modular OOP class hierarchies, data "
                                "structures, and GCC/GDB debugging in WSL."
                            ),
                            "href": "#projects-bento",
                            "filter": "c++",
                        },
                        {
                            "tone": "forest",
                            "code": "DATA",
                            "title": "Data Modeling & ER",
                            "subtitle": "Associative Tables & 3NF",
                            "detail": (
                                "Entity-Relationship (ER) diagrams, M:N "
                                "associative tables, and 3NF schemas."
                            ),
                            "href": "#projects-bento",
                            "filter": "er schema",
                        },
                        {
                            "tone": "steel",
                            "code": "API",
                            "title": "Python & Flask APIs",
                            "subtitle": "Jinja2 · i18n · JSON",
                            "detail": (
                                "Python 3, Flask, Jinja2, header-based "
                                "i18n localization, and JSON persistence."
                            ),
                            "href": "#projects-bento",
                            "filter": "python flask",
                        },
                        {
                            "tone": "copper",
                            "code": "SENS",
                            "title": "Sensors & AI Camera",
                            "subtitle": "Ultrasonic · Relays · PWM",
                            "detail": (
                                "External AI camera module, ultrasonic "
                                "distance telemetry, relays, and motors."
                            ),
                            "href": "#projects-bento",
                            "filter": "ultrasonic camera sensor",
                        },
                        {
                            "tone": "bronze",
                            "code": "HW",
                            "title": "KiCad & Prototyping",
                            "subtitle": "Schematics & Integration",
                            "detail": (
                                "Circuit schematic capture, PCB layout "
                                "in KiCad, and hardware system testing."
                            ),
                            "href": "#skills-bento",
                            "filter": "embedded",
                        },
                    ],
                },
                {
                    "id": "leadership",
                    "label": "3 · Leadership & Parcours",
                    "nodes": [
                        {
                            "tone": "bronze",
                            "code": "ACES",
                            "title": "ACES Dept. President",
                            "subtitle": "Tech Week · Codefest 2026",
                            "detail": (
                                "ACES Department President at KNUST: "
                                "Tech Week, Codefest 2026, Faculty Games "
                                "& Digital Media Expansion."
                            ),
                            "href": "#leadership-bento",
                            "filter": "",
                        },
                        {
                            "tone": "steel",
                            "code": "GHAFRA",
                            "title": "GHAFRA Nord Lille",
                            "subtitle": "Strategy & Organizing",
                            "detail": (
                                "Strategic planning, regional operations, "
                                "and community organizing in Lille."
                            ),
                            "href": "#leadership-bento",
                            "filter": "",
                        },
                        {
                            "tone": "copper",
                            "code": "HUB",
                            "title": "H & D'S HUB",
                            "subtitle": "Mobile Hardware Venture",
                            "detail": (
                                "Commercial operations founder for H & D'S "
                                "HUB and mobile hardware import/resale."
                            ),
                            "href": "#leadership-bento",
                            "filter": "",
                        },
                        {
                            "tone": "zinc",
                            "code": "JUNIA",
                            "title": "JUNIA Lille (M1)",
                            "subtitle": "Autonomous Robotics R&D",
                            "detail": (
                                "M1 Electronics & Embedded Systems at JUNIA "
                                "Lille — 7-member street-cleaning robot R&D."
                            ),
                            "href": "#projects-bento",
                            "filter": "junia",
                        },
                        {
                            "tone": "navy",
                            "code": "KNUST",
                            "title": "KNUST (BSc)",
                            "subtitle": "Computer Engineering",
                            "detail": (
                                "BSc Computer Engineering at KNUST and "
                                "Project Lead for C++ OOP systems."
                            ),
                            "href": "#projects-bento",
                            "filter": "c++",
                        },
                        {
                            "tone": "forest",
                            "code": "I18N",
                            "title": "Bilateral FR / EN",
                            "subtitle": "Cross-Border Engineering",
                            "detail": (
                                "Bilingual French/English technical "
                                "collaboration across France and Ghana."
                            ),
                            "href": "/about#contact",
                            "filter": "",
                        },
                    ],
                },
            ],
        },
        "status": {
            "completed": "Completed",
            "in_progress": "In Progress — Active R&D",
            "filter_all": "All",
            "filter_completed": "Completed",
            "filter_in_progress": "In Progress (R&D)",
            "toggle_btn": "Toggle Status",
        },
        "studio": {
            "new_project_btn": "+ New Project",
            "modal_title": "Project Studio — Create New Project",
            "modal_subtitle": (
                "Persisted directly to projects.json (Localhost Studio)."
            ),
            "title_en": "Project Title (EN)",
            "title_fr": "Project Title (FR)",
            "category": "Category",
            "status": "Lifecycle Status",
            "tone": "Accent Color",
            "tech_stack": "Tech Stack (comma-separated)",
            "block_diagram": "System Block Diagram (3-4 steps separated by |)",
            "summary_en": "Technical Summary (EN)",
            "summary_fr": "Technical Summary (FR)",
            "highlights_en": "Technical Highlights EN (separated by |)",
            "highlights_fr": "Technical Highlights FR (separated by |)",
            "team_ack": "Team & Collaborators Acknowledgment",
            "save_btn": "Save to projects.json",
            "cancel_btn": "Cancel",
        },
        "drawer": {
            "badge": "ENGINEERING CASE STUDY",
            "close_aria": "Close case study drawer",
            "block_diagram_title": "Visual System Block Diagram",
            "highlights_title": "Technical Architecture & Highlights",
            "tech_stack_title": "Toolchain & Stack",
            "team_title": "Team & Collaborators Acknowledgment",
            "team_edit_label": (
                "Update Teammate Names & Credits (Localhost):"
            ),
            "team_save_btn": "Save Teammate Credits",
            "open_case_study": "Open engineering case study drawer",
        },
        "bento": {
            "projects_title": "Projects & Active R&D",
            "projects_subtitle": (
                "Click + on any card to open its block diagram & team drawer."
            ),
            "view_all_projects": "Catalog (5) →",
            "skills_title": "Circular Skill Matrix",
            "skills_subtitle": (
                "Color-coded technical capsules by domain."
            ),
            "leadership_title": "Executive Leadership",
            "leadership_subtitle": (
                "Presidency, strategic organizing & hardware ventures."
            ),
            "leadership_more": "Full leadership profile →",
            "no_search_results": (
                "No items match your current filter."
            ),
            "domains": {
                "copper": {
                    "title": "Embedded MCUs & Sensors",
                    "code": "EMB",
                },
                "navy": {
                    "title": "C/C++, OOP & WSL GCC/GDB",
                    "code": "C++",
                },
                "forest": {
                    "title": "ER Data Modeling & Python",
                    "code": "DATA",
                },
                "bronze": {
                    "title": "Leadership & Ventures",
                    "code": "LEAD",
                },
                "zinc": {
                    "title": "Academic Formation & R&D",
                    "code": "EDU",
                },
                "steel": {
                    "title": "Bilingual & Direct Contact",
                    "code": "CV",
                },
            },
        },
        "projects_page": {
            "title": "Engineering Projects Catalog",
            "subtitle": (
                "Completed engineering builds and active M1 R&D systems "
                "backed by projects.json."
            ),
            "filter_all": "All Categories",
            "filter_embedded": "Embedded & Hardware",
            "filter_software": "Software & Systems",
            "empty": "No projects found matching this filter.",
        },
        "about_page": {
            "title": "Trajectory, Leadership & System Architecture",
            "education_title": "Academic Background",
            "skills_title": "Technical Stack & Toolchains",
            "leadership_title": (
                "Executive Leadership, Organizing & Commercial Ventures"
            ),
            "contact_title": "CV & Direct Contact",
            "contact_text": (
                "Open to connecting regarding embedded systems, autonomous "
                "robotics R&D, and engineering opportunities."
            ),
            "aces_role": (
                "ACES Department President — KNUST (Association of "
                "Computer Engineering Students)"
            ),
            "aces_points": [
                (
                    "Directed full executive governance and official student "
                    "representation for the Computer Engineering department."
                ),
                (
                    "Spearheaded flagship technical and community programs: "
                    "Tech Week, Codefest 2026, and Faculty Games."
                ),
                (
                    "Led the Digital Media Expansion initiative to modernize "
                    "departmental communication and technical visibility."
                ),
            ],
            "ghafra_role": (
                "Strategic Planning & Organizing Leadership — GHAFRA Nord "
                "(Lille, France)"
            ),
            "ghafra_points": [
                (
                    "Driving strategic planning, event coordination, and "
                    "community organizing across the Lille metropolitan area."
                ),
                (
                    "Building cross-cultural support networks for students "
                    "and professionals in Northern France."
                ),
            ],
            "venture_role": (
                "Founder & Commercial Operations — H & D'S HUB & Mobile "
                "Hardware Enterprise"
            ),
            "venture_points": [
                (
                    "Founded and operated H & D'S HUB alongside a commercial "
                    "mobile hardware import, diagnostics, and resale venture."
                ),
                (
                    "Managed end-to-end device sourcing, hardware quality "
                    "verification, pricing strategy, and client delivery."
                ),
            ],
        },
        "footer": {
            "tagline": (
                "Gallery Alabaster & True OLED Black Architecture · "
                "Python & Flask · Hanz Ofosuhene-Sintim"
            ),
        },
    },
}
