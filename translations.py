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
        "gallery": {
            "aria": "Galerie photo",
            "prev": "Photo précédente",
            "next": "Photo suivante",
            "expand": "Agrandir",
            "expand_aria": "Ouvrir la photo en plein écran",
            "close": "Fermer",
            "dots_label": "Choisir une photo",
            "slides": [
                {
                    "id": "lille",
                    "file": "gallery-lille.jpg",
                    "caption": "Palais Rameau & architecture lilloise",
                    "alt": "Palais Rameau et architecture de Lille",
                },
                {
                    "id": "lab",
                    "file": "gallery-lab.jpg",
                    "caption": (
                        "JUNIA Lille — M1 Microélectronique & "
                        "Systèmes Embarqués"
                    ),
                    "alt": "Laboratoire d'électronique à JUNIA Lille",
                },
                {
                    "id": "knust",
                    "file": "gallery-knust.jpg",
                    "caption": "KNUST — Présidence ACES & Codefest",
                    "alt": "Campus KNUST, présidence ACES et Codefest",
                },
                {
                    "id": "hardware",
                    "file": "gallery-hardware.jpg",
                    "caption": (
                        "Matériel embarqué — STM32 · ESP32 · "
                        "prototypage KiCad"
                    ),
                    "alt": "Cartes de prototypage embarqué",
                },
            ],
        },
        "dock": {
            "aria": "Télémétrie rapide et navigation",
            "projects": "Projets d'ingénierie",
            "completed": "Terminés",
            "active": "R&D active",
            "architecture": "Architecture clé :",
            "architecture_value": "C++ · STM32/ESP32 · Python · KiCad",
            "leadership": "Leadership exécutif :",
            "leadership_value": "Président ACES · GHAFRA Nord",
        },
        "palette": {
            "badge_page": "Page",
            "badge_project": "Projet",
            "badge_leadership": "Leadership",
            "role_aces": "Président du département ACES",
            "role_ghafra": "GHAFRA Nord Lille — Planification stratégique",
            "role_hub": "H & D'S HUB — Fondateur",
            "listbox_label": "Résultats de recherche",
            "suggested": "Accès rapide",
            "results": "Résultats",
            "empty": "Aucun résultat pour",
            "hint_navigate": "naviguer",
            "hint_open": "ouvrir",
            "hint_close": "fermer",
        },
        "beacon": {
            "aria": "Télémétrie en direct de l'ingénieur",
            "title": "TÉLÉMÉTRIE EN DIRECT",
            "status_label": "Statut",
            "status": "Disponible pour R&D Embarqué & Logiciel / Stages",
            "location_label": "Lieu & heure locale",
            "location": "Lille, France",
            "focus_label": "Focus actuel",
            "focus": "M1 JUNIA Lille · Robotique autonome & systèmes C++",
            "copy_email": "Copier l'e-mail",
            "copied": "Copié ✓",
            "copy_failed": "Copie impossible",
        },
        "mindmap": {
            "badge": "ORBITE RADIALE INTERACTIVE · 3 VUES",
            "title": "Cartographie Radiale & Flux Système",
            "subtitle": (
                "Cliquez sur une capsule orbitale pour pulser son flux "
                "SVG, inspecter les détails et ouvrir la page ou le filtre "
                "de projets correspondant."
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
                "et ouvre la section ou le filtre de projets correspondant."
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
            "filtered_by": "FILTRE",
            "clear_filter": "Effacer le filtre",
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
        "gallery": {
            "aria": "Photo gallery",
            "prev": "Previous photo",
            "next": "Next photo",
            "expand": "Expand",
            "expand_aria": "Open photo in fullscreen",
            "close": "Close",
            "dots_label": "Choose a photo",
            "slides": [
                {
                    "id": "lille",
                    "file": "gallery-lille.jpg",
                    "caption": "Palais Rameau & Lille Architecture",
                    "alt": "Palais Rameau and Lille architecture",
                },
                {
                    "id": "lab",
                    "file": "gallery-lab.jpg",
                    "caption": (
                        "JUNIA Lille — M1 Microelectronics & "
                        "Embedded Systems"
                    ),
                    "alt": "Electronics lab at JUNIA Lille",
                },
                {
                    "id": "knust",
                    "file": "gallery-knust.jpg",
                    "caption": "KNUST — ACES Presidency & Codefest",
                    "alt": "KNUST campus, ACES presidency and Codefest",
                },
                {
                    "id": "hardware",
                    "file": "gallery-hardware.jpg",
                    "caption": (
                        "Embedded Hardware — STM32 · ESP32 · "
                        "KiCad Prototyping"
                    ),
                    "alt": "Embedded prototyping boards",
                },
            ],
        },
        "dock": {
            "aria": "Quick telemetry and navigation",
            "projects": "Engineering Projects",
            "completed": "Completed",
            "active": "Active R&D",
            "architecture": "Core Architecture:",
            "architecture_value": "C++ · STM32/ESP32 · Python · KiCad",
            "leadership": "Executive Leadership:",
            "leadership_value": "ACES President · GHAFRA Nord",
        },
        "palette": {
            "badge_page": "Page",
            "badge_project": "Project",
            "badge_leadership": "Leadership",
            "role_aces": "ACES Department President",
            "role_ghafra": "GHAFRA Nord Lille — Strategic Planning",
            "role_hub": "H & D'S HUB — Founder",
            "listbox_label": "Search results",
            "suggested": "Quick jump",
            "results": "Results",
            "empty": "No results for",
            "hint_navigate": "navigate",
            "hint_open": "open",
            "hint_close": "close",
        },
        "beacon": {
            "aria": "Live engineer telemetry",
            "title": "LIVE ENGINEER TELEMETRY",
            "status_label": "Status",
            "status": "Available for Embedded & Software R&D / Internships",
            "location_label": "Location & local time",
            "location": "Lille, France",
            "focus_label": "Current focus",
            "focus": "M1 JUNIA Lille · Autonomous Robotics & C++ Systems",
            "copy_email": "Copy Email",
            "copied": "Copied ✓",
            "copy_failed": "Copy failed",
        },
        "mindmap": {
            "badge": "RADIAL ORBIT ARCHITECTURE · 3 VIEWS",
            "title": "Interactive Radial Orbit & Signal Trace",
            "subtitle": (
                "Click any orbiting capsule pill to pulse its kinetic SVG "
                "signal wire, inspect details, then jump to the matching "
                "page or project filter."
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
                "pulse and opens the matching section or project filter."
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
            "filtered_by": "FILTER",
            "clear_filter": "Clear filter",
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

# Update FR
UI_TEXT["fr"]["sidebar"]["api_inspector"] = "Inspecteur API"
UI_TEXT["fr"]["drawer"]["tradeoffs_title"] = (
    "Arbitrages d'Ingénierie & Décisions d'Architecture"
)
UI_TEXT["fr"]["drawer"]["datasheet_btn"] = "Fiche +"

UI_TEXT["fr"]["projects_page"].update(
    {
        "eyebrow": "ÉTABLI D'INGÉNIERIE R&D & SYSTÈMES",
        "title": "Établi d'Ingénierie R&D & Catalogue Systèmes",
        "subtitle": (
            "Filtrage instantané sans rechargement, piste R&D active avec "
            "pipeline de jalons interactif et fiches techniques schémas-blocs."
        ),
        "status_all": "Tous les systèmes",
        "status_completed": "🟢 Systèmes Terminés",
        "status_active": "🟠 R&D Active",
        "tech_filter_label": "STACK TECHNIQUE :",
        "tech_all": "Toutes les stacks",
        "spotlight_badge": "PISTE R&D ACTIVE · PIPELINE DE JALONS",
        "spotlight_title": "Systèmes en Recherche & Développement Actif",
        "spotlight_subtitle": (
            "Cliquez sur une étape du pipeline pour inspecter ses livrables "
            "ou sur + pour ouvrir la fiche technique complète."
        ),
        "completed_badge": "SYSTÈMES VALIDÉS · GRILLE BENTO 2 COLONNES",
        "completed_title": "Systèmes & Architectures Terminés",
        "completed_subtitle": (
            "Réalisations matérielles et logicielles validées avec "
            "schémas-blocs et arbitrages d'architecture."
        ),
        "pipeline_label": "PIPELINE DE JALONS R&D (CLIQUEZ SUR UNE ÉTAPE)",
        "open_datasheet": "Fiche +",
        "tradeoffs_preview": "Arbitrage clé :",
    }
)

UI_TEXT["fr"]["experience_page"] = {
    "eyebrow": "GOUVERNANCE EXÉCUTIVE · STRATÉGIE · ENTREPRENEURIAT",
    "title": "Leadership Exécutif & Opérations Stratégiques",
    "subtitle": (
        "Chronologie interactive des mandats exécutifs, de l'organisation "
        "régionale en France et des opérations commerciales matérielles."
    ),
    "metrics": [
        {"value": "3", "label": "Mandats Directeurs", "tone": "bronze"},
        {"value": "500+", "label": "Étudiants Représentés (ACES)", "tone": "navy"},
        {"value": "2", "label": "Pôles (Ghana · France)", "tone": "forest"},
    ],
    "filters": {
        "all": "Tous les mandats",
        "governance": "Gouvernance Académique",
        "strategy": "Stratégie & Communauté",
        "venture": "Entrepreneuriat Matériel",
    },
    "roles": [
        {
            "id": "role-aces",
            "category": "governance",
            "tone": "bronze",
            "code": "ACES · KNUST",
            "period": "Mandat Exécutif · KNUST",
            "location": "Kumasi, Ghana · Département Génie Informatique",
            "title": "Président du Département ACES (Association of Computer Engineering Students)",
            "summary": (
                "Direction exécutive de l'association des étudiants en génie "
                "informatique à KNUST, représentation officielle auprès de la "
                "faculté et pilotage des programmes techniques majeurs."
            ),
            "pillars": [
                {
                    "tag": "Tech Week & Codefest 2026",
                    "detail": (
                        "Direction générale de la Tech Week départementale et "
                        "de Codefest 2026 : hackathons, ateliers embarqués/logiciels "
                        "et jurys d'ingénierie."
                    ),
                },
                {
                    "tag": "Faculty Games & Cohésion",
                    "detail": (
                        "Organisation et mobilisation logistique pour les "
                        "Faculty Games, renforçant l'esprit de corps inter-promotions."
                    ),
                },
                {
                    "tag": "Digital Media Expansion",
                    "detail": (
                        "Modernisation complète de l'identité numérique et "
                        "des canaux de communication technique du département ACES."
                    ),
                },
                {
                    "tag": "Bien-être Étudiant & Représentation",
                    "detail": (
                        "Porte-parole officiel des étudiants auprès de "
                        "l'administration académique, mentorat et défense des "
                        "intérêts étudiants."
                    ),
                },
            ],
            "badges": [
                "Tech Week",
                "Codefest 2026",
                "Faculty Games",
                "Digital Media Expansion",
                "Bien-être Étudiant",
            ],
        },
        {
            "id": "role-ghafra",
            "category": "strategy",
            "tone": "steel",
            "code": "GHAFRA NORD · LILLE",
            "period": "Actif · Hauts-de-France",
            "location": "Lille, France · Métropole Européenne de Lille",
            "title": "Responsable Planification Stratégique & Organisation — GHAFRA Nord",
            "summary": (
                "Structuration stratégique, coordination opérationnelle et "
                "mobilisation communautaire au sein de GHAFRA Nord à Lille."
            ),
            "pillars": [
                {
                    "tag": "Planification Stratégique",
                    "detail": (
                        "Élaboration des feuilles de route trimestrielles, "
                        "allocation des ressources et coordination des équipes "
                        "régionales dans le Nord de la France."
                    ),
                },
                {
                    "tag": "Organisation Communautaire",
                    "detail": (
                        "Accueil, intégration administrative et mise en réseau "
                        "des étudiants et professionnels ghanéens en France."
                    ),
                },
                {
                    "tag": "Opérations Lille & Partenariats",
                    "detail": (
                        "Pilotage logistique des événements culturels et "
                        "institutionnels à Lille."
                    ),
                },
            ],
            "badges": [
                "Planification Stratégique",
                "Organisation Communautaire",
                "Opérations Lille",
                "Coordination Franco-Ghanéenne",
            ],
        },
        {
            "id": "role-hub",
            "category": "venture",
            "tone": "copper",
            "code": "H & D'S HUB · VENTURE",
            "period": "Fondateur & Opérations",
            "location": "Opérations Commerciales & Import Matériel",
            "title": "Fondateur & Direction Opérationnelle — H & D'S HUB & Matériel Mobile",
            "summary": (
                "Création et gestion de H & D'S HUB ainsi que d'une activité "
                "commerciale d'importation, diagnostic matériel et revente "
                "d'appareils mobiles."
            ),
            "pillars": [
                {
                    "tag": "Importation & Chaîne d'Approvisionnement",
                    "detail": (
                        "Sourcing international, négociation fournisseurs et "
                        "gestion des flux logistiques d'équipements mobiles."
                    ),
                },
                {
                    "tag": "Diagnostic Matériel & Contrôle Qualité",
                    "detail": (
                        "Inspection matérielle systématique, tests de "
                        "composants et validation fonctionnelle avant mise en vente."
                    ),
                },
                {
                    "tag": "Opérations Commerciales & Revente",
                    "detail": (
                        "Stratégie tarifaire, gestion de trésorerie, relation "
                        "clientèle et croissance de la marque H & D'S HUB."
                    ),
                },
            ],
            "badges": [
                "H & D'S HUB",
                "Import & Revente Mobile",
                "Diagnostic Matériel",
                "Gestion Commerciale",
            ],
        },
    ],
}

UI_TEXT["fr"]["education_page"] = {
    "eyebrow": "FORMATION D'INGÉNIEUR · RECHERCHE R&D · TÉLÉMÉTRIE",
    "title": "Formation Académique, R&D & Console API",
    "subtitle": (
        "Parcours d'ingénierie entre la France (JUNIA Lille) et le Ghana "
        "(KNUST, PRESEC Legon), couplé à l'inspecteur d'API JSON temps réel."
    ),
    "institutions": [
        {
            "id": "junia",
            "tone": "zinc",
            "code": "M1 · LILLE, FRANCE",
            "period": "En cours · Cycle Ingénieur M1",
            "school": "JUNIA Lille — Grande École d'Ingénieurs",
            "degree": "M1 Microélectronique & Systèmes Embarqués",
            "location": "Lille, France",
            "summary": (
                "Formation approfondie en microélectronique, architecture des "
                "systèmes embarqués, programmation bas niveau C/C++ et "
                "prototypage robotique collaboratif."
            ),
            "highlights": [
                "R&D Active : Prototype de Robot Autonome de Nettoyage Urbain au sein d'une équipe de 7 élèves-ingénieurs.",
                "Conception de firmware C/C++ sur STM32 et ESP32, commande moteur PWM et intégration d'un module caméra IA externe.",
                "Conception électronique, schématique et routage PCB sous KiCad.",
            ],
            "modules": [
                "STM32 / ESP32",
                "Microélectronique",
                "C/C++ Embarqué",
                "Fusion Capteurs",
                "KiCad PCB",
                "Robotique Autonome",
            ],
        },
        {
            "id": "knust",
            "tone": "navy",
            "code": "BSc · KUMASI, GHANA",
            "period": "Diplômé · BSc Engineering",
            "school": "KNUST — Kwame Nkrumah University of Science & Technology",
            "degree": "BSc Computer Engineering (Génie Informatique)",
            "location": "Kumasi, Ghana",
            "summary": (
                "Ingénierie informatique couvrant l'architecture des "
                "ordinateurs, les systèmes embarqués, la programmation orientée "
                "objet C++ et la modélisation de bases de données."
            ),
            "highlights": [
                "Président du Département ACES : direction de la Tech Week, Codefest 2026, Faculty Games et Digital Media Expansion.",
                "Chef de Projet pour le Système C++ de Gestion de Centre Commercial (POO, chaîne GCC/GDB sous WSL).",
                "Modélisation Entité-Association (ER), tables associatives et normalisation 3NF pour systèmes logistiques.",
            ],
            "modules": [
                "C++ & POO",
                "GCC / GDB (WSL)",
                "Schémas ER & 3NF",
                "Arduino & Capteurs",
                "Architecture Système",
                "Présidence ACES",
            ],
        },
        {
            "id": "presec",
            "tone": "forest",
            "code": "SCIENCES · ACCRA, GHANA",
            "period": "Enseignement Secondaire",
            "school": "Presbyterian Boys' Secondary School (PRESEC Legon)",
            "degree": "General Science — Mathématiques, Physique & Sciences",
            "location": "Legon, Accra, Ghana",
            "summary": (
                "Formation scientifique d'excellence (tradition Odadeɛ) axée "
                "sur la physique, les mathématiques avancées et la rigueur "
                "analytique."
            ),
            "highlights": [
                "Socle intensif en mathématiques pures, mécanique, électromagnétisme et algorithmique.",
                "Culture d'excellence académique et de leadership collectif.",
            ],
            "modules": [
                "Physique & Électronique",
                "Mathématiques Avancées",
                "Analyse Scientifique",
            ],
        },
    ],
}

UI_TEXT["fr"]["api_inspector_page"] = {
    "eyebrow": "CONSOLE DE TÉLÉMÉTRIE REST · JSON EN DIRECT",
    "title": "Inspecteur d'API Temps Réel & Télémétrie JSON",
    "subtitle": (
        "Exécutez de vraies requêtes HTTP GET contre /api/projects, mesurez "
        "la latence en millisecondes et inspectez la charge utile JSON."
    ),
    "endpoints_label": "POINTS D'ENTRÉE REST DISPONIBLES :",
    "ping_btn": "⚡ Ping /api/projects",
    "copy_btn": "Copier JSON",
    "copied_btn": "JSON Copié ✓",
    "raw_btn": "Ouvrir JSON Brut ↗",
    "full_console_link": "Ouvrir l'Inspecteur API plein écran →",
    "status_label": "STATUT HTTP",
    "latency_label": "LATENCE RTT",
    "size_label": "TAILLE PAYLOAD",
    "records_label": "PROJETS REÇUS",
    "schema_title": "Garanties du Schéma REST (`/api/projects`)",
    "schema_points": [
        "Sérialisation JSON UTF-8 directe depuis `projects.json` sans surcharge ORM.",
        "Filtrage par paramètre de requête : `?status=in_progress`, `?status=completed` ou `?slug=<slug>`.",
        "Chaque entrée expose les clés bilingues (`en`, `fr`), `block_diagram`, `milestones`, `tradeoffs` et `team_acknowledgment`.",
    ],
}

# Update EN
UI_TEXT["en"]["sidebar"]["api_inspector"] = "API Inspector"
UI_TEXT["en"]["drawer"]["tradeoffs_title"] = (
    "Engineering Tradeoffs & Design Decisions"
)
UI_TEXT["en"]["drawer"]["datasheet_btn"] = "Datasheet +"

UI_TEXT["en"]["projects_page"].update(
    {
        "eyebrow": "R&D ENGINEERING WORKBENCH & SYSTEMS CATALOG",
        "title": "R&D Engineering Workbench & Systems Catalog",
        "subtitle": (
            "Zero-reload client-side filtering, Active R&D milestone pipeline, "
            "and slide-over system block-diagram datasheets."
        ),
        "status_all": "All Systems",
        "status_completed": "🟢 Completed Systems",
        "status_active": "🟠 Active R&D",
        "tech_filter_label": "TECH STACK:",
        "tech_all": "All Tech",
        "spotlight_badge": "ACTIVE R&D SPOTLIGHT TRACK · MILESTONE PIPELINE",
        "spotlight_title": "Active Research & Development Spotlight",
        "spotlight_subtitle": (
            "Click any stage in the milestone pipeline to inspect its live "
            "deliverables, or click + to open the full engineering datasheet."
        ),
        "completed_badge": "COMPLETED SYSTEMS · 2-COLUMN BENTO GRID",
        "completed_title": "Completed Engineering Systems",
        "completed_subtitle": (
            "Verified hardware and software builds with sequential block "
            "diagrams and architectural tradeoffs."
        ),
        "pipeline_label": "R&D MILESTONE PIPELINE (CLICK STAGE TO INSPECT)",
        "open_datasheet": "Datasheet +",
        "tradeoffs_preview": "Key Tradeoff:",
    }
)

UI_TEXT["en"]["experience_page"] = {
    "eyebrow": "EXECUTIVE GOVERNANCE · REGIONAL STRATEGY · HARDWARE VENTURES",
    "title": "Executive Leadership & Venture Operations",
    "subtitle": (
        "Interactive executive timeline spanning departmental presidency at "
        "KNUST, strategic organizing in Lille, and commercial hardware operations."
    ),
    "metrics": [
        {"value": "3", "label": "Executive Mandates", "tone": "bronze"},
        {"value": "500+", "label": "Engineering Students Represented", "tone": "navy"},
        {"value": "2", "label": "Operating Regions (GH · FR)", "tone": "forest"},
    ],
    "filters": {
        "all": "All Mandates",
        "governance": "Academic Governance",
        "strategy": "Strategy & Organizing",
        "venture": "Hardware Venture",
    },
    "roles": [
        {
            "id": "role-aces",
            "category": "governance",
            "tone": "bronze",
            "code": "ACES · KNUST",
            "period": "Executive Term · KNUST",
            "location": "Kumasi, Ghana · Department of Computer Engineering",
            "title": "ACES Department President (Association of Computer Engineering Students)",
            "summary": (
                "Directed full executive governance, financial stewardship, "
                "and official student representation for the Computer "
                "Engineering department at KNUST."
            ),
            "pillars": [
                {
                    "tag": "Tech Week & Codefest 2026",
                    "detail": (
                        "Spearheaded the flagship departmental Tech Week and "
                        "Codefest 2026 hackathon, uniting hardware/software "
                        "project teams with industry mentors."
                    ),
                },
                {
                    "tag": "Faculty Games & Department Cohesion",
                    "detail": (
                        "Organized cross-cohort participation and logistics "
                        "for the Faculty Games, strengthening student community."
                    ),
                },
                {
                    "tag": "Digital Media Expansion",
                    "detail": (
                        "Modernized ACES digital communications, technical "
                        "spotlights, and departmental media presence."
                    ),
                },
                {
                    "tag": "Student Welfare & Representation",
                    "detail": (
                        "Served as the primary student voice before faculty "
                        "leadership, championing academic support and lab access."
                    ),
                },
            ],
            "badges": [
                "Tech Week",
                "Codefest 2026",
                "Faculty Games",
                "Digital Media Expansion",
                "Student Welfare",
            ],
        },
        {
            "id": "role-ghafra",
            "category": "strategy",
            "tone": "steel",
            "code": "GHAFRA NORD · LILLE",
            "period": "Active · Northern France",
            "location": "Lille, France · Hauts-de-France",
            "title": "Strategic Planning & Organizing Lead — GHAFRA Nord (Lille, France)",
            "summary": (
                "Driving strategic planning, operational logistics, and "
                "community organizing across the Lille metropolitan area."
            ),
            "pillars": [
                {
                    "tag": "Strategic Planning",
                    "detail": (
                        "Structuring regional roadmaps, event calendars, and "
                        "cross-team execution for GHAFRA Nord in Lille."
                    ),
                },
                {
                    "tag": "Community Organizing & Onboarding",
                    "detail": (
                        "Coordinating student and professional integration, "
                        "housing guidance, and peer networks in Northern France."
                    ),
                },
                {
                    "tag": "Lille Regional Operations",
                    "detail": (
                        "Leading venue logistics, institutional outreach, and "
                        "cultural programming across Lille."
                    ),
                },
            ],
            "badges": [
                "Strategic Planning",
                "Community Organizing",
                "Lille Operations",
                "Cross-Cultural Leadership",
            ],
        },
        {
            "id": "role-hub",
            "category": "venture",
            "tone": "copper",
            "code": "H & D'S HUB · VENTURE",
            "period": "Founder & Commercial Ops",
            "location": "Commercial Hardware & Import Operations",
            "title": "Founder & Commercial Operations — H & D'S HUB & Mobile Hardware Venture",
            "summary": (
                "Founded and operated H & D'S HUB alongside a commercial "
                "mobile hardware import, diagnostics, and resale enterprise."
            ),
            "pillars": [
                {
                    "tag": "Supply Chain & Hardware Import",
                    "detail": (
                        "Managed supplier sourcing, import logistics, and "
                        "inventory allocation for consumer mobile hardware."
                    ),
                },
                {
                    "tag": "Hardware Diagnostics & QA",
                    "detail": (
                        "Performed systematic device diagnostics, component "
                        "verification, and quality grading prior to resale."
                    ),
                },
                {
                    "tag": "Commercial Pricing & Client Fulfillment",
                    "detail": (
                        "Directed unit economics, pricing strategy, and "
                        "end-to-end customer fulfillment."
                    ),
                },
            ],
            "badges": [
                "H & D'S HUB",
                "Mobile Hardware Import/Resale",
                "Hardware Diagnostics & QA",
                "Commercial Operations",
            ],
        },
    ],
}

UI_TEXT["en"]["education_page"] = {
    "eyebrow": "ACADEMIC FORMATION · EMBEDDED R&D · LIVE TELEMETRY",
    "title": "Academic Formation, R&D & Live API Telemetry",
    "subtitle": (
        "Cross-border engineering formation across JUNIA Lille (France), "
        "KNUST (Kumasi), and PRESEC Legon, paired with a live JSON API console."
    ),
    "institutions": [
        {
            "id": "junia",
            "tone": "zinc",
            "code": "M1 · LILLE, FRANCE",
            "period": "Active · M1 Graduate Engineering",
            "school": "JUNIA Lille — Graduate School of Science & Engineering",
            "degree": "M1 Microelectronics & Embedded Systems",
            "location": "Lille, France",
            "summary": (
                "Graduate engineering specialization in microelectronics, "
                "embedded microcontroller systems, real-time C/C++ firmware, "
                "and collaborative robotics R&D."
            ),
            "highlights": [
                "Active R&D: 7-Member Autonomous Street-Cleaning Robot Prototype engineered for urban Lille pavements.",
                "Developing embedded C/C++ control firmware across STM32 and ESP32 MCUs with external AI camera integration.",
                "Hardware schematic capture, sensor conditioning, and PCB layout in KiCad.",
            ],
            "modules": [
                "STM32 / ESP32",
                "Microelectronics",
                "Embedded C/C++",
                "Sensor Fusion",
                "KiCad PCB",
                "Autonomous Robotics",
            ],
        },
        {
            "id": "knust",
            "tone": "navy",
            "code": "BSc · KUMASI, GHANA",
            "period": "Graduated · BSc Engineering",
            "school": "KNUST — Kwame Nkrumah University of Science & Technology",
            "degree": "BSc Computer Engineering",
            "location": "Kumasi, Ghana",
            "summary": (
                "Rigorous undergraduate training across computer architecture, "
                "embedded hardware, object-oriented C++ software systems, and "
                "relational data modeling."
            ),
            "highlights": [
                "Elected ACES Department President: led Tech Week, Codefest 2026, Faculty Games, and Digital Media Expansion.",
                "Project Lead for the C++ Shopping Mall Management System (OOP class hierarchies under WSL GCC/GDB).",
                "Engineered normalized 3NF Entity-Relationship (ER) schemas and closed-loop Arduino ultrasonic control systems.",
            ],
            "modules": [
                "C++ & OOP",
                "GCC / GDB (WSL)",
                "ER Schemas & 3NF",
                "Arduino & Sensors",
                "Computer Architecture",
                "ACES Presidency",
            ],
        },
        {
            "id": "presec",
            "tone": "forest",
            "code": "SCIENCE · ACCRA, GHANA",
            "period": "Secondary Education",
            "school": "Presbyterian Boys' Secondary School (PRESEC Legon)",
            "degree": "General Science (Physics, Advanced Mathematics, Chemistry)",
            "location": "Legon, Accra, Ghana",
            "summary": (
                "Foundational scientific training at Ghana's premier "
                "science secondary institution (Odadeɛ), emphasizing physics, "
                "calculus, and analytical problem solving."
            ),
            "highlights": [
                "Intensive grounding in mechanics, electromagnetism, calculus, and quantitative reasoning.",
                "Cultivated disciplined analytical habits and collaborative leadership.",
            ],
            "modules": [
                "Physics & Electromagnetism",
                "Further Mathematics",
                "Analytical Science",
            ],
        },
    ],
}

UI_TEXT["en"]["api_inspector_page"] = {
    "eyebrow": "LIVE REST TELEMETRY CONSOLE · JSON API",
    "title": "Interactive API Inspector & Live JSON Telemetry",
    "subtitle": (
        "Ping `/api/projects` in real time, inspect the live HTTP 200 payload, "
        "and measure round-trip response latency in milliseconds."
    ),
    "endpoints_label": "LIVE REST ENDPOINTS:",
    "ping_btn": "⚡ Ping /api/projects",
    "copy_btn": "Copy JSON",
    "copied_btn": "Copied JSON ✓",
    "raw_btn": "Open Raw JSON ↗",
    "full_console_link": "Open Fullscreen API Inspector →",
    "status_label": "HTTP STATUS",
    "latency_label": "RESPONSE TIME",
    "size_label": "PAYLOAD SIZE",
    "records_label": "RECORDS RETURNED",
    "schema_title": "REST Endpoint Guarantees (`/api/projects`)",
    "schema_points": [
        "Direct UTF-8 JSON serialization backed by `projects.json` with zero ORM overhead.",
        "Supports live query filtering via `?status=in_progress`, `?status=completed`, or `?slug=<slug>`.",
        "Every record exposes bilingual (`en`, `fr`) payloads, `block_diagram`, `milestones`, `tradeoffs`, and `team_acknowledgment`.",
    ],
}
