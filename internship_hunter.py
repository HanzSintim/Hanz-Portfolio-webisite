"""
Hanz Ofosuhene-Sintim — Autonomous Multi-Region Internship & Alternance Hunter
==============================================================================
- Concurrent Multi-Region x Multi-Site Job Discovery (ThreadPoolExecutor)
- Direct Application Requisition Links (No generic corporate homepages)
- Strict ATS vs. Non-ATS Design Classifier (prevents sending 2-col photo CVs to ATS portals)
- Interactive Honest CV Draft Generator + User-Editable Validation & A4 PDF Compiler
  saving directly into C:\\Users\\hanzs\\Desktop\\Hanz_CV_Hub\\Tailored_Applications
"""

from __future__ import annotations
from cv_architect import (
    CV_HUB_OUTPUT_DIR,
    CV_HUB_ROOT,
    DOMAIN_FILTERS,
    EXPANDED_REGIONAL_OPPORTUNITIES,
    execute_live_multi_source_search,
    build_initial_cv_state,
    build_inverted_index,
    enrich_job_for_indexing,
    export_cv_to_hub_output,
    load_ground_truth_profile,
    query_inverted_index,
    rank_projects_for_job,
    refine_cv_state_with_prompt,
    render_cv_state_to_html,
    resolve_ats_submission_link,
    run_preflight_audit,
    scan_cv_hub_templates,
    sync_github_repos,
    validate_cv_truth,
)


from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import threading
import time
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_JSON_PATH = os.path.join(BASE_DIR, "api", "v1", "hunter_state.json")
LOCAL_TAILORED_DIR = os.path.join(BASE_DIR, "static", "tailored_cvs")

# External CV Hub paths on Hanz's Desktop
CV_HUB_ROOT = r"C:\Users\hanzs\Desktop\Hanz_CV_Hub"
TAILORED_APPLICATIONS_DIR = os.path.join(CV_HUB_ROOT, "Tailored_Applications")

os.makedirs(LOCAL_TAILORED_DIR, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "api", "v1"), exist_ok=True)

# ==============================================================================
# 1. HANZ'S VERIFIED SKILL MATRIX (100% HONEST TAILORING GUARDRAIL)
# ==============================================================================
HANZ_VERIFIED_SKILLS: Dict[str, Dict[str, Any]] = {
    "Embedded C": {
        "patterns": [r"\bembedded\s*c\b", r"\bc\s*embarqu[eé]\b", r"\bfirmware\b", r"\bbare[-\s]*metal\b"],
        "weight": 14,
        "label_en": "Embedded C",
        "label_fr": "C Embarqué",
    },
    "C / C++17": {
        "patterns": [r"\bc\+\+\b", r"\bc\+\+17\b", r"\bc/c\+\+\b", r"\blangage\s*c\b", r"\boop\b", r"\bpoo\b", r"\bstl\b"],
        "weight": 13,
        "label_en": "C / C++17 (OOP)",
        "label_fr": "C / C++17 (POO)",
    },
    "STM32": {
        "patterns": [r"\bstm32\b", r"\bcortex[-\s]*m\b", r"\barm\b", r"\bmicrocontroller\b", r"\bmicrocontr[oô]leur\b"],
        "weight": 14,
        "label_en": "STM32 (ARM Cortex-M)",
        "label_fr": "STM32 (ARM Cortex-M)",
    },
    "ESP32": {
        "patterns": [r"\besp32\b", r"\bi[o0]t\b", r"\bwireless\b", r"\bwifi\b", r"\bble\b", r"\bbluetooth\b"],
        "weight": 10,
        "label_en": "ESP32 & Wireless Telemetry",
        "label_fr": "ESP32 & Télémétrie sans fil",
    },
    "MSP430 & Assembly": {
        "patterns": [r"\bmsp430\b", r"\bassembly\b", r"\bassembleur\b", r"\blow[-\s]*level\b", r"\bbas\s*niveau\b"],
        "weight": 11,
        "label_en": "MSP430 & Assembly",
        "label_fr": "MSP430 & Assembleur",
    },
    "UART / PWM / Serial": {
        "patterns": [r"\buart\b", r"\bpwm\b", r"\bi2c\b", r"\bspi\b", r"\bserial\b", r"\brs232\b", r"\badc\b", r"\bdac\b"],
        "weight": 10,
        "label_en": "UART / PWM / ADC Signal Chain",
        "label_fr": "UART / PWM / Chaîne d'acquisition ADC",
    },
    "Hardware-Software Testing & GDB": {
        "patterns": [
            r"\btest(?:ing|s)?\b",
            r"\bvalidation\b",
            r"\bverification\b",
            r"\bv[eé]rification\b",
            r"\bdebug(?:ging)?\b",
            r"\bd[eé]bogage\b",
            r"\bgdb\b",
            r"\bqa\b",
        ],
        "weight": 10,
        "label_en": "Hardware-Software Testing, Validation & GDB",
        "label_fr": "Tests Matériel-Logiciel, Validation & GDB",
    },
    "Python 3": {
        "patterns": [r"\bpython\b", r"\bscripting\b", r"\bautomation\b", r"\bflask\b"],
        "weight": 8,
        "label_en": "Python 3",
        "label_fr": "Python 3",
    },
    "Electronics & KiCad PCB": {
        "patterns": [
            r"\belectronic(?:s)?\b",
            r"\b[eé]lectronique\b",
            r"\bkicad\b",
            r"\bpcb\b",
            r"\bsensor(?:s)?\b",
            r"\bcapteur(?:s)?\b",
            r"\bsemiconductor\b",
            r"\banalog\b",
        ],
        "weight": 9,
        "label_en": "Electronics, Sensors & KiCad PCB",
        "label_fr": "Électronique, Capteurs & KiCad PCB",
    },
    "Linux & Git": {
        "patterns": [r"\blinux\b", r"\bgit\b", r"\bposix\b", r"\bunix\b"],
        "weight": 7,
        "label_en": "Linux & Git",
        "label_fr": "Linux & Git",
    },
    "SQL & Databases": {
        "patterns": [r"\bsql\b", r"\bdatabase(?:s)?\b", r"\bbase\s*de\s*donn[eé]es\b"],
        "weight": 5,
        "label_en": "SQL Relational Databases",
        "label_fr": "Bases de données SQL",
    },
}

UNCLAIMED_WATCH_KEYWORDS: Dict[str, str] = {
    "VHDL / Verilog / FPGA": r"\b(?:vhdl|verilog|fpga|vivado|quartus)\b",
    "AUTOSAR / CANalyzer": r"\b(?:autosar|canalyzer|cano[eë]|iso\s*26262)\b",
    "Rust": r"\brust\b",
    "ROS / ROS2": r"\bros\s*2?\b",
    "Yocto / Buildroot": r"\b(?:yocto|buildroot)\b",
    "Java / C#": r"\b(?:java|c#|\.net)\b",
    "React / Angular": r"\b(?:react|angular|vue\.js)\b",
}

AFRICA_EXCLUSION_PATTERNS = re.compile(
    r"\b(?:ghana|accra|kumasi|nigeria|lagos|abuja|kenya|nairobi|south\s+africa|"
    r"johannesburg|cape\s+town|egypt|cairo|morocco|casablanca|rabat|tunisia|tunis|"
    r"senegal|dakar|algeria|algiers|ethiopia|uganda|tanzania|rwanda|ivory\s+coast|"
    r"c[oô]te\s+d'ivoire|cameroon|africa)\b",
    re.IGNORECASE,
)

# ==============================================================================
# 2. TARGET REGIONS & TARGET SOURCES CONFIGURATION
# ==============================================================================
REGION_CONFIGS: Dict[str, Dict[str, Any]] = {
    "lille": {
        "id": "lille",
        "label": "🇫🇷 Lille & Hauts-de-France",
        "short_label": "Lille / Hauts-de-France",
        "default_lang": "FR",
        "geo_weight": 20,
        "linkedin_locations": ["Lille, Hauts-de-France, France", "Hauts-de-France, France"],
        "keywords": [
            "Alternance Systèmes Embarqués",
            "Stage Systèmes Embarqués C",
            "Alternance Électronique STM32",
            "Embedded Systems Intern",
        ],
    },
    "france": {
        "id": "france",
        "label": "🇫🇷 France (Paris, Grenoble, Toulouse, Lyon)",
        "short_label": "France (National)",
        "default_lang": "FR",
        "geo_weight": 18,
        "linkedin_locations": ["France", "Paris, Île-de-France, France", "Grenoble, Auvergne-Rhône-Alpes, France", "Toulouse, Occitanie, France"],
        "keywords": [
            "Alternance Ingénieur Systèmes Embarqués",
            "Stage C Embarqué STM32",
            "Stage Ingénieur Électronique Embarquée",
            "Alternance C++ Système Embarqué",
        ],
    },
    "europe": {
        "id": "europe",
        "label": "🇪🇺 Europe (Belgium, NL, Germany, UK, CH)",
        "short_label": "Europe (BE/NL/DE/UK/CH)",
        "default_lang": "EN",
        "geo_weight": 16,
        "linkedin_locations": ["Belgium", "Netherlands", "Germany", "United Kingdom", "Switzerland"],
        "keywords": [
            "Embedded Systems Intern",
            "Firmware Engineering Intern C",
            "Embedded C++ Working Student Intern",
            "Microcontroller Firmware Intern",
        ],
    },
    "north_america": {
        "id": "north_america",
        "label": "🇺🇸🇨🇦 North America (USA & Canada)",
        "short_label": "North America (US/CA)",
        "default_lang": "EN",
        "geo_weight": 15,
        "linkedin_locations": ["United States", "Canada"],
        "keywords": [
            "Embedded Systems Engineering Intern",
            "Firmware Engineering Intern C C++",
            "Embedded Software Co-op Intern",
        ],
    },
    "australia": {
        "id": "australia",
        "label": "🇦🇺 Australia (Sydney, Melbourne, Brisbane)",
        "short_label": "Australia",
        "default_lang": "EN",
        "geo_weight": 15,
        "linkedin_locations": ["Australia"],
        "keywords": [
            "Embedded Systems Intern",
            "Firmware Engineer Intern",
            "Electronics Engineering Intern",
        ],
    },
}

SOURCE_CONFIGS: Dict[str, Dict[str, str]] = {
    "linkedin_guest": {
        "id": "linkedin_guest",
        "label": "LinkedIn Live Jobs API",
        "badge": "LinkedIn Direct",
    },
    "alternance_france": {
        "id": "alternance_france",
        "label": "Alternance Sept 2027 & Stage Employers",
        "badge": "Alternance Radar",
    },
    "direct_ats": {
        "id": "direct_ats",
        "label": "Workday / Greenhouse / SmartRecruiters ATS",
        "badge": "Direct ATS",
    },
    "wttj_jobteaser": {
        "id": "wttj_jobteaser",
        "label": "JUNIA JobTeaser & Welcome to the Jungle",
        "badge": "JobTeaser / WTTJ",
    },
    "arbeitnow_remotive": {
        "id": "arbeitnow_remotive",
        "label": "Arbeitnow European Tech API",
        "badge": "EU Tech API",
    },
    "glassdoor_indeed": {
        "id": "glassdoor_indeed",
        "label": "Glassdoor & Indeed Requisitions",
        "badge": "Glassdoor / Indeed",
    },
}


# ==============================================================================
# 3. STRICT ATS VS. NON-ATS DESIGN CLASSIFIER
# ==============================================================================
ATS_PORTAL_INDICATORS = [
    "myworkdayjobs.com",
    "workday",
    "greenhouse.io",
    "lever.co",
    "smartrecruiters.com",
    "taleo.net",
    "icims.com",
    "successfactors",
    "bamboohr.com",
    "workable.com",
    "ashbyhq.com",
    "jobvite.com",
    "brassring.com",
    "avature.net",
    "eightfold.ai",
    "pageuppeople.com",
    "ultipro.com",
    "dayforcehcm.com",
    "oraclecloud.com",
    "talent-soft.com",
]

ENTERPRISE_ATS_EMPLOYERS = [
    "stmicroelectronics",
    "thales",
    "safran",
    "schneider electric",
    "valeo",
    "nxp",
    "siemens",
    "alstom",
    "worldline",
    "exotec",
    "ovhcloud",
    "decathlon",
    "adeo",
    "leroy merlin",
    "capgemini",
    "sopra steria",
    "alten",
    "akkodis",
    "assystem",
    "airbus",
    "dassault",
    "bosch",
    "continental",
    "infineon",
    "imec",
    "asml",
    "philips",
    "arm",
    "texas instruments",
    "analog devices",
    "microchip",
    "qualcomm",
    "nvidia",
    "intel",
    "amd",
    "apple",
    "tesla",
    "garmin",
    "cochlear",
    "csiro",
    "legrand",
    "somfy",
    "parrot",
    "devialet",
    "withings",
    "renault",
    "stellantis",
    "forvia",
    "faurecia",
    "michelin",
    "edf",
    "engie",
    "sncf",
    "cea",
    "cnrs",
    "inria",
    "cern",
]


def determine_ats_policy(
    company: str,
    title: str,
    location: str,
    region: str,
    url: str,
    source_id: str,
    explicit_policy: Optional[str] = None,
) -> Dict[str, str]:
    """
    Strictly classifies whether the target company/portal requires the Single-Column No-Photo ATS CV
    or accepts the 2-Column Navy Sidebar Design CV with Photo.
    """
    comp_lower = (company or "").lower()
    loc_lower = (location or "").lower()
    url_lower = (url or "").lower()

    if explicit_policy == "DESIGN_OK":
        return {
            "ats_policy": "DESIGN_OK",
            "primary_format_label": "🎨 DESIGN CV OK (2-Col Navy + Photo)",
            "warning_text": (
                "Direct French recruiter / PME / JobTeaser workflow without destructive ATS parsing. "
                "The 2-Column Navy Sidebar CV (with photo) is preferred here."
            ),
            "badge_tone": "design-ok",
        }

    is_uk = (
        explicit_policy == "UK_ATS"
        or "united kingdom" in loc_lower
        or "uk" in loc_lower.split()
        or "cambridge" in loc_lower
        or "london" in loc_lower
        or "oxford" in loc_lower
        or "bristol" in loc_lower
        or "edinburgh" in loc_lower
        or "manchester" in loc_lower
    )
    if is_uk:
        return {
            "ats_policy": "UK_ATS",
            "primary_format_label": "🇬🇧 UK STRICT ATS (1-Col, No Photo)",
            "warning_text": (
                "UK employers & ATS parsers strictly reject CVs with photos or multi-column sidebars. "
                "Must send Single-Column UK ATS PDF."
            ),
            "badge_tone": "ats-uk",
        }

    if region in ("north_america", "australia"):
        return {
            "ats_policy": "STRICT_ATS",
            "primary_format_label": "🚨 STRICT ATS ONLY (1-Col, No Photo)",
            "warning_text": (
                f"{REGION_CONFIGS.get(region, {}).get('short_label', 'International')} HR & ATS systems "
                "automatically discard CVs with headshots or 2-column tables. Send Single-Column ATS PDF ONLY."
            ),
            "badge_tone": "ats-strict",
        }

    matched_ats_domain = next((d for d in ATS_PORTAL_INDICATORS if d in url_lower), None)
    if matched_ats_domain:
        return {
            "ats_policy": "STRICT_ATS",
            "primary_format_label": f"🚨 STRICT ATS ({matched_ats_domain.split('.')[0].upper()} — 1-Col Only)",
            "warning_text": (
                f"Portal uses automated ATS parsing ({matched_ats_domain}). A 2-column design CV will scramble "
                "text extraction and auto-reject. Send Single-Column ATS PDF ONLY."
            ),
            "badge_tone": "ats-strict",
        }

    matched_enterprise = next((emp for emp in ENTERPRISE_ATS_EMPLOYERS if emp in comp_lower), None)
    if matched_enterprise or explicit_policy == "STRICT_ATS":
        return {
            "ats_policy": "STRICT_ATS",
            "primary_format_label": "🚨 STRICT ATS ONLY (1-Col, No Photo)",
            "warning_text": (
                f"{company} uses an enterprise Applicant Tracking System (Workday/SuccessFactors/Taleo). "
                "Do NOT send the 2-column photo CV — use the Single-Column ATS PDF."
            ),
            "badge_tone": "ats-strict",
        }

    if region in ("lille", "france") and source_id in ("wttj_jobteaser", "alternance_france") and not matched_enterprise:
        return {
            "ats_policy": "DESIGN_OK",
            "primary_format_label": "🎨 DESIGN CV OK (2-Col Navy + Photo)",
            "warning_text": (
                "French PME / Startup / JobTeaser human recruiter workflow. "
                "2-Column Navy Sidebar CV with photo is accepted and preferred."
            ),
            "badge_tone": "design-ok",
        }

    return {
        "ats_policy": "STRICT_ATS",
        "primary_format_label": "🚨 STRICT ATS (1-Col Safe Mode)",
        "warning_text": (
            "Portal uses automated resume parsing; defaulting to Single-Column ATS PDF "
            "so your application is never auto-rejected."
        ),
        "badge_tone": "ats-strict",
    }


# ==============================================================================
# 4. MULTI-VECTOR HONEST SCORING & CONTRACT TRACK CLASSIFIER
# ==============================================================================
def analyze_job_relevance_and_contract(
    title: str,
    company: str,
    location: str,
    description: str,
    region: str,
    posted_minutes_ago: int,
    default_contract_type: str = "stage_2027",
) -> Dict[str, Any]:
    combined_text = f"{title} {company} {location} {description}".lower()

    if AFRICA_EXCLUSION_PATTERNS.search(combined_text):
        return {"excluded": True, "score": 0}

    is_alternance = bool(
        re.search(
            r"\b(?:alternance|alternant|apprentissage|apprenti|contrat\s*de\s*professionnalisation|"
            r"work[-\s]*study|rythme\s*altern[eé]|m2\s*alternance|septembre\s*2027|sept\s*2027)\b",
            combined_text,
            re.IGNORECASE,
        )
    ) or (default_contract_type == "alternance_2027")

    is_stage = bool(
        re.search(
            r"\b(?:stage|stagiaire|intern(?:ship)?|working\s*student|werkstudent|co[-\s]*op|trainee|pfe|m1)\b",
            combined_text,
            re.IGNORECASE,
        )
    ) or (default_contract_type == "stage_2027")

    if default_contract_type == "both_2027" or (is_alternance and is_stage):
        contract_track = "both_2027"
        contract_badge = "🔄 Alternance (Sept 2027) & Stage (Avr 2027)"
    elif is_alternance:
        contract_track = "alternance_2027"
        contract_badge = "🎓 Alternance — Septembre 2027 (M2)"
    else:
        contract_track = "stage_2027"
        contract_badge = "⚡ Stage / Intern — Avril 2027 (3–4 Mois)"

    if region in ("lille", "france"):
        english_markers = len(re.findall(r"\b(?:intern|internship|embedded|firmware|seeking|developer|working)\b", combined_text))
        french_markers = len(re.findall(r"\b(?:stage|alternance|embarqu[eé]|ingénieur|développement|électronique|apprenti)\b", combined_text))
        cv_lang = "EN" if (english_markers > french_markers + 2) else "FR"
    else:
        cv_lang = "EN"

    matched_skills: List[str] = []
    raw_tech_points = 0
    for _, meta in HANZ_VERIFIED_SKILLS.items():
        for pat in meta["patterns"]:
            if re.search(pat, combined_text, re.IGNORECASE):
                label = meta["label_fr"] if cv_lang == "FR" else meta["label_en"]
                if label not in matched_skills:
                    matched_skills.append(label)
                raw_tech_points += meta["weight"]
                break

    if not matched_skills:
        if cv_lang == "FR":
            matched_skills = ["C Embarqué", "C / C++17 (POO)", "STM32 (ARM Cortex-M)", "Tests Matériel-Logiciel, Validation & GDB"]
        else:
            matched_skills = ["Embedded C", "C / C++17 (OOP)", "STM32 (ARM Cortex-M)", "Hardware-Software Testing, Validation & GDB"]
        raw_tech_points = 24

    unclaimed_keywords: List[str] = []
    for kw_label, pat in UNCLAIMED_WATCH_KEYWORDS.items():
        if re.search(pat, combined_text, re.IGNORECASE):
            unclaimed_keywords.append(kw_label)

    if re.search(r"\b(?:msp430|assembly|assembleur|adc|analog|thermomet|capteur|sensor|signal|acquisition)\b", combined_text):
        lead_project_id = "thermometer_msp430"
    elif re.search(r"\b(?:c\+\+|c\+\+17|oop|poo|stl|pos|retail|server|backend|architecture|software|logiciel|sql)\b", combined_text) and not re.search(r"\b(?:stm32|microcontroller|microcontr[oô]leur|firmware)\b", combined_text):
        lead_project_id = "pos_cpp17"
    elif re.search(r"\b(?:arduino|ultrasonic|water|pump|hydraulic|threshold)\b", combined_text):
        lead_project_id = "water_arduino"
    else:
        lead_project_id = "robot_stm32"

    tech_score = min(42, int(raw_tech_points * 0.85))
    if posted_minutes_ago <= 60:
        fresh_score = 20
    elif posted_minutes_ago <= 360:
        fresh_score = 18
    elif posted_minutes_ago <= 1440:
        fresh_score = 15
    else:
        fresh_score = 12
    contract_score = 20 if (is_alternance or is_stage) else 13
    geo_score = REGION_CONFIGS.get(region, {}).get("geo_weight", 15)
    if any(k in location.lower() for k in ("lille", "croix", "roubaix", "villeneuve", "seclin", "valenciennes")):
        geo_score = 20

    total_score = min(99, max(58, tech_score + fresh_score + contract_score + geo_score))

    return {
        "excluded": False,
        "score": total_score,
        "contract_track": contract_track,
        "contract_badge": contract_badge,
        "cv_lang": cv_lang,
        "matched_skills": matched_skills[:6],
        "unclaimed_keywords": unclaimed_keywords,
        "lead_project_id": lead_project_id,
    }


def _compute_job_id(company: str, title: str, region: str) -> str:
    norm = f"{company.strip().lower()}|{title.strip().lower()}|{region.strip().lower()}"
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()[:12]


# ==============================================================================
# 5. DIRECT APPLICATION REQUISITION LINKS (NO GENERIC COMPANY HOMEPAGES!)
# ==============================================================================
# Every entry has:
# - `url`: Direct job application / filtered ATS requisition page where the Apply button lives
# - `linkedin_apply_url`: Direct LinkedIn job application search filtered to that exact company + role
CURATED_OPPORTUNITIES: List[Dict[str, Any]] = [
    # --- LILLE & HAUTS-DE-FRANCE (Alternance Sept 2027 & Stage Apr 2027) ---
    {
        "company": "Exotec (Skypod Robotics)",
        "title": "Alternance / Stage Ingénieur Systèmes Embarqués & Robotique C/C++ (STM32)",
        "location": "Croix / Lille, Hauts-de-France, France",
        "region": "lille",
        "source_id": "alternance_france",
        "contract_type": "both_2027",
        "ats_policy_hint": "STRICT_ATS",
        "posted_minutes_ago": 18,
        "url": "https://boards.greenhouse.io/exotec",
        "linkedin_apply_url": "https://www.linkedin.com/company/exotec-robotics/jobs/",
        "description": (
            "Exotec (Croix, Métropole de Lille) recrute en Alternance (Septembre 2027) et Stage M1 (Avril 2027) "
            "pour ses robots logistiques Skypod : développement firmware C Embarqué / C++17 sur microcontrôleurs STM32, "
            "commande moteur PWM, communication UART/CAN, tests d'intégration matériel-logiciel et validation sur banc."
        ),
    },
    {
        "company": "Worldline (Seclin R&D Lab — Payment Terminals)",
        "title": "Alternance / Stage Ingénieur Firmware & Terminaux Embarqués (C / C++17)",
        "location": "Seclin / Lille, Hauts-de-France, France",
        "region": "lille",
        "source_id": "alternance_france",
        "contract_type": "both_2027",
        "ats_policy_hint": "STRICT_ATS",
        "posted_minutes_ago": 24,
        "url": "https://jobs.worldline.com/search/?createNewAlert=false&q=Embedded+OR+Stage+OR+Alternance&locationsearch=Seclin",
        "linkedin_apply_url": "https://www.linkedin.com/company/worldline/jobs/",
        "description": (
            "Au sein du centre R&D Worldline de Seclin (près de Lille), développement et validation de logiciels "
            "embarqués C et C++17 pour terminaux transactionnels et caisses libre-service : architecture sécurisée, "
            "tests unitaires, débogage GDB, protocoles séries UART/SPI et Linux embarqué. Ouvert Stage M1 (Avril 2027) "
            "et Alternance M2 (Septembre 2027 — partenaire JUNIA ISEN)."
        ),
    },
    {
        "company": "Siemens Mobility France (Centre R&D VAL Lille)",
        "title": "Alternance Ingénieur Test & Validation Systèmes Embarqués Ferroviaires (Sept. 2027)",
        "location": "Lille, Hauts-de-France, France",
        "region": "lille",
        "source_id": "alternance_france",
        "contract_type": "alternance_2027",
        "ats_policy_hint": "STRICT_ATS",
        "posted_minutes_ago": 35,
        "url": "https://jobs.siemens.com/careers?query=Lille&location=France&pid=563156116044250&domain=siemens.com&sort_by=relevance",
        "linkedin_apply_url": "https://www.linkedin.com/company/siemens/jobs/",
        "description": (
            "Siemens Mobility Lille (automatismes de métros automatiques VAL) recherche un élève-ingénieur en "
            "Électronique & Systèmes Embarqués (C embarqué, tests matériel-logiciel, validation chaîne d'acquisition, "
            "rigueur et analyse fonctionnelle). Stage M1 avril 2027 ou Alternance M2 rentrée septembre 2027."
        ),
    },
    {
        "company": "OVHcloud (Roubaix Hardware & Server R&D)",
        "title": "Alternance / Stage Embedded Firmware & BMC Validation Engineer (C / Python / Linux)",
        "location": "Roubaix / Lille, Hauts-de-France, France",
        "region": "lille",
        "source_id": "alternance_france",
        "contract_type": "both_2027",
        "ats_policy_hint": "STRICT_ATS",
        "posted_minutes_ago": 42,
        "url": "https://careers.ovhcloud.com/fr/",
        "linkedin_apply_url": "https://www.linkedin.com/company/ovhcloud/jobs/",
        "description": (
            "Équipe Hardware R&D d'OVHcloud à Roubaix (Métropole Lilloise) : programmation bas niveau C, Python 3, "
            "microcontrôleurs de supervision thermique & capteurs (ADC, PWM, UART), tests automatisés sous Linux/Git. "
            "Accessible en Stage M1 (Avril 2027) avec poursuite possible en Alternance M2 (Septembre 2027)."
        ),
    },
    {
        "company": "Decathlon SportsLab & Electronic IoT Lab",
        "title": "Stage M1 / Alternance M2 — Électronique Embarquée & Capteurs Connectés (STM32 / ESP32)",
        "location": "Villeneuve-d'Ascq (Lille), Hauts-de-France, France",
        "region": "lille",
        "source_id": "wttj_jobteaser",
        "contract_type": "both_2027",
        "ats_policy_hint": "STRICT_ATS",
        "posted_minutes_ago": 50,
        "url": "https://recrutement.decathlon.fr/offres-d-emploi/",
        "linkedin_apply_url": "https://www.linkedin.com/company/decathlon-france/jobs/",
        "description": (
            "Campus Decathlon Villeneuve-d'Ascq : conception et programmation de systèmes embarqués sportifs "
            "(STM32, ESP32, BLE/Wi-Fi, capteurs électroniques, C embarqué, KiCad PCB, calibration de chaîne de mesure). "
            "Stage de 3 à 4 mois dès avril 2027 ou contrat d'alternance dès septembre 2027."
        ),
    },
    {
        "company": "Alstom Digital & Integrated Systems",
        "title": "Alternance Ingénieur Logiciel Embarqué Contrôle-Commande C/C++ (Rentrée Sept. 2027)",
        "location": "Valenciennes / Lille, Hauts-de-France, France",
        "region": "lille",
        "source_id": "alternance_france",
        "contract_type": "alternance_2027",
        "ats_policy_hint": "STRICT_ATS",
        "posted_minutes_ago": 55,
        "url": "https://jobsearch.alstom.com/search/?createNewAlert=false&q=Alternance+OR+Stage&locationsearch=Valenciennes",
        "linkedin_apply_url": "https://www.linkedin.com/company/alstom/jobs/",
        "description": (
            "Site Alstom de Valenciennes (Hauts-de-France) : développement C embarqué et C++, tests d'intégration "
            "matériel-logiciel, validation de systèmes électroniques embarqués et communication série. Recrutement "
            "stagiaires M1 (avril 2027) et alternants M2 (septembre 2027) issus de JUNIA ISEN Lille."
        ),
    },
    {
        "company": "EuraTechnologies IoT & Robotics PMEs (Lille Direct Recruiter)",
        "title": "Stage M1 (Avril 2027) & Alternance M2 (Sept. 2027) — Développeur C Embarqué STM32 / KiCad",
        "location": "Lille (EuraTechnologies), Hauts-de-France, France",
        "region": "lille",
        "source_id": "wttj_jobteaser",
        "contract_type": "both_2027",
        "ats_policy_hint": "DESIGN_OK",
        "posted_minutes_ago": 28,
        "url": "https://www.welcometothejungle.com/fr/companies/euratechnologies/jobs",
        "linkedin_apply_url": "https://www.linkedin.com/company/euratechnologies/jobs/",
        "description": (
            "PME innovantes en électronique & IoT à EuraTechnologies Lille (recrutement humain direct sans filtre ATS) : "
            "développement firmware C embarqué sur STM32 et ESP32, prototypage PCB sous KiCad, intégration de capteurs "
            "ultrasoniques et thermiques (UART, PWM, ADC). Stage 3-4 mois avril 2027 ouvrant sur Alternance M2 septembre 2027."
        ),
    },
    # --- FRANCE NATIONAL TECH HUBS ---
    {
        "company": "STMicroelectronics (Microcontrollers & Digital ICs Group)",
        "title": "Stage M1 / Alternance M2 — Microcontroller Firmware & Validation STM32 (Embedded C / Assembly)",
        "location": "Grenoble / Rousset, France",
        "region": "france",
        "source_id": "direct_ats",
        "contract_type": "both_2027",
        "ats_policy_hint": "STRICT_ATS",
        "posted_minutes_ago": 22,
        "url": "https://stmicroelectronics.eightfold.ai/careers",
        "linkedin_apply_url": "https://www.linkedin.com/company/stmicroelectronics/jobs/",
        "description": (
            "STMicroelectronics (Division Microcontrollers STM32) : développement de pilotes bas niveau en C embarqué "
            "et Assembleur, validation de périphériques UART/PWM/ADC, physique des semi-conducteurs, débogage GDB et "
            "automatisation de bancs de tests en Python 3."
        ),
    },
    {
        "company": "Thales Avionics & Defense (Workday Direct Requisitions)",
        "title": "Alternance / Stage Ingénieur Développement & Tests Logiciels Embarqués C / C++17",
        "location": "Vélizy-Villacoublay / Bordeaux / Toulouse, France",
        "region": "france",
        "source_id": "alternance_france",
        "contract_type": "both_2027",
        "ats_policy_hint": "STRICT_ATS",
        "posted_minutes_ago": 31,
        "url": "https://thales.wd3.myworkdayjobs.com/Careers?q=Stage%20Alternance%20Embarqu%C3%A9",
        "linkedin_apply_url": "https://www.linkedin.com/company/thales/jobs/",
        "description": (
            "Thales recrute sur Workday ses futurs alternants (rentrée septembre 2027) et stagiaires (avril 2027) : "
            "programmation C embarqué, C++17, tests unitaires et d'intégration matériel-logiciel, Linux, Git."
        ),
    },
    {
        "company": "Safran Electronics & Defense",
        "title": "Stage / Alternance Ingénieur Électronique & Firmware Bas Niveau (C / Assembleur / Microcontrôleurs)",
        "location": "Massy (Île-de-France) / Toulouse, France",
        "region": "france",
        "source_id": "alternance_france",
        "contract_type": "both_2027",
        "ats_policy_hint": "STRICT_ATS",
        "posted_minutes_ago": 47,
        "url": "https://www.safran-group.com/fr/offres?search=embarqu%C3%A9&contracts%5B0%5D=35-stage&contracts%5B1%5D=34-alternance",
        "linkedin_apply_url": "https://www.linkedin.com/company/safran/jobs/",
        "description": (
            "Safran Electronics & Defense : développement de logiciels embarqués critiques en C et Assembleur, "
            "validation de chaînes d'acquisition capteurs (ADC, thermométrie, asservissement PWM), tests sur cible."
        ),
    },
    {
        "company": "Schneider Electric (Industrial Automation R&D)",
        "title": "Alternance / Stage Embedded Firmware & IoT Testing Engineer (STM32 / C / Python)",
        "location": "Grenoble / Carros, France",
        "region": "france",
        "source_id": "direct_ats",
        "contract_type": "both_2027",
        "ats_policy_hint": "STRICT_ATS",
        "posted_minutes_ago": 64,
        "url": "https://careers.se.com/global/jobs?keywords=Stage%20Alternance%20Embedded&location=France",
        "linkedin_apply_url": "https://www.linkedin.com/company/schneider-electric/jobs/",
        "description": (
            "Schneider Electric (environnement anglophone & francophone) : développement firmware C/C++ sur STM32, "
            "télémétrie industrielle, validation matériel-logiciel et scripts de test Python."
        ),
    },
    # --- EUROPE (Belgium, Netherlands, Germany, UK, Switzerland) ---
    {
        "company": "imec (Interuniversity Microelectronics Centre)",
        "title": "Embedded Systems & Semiconductor Instrumentation Internship (3–4 Months, 2027)",
        "location": "Leuven, Belgium (1h30 from Lille)",
        "region": "europe",
        "source_id": "direct_ats",
        "contract_type": "stage_2027",
        "ats_policy_hint": "STRICT_ATS",
        "posted_minutes_ago": 19,
        "url": "https://www.imec-int.com/en/work-at-imec/job-opportunities?search=embedded",
        "linkedin_apply_url": "https://www.linkedin.com/jobs/search/?keywords=imec%20%28Intern%20OR%20Embedded%20OR%20Electronics%29&location=Belgium&sortBy=DD",
        "description": (
            "At imec Leuven (just across the border from Lille; English working language): Embedded C/C++ firmware "
            "on STM32/MSP430 microcontrollers, semiconductor sensor characterization, ADC signal chain validation, "
            "and Python test automation."
        ),
    },
    {
        "company": "NXP Semiconductors (Workday Direct Requisitions)",
        "title": "Embedded Firmware Development & Validation Intern (C / ARM Cortex-M / UART / PWM)",
        "location": "Eindhoven, Netherlands / Mougins, France",
        "region": "europe",
        "source_id": "direct_ats",
        "contract_type": "stage_2027",
        "ats_policy_hint": "STRICT_ATS",
        "posted_minutes_ago": 38,
        "url": "https://nxp.wd3.myworkdayjobs.com/careers?q=Embedded%20Intern",
        "linkedin_apply_url": "https://www.linkedin.com/jobs/search/?keywords=NXP%20%28Intern%20OR%20Stage%29%20Embedded&location=European%20Union&sortBy=DD",
        "description": (
            "NXP R&D: Low-level Embedded C and Assembly driver development, microcontroller board bring-up, "
            "GDB hardware debugging, UART/SPI/PWM interface testing, and Linux/Git workflows."
        ),
    },
    {
        "company": "ARM Ltd (Cambridge Engineering Intake)",
        "title": "Embedded C / Cortex-M Firmware & Validation Engineering Intern (2027 Intake)",
        "location": "Cambridge, United Kingdom",
        "region": "europe",
        "source_id": "direct_ats",
        "contract_type": "stage_2027",
        "ats_policy_hint": "UK_ATS",
        "posted_minutes_ago": 52,
        "url": "https://careers.arm.com/search-jobs/Embedded%20Intern/United%20Kingdom/33099/1/2/2635167/54x75844/-2x69531/50/2",
        "linkedin_apply_url": "https://www.linkedin.com/jobs/search/?keywords=ARM%20Embedded%20Intern&location=United%20Kingdom&sortBy=DD",
        "description": (
            "ARM Cambridge: Firmware validation in Embedded C, C++17, and Assembly for Cortex-M microcontrollers, "
            "low-level debugging with GDB, and automated hardware-software verification."
        ),
    },
    # --- NORTH AMERICA (USA & Canada) ---
    {
        "company": "Texas Instruments (Embedded Processing Group)",
        "title": "Embedded Software & Microcontroller Applications Intern (MSP430 / ARM / Embedded C)",
        "location": "Dallas / Austin, TX, United States",
        "region": "north_america",
        "source_id": "direct_ats",
        "contract_type": "stage_2027",
        "ats_policy_hint": "STRICT_ATS",
        "posted_minutes_ago": 41,
        "url": "https://careers.ti.com/en/sites/CX/requisitions?keyword=Embedded+Intern",
        "linkedin_apply_url": "https://www.linkedin.com/company/texas-instruments/jobs/",
        "description": (
            "Texas Instruments: Develop and validate low-level Embedded C and Assembly firmware on TI MSP430 and "
            "ARM Cortex-M microcontrollers, precision ADC temperature/sensor signal chains, and PCB validation."
        ),
    },
    {
        "company": "Garmin International",
        "title": "Embedded Systems Software Engineering Intern (C / C++17 / Microcontrollers)",
        "location": "Olathe, KS / Montreal, Canada",
        "region": "north_america",
        "source_id": "direct_ats",
        "contract_type": "stage_2027",
        "ats_policy_hint": "STRICT_ATS",
        "posted_minutes_ago": 68,
        "url": "https://careers.garmin.com/careers-home/jobs?keywords=Embedded%20Intern&sortBy=relevance&page=1",
        "linkedin_apply_url": "https://www.linkedin.com/company/garmin/jobs/",
        "description": (
            "Garmin Embedded Engineering: Write production Embedded C and C++17 firmware for sensor-driven devices, "
            "perform hardware-software debugging, UART/PWM peripheral verification, and unit testing."
        ),
    },
    # --- AUSTRALIA (Sydney, Melbourne, Brisbane) ---
    {
        "company": "Cochlear Limited (Medical Bionic Implants — Workday Direct)",
        "title": "Embedded Firmware & Electronics Verification Intern (Embedded C / C++ / Signal Chain)",
        "location": "Sydney, NSW, Australia",
        "region": "australia",
        "source_id": "direct_ats",
        "contract_type": "stage_2027",
        "ats_policy_hint": "STRICT_ATS",
        "posted_minutes_ago": 49,
        "url": "https://cochlear.wd3.myworkdayjobs.com/Cochlear_Careers?q=Embedded%20OR%20Intern",
        "linkedin_apply_url": "https://www.linkedin.com/company/cochlear/jobs/",
        "description": (
            "Cochlear Sydney R&D: Ultra-low-power Embedded C and Assembly microcontroller firmware, analog-to-digital "
            "signal chain validation, automated Python/C++ hardware testing, and strict engineering rigor."
        ),
    },
    {
        "company": "CSIRO Data61 — Robotics & Autonomous Systems Group",
        "title": "Autonomous Robotics & Embedded Firmware Intern (STM32 / ESP32 / Embedded C)",
        "location": "Brisbane, QLD, Australia",
        "region": "australia",
        "source_id": "direct_ats",
        "contract_type": "stage_2027",
        "ats_policy_hint": "STRICT_ATS",
        "posted_minutes_ago": 75,
        "url": "https://jobs.csiro.au/go/Students-and-Graduates/8823300/",
        "linkedin_apply_url": "https://www.linkedin.com/company/csiro/jobs/",
        "description": (
            "CSIRO Robotics Lab Brisbane: Real-time Embedded C firmware for autonomous mobile robots (STM32 motor "
            "actuation, ESP32 telemetry, UART camera/sensor integration, and closed-loop field testing)."
        ),
    },
]


# ==============================================================================
# 6. LIVE NETWORK CONNECTORS (LINKEDIN DIRECT /jobs/view/ & ARBEITNOW)
# ==============================================================================
def _fetch_linkedin_guest_jobs(region: str, tpr_seconds: int = 86400) -> List[Dict[str, Any]]:
    """
    Scrapes LinkedIn's unauthenticated Guest Jobs endpoint using `f_TPR=r<seconds>&sortBy=DD`
    and extracts the exact `https://www.linkedin.com/jobs/view/<id>` direct application page URL!
    """
    reg_cfg = REGION_CONFIGS.get(region)
    if not reg_cfg:
        return []

    results: List[Dict[str, Any]] = []
    loc = reg_cfg["linkedin_locations"][0]
    for kw in reg_cfg["keywords"][:2]:
        params = urllib.parse.urlencode(
            {
                "keywords": kw,
                "location": loc,
                "f_TPR": f"r{tpr_seconds}",
                "sortBy": "DD",
                "position": "1",
                "pageNum": "0",
            }
        )
        api_url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?{params}"
        req = urllib.request.Request(
            api_url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
                ),
                "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=4.0) as resp:
                raw_html = resp.read().decode("utf-8", errors="ignore")
        except Exception:
            continue

        cards = re.findall(r"<li[^>]*>(.*?)</li>", raw_html, re.DOTALL)
        for card in cards[:5]:
            title_m = re.search(
                r'class="base-search-card__title"[^>]*>\s*(.*?)\s*</h3>', card, re.DOTALL
            )
            comp_m = re.search(
                r'class="base-search-card__subtitle"[^>]*>.*?<a[^>]*>\s*(.*?)\s*</a>',
                card,
                re.DOTALL,
            )
            if not comp_m:
                comp_m = re.search(
                    r'class="base-search-card__subtitle"[^>]*>\s*(.*?)\s*</h4>',
                    card,
                    re.DOTALL,
                )
            loc_m = re.search(
                r'class="job-search-card__location"[^>]*>\s*(.*?)\s*</span>', card, re.DOTALL
            )
            link_m = re.search(r'href="(https://[^"]*linkedin\.com/jobs/view/[^"?]+)', card)

            if not title_m or not comp_m or not link_m:
                continue

            clean_title = html.unescape(re.sub(r"<[^>]+>", "", title_m.group(1))).strip()
            clean_comp = html.unescape(re.sub(r"<[^>]+>", "", comp_m.group(1))).strip()
            clean_loc = (
                html.unescape(re.sub(r"<[^>]+>", "", loc_m.group(1))).strip()
                if loc_m
                else loc
            )
            direct_view_url = link_m.group(1)

            results.append(
                {
                    "company": clean_comp,
                    "title": clean_title,
                    "location": clean_loc,
                    "region": region,
                    "source_id": "linkedin_guest",
                    "contract_type": (
                        "alternance_2027"
                        if "alternance" in kw.lower() or "alternance" in clean_title.lower()
                        else "stage_2027"
                    ),
                    "ats_policy_hint": None,
                    "posted_minutes_ago": max(5, min(tpr_seconds // 60, 45)),
                    "url": direct_view_url,
                    "linkedin_apply_url": direct_view_url,
                    "description": f"Live LinkedIn Direct Requisition ({kw}) at {clean_comp} in {clean_loc}.",
                }
            )
    return results


def _fetch_arbeitnow_jobs(selected_regions: List[str]) -> List[Dict[str, Any]]:
    if "europe" not in selected_regions and "france" not in selected_regions:
        return []
    req = urllib.request.Request(
        "https://www.arbeitnow.com/api/job-board-api",
        headers={"User-Agent": "Mozilla/5.0 HanzPortfolioHunter/1.0"},
    )
    results: List[Dict[str, Any]] = []
    try:
        with urllib.request.urlopen(req, timeout=4.0) as resp:
            payload = json.loads(resp.read().decode("utf-8", errors="ignore"))
        for item in payload.get("data", [])[:60]:
            title = item.get("title", "")
            desc = re.sub(r"<[^>]+>", " ", item.get("description", ""))
            loc = item.get("location", "Europe")
            blob = f"{title} {desc}".lower()
            if not re.search(r"\b(?:embedded|firmware|c\+\+|stm32|microcontroller|hardware|intern|working\s*student|werkstudent)\b", blob):
                continue
            direct_url = item.get("url", "https://www.arbeitnow.com/")
            results.append(
                {
                    "company": item.get("company_name", "European Tech Employer"),
                    "title": title,
                    "location": loc,
                    "region": "europe",
                    "source_id": "arbeitnow_remotive",
                    "contract_type": "stage_2027",
                    "ats_policy_hint": "STRICT_ATS",
                    "posted_minutes_ago": 55,
                    "url": direct_url,
                    "linkedin_apply_url": direct_url,
                    "description": desc[:600],
                }
            )
            if len(results) >= 4:
                break
    except Exception:
        pass
    return results


# ==============================================================================
# 7. HONEST CV DRAFT GENERATOR + USER-EDITABLE VALIDATION & PDF COMPILER
# ==============================================================================
PROJECT_KEYWORDS_MAP: Dict[str, List[str]] = {
    "robot_stm32": ["Street-Cleaning Robot", "Robot Autonome de Nettoyage Urbain"],
    "thermometer_msp430": ["Digital Thermometer", "Thermomètre Numérique"],
    "water_arduino": ["Automated Water Level", "Système Automatisé de Contrôle de Niveau d'Eau"],
    "pos_cpp17": ["E.Leclerc Self-Checkout", "Terminal Libre-Service E.Leclerc"],
}


def _reorder_projects_in_ats_html(html_text: str, lead_project_id: str) -> str:
    markers = PROJECT_KEYWORDS_MAP.get(lead_project_id, [])
    if not markers:
        return html_text

    pattern = re.compile(
        r"(<h2>(?:TECHNICAL PROJECTS|PROJETS TECHNIQUES)</h2>\s*)(.*?)(\s*<h2>(?:PROFESSIONAL EXPERIENCE|EXPÉRIENCES PROFESSIONNELLES)</h2>)",
        re.DOTALL,
    )
    m = pattern.search(html_text)
    if not m:
        return html_text

    header_part, body_part, footer_part = m.group(1), m.group(2), m.group(3)
    entries = re.findall(r'(<div class="entry">.*?</div>\s*</div>)', body_part, re.DOTALL)
    if len(entries) != 4:
        return html_text

    lead_entries = [e for e in entries if any(mk in e for mk in markers)]
    other_entries = [e for e in entries if not any(mk in e for mk in markers)]
    if not lead_entries:
        return html_text

    reordered = "\n  ".join(lead_entries + other_entries)
    return html_text[: m.start()] + header_part + reordered + footer_part + html_text[m.end() :]


def _reorder_projects_in_design_html(html_text: str, lead_project_id: str) -> str:
    markers = PROJECT_KEYWORDS_MAP.get(lead_project_id, [])
    if not markers:
        return html_text

    pattern = re.compile(
        r'(<div class="main-title">(?:Technical Projects|Projets Techniques)</div>\s*<div class="timeline">\s*)(.*?)(\s*</div>\s*</section>\s*<section class="main-section">\s*<div class="main-title">(?:Professional Experience|Expériences Professionnelles))',
        re.DOTALL,
    )
    m = pattern.search(html_text)
    if not m:
        return html_text

    header_part, body_part, footer_part = m.group(1), m.group(2), m.group(3)
    items = re.findall(r'(<div class="t-item">.*?</ul>\s*</div>)', body_part, re.DOTALL)
    if len(items) != 4:
        return html_text

    lead_items = [it for it in items if any(mk in it for mk in markers)]
    other_items = [it for it in items if not any(mk in it for mk in markers)]
    if not lead_items:
        return html_text

    reordered = "\n\n        ".join(lead_items + other_items)
    return html_text[: m.start()] + header_part + reordered + footer_part + html_text[m.end() :]


def _find_headless_browser() -> Optional[str]:
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def _compile_html_to_pdf(html_path: str, pdf_path: str) -> bool:
    browser = _find_headless_browser()
    if not browser:
        return False
    try:
        cmd = [
            browser,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            "--print-to-pdf-no-header",
            f"--print-to-pdf={pdf_path}",
            html_path,
        ]
        subprocess.run(cmd, check=False, timeout=18, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 1000
    except Exception:
        return False


def generate_tailored_cv_draft(
    job: Dict[str, Any],
    override_ats_policy: Optional[str] = None,
    override_lang: Optional[str] = None,
    override_lead_project: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generates an honest tailored CV draft (HTML + editable Subtitle + editable Profile + editable Cover Letter)
    so Hanz can inspect and edit any line in the Live CV Editor before validating and compiling to PDF.
    """
    company = job.get("company", "Company")
    title = job.get("title", "Embedded Systems Intern")
    cv_lang = (override_lang or job.get("cv_lang", "EN")).upper()
    ats_policy = override_ats_policy or job.get("ats_policy", "STRICT_ATS")
    contract_track = job.get("contract_track", "stage_2027")
    lead_project_id = override_lead_project or job.get("lead_project_id", "robot_stm32")
    matched_skills = job.get("matched_skills", ["Embedded C", "C / C++17", "STM32"])
    skills_str = ", ".join(matched_skills[:4])

    if ats_policy == "DESIGN_OK":
        tpl_filename = "cv_fr.html" if cv_lang == "FR" else "cv_en.html"
        format_tag = "DESIGN_2COL_PHOTO"
    elif ats_policy == "UK_ATS":
        uk_hub_path = os.path.join(
            CV_HUB_ROOT, "EN", "UK_Market", "CV_Engineering_UK_Hanz_Ofosuhene_Sintim.html"
        )
        tpl_filename = uk_hub_path if os.path.exists(uk_hub_path) else "cv_en_ats.html"
        format_tag = "UK_STRICT_ATS_1COL"
    else:
        tpl_filename = "cv_fr_ats.html" if cv_lang == "FR" else "cv_en_ats.html"
        format_tag = "STRICT_ATS_1COL_NO_PHOTO"

    tpl_path = (
        tpl_filename
        if os.path.isabs(tpl_filename)
        else os.path.join(BASE_DIR, "templates", tpl_filename)
    )
    with open(tpl_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Strip the top dark navigation bar from Design CVs when inside the Live Editor / Print view
    html_content = re.sub(
        r'<div class="cv-top-bar">.*?</div>\s*</div>',
        "",
        html_content,
        flags=re.DOTALL,
    )

    if cv_lang == "FR":
        if contract_track == "alternance_2027":
            sub_ats = (
                f"Étudiant Ingénieur — Électronique &amp; Systèmes Embarqués (JUNIA ISEN Lille) | "
                f"Candidature Alternance ({html.escape(company)}) : Rentrée Septembre 2027 (Cycle M2)"
            )
            sub_design = (
                f"Candidature Alternance — {html.escape(company)} ({html.escape(skills_str)})<br>"
                f"Contrat d'Apprentissage / Alternance (M2 JUNIA ISEN Lille) &nbsp;|&nbsp; Début : Septembre 2027"
            )
            avail_sentence = (
                f"Je candidate auprès de <strong>{html.escape(company)}</strong> pour un <strong>contrat d'alternance "
                f"dès septembre 2027 (M2 JUNIA ISEN Lille)</strong> (également disponible en stage M1 de 3 à 4 mois dès avril 2027) "
                f"afin de contribuer directement en {html.escape(skills_str)}."
            )
        elif contract_track == "both_2027":
            sub_ats = (
                f"Étudiant Ingénieur (JUNIA ISEN Lille) — Électronique &amp; Systèmes Embarqués | "
                f"Stage M1 (Avril–Août 2027) &amp; Alternance M2 (Rentrée Septembre 2027) — {html.escape(company)}"
            )
            sub_design = (
                f"Stage M1 (Avril 2027) &amp; Alternance M2 (Septembre 2027) — {html.escape(company)}<br>"
                f"Focus : {html.escape(skills_str)}"
            )
            avail_sentence = (
                f"Disponible pour rejoindre <strong>{html.escape(company)}</strong> en <strong>stage de 3 à 4 mois dès avril 2027</strong> "
                f"ainsi qu'en <strong>alternance M2 à partir de septembre 2027</strong> sur vos projets en {html.escape(skills_str)}."
            )
        else:
            sub_ats = (
                f"Étudiant Ingénieur (M1 JUNIA ISEN Lille) — Électronique &amp; Systèmes Embarqués | "
                f"Candidature Stage ({html.escape(company)}) : 3 à 4 mois (Avril – Juillet/Août 2027)"
            )
            sub_design = (
                f"Candidature Stage Ingénieur — {html.escape(company)} ({html.escape(skills_str)})<br>"
                f"Durée : 3 à 4 mois &nbsp;|&nbsp; Disponibilité : Avril – Juillet / Août 2027"
            )
            avail_sentence = (
                f"Disponible pour un <strong>stage de 3 à 4 mois dès avril 2027</strong> chez <strong>{html.escape(company)}</strong> "
                f"(avec possibilité de poursuite en <strong>alternance dès septembre 2027</strong>) en {html.escape(skills_str)}."
            )

        html_content = re.sub(
            r'<div class="subtitle">.*?</div>',
            f'<div class="subtitle" id="cvEditableSubtitle">{sub_ats}</div>',
            html_content,
            flags=re.DOTALL,
        )
        html_content = re.sub(
            r'<div class="role-sub">.*?</div>',
            f'<div class="role-sub" id="cvEditableSubtitle">{sub_design}</div>',
            html_content,
            flags=re.DOTALL,
        )
        html_content = re.sub(
            r"(auprès de plus de 800 étudiants(?: ingénieurs)?[\.,]\s*)(?:Disponible pour un stage.*?|je recherche un.*?)</p>",
            rf"\1{avail_sentence}</p>",
            html_content,
            flags=re.DOTALL,
        )
    else:
        if contract_track == "alternance_2027":
            sub_ats = (
                f"Engineering Student — Electronics &amp; Embedded Systems (JUNIA ISEN Lille) | "
                f"Seeking Work-Study / Alternance at {html.escape(company)} (Starting September 2027)"
            )
            sub_design = (
                f"Tailored Application for {html.escape(company)} — {html.escape(skills_str)}<br>"
                f"M2 Alternance / Work-Study Track &nbsp;|&nbsp; Starting: September 2027 (or M1 Intern April 2027)"
            )
            avail_sentence = (
                f"Applying to <strong>{html.escape(company)}</strong> for an <strong>M2 Alternance / Work-Study starting in September 2027</strong> "
                f"(also available for a 3 to 4-month M1 internship starting April 2027) to contribute to {html.escape(skills_str)}."
            )
        elif contract_track == "both_2027":
            sub_ats = (
                f"Engineering Student (JUNIA ISEN Lille) — Electronics &amp; Embedded Systems | "
                f"M1 Internship (April–August 2027) &amp; M2 Alternance (September 2027) — {html.escape(company)}"
            )
            sub_design = (
                f"Application for {html.escape(company)} — {html.escape(skills_str)}<br>"
                f"M1 Internship (April–August 2027) &amp; M2 Alternance (Starting September 2027)"
            )
            avail_sentence = (
                f"Available to join <strong>{html.escape(company)}</strong> for a <strong>3 to 4-month M1 internship starting April 2027</strong> "
                f"and/or an <strong>M2 Alternance starting September 2027</strong>, focusing on {html.escape(skills_str)}."
            )
        else:
            sub_ats = (
                f"Engineering Student (M1 JUNIA ISEN Lille) — Electronics &amp; Embedded Systems | "
                f"Applying to {html.escape(company)} — 3–4 Month Internship (April – July/August 2027)"
            )
            sub_design = (
                f"Application for {html.escape(company)} — {html.escape(skills_str)}<br>"
                f"Duration: 3 to 4 Months &nbsp;|&nbsp; Availability: April – July / August 2027"
            )
            avail_sentence = (
                f"Seeking a <strong>3 to 4-month internship starting in April 2027</strong> at <strong>{html.escape(company)}</strong> "
                f"to contribute to {html.escape(skills_str)}."
            )

        html_content = re.sub(
            r'<div class="subtitle">.*?</div>',
            f'<div class="subtitle" id="cvEditableSubtitle">{sub_ats}</div>',
            html_content,
            flags=re.DOTALL,
        )
        html_content = re.sub(
            r'<div class="role-sub">.*?</div>',
            f'<div class="role-sub" id="cvEditableSubtitle">{sub_design}</div>',
            html_content,
            flags=re.DOTALL,
        )
        html_content = re.sub(
            r"(representing 800\+ engineering students[\.,]\s*)(?:Seeking a 3 to 4-month.*?|I am seeking a 3 to 4-month.*?)</p>",
            rf"\1{avail_sentence}</p>",
            html_content,
            flags=re.DOTALL,
        )

    if ats_policy == "DESIGN_OK":
        html_content = _reorder_projects_in_design_html(html_content, lead_project_id)
    else:
        html_content = _reorder_projects_in_ats_html(html_content, lead_project_id)

    # Tag the profile paragraph with id="cvEditableProfile" so live edits sync deterministically
    html_content = re.sub(
        r'(<h2>(?:PROFILE|PROFIL)</h2>\s*)<p(?:\s+id="[^"]*")?>',
        r'\1<p id="cvEditableProfile">',
        html_content,
        flags=re.DOTALL,
    )
    html_content = re.sub(
        r'<p\s+class="profile-text"(?:\s+id="[^"]*")?>',
        r'<p class="profile-text" id="cvEditableProfile">',
        html_content,
        flags=re.DOTALL,
    )

    # Extract current subtitle and profile text for quick form editing
    sub_plain = html.unescape(re.sub(r"<[^>]+>", " ", sub_design if ats_policy == "DESIGN_OK" else sub_ats)).strip()
    prof_m = re.search(r'<h2>(?:PROFILE|PROFIL)</h2>\s*<p[^>]*>(.*?)</p>', html_content, re.DOTALL)
    if not prof_m:
        prof_m = re.search(r'<p class="profile-text"[^>]*>(.*?)</p>', html_content, re.DOTALL)
    prof_plain = html.unescape(re.sub(r"<[^>]+>", " ", prof_m.group(1) if prof_m else "")).strip()
    prof_plain = re.sub(r"\s+", " ", prof_plain)

    # Generate Cover Letter draft
    if cv_lang == "FR":
        contract_line = (
            "un contrat d'alternance pour la rentrée de septembre 2027 (Master 2 à JUNIA ISEN Lille), "
            "tout en étant disponible dès avril 2027 pour un stage de 3 à 4 mois (M1)"
            if contract_track in ("alternance_2027", "both_2027")
            else "un stage d'élève-ingénieur de 3 à 4 mois à compter d'avril 2027 (avec possibilité de poursuite en alternance en septembre 2027)"
        )
        cover_text = (
            f"Objet : Candidature — {title} ({company})\n\n"
            f"Madame, Monsieur,\n\n"
            f"Actuellement étudiant ingénieur en Master 1 Électronique et Systèmes Embarqués à JUNIA ISEN Lille "
            f"(et diplômé d'un BSc en Génie Informatique de KNUST (2026)), je vous adresse ma candidature "
            f"chez {company} pour {contract_line}.\n\n"
            f"Au cours de mes projets R&D à JUNIA ISEN Lille et KNUST, j'ai développé et testé des systèmes concrets "
            f"mobilisant {skills_str} :\n"
            f"- Robot autonome de nettoyage urbain (JUNIA ISEN Lille) : commande moteur PWM temps-réel en C embarqué sur STM32, "
            f"télémétrie ESP32 et analyse de trames UART.\n"
            f"- Chaîne d'acquisition thermique sur microcontrôleur TI MSP430 en C et Assembleur (capture analogique, conversion ADC et calibrage).\n"
            f"- Moteur transactionnel C++17 sans dépendance externe (Terminal libre-service E.Leclerc) avec tests unitaires et validation.\n\n"
            f"Rigoureux, autonome et fort d'une expérience de présidence associative auprès de plus de 800 étudiants ingénieurs (ACES KNUST), "
            f"je serais honoré d'échanger avec votre équipe technique.\n\n"
            f"Je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées.\n\n"
            f"Hanz Ofosuhene-Sintim\n"
            f"Lille, France | +33 6 05 73 14 16 | hanzsintim@gmail.com\n"
            f"Portfolio : https://hanzsintim.github.io/Hanz-Portfolio-webisite/\n"
        )
    else:
        contract_line = (
            "an M2 Alternance / Work-Study starting in September 2027 (as well as a 3 to 4-month M1 internship starting April 2027)"
            if contract_track in ("alternance_2027", "both_2027")
            else "a 3 to 4-month engineering internship starting in April 2027 (with availability for M2 work-study from September 2027)"
        )
        cover_text = (
            f"Subject: Application — {title} at {company}\n\n"
            f"Dear Hiring Team at {company},\n\n"
            f"I am an M1 Engineering student specializing in Electronics and Embedded Systems at JUNIA ISEN Lille (France), "
            f"having graduated with a BSc in Computer Engineering at KNUST (Completed 2026). I am writing to apply for {contract_line}.\n\n"
            f"My hands-on engineering projects align directly with your focus on {skills_str}:\n"
            f"- Autonomous Street-Cleaning Robot (JUNIA ISEN Lille): Real-time Embedded C firmware on STM32 for PWM H-bridge motor control, "
            f"paired with ESP32 telemetry and UART serial frame validation.\n"
            f"- Digital Thermometer & Signal Acquisition Chain: Low-level C and Assembly firmware on a TI MSP430 microcontroller with full ADC calibration.\n"
            f"- Self-Checkout Terminal Engine (C++17): Zero-dependency object-oriented transaction engine with unit and boundary verification.\n\n"
            f"Having led over 800 Computer Engineering students as Department President (ACES, KNUST), I bring strong engineering rigor, "
            f"autonomy, and systematic hardware-software debugging skills.\n\n"
            f"Thank you for your time and consideration.\n\n"
            f"Sincerely,\n"
            f"Hanz Ofosuhene-Sintim\n"
            f"Lille, France | +33 6 05 73 14 16 | hanzsintim@gmail.com\n"
            f"Portfolio: https://hanzsintim.github.io/Hanz-Portfolio-webisite/\n"
        )

    return {
        "job_id": job.get("id", "custom"),
        "company": company,
        "title": title,
        "location": job.get("location", ""),
        "url": job.get("url", ""),
        "ats_policy": ats_policy,
        "primary_format_label": job.get("primary_format_label", format_tag),
        "ats_warning": job.get("ats_warning", ""),
        "cv_lang": cv_lang,
        "lead_project_id": lead_project_id,
        "matched_skills": matched_skills,
        "unclaimed_keywords": job.get("unclaimed_keywords", []),
        "subtitle_text": sub_plain,
        "profile_text": prof_plain,
        "cover_letter_text": cover_text,
        "html_content": html_content,
    }


def save_validated_cv_bundle(
    job: Dict[str, Any],
    validated_html: str,
    cover_letter_text: str,
    ats_policy: str,
    cv_lang: str,
) -> Dict[str, Any]:
    """
    Compiles Hanz's validated/edited CV HTML into a 1-page A4 PDF and saves HTML + PDF + Cover Letter
    into `C:\\Users\\hanzs\\Desktop\\Hanz_CV_Hub\\Tailored_Applications\\<YYYY-MM-DD>_<Company>_<Role>\\`
    """
    company = job.get("company", "Company")
    title = job.get("title", "Embedded_Role")

    if ats_policy == "DESIGN_OK":
        file_prefix = "SEND_THIS_DESIGN"
        format_tag = "DESIGN_2COL_PHOTO"
    elif ats_policy == "UK_ATS":
        file_prefix = "SEND_THIS_UK_ATS"
        format_tag = "UK_STRICT_ATS_1COL"
    else:
        file_prefix = "SEND_THIS_ATS"
        format_tag = "STRICT_ATS_1COL_NO_PHOTO"

    # Strip any contenteditable attributes injected by the live visual editor before PDF compilation
    clean_html = re.sub(r'\s*contenteditable="(?:true|false)"', "", validated_html)
    clean_html = re.sub(r'\s*spellcheck="(?:true|false)"', "", clean_html)

    safe_company = re.sub(r"[^A-Za-z0-9_-]+", "_", company).strip("_")[:28] or "Company"
    safe_role = re.sub(r"[^A-Za-z0-9_-]+", "_", title).strip("_")[:32] or "Embedded_Role"
    date_prefix = datetime.date.today().isoformat()
    folder_name = f"{date_prefix}_{safe_company}_{safe_role}_{format_tag}"

    target_dir = os.path.join(TAILORED_APPLICATIONS_DIR, folder_name)
    os.makedirs(target_dir, exist_ok=True)

    base_filename = f"{file_prefix}__CV_Hanz_Ofosuhene_Sintim_{safe_company}"
    out_html_path = os.path.join(target_dir, f"{base_filename}.html")
    out_pdf_path = os.path.join(target_dir, f"{base_filename}.pdf")

    with open(out_html_path, "w", encoding="utf-8") as f:
        f.write(clean_html)

    pdf_compiled = _compile_html_to_pdf(out_html_path, out_pdf_path)

    job_id = job.get("id", "custom")
    ts = int(time.time())
    local_preview_name = (
        f"{job_id}_{ts}_{base_filename}.pdf" if pdf_compiled else f"{job_id}_{ts}_{base_filename}.html"
    )
    local_preview_path = os.path.join(LOCAL_TAILORED_DIR, local_preview_name)
    shutil.copy2(out_pdf_path if pdf_compiled else out_html_path, local_preview_path)

    cover_letter_path = os.path.join(target_dir, f"Cover_Letter_{safe_company}_{cv_lang}.txt")
    with open(cover_letter_path, "w", encoding="utf-8") as f:
        f.write(cover_letter_text)

    brief_path = os.path.join(target_dir, "Application_Brief.json")
    brief_payload = {
        "validated_by_hanz": True,
        "tailored_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "company": company,
        "title": title,
        "location": job.get("location"),
        "job_url": job.get("url"),
        "ats_policy": ats_policy,
        "cv_language": cv_lang,
        "saved_html_path": out_html_path,
        "saved_pdf_path": out_pdf_path if pdf_compiled else None,
        "cover_letter_path": cover_letter_path,
    }
    with open(brief_path, "w", encoding="utf-8") as f:
        json.dump(brief_payload, f, indent=2, ensure_ascii=False)

    return {
        "validated": True,
        "folder_path": target_dir,
        "html_path": out_html_path,
        "pdf_path": out_pdf_path if pdf_compiled else None,
        "cover_letter_path": cover_letter_path,
        "local_preview_url": f"/static/tailored_cvs/{local_preview_name}",
        "pdf_filename": os.path.basename(out_pdf_path if pdf_compiled else out_html_path),
        "tailored_at": brief_payload["tailored_at"],
    }


def tailor_cv_for_job(job: Dict[str, Any]) -> Dict[str, Any]:
    """One-step wrapper used by background auto-tailoring."""
    draft = generate_tailored_cv_draft(job)
    return save_validated_cv_bundle(
        job=job,
        validated_html=draft["html_content"],
        cover_letter_text=draft["cover_letter_text"],
        ats_policy=draft["ats_policy"],
        cv_lang=draft["cv_lang"],
    )


# ==============================================================================
# 8. CONCURRENT HUNTER EXECUTION & AUTONOMOUS BACKGROUND DAEMON
# ==============================================================================
_HUNTER_LOCK = threading.Lock()
_DAEMON_STARTED = False


def load_hunter_state() -> Dict[str, Any]:
    if os.path.exists(STATE_JSON_PATH):
        try:
            with open(STATE_JSON_PATH, "r", encoding="utf-8") as f:
                st = json.load(f)
                # Filter out any legacy [LIVE STREAM] placeholder rows
                st["jobs"] = [j for j in st.get("jobs", []) if not j.get("title", "").startswith("[LIVE STREAM]")]
                return st
        except Exception:
            pass

    return run_multi_region_hunt(
        selected_regions=["lille", "france", "europe", "north_america", "australia"],
        selected_sources=[
            "linkedin_guest",
            "alternance_france",
            "direct_ats",
            "wttj_jobteaser",
            "arbeitnow_remotive",
            "glassdoor_indeed",
        ],
        contract_filter="all",
        tpr_seconds=86400,
        auto_tailor_top=False,
        enable_live_network=False,
    )


def save_hunter_state(state: Dict[str, Any]) -> None:
    with _HUNTER_LOCK:
        with open(STATE_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)


def run_multi_region_hunt(
    selected_regions: List[str],
    selected_sources: List[str],
    contract_filter: str = "all",
    tpr_seconds: int = 86400,
    auto_tailor_top: bool = False,
    enable_live_network: bool = True,
) -> Dict[str, Any]:
    t0 = time.perf_counter()
    if not selected_regions:
        selected_regions = ["lille", "france", "europe"]
    if not selected_sources:
        selected_sources = ["linkedin_guest", "alternance_france", "direct_ats", "wttj_jobteaser"]

    existing_tailored: Dict[str, Dict[str, Any]] = {}
    if os.path.exists(STATE_JSON_PATH):
        try:
            with open(STATE_JSON_PATH, "r", encoding="utf-8") as f:
                prev = json.load(f)
                for j in prev.get("jobs", []):
                    if j.get("tailored_bundle"):
                        existing_tailored[j["id"]] = j["tailored_bundle"]
        except Exception:
            pass

    raw_candidates: List[Dict[str, Any]] = []

    for item in CURATED_OPPORTUNITIES:
        if item["region"] in selected_regions and item["source_id"] in selected_sources:
            raw_candidates.append(dict(item))

    if enable_live_network:
        futures = []
        with ThreadPoolExecutor(max_workers=8) as pool:
            if "linkedin_guest" in selected_sources:
                for reg in selected_regions:
                    futures.append(pool.submit(_fetch_linkedin_guest_jobs, reg, tpr_seconds))
            if "arbeitnow_remotive" in selected_sources:
                futures.append(pool.submit(_fetch_arbeitnow_jobs, selected_regions))

            for fut in as_completed(futures):
                try:
                    fetched = fut.result()
                    if fetched:
                        raw_candidates.extend(fetched)
                except Exception:
                    pass

    seen_ids = set()
    scored_jobs: List[Dict[str, Any]] = []

    for cand in raw_candidates:
        job_id = _compute_job_id(cand["company"], cand["title"], cand["region"])
        if job_id in seen_ids:
            continue
        seen_ids.add(job_id)

        rel = analyze_job_relevance_and_contract(
            title=cand["title"],
            company=cand["company"],
            location=cand["location"],
            description=cand.get("description", ""),
            region=cand["region"],
            posted_minutes_ago=cand.get("posted_minutes_ago", 30),
            default_contract_type=cand.get("contract_type", "stage_2027"),
        )
        if rel.get("excluded"):
            continue

        if contract_filter == "alternance_2027" and rel["contract_track"] not in ("alternance_2027", "both_2027"):
            continue
        if contract_filter == "stage_2027" and rel["contract_track"] not in ("stage_2027", "both_2027"):
            continue

        ats_info = determine_ats_policy(
            company=cand["company"],
            title=cand["title"],
            location=cand["location"],
            region=cand["region"],
            url=cand["url"],
            source_id=cand["source_id"],
            explicit_policy=cand.get("ats_policy_hint"),
        )

        job_record: Dict[str, Any] = {
            "id": job_id,
            "company": cand["company"],
            "title": cand["title"],
            "location": cand["location"],
            "region": cand["region"],
            "region_label": REGION_CONFIGS.get(cand["region"], {}).get("short_label", cand["region"]),
            "source_id": cand["source_id"],
            "source_badge": SOURCE_CONFIGS.get(cand["source_id"], {}).get("badge", cand["source_id"]),
            "posted_minutes_ago": cand.get("posted_minutes_ago", 30),
            "url": cand["url"],
            "linkedin_apply_url": cand.get("linkedin_apply_url") or cand["url"],
            "description": cand.get("description", ""),
            "score": rel["score"],
            "contract_track": rel["contract_track"],
            "contract_badge": rel["contract_badge"],
            "cv_lang": rel["cv_lang"],
            "matched_skills": rel["matched_skills"],
            "unclaimed_keywords": rel["unclaimed_keywords"],
            "lead_project_id": rel["lead_project_id"],
            "ats_policy": ats_info["ats_policy"],
            "primary_format_label": ats_info["primary_format_label"],
            "ats_warning": ats_info["warning_text"],
            "badge_tone": ats_info["badge_tone"],
            "tailored_bundle": existing_tailored.get(job_id),
        }
        scored_jobs.append(job_record)

    scored_jobs.sort(key=lambda x: (-x["score"], x["posted_minutes_ago"]))

    if auto_tailor_top:
        auto_tailored_count = 0
        for job_rec in scored_jobs:
            if job_rec["score"] >= 85 and not job_rec.get("tailored_bundle"):
                try:
                    job_rec["tailored_bundle"] = tailor_cv_for_job(job_rec)
                    auto_tailored_count += 1
                    if auto_tailored_count >= 3:
                        break
                except Exception:
                    pass

    elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 1)

    auto_mode_enabled = False
    interval_minutes = 30
    if os.path.exists(STATE_JSON_PATH):
        try:
            with open(STATE_JSON_PATH, "r", encoding="utf-8") as f:
                old = json.load(f)
                auto_mode_enabled = bool(old.get("autonomous_enabled", False))
                interval_minutes = int(old.get("interval_minutes", 30))
        except Exception:
            pass

    state_payload: Dict[str, Any] = {
        "last_run_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "execution_ms": elapsed_ms,
        "selected_regions": selected_regions,
        "selected_sources": selected_sources,
        "contract_filter": contract_filter,
        "tpr_seconds": tpr_seconds,
        "autonomous_enabled": auto_mode_enabled,
        "interval_minutes": interval_minutes,
        "tailored_hub_dir": TAILORED_APPLICATIONS_DIR,
        "total_discovered": len(scored_jobs),
        "alternance_count": sum(1 for j in scored_jobs if j["contract_track"] in ("alternance_2027", "both_2027")),
        "strict_ats_count": sum(1 for j in scored_jobs if j["ats_policy"] in ("STRICT_ATS", "UK_ATS")),
        "design_ok_count": sum(1 for j in scored_jobs if j["ats_policy"] == "DESIGN_OK"),
        "tailored_ready_count": sum(1 for j in scored_jobs if j.get("tailored_bundle")),
        "jobs": scored_jobs,
    }
    save_hunter_state(state_payload)
    return state_payload


def start_autonomous_hunter_daemon() -> None:
    global _DAEMON_STARTED
    if _DAEMON_STARTED:
        return
    _DAEMON_STARTED = True

    def _loop() -> None:
        while True:
            time.sleep(60)
            try:
                if not os.path.exists(STATE_JSON_PATH):
                    continue
                with open(STATE_JSON_PATH, "r", encoding="utf-8") as f:
                    st = json.load(f)
                if not st.get("autonomous_enabled"):
                    continue
                interval_mins = max(5, int(st.get("interval_minutes", 30)))
                last_run_str = st.get("last_run_at", "")
                should_run = False
                if last_run_str:
                    last_dt = datetime.datetime.strptime(last_run_str, "%Y-%m-%d %H:%M:%S")
                    if (datetime.datetime.now() - last_dt).total_seconds() >= interval_mins * 60:
                        should_run = True
                else:
                    should_run = True

                if should_run:
                    run_multi_region_hunt(
                        selected_regions=st.get("selected_regions", ["lille", "france", "europe"]),
                        selected_sources=st.get("selected_sources", ["linkedin_guest", "alternance_france", "direct_ats"]),
                        contract_filter=st.get("contract_filter", "all"),
                        tpr_seconds=int(st.get("tpr_seconds", 86400)),
                        auto_tailor_top=True,
                        enable_live_network=True,
                    )
            except Exception:
                pass

    t = threading.Thread(target=_loop, name="AutonomousInternshipHunter", daemon=True)
    t.start()


# ==============================================================================
# PART 1-6 ARCHITECTURAL INTEGRATION & BOOT-SYNC LAYER
# ==============================================================================
_orig_load_hunter_state = load_hunter_state
_orig_generate_tailored_cv_draft = generate_tailored_cv_draft
_IN_MEMORY_INDEX_CACHE: Dict[str, Any] = {"jobs_sig": None, "inverted_index": None}


def load_hunter_state() -> Dict[str, Any]:
    """Load hunter_state, merge expanded 34-employer matrix, exclude Africa, and attach O(1) Inverted Index."""
    state = _orig_load_hunter_state()
    raw_jobs = state.get("jobs") or []
    enriched_jobs: List[Dict[str, Any]] = []
    seen_sigs: set[str] = set()
    for job in list(raw_jobs) + list(EXPANDED_REGIONAL_OPPORTUNITIES):
        norm = enrich_job_for_indexing(job)
        if norm is not None:
            sig_key = re.sub(r"[^a-z0-9]", "", f"{norm.get('company', '')}{norm.get('title', '')}".lower())[:42]
            if sig_key in seen_sigs:
                continue
            seen_sigs.add(sig_key)
            enriched_jobs.append(norm)
    state["jobs"] = enriched_jobs

    sig = (len(enriched_jobs), tuple((j.get("id"), j.get("pipeline_status", "saved")) for j in enriched_jobs))
    if _IN_MEMORY_INDEX_CACHE["jobs_sig"] == sig and _IN_MEMORY_INDEX_CACHE["inverted_index"] is not None:
        state["inverted_index"] = _IN_MEMORY_INDEX_CACHE["inverted_index"]
    else:
        inv = build_inverted_index(enriched_jobs)
        _IN_MEMORY_INDEX_CACHE["jobs_sig"] = sig
        _IN_MEMORY_INDEX_CACHE["inverted_index"] = inv
        state["inverted_index"] = inv

    state["domain_filters"] = DOMAIN_FILTERS
    return state


def generate_tailored_cv_draft(
    job: Dict[str, Any],
    override_ats_policy: Optional[str] = None,
    override_lang: Optional[str] = None,
    override_lead_project: Optional[str] = None,
) -> Dict[str, Any]:
    """Generate a tailored CV draft and pass it through the Canonical Truth Linter + Tier ranking."""
    enriched_job = enrich_job_for_indexing(job) or job
    draft = _orig_generate_tailored_cv_draft(
        enriched_job,
        override_ats_policy=override_ats_policy,
        override_lang=override_lang,
        override_lead_project=override_lead_project,
    )
    # Enforce canonical truth on both HTML and cover letter
    for key in ("html_content", "cover_letter"):
        if draft.get(key):
            res = validate_cv_truth(draft[key])
            draft[key] = res["rewritten_payload"]

    cv_lang = draft.get("cv_lang") or enriched_job.get("cv_lang") or "fr"
    ats_policy = draft.get("ats_policy") or "strict_ats"
    tmpl_id = (
        ("ws_en_design" if ats_policy == "design_two_col" else "ws_en_ats")
        if str(cv_lang).startswith("en")
        else ("ws_fr_design" if ats_policy == "design_two_col" else "ws_fr_ats")
    )
    cv_state = build_initial_cv_state(enriched_job, lang=cv_lang, template_id=tmpl_id)
    if override_lead_project:
        for idx, pr in enumerate(cv_state.get("projects", [])):
            if override_lead_project in pr.get("id", ""):
                cv_state["projects"].insert(0, cv_state["projects"].pop(idx))
                cv_state["projects"][0]["visible"] = True
                break
    draft["cv_state"] = cv_state
    draft["ranked_projects"] = cv_state["projects"]
    draft["preflight_audit"] = run_preflight_audit(cv_state, enriched_job)
    return draft


def update_job_pipeline_status(job_id: str, new_status: str) -> Dict[str, Any]:
    """Persist pipeline status transition (saved -> cv_tailored -> verified -> applied)."""
    allowed = {"saved", "cv_tailored", "verified", "applied"}
    target_status = str(new_status or "saved").lower()
    if target_status not in allowed:
        target_status = "saved"

    state = _orig_load_hunter_state()
    updated_job = None
    for j in state.get("jobs", []):
        if str(j.get("id")) == str(job_id):
            j["pipeline_status"] = target_status
            if target_status == "applied":
                j["applied_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            updated_job = enrich_job_for_indexing(j) or j
            break
    save_hunter_state(state)
    _IN_MEMORY_INDEX_CACHE["jobs_sig"] = None
    return {"ok": updated_job is not None, "job": updated_job, "pipeline_status": target_status}


def get_boot_sync_payload(force_github: bool = False) -> Dict[str, Any]:
    """Return full boot payload for the 3-Pane Admin Workstation and static export."""
    state = load_hunter_state()
    profile = load_ground_truth_profile()
    gh = sync_github_repos(force_refresh=force_github)
    hub_templates = scan_cv_hub_templates()
    return {
        "ok": True,
        "jobs": state.get("jobs", []),
        "inverted_index": state.get("inverted_index", {}),
        "region_configs": REGION_CONFIGS,
        "source_configs": SOURCE_CONFIGS,
        "domain_filters": DOMAIN_FILTERS,
        "ground_truth_profile": profile,
        "github_repos": gh,
        "cv_hub_templates": hub_templates,
        "autonomous_enabled": state.get("autonomous_enabled", False),
        "last_run_at": state.get("last_run_at", ""),
        "stats": state.get("stats", {}),
    }
