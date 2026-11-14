"""
cv_studio.py — Application Studio engine (CV + Cover Letter + Message) for Hanz Ofosuhene-Sintim
===============================================================================================

Source of truth
---------------
The four master CVs inside ``Hanz_CV_Hub`` ARE the truth. Nothing is invented:

    FR/ATS/CV_Ingenieur_FR_ATS_Hanz_Ofosuhene_Sintim.html        (1-col ATS, French)
    FR/Non_ATS_Design/CV_Ingenieur_FR_Hanz_Ofosuhene_Sintim.html  (navy sidebar design, French)
    EN/ATS/CV_Engineering_EN_ATS_Hanz_Ofosuhene_Sintim.html       (1-col ATS, English)
    EN/Non_ATS_Design/CV_Engineering_EN_Hanz_Ofosuhene_Sintim.html (navy sidebar design, English)

If Hanz edits one of those HTML files, every new CV follows automatically (they are re-parsed
on each request, keyed by file hash). Tailored CVs are produced by *re-using the exact master
markup and CSS* and only changing: headline, last sentence of the profile, project selection /
order (from the verified project pool), and the order of items inside skill lines.

Website sync
------------
``api/v1/projects.json`` (what the portfolio + CMS use) is fingerprinted per project. The studio
reports (a) website projects that are not yet in the CV project pool and (b) linked projects whose
website content changed since last acknowledged. Applying an update rewrites the matching entry in
every existing CV in the hub (masters, variants, saved application packs) and re-exports PDFs.
"""

from __future__ import annotations

import copy
import datetime as _dt
import hashlib
import html
import json
import os
import pathlib
import re
import shutil
import subprocess
import tempfile
import urllib.request
from html.parser import HTMLParser
from typing import Any, Dict, List, Optional, Tuple

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECTS_JSON_PATH = os.path.join(BASE_DIR, "api", "v1", "projects.json")
LIVE_PROJECTS_URL = "https://hanzsintim.github.io/Hanz-Portfolio-webisite/api/v1/projects.json"

MASTER_FILES = {
    ("fr", "ats"): os.path.join("FR", "ATS", "CV_Ingenieur_FR_ATS_Hanz_Ofosuhene_Sintim.html"),
    ("fr", "design"): os.path.join("FR", "Non_ATS_Design", "CV_Ingenieur_FR_Hanz_Ofosuhene_Sintim.html"),
    ("en", "ats"): os.path.join("EN", "ATS", "CV_Engineering_EN_ATS_Hanz_Ofosuhene_Sintim.html"),
    ("en", "design"): os.path.join("EN", "Non_ATS_Design", "CV_Engineering_EN_Hanz_Ofosuhene_Sintim.html"),
}

VOID_TAGS = {"meta", "br", "img", "hr", "link", "input", "source", "wbr"}

# A4 page geometry used by the masters
ATS_PRINT_WIDTH_MM = 184   # 210mm - 2 x 13mm (@page margin)
ATS_PRINT_HEIGHT_MM = 281  # 297mm - 2 x 8mm


def hub_root() -> str:
    """Hub location (overridable for tests via HANZ_CV_HUB)."""
    return os.environ.get("HANZ_CV_HUB", r"C:\Users\hanzs\Desktop\Hanz_CV_Hub")


def studio_dir() -> str:
    d = os.path.join(hub_root(), "_studio")
    os.makedirs(d, exist_ok=True)
    return d


def applications_dir() -> str:
    d = os.path.join(hub_root(), "Applications")
    os.makedirs(d, exist_ok=True)
    return d


# =============================================================================
# 1. MINIMAL LOSSLESS HTML TREE (stdlib only)
# =============================================================================
class Node:
    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag: str, attrs: Optional[List[Tuple[str, Optional[str]]]] = None, parent: "Node" = None):
        self.tag = tag
        self.attrs = attrs or []
        self.children: List[Any] = []
        self.parent = parent

    def get(self, name: str, default: str = "") -> str:
        for k, v in self.attrs:
            if k == name:
                return v if v is not None else ""
        return default

    @property
    def classes(self) -> List[str]:
        return self.get("class").split()

    def elements(self) -> List["Node"]:
        return [c for c in self.children if isinstance(c, Node)]

    def iter(self):
        for c in self.children:
            if isinstance(c, Node):
                yield c
                yield from c.iter()

    def find_all(self, tag: str = None, cls: str = None) -> List["Node"]:
        return [n for n in self.iter() if (tag is None or n.tag == tag) and (cls is None or cls in n.classes)]

    def find(self, tag: str = None, cls: str = None) -> Optional["Node"]:
        for n in self.iter():
            if (tag is None or n.tag == tag) and (cls is None or cls in n.classes):
                return n
        return None

    def inner_html(self) -> str:
        return "".join(_serialize(c) for c in self.children)

    def text(self) -> str:
        return html.unescape(re.sub(r"<[^>]+>", "", self.inner_html()))


def _serialize(node: Any) -> str:
    if isinstance(node, str):
        return node
    attrs = "".join(f' {k}="{v}"' if v is not None else f" {k}" for k, v in node.attrs)
    if node.tag in VOID_TAGS:
        return f"<{node.tag}{attrs}>"
    return f"<{node.tag}{attrs}>{node.inner_html()}</{node.tag}>"


class _TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.root = Node("#root")
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.cur)
        self.cur.children.append(node)
        if tag not in VOID_TAGS:
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not None and n.tag != tag:
            n = n.parent
        if n is not None and n.parent is not None:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.children.append(data)

    def handle_entityref(self, name):
        self.cur.children.append(f"&{name};")

    def handle_charref(self, name):
        self.cur.children.append(f"&#{name};")


def parse_html(src: str) -> Node:
    b = _TreeBuilder()
    b.feed(src)
    b.close()
    return b.root


def _clean(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def visible_text(src: str) -> str:
    """Normalised visible text of an HTML document (used for fidelity tests and keyword checks)."""
    body = src.split("<body", 1)[-1]
    body = re.sub(r"<(style|script)[^>]*>.*?</\1>", " ", body, flags=re.S | re.I)
    body = re.sub(r"<br\s*/?>", " ", body, flags=re.I)
    return _clean(html.unescape(re.sub(r"<[^>]+>", " ", body)))


def strip_tags(s: str) -> str:
    return _clean(html.unescape(re.sub(r"<[^>]+>", "", s or "")))


def slugify(s: str, max_words: int = 5) -> str:
    s = strip_tags(s).lower()
    s = re.split(r"\s[—–-]\s|\(", s)[0]
    s = (s.replace("é", "e").replace("è", "e").replace("ê", "e").replace("à", "a")
         .replace("ç", "c").replace("ô", "o").replace("î", "i").replace("û", "u"))
    words = re.findall(r"[a-z0-9]+", s)
    return "-".join(words[:max_words]) or "project"


# =============================================================================
# 2. DOCUMENT MODELS — PARSE THE MASTER MARKUP
# =============================================================================
def _head_of(src: str) -> str:
    i = src.find("<body")
    return src[:i] if i >= 0 else src


def parse_ats(src: str) -> Dict[str, Any]:
    root = parse_html(src)
    body = root.find("body")
    if body is None or body.find("h1") is None or body.find("div", "subtitle") is None:
        raise ValueError("Not an ATS master-format CV")
    doc: Dict[str, Any] = {
        "kind": "ats",
        "head": _head_of(src),
        "name": body.find("h1").inner_html(),
        "subtitle": body.find("div", "subtitle").inner_html(),
        "contact": body.find("div", "contact").inner_html(),
        "sections": [],
    }
    section = None
    for el in body.elements():
        if el.tag == "h2":
            section = {"heading": el.inner_html(), "kind": None, "items": []}
            doc["sections"].append(section)
            continue
        if section is None:
            continue
        if el.tag == "p":
            section["kind"] = "paragraph"
            section["html"] = el.inner_html()
        elif el.tag == "div" and "entry" in el.classes:
            section["kind"] = "entries"
            row = el.find("div", "row")
            sub = el.find("div", "sub")
            ul = el.find("ul")
            section["items"].append({
                "pid": el.get("data-pid"),
                "title": row.find("span", "title").inner_html() if row else "",
                "date": row.find("span", "date").inner_html() if row and row.find("span", "date") else "",
                "sub": sub.inner_html() if sub is not None else None,
                "bullets": [li.inner_html() for li in ul.elements() if li.tag == "li"] if ul else [],
            })
        elif el.tag == "ul":
            section["kind"] = "list"
            section["items"] = [li.inner_html() for li in el.elements() if li.tag == "li"]
    return doc


def parse_design(src: str) -> Dict[str, Any]:
    root = parse_html(src)
    page = root.find("div", "page")
    side = root.find("aside", "sidebar")
    main = root.find("main", "main")
    if page is None or side is None or main is None:
        raise ValueError("Not a design master-format CV")
    img = side.find("img")
    doc: Dict[str, Any] = {
        "kind": "design",
        "head": _head_of(src),
        "photo_src": img.get("src") if img is not None else "",
        "photo_alt": img.get("alt") if img is not None else "",
        "side": [],
        "name": main.find("div", "name").inner_html(),
        "role_title": main.find("div", "role-title").inner_html(),
        "role_sub": main.find("div", "role-sub").inner_html(),
        "main": [],
    }
    for sec in side.find_all("div", "side-section"):
        title = sec.find("div", "side-title").inner_html()
        if sec.find("ul", "contact-list") is not None:
            doc["side"].append({"title": title, "kind": "contact",
                                "items": [li.inner_html() for li in sec.find("ul", "contact-list").elements()]})
        elif sec.find("div", "edu-item") is not None:
            items = []
            for it in sec.find_all("div", "edu-item"):
                items.append({k: (it.find("div", c).inner_html() if it.find("div", c) is not None else None)
                              for k, c in (("date", "edu-date"), ("school", "edu-school"),
                                           ("degree", "edu-deg"), ("note", "edu-note"))})
            doc["side"].append({"title": title, "kind": "edu", "items": items})
        elif sec.find("div", "skill-group") is not None:
            groups = []
            for g in sec.find_all("div", "skill-group"):
                strong = g.find("strong")
                label = strong.inner_html() if strong is not None else ""
                rest = "".join(_serialize(c) for c in g.children if c is not strong)
                groups.append({"label": label, "text": _clean(rest)})
            doc["side"].append({"title": title, "kind": "skills", "items": groups})
        elif sec.find("ul", "side-bullets") is not None:
            doc["side"].append({"title": title, "kind": "bullets",
                                "items": [li.inner_html() for li in sec.find("ul", "side-bullets").elements()]})
    for sec in main.find_all("section", "main-section"):
        title = sec.find("div", "main-title").inner_html()
        prof = sec.find("p", "profile-text")
        if prof is not None:
            doc["main"].append({"title": title, "kind": "profile", "html": _clean(prof.inner_html())})
            continue
        items = []
        for t in sec.find_all("div", "t-item"):
            ul = t.find("ul", "t-bullets")
            items.append({
                "pid": t.get("data-pid"),
                "title": t.find("span", "t-title").inner_html(),
                "date": t.find("span", "t-date").inner_html() if t.find("span", "t-date") is not None else "",
                "meta": t.find("div", "t-meta").inner_html() if t.find("div", "t-meta") is not None else "",
                "bullets": [li.inner_html() for li in ul.elements() if li.tag == "li"] if ul else [],
            })
        doc["main"].append({"title": title, "kind": "timeline", "items": items})
    return doc


def parse_cv(src: str) -> Dict[str, Any]:
    if 'class="page"' in src and 'class="sidebar"' in src:
        return parse_design(src)
    return parse_ats(src)


# =============================================================================
# 3. RENDERERS — SAME MARKUP & CSS AS THE MASTERS
# =============================================================================
def _pid_attr(pid: Optional[str]) -> str:
    return f' data-pid="{html.escape(pid, quote=True)}"' if pid else ""


def render_ats(doc: Dict[str, Any]) -> str:
    out = [doc["head"].rstrip(), "\n<body>\n"]
    out.append(f'  <h1>{doc["name"]}</h1>\n')
    out.append(f'  <div class="subtitle">{doc["subtitle"]}</div>\n')
    out.append(f'  <div class="contact">{doc["contact"]}</div>\n')
    for sec in doc["sections"]:
        out.append(f'\n  <h2>{sec["heading"]}</h2>\n')
        if sec["kind"] == "paragraph":
            out.append(f'  <p>{sec["html"]}</p>\n')
        elif sec["kind"] == "entries":
            for it in sec["items"]:
                out.append(f'  <div class="entry"{_pid_attr(it.get("pid"))}>\n    <div class="row">\n'
                           f'      <span class="title">{it["title"]}</span>\n'
                           f'      <span class="date">{it["date"]}</span>\n    </div>\n')
                if it.get("sub") is not None:
                    out.append(f'    <div class="sub">{it["sub"]}</div>\n')
                if it.get("bullets"):
                    out.append("    <ul>\n" + "".join(f"      <li>{b}</li>\n" for b in it["bullets"]) + "    </ul>\n")
                out.append("  </div>\n")
        elif sec["kind"] == "list":
            out.append("  <ul>\n" + "".join(f"    <li>{li}</li>\n" for li in sec["items"]) + "  </ul>\n")
    out.append("</body>\n</html>\n")
    return "".join(out)


def render_design(doc: Dict[str, Any]) -> str:
    o = [doc["head"].rstrip(), '\n<body>\n<div class="page">\n  <aside class="sidebar">\n']
    if doc.get("photo_src"):
        o.append(f'    <div class="photo-wrap">\n      <img src="{doc["photo_src"]}" alt="{doc.get("photo_alt", "")}">\n    </div>\n')
    for sec in doc["side"]:
        o.append(f'\n    <div class="side-section">\n      <div class="side-title">{sec["title"]}</div>\n')
        if sec["kind"] == "contact":
            o.append('      <ul class="contact-list">\n' + "".join(f"        <li>{li}</li>\n" for li in sec["items"]) + "      </ul>\n")
        elif sec["kind"] == "edu":
            for it in sec["items"]:
                o.append('      <div class="edu-item">\n')
                for key, cls in (("date", "edu-date"), ("school", "edu-school"), ("degree", "edu-deg"), ("note", "edu-note")):
                    if it.get(key) is not None:
                        o.append(f'        <div class="{cls}">{it[key]}</div>\n')
                o.append("      </div>\n")
        elif sec["kind"] == "skills":
            for g in sec["items"]:
                o.append(f'      <div class="skill-group">\n        <strong>{g["label"]}</strong>\n        {g["text"]}\n      </div>\n')
        elif sec["kind"] == "bullets":
            o.append('      <ul class="side-bullets">\n' + "".join(f"        <li>{li}</li>\n" for li in sec["items"]) + "      </ul>\n")
        o.append("    </div>\n")
    o.append('  </aside>\n\n  <main class="main">\n    <header class="header-box">\n')
    o.append(f'      <div class="name">{doc["name"]}</div>\n')
    o.append(f'      <div class="role-title">{doc["role_title"]}</div>\n')
    o.append(f'      <div class="role-sub">{doc["role_sub"]}</div>\n')
    o.append('      <div class="header-bar"></div>\n    </header>\n')
    for sec in doc["main"]:
        o.append(f'\n    <section class="main-section">\n      <div class="main-title">{sec["title"]}</div>\n')
        if sec["kind"] == "profile":
            o.append(f'      <p class="profile-text">\n        {sec["html"]}\n      </p>\n')
        else:
            o.append('      <div class="timeline">\n')
            for it in sec["items"]:
                o.append(f'        <div class="t-item"{_pid_attr(it.get("pid"))}>\n          <div class="t-dot"></div>\n'
                         f'          <div class="t-head">\n            <span class="t-title">{it["title"]}</span>\n'
                         f'            <span class="t-date">{it["date"]}</span>\n          </div>\n'
                         f'          <div class="t-meta">{it["meta"]}</div>\n')
                if it.get("bullets"):
                    o.append('          <ul class="t-bullets">\n' + "".join(f"            <li>{b}</li>\n" for b in it["bullets"]) + "          </ul>\n")
                o.append("        </div>\n")
            o.append("      </div>\n")
        o.append("    </section>\n")
    o.append("  </main>\n</div>\n</body>\n</html>\n")
    return "".join(o)


def render_doc(doc: Dict[str, Any]) -> str:
    return render_design(doc) if doc["kind"] == "design" else render_ats(doc)


# --- Section helpers (language independent: rely on structure, not headings) ---
def ats_project_section(doc: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """First 'entries' section whose entries have no .sub line = projects (education/experience have one)."""
    for sec in doc["sections"]:
        if sec["kind"] == "entries" and sec["items"] and all(it.get("sub") is None for it in sec["items"]):
            return sec
    return None


def ats_profile_section(doc):
    return next((s for s in doc["sections"] if s["kind"] == "paragraph"), None)


def ats_skills_section(doc):
    lists = [s for s in doc["sections"] if s["kind"] == "list"]
    return lists[0] if lists else None


def design_project_section(doc):
    tls = [s for s in doc["main"] if s["kind"] == "timeline"]
    return tls[0] if tls else None


def design_profile_section(doc):
    return next((s for s in doc["main"] if s["kind"] == "profile"), None)


def design_skills_section(doc):
    return next((s for s in doc["side"] if s["kind"] == "skills"), None)


# =============================================================================
# 4. MASTERS + VERIFIED PROJECT POOL
# =============================================================================
def _sha(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:12]


def _read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _write(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def _json_load(path: str, default: Any) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return copy.deepcopy(default)


def _json_save(path: str, data: Any) -> None:
    _write(path, json.dumps(data, indent=2, ensure_ascii=False))


def load_masters() -> Dict[str, Any]:
    """Parse the four master CVs. Projects get a stable pid (slug of the EN design title)."""
    masters: Dict[str, Any] = {"docs": {}, "files": {}, "hash": {}, "errors": []}
    for key, rel in MASTER_FILES.items():
        path = os.path.join(hub_root(), rel)
        if not os.path.exists(path):
            masters["errors"].append(f"Missing master: {rel}")
            continue
        src = _read(path)
        try:
            masters["docs"][key] = parse_cv(src)
            masters["files"][key] = path
            masters["hash"][key] = _sha(src)
        except Exception as exc:  # pragma: no cover - defensive
            masters["errors"].append(f"Cannot parse {rel}: {exc}")
    _assign_master_pids(masters)
    return masters


def _master_project_items(masters, key) -> List[Dict[str, Any]]:
    doc = masters["docs"].get(key)
    if not doc:
        return []
    sec = design_project_section(doc) if doc["kind"] == "design" else ats_project_section(doc)
    return sec["items"] if sec else []


def _assign_master_pids(masters) -> None:
    """Project i is the same project in all four masters; the id comes from the EN design title."""
    ref = _master_project_items(masters, ("en", "design")) or _master_project_items(masters, ("en", "ats"))
    pids = [it.get("pid") or slugify(it["title"]) for it in ref]
    for key in MASTER_FILES:
        for i, it in enumerate(_master_project_items(masters, key)):
            if not it.get("pid"):
                it["pid"] = pids[i] if i < len(pids) else slugify(it["title"])
    masters["project_ids"] = pids


def pool_path() -> str:
    return os.path.join(studio_dir(), "project_pool.json")


def load_project_pool(masters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Master projects (always) + projects Hanz approved from the website (``_studio/project_pool.json``)."""
    masters = masters or load_masters()
    pool: List[Dict[str, Any]] = []
    for i, pid in enumerate(masters.get("project_ids", [])):
        entry = {"pid": pid, "origin": "master", "order": i, "fr": {}, "en": {}}
        for lang in ("fr", "en"):
            for kind in ("ats", "design"):
                items = _master_project_items(masters, (lang, kind))
                if i < len(items):
                    entry[lang][kind] = copy.deepcopy(items[i])
        pool.append(entry)
    extra = _json_load(pool_path(), [])
    known = {p["pid"] for p in pool}
    for j, p in enumerate(extra):
        if p.get("pid") and p["pid"] not in known:
            p = copy.deepcopy(p)
            p["origin"] = "website"
            p["order"] = 100 + j
            pool.append(p)
    return pool


def project_text(entry: Dict[str, Any], lang: str) -> str:
    parts = []
    for kind in ("ats", "design"):
        it = entry.get(lang, {}).get(kind) or {}
        parts += [it.get("title", ""), it.get("meta", ""), " ".join(it.get("bullets", []))]
    parts.append(" ".join(entry.get("tech_stack", [])))
    return strip_tags(" ".join(parts))


# =============================================================================
# 5. OFFER ANALYSIS (deterministic, offline, never invents skills)
# =============================================================================
# (offer regex, FR label, EN label). "Have" = the same regex matches Hanz's master CV text.
SKILL_LEXICON: List[Tuple[str, str, str]] = [
    (r"\bstm\s?32\b", "STM32", "STM32"),
    (r"\besp\s?32\b", "ESP32", "ESP32"),
    (r"\bmsp\s?430\b", "MSP430", "MSP430"),
    (r"\barduino\b", "Arduino", "Arduino"),
    (r"c\s?embarqu|embedded\s?c\b|langage\s?c\b|\bc\s?/\s?c\+\+|\bc\b(?![+#/])", "C embarqué", "Embedded C"),
    (r"c\+\+", "C++", "C++"),
    (r"assembl", "Assembleur", "Assembly"),
    (r"firmware|micrologiciel|logiciel\s?embarqu|embedded\s?software", "Firmware", "Firmware"),
    (r"syst[eè]mes?\s?embarqu|embedded\s?systems?", "Systèmes embarqués", "Embedded systems"),
    (r"microcontr[oô]l", "Microcontrôleurs", "Microcontrollers"),
    (r"\bpython\b", "Python", "Python"),
    (r"\bsql\b|postgres|mysql", "SQL", "SQL"),
    (r"\blinux\b", "Linux", "Linux"),
    (r"\bgit\b", "Git", "Git"),
    (r"\bgdb\b|d[ée]bog|debug", "Débogage", "Debugging"),
    (r"\btests?\b|testing|validation|v[ée]rification|\bqa\b|qualit", "Tests & validation", "Testing & validation"),
    (r"\buart\b", "UART", "UART"),
    (r"\bpwm\b", "PWM", "PWM"),
    (r"\bspi\b", "SPI", "SPI"),
    (r"\bi2c\b|i²c", "I2C", "I2C"),
    (r"\bcan\b(?:\s?bus)?|can-?bus", "CAN", "CAN"),
    (r"capteur|sensor", "Capteurs", "Sensors"),
    (r"\bkicad\b", "KiCad", "KiCad"),
    (r"\bpcb\b|carte\s?[ée]lectronique|circuit\s?imprim", "PCB", "PCB"),
    (r"semi-?conduct|microélectron|microelectron", "Semi-conducteurs", "Semiconductors"),
    (r"robot", "Robotique", "Robotics"),
    (r"\biot\b|objets?\s?connect", "IoT", "IoT"),
    (r"t[ée]l[ée]m[ée]trie|telemetry|sans\s?fil|wireless", "Télémétrie sans fil", "Wireless telemetry"),
    (r"temps[-\s]r[ée]el|real[-\s]time", "Temps réel", "Real-time"),
    (r"\badc\b|\bcan\s?\(adc\)|acquisition", "Acquisition (ADC)", "Signal acquisition (ADC)"),
    (r"javascript|\bjs\b", "JavaScript", "JavaScript"),
    (r"\bhtml\b|\bcss\b", "HTML/CSS", "HTML/CSS"),
    (r"\bpoo\b|\boop\b|orient[ée]e?\s?objet|object[-\s]oriented", "POO", "OOP"),
    (r"leadership|encadr|team\s?lead", "Leadership", "Leadership"),
    # Frequent asks that Hanz may NOT have yet — reported as gaps, never added to the CV
    (r"\brtos\b|freertos|zephyr", "RTOS", "RTOS"),
    (r"yocto|buildroot|linux\s?embarqu|embedded\s?linux", "Linux embarqué", "Embedded Linux"),
    (r"\bfpga\b", "FPGA", "FPGA"),
    (r"\bvhdl\b|verilog", "VHDL/Verilog", "VHDL/Verilog"),
    (r"matlab|simulink", "MATLAB/Simulink", "MATLAB/Simulink"),
    (r"altium", "Altium", "Altium"),
    (r"oscillosc", "Oscilloscope", "Oscilloscope"),
    (r"labview", "LabVIEW", "LabVIEW"),
    (r"\bros2?\b", "ROS", "ROS"),
    (r"autosar|automobile|automotive", "Automobile / AUTOSAR", "Automotive / AUTOSAR"),
    (r"\bjava\b(?!script)", "Java", "Java"),
    (r"docker|kubernetes", "Docker", "Docker"),
    (r"vision|opencv", "Vision (OpenCV)", "Computer vision"),
    (r"bluetooth|\bble\b", "Bluetooth/BLE", "Bluetooth/BLE"),
    (r"cyber|s[ée]curit[ée]\s?informatique", "Cybersécurité", "Cybersecurity"),
]

FR_STOP = {"le", "la", "les", "des", "et", "pour", "vous", "nous", "avec", "une", "du", "dans", "sur", "est", "au", "votre", "notre", "poste", "stage", "mission", "profil"}
EN_STOP = {"the", "and", "for", "you", "with", "our", "will", "to", "of", "is", "your", "we", "are", "in", "role", "internship", "team", "skills"}


def detect_language(text: str, default: str = "fr") -> str:
    words = re.findall(r"[a-zàâçéèêëîïôûùüÿœ']+", (text or "").lower())
    fr = sum(1 for w in words if w in FR_STOP)
    en = sum(1 for w in words if w in EN_STOP)
    if fr == en:
        return default
    return "fr" if fr > en else "en"


def detect_contract(text: str) -> str:
    low = (text or "").lower()
    if re.search(r"alternan|apprenti|work[-\s]?study|contrat\s?pro", low):
        return "alternance"
    return "stage"


def _first_match(patterns: List[str], text: str) -> str:
    for p in patterns:
        m = re.search(p, text, flags=re.I | re.M)
        if m:
            return _clean(m.group(1))[:80]
    return ""


def extract_company_role(text: str) -> Tuple[str, str]:
    try:
        import cv_architect
        intel = cv_architect.extract_offer_intelligence(text or "")
        comp = intel.get("company") or ""
        rl = intel.get("role") or intel.get("mission_topic") or ""
        if comp or rl:
            return comp, rl
    except Exception:
        pass
    company = _first_match([
        r"^\s*(?:entreprise|soci[ée]t[ée]|company|employer|employeur)\s*[:\-–]\s*(.+)$",
        r"\b(?:within the|within|chez|rejoindre|join|at)\s+([A-Z][\w&.'\- ]{1,40}?)(?:[,.!\n()]| et | and | pour | to |$)",
    ], text)
    if company and company.lower() in ("the innovation department", "innovation department", "the", "our"):
        company = ""
    role = _first_match([
        r"^\s*(?:poste|intitul[ée]|titre|job\s?title|role|position|following project)\s*[:\-–]\s*(.+)$",
        r"^(.*\b(?:stage|stagiaire|alternance|alternant|internship|intern|apprenti)\b.*)$",
        r"^(.*\b(?:ing[ée]nieur|engineer|d[ée]veloppeur|developer)\b.*)$",
    ], text)
    return company, role


def analyze_offer(text: str, masters: Dict[str, Any], lang: str) -> Dict[str, Any]:
    low = (text or "").lower()
    cv_text = " ".join(visible_text(render_doc(d)) for d in masters["docs"].values()).lower()
    matched, gaps = [], []
    for pattern, fr, en in SKILL_LEXICON:
        if re.search(pattern, low, flags=re.I):
            label = fr if lang == "fr" else en
            entry = {"label": label, "pattern": pattern}
            (matched if re.search(pattern, cv_text, flags=re.I) else gaps).append(entry)
    warnings: List[str] = []
    fr = lang == "fr"
    months = [int(m) for m in re.findall(r"(\d{1,2})\s*(?:mois|months?)", low)]
    if detect_contract(text) == "stage" and months and max(months) > 4:
        warnings.append(f"L'offre mentionne {max(months)} mois — ton stage M1 est de 3 à 4 mois (avril → juillet/août 2027). Vérifie avant d'envoyer."
                        if fr else f"Offer mentions {max(months)} months — your M1 internship window is 3–4 months (April → July/August 2027). Check before sending.")
    if re.search(r"fran[cç]ais\s?(courant|bilingue|natif|c1|c2|fluent)|fluent\s?french|french\s?(c1|c2|native|fluent)|maîtrise\s?du\s?fran", low):
        warnings.append("L'offre demande un français courant — ton CV indique honnêtement A2. Mets en avant ton anglais C2 et ta progression."
                        if fr else "Offer asks for fluent French — your CV honestly states A2. Lean on native English and your progress in French.")
    if re.search(r"\b(2025|2026)\b", low) and not re.search(r"\b2027\b", low):
        warnings.append("Les dates de l'offre semblent antérieures à 2027 — l'offre est peut-être expirée."
                        if fr else "Offer dates look earlier than 2027 — the posting may be expired.")
    if re.search(r"bac\s?\+\s?5|m2\b|final[-\s]year|dernière\s?année|fin\s?d['’]?[ée]tudes", low) and detect_contract(text) == "stage":
        warnings.append("L'offre cible peut-être un stage de fin d'études (M2/Bac+5) — tu es en M1."
                        if fr else "Offer may target a final-year (M2) internship — you are in M1.")
    return {"matched": matched, "gaps": gaps, "warnings": warnings}


# =============================================================================
# 6. TAILORING
# =============================================================================
AVAIL = {
    ("fr", "stage"): "stage de 3 à 4 mois dès avril 2027",
    ("en", "stage"): "3 to 4-month internship starting in April 2027",
    ("fr", "alternance"): "alternance dès septembre 2027",
    ("en", "alternance"): "work-study (alternance) contract starting in September 2027",
}


def _focus_phrase(matched: List[Dict[str, str]], lang: str, default: str) -> str:
    labels = []
    for m in matched:
        if m["label"] not in labels and m["label"] not in ("Leadership", "Systèmes embarqués", "Embedded systems", "Microcontrôleurs", "Microcontrollers"):
            labels.append(m["label"])
    if not labels:
        return default
    return ", ".join(labels[:4])


def _headline_ats(lang: str, contract: str, focus: str, master_subtitle: str) -> str:
    base = master_subtitle.split("|")[0].strip()  # "Étudiant Ingénieur (M1) — Électronique &amp; Systèmes Embarqués"
    f = html.escape(focus, quote=False)
    if lang == "fr":
        tail = (f"Recherche de stage : {f} (3 à 4 mois, Avril – Juillet/Août 2027)" if contract == "stage"
                else f"Recherche d'alternance : {f} (dès Septembre 2027)")
    else:
        tail = (f"Seeking a 3–4 Month Internship in {f} (April – July/August 2027)" if contract == "stage"
                else f"Seeking a Work-Study (Alternance) Contract in {f} (from September 2027)")
    return f"{base} | {tail}"


def _role_sub_design(lang: str, contract: str, focus: str) -> str:
    f = html.escape(focus, quote=False)
    if lang == "fr":
        if contract == "stage":
            return f"Recherche de stage : {f}<br>Durée : 3 à 4 mois &nbsp;|&nbsp; Disponibilité : Avril – Juillet / Août 2027"
        return f"Recherche d'alternance : {f}<br>Début : Septembre 2027 &nbsp;|&nbsp; Cycle Ingénieur JUNIA ISEN"
    if contract == "stage":
        return f"Seeking an internship: {f}<br>Duration: 3–4 months &nbsp;|&nbsp; Availability: April – July / August 2027"
    return f"Seeking a work-study (alternance) contract: {f}<br>Start: September 2027 &nbsp;|&nbsp; JUNIA ISEN Engineering Cycle"


def _split_sentences(text_html: str) -> List[str]:
    parts = re.split(r"(?<=[.!?])\s+(?=[A-ZÀ-ÖØ-Ý<])", _clean(text_html))
    return [p for p in parts if p]


def _profile_last_sentence(lang: str, kind: str, contract: str, company: str, focus: str) -> str:
    av = AVAIL[(lang, contract)]
    c = html.escape(company, quote=False) if company else ""
    f = html.escape(focus.lower() if lang == "fr" else focus, quote=False)
    if lang == "fr":
        at = f" chez <strong>{c}</strong>" if (c and kind == "design") else (f" chez {c}" if c else "")
        if kind == "design":
            return (f"Rigoureux et autonome, fort d'une expérience de présidence associative auprès de plus de 800 étudiants, "
                    f"je recherche un <strong>{av}</strong>{at} pour contribuer à des missions en {f}.")
        return f"Disponible pour un {av}{at}, en {f}."
    at = f" at <strong>{c}</strong>" if (c and kind == "design") else (f" at {c}" if c else "")
    if kind == "design":
        return (f"Rigorous and autonomous, with executive leadership experience representing 800+ students, "
                f"I am seeking a <strong>{av}</strong>{at} to contribute to {f}.")
    return f"Seeking a {av}{at} to contribute to {f}."


def _reorder_skill_items(text: str, matched: List[Dict[str, str]]) -> str:
    """Move items that match the offer to the front of a comma-separated skill line (never adds items)."""
    items = [i.strip() for i in re.split(r",\s*", text) if i.strip()]
    if len(items) < 2:
        return text

    def hit(item: str) -> bool:
        plain = strip_tags(item).lower()
        return any(re.search(m["pattern"], plain, flags=re.I) for m in matched)

    front = [i for i in items if hit(i)]
    back = [i for i in items if not hit(i)]
    return ", ".join(front + back)


def rank_pool(pool: List[Dict[str, Any]], matched: List[Dict[str, str]], lang: str, links: Dict[str, str],
              website: Dict[str, Dict[str, Any]]) -> List[Tuple[int, Dict[str, Any]]]:
    scored = []
    for entry in pool:
        txt = project_text(entry, lang).lower()
        slug = links.get(entry["pid"]) or entry.get("source_slug")
        if slug and slug in website:
            txt += " " + " ".join(website[slug].get("tech_stack", [])).lower()
        score = sum(1 for m in matched if re.search(m["pattern"], txt, flags=re.I))
        if entry.get("origin") == "master":
            score += 0.25  # tie-break in favour of Hanz's curated master selection
        scored.append((score, entry))
    scored.sort(key=lambda t: (-t[0], t[1].get("order", 99)))
    return scored


def build_tailored_docs(masters, pool, req: Dict[str, Any], analysis: Dict[str, Any],
                        links: Dict[str, str], website: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    lang, contract = req["lang"], req["contract"]
    company = req.get("company", "")
    ats = copy.deepcopy(masters["docs"][(lang, "ats")])
    des = copy.deepcopy(masters["docs"][(lang, "design")])
    matched = analysis["matched"]
    default_focus = ("C embarqué / Assembleur, Tests & Analyse" if lang == "fr"
                     else "Embedded C / Assembly, Testing & Analysis")
    focus = req.get("focus") or _focus_phrase(matched, lang, default_focus)

    # Headlines
    ats["subtitle"] = req.get("headline") or _headline_ats(lang, contract, focus, ats["subtitle"])
    des["role_sub"] = _role_sub_design(lang, contract, focus)

    # Profile: keep Hanz's sentences, replace only the availability/target sentence
    for doc, sec, kind in ((ats, ats_profile_section(ats), "ats"), (des, design_profile_section(des), "design")):
        if not sec:
            continue
        if req.get("profile"):
            sec["html"] = html.escape(req["profile"], quote=False) if kind == "ats" else req["profile"]
            continue
        sents = _split_sentences(sec["html"])
        if len(sents) >= 2:
            sents[-1] = _profile_last_sentence(lang, kind, contract, company, focus)
        sec["html"] = " ".join(sents)

    # Projects: choose the N most relevant from the verified pool (N = master count -> keeps 1 page)
    n = len(ats_project_section(ats)["items"]) if ats_project_section(ats) else 4
    if req.get("project_ids"):
        by_id = {p["pid"]: p for p in pool}
        chosen = [by_id[i] for i in req["project_ids"] if i in by_id][:n]
    else:
        chosen = [e for _, e in rank_pool(pool, matched, lang, links, website)][:n]
    asec, dsec = ats_project_section(ats), design_project_section(des)
    if asec:
        asec["items"] = [copy.deepcopy(e[lang]["ats"]) for e in chosen if e.get(lang, {}).get("ats")]
    if dsec:
        dsec["items"] = [copy.deepcopy(e[lang]["design"]) for e in chosen if e.get(lang, {}).get("design")]

    # Skills: reorder inside lines (offer-matched first). Never adds a skill.
    ssec = ats_skills_section(ats)
    if ssec:
        new_items = []
        for li in ssec["items"]:
            m = re.match(r"(\s*<strong>.*?</strong>\s*)(.*)$", li, flags=re.S)
            new_items.append(m.group(1) + _reorder_skill_items(m.group(2), matched) if m else li)
        ssec["items"] = new_items
    dsk = design_skills_section(des)
    if dsk:
        for g in dsk["items"]:
            g["text"] = _reorder_skill_items(g["text"], matched)

    return {"ats": ats, "design": des, "focus": focus, "project_ids": [e["pid"] for e in chosen]}


# =============================================================================
# 7. COVER LETTER + OUTREACH MESSAGE (Hanz's facts only)
# =============================================================================
MONTHS_FR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]


def _lower_first(s: str) -> str:
    return s[:1].lower() + s[1:] if s else s


def _short_title(title_html: str) -> str:
    return re.split(r"\s[—–]\s", strip_tags(title_html))[0].strip()


def build_cover_letter(req: Dict[str, Any], tailored: Dict[str, Any], pool: List[Dict[str, Any]],
                       analysis: Dict[str, Any], today: Optional[_dt.date] = None) -> str:
    lang, contract = req["lang"], req["contract"]
    today = today or _dt.date.today()
    company = req.get("company") or ("votre entreprise" if lang == "fr" else "your company")
    role = req.get("role") or ("Stage Ingénieur Systèmes Embarqués" if lang == "fr" else "Embedded Systems Engineering Internship")
    contact = req.get("contact") or ""
    notes = _clean(req.get("notes", ""))
    by_id = {p["pid"]: p for p in pool}
    top = [by_id[i] for i in tailored["project_ids"][:2] if i in by_id]
    skills = [m["label"] for m in analysis["matched"]][:4]
    proj_lines = []
    for p in top:
        it = p[lang].get("ats") or p[lang].get("design")
        if it and it.get("bullets"):
            proj_lines.append(f"– {_short_title(it['title'])} : {_lower_first(strip_tags(it['bullets'][0]))}"
                              if lang == "fr" else f"– {_short_title(it['title'])}: {_lower_first(strip_tags(it['bullets'][0]))}")
    if lang == "fr":
        date = f"Lille, le {today.day} {MONTHS_FR[today.month - 1]} {today.year}"
        greet = f"Madame, Monsieur{(' ' + contact) if contact and not contact.lower().startswith(('m.', 'mme', 'madame', 'monsieur')) else ''}," if not contact else (
            f"{contact}," if contact.lower().startswith(("madame", "monsieur")) else f"Bonjour {contact},")
        objet = f"Objet : Candidature — {role} ({AVAIL[('fr', contract)]})"
        motivation = notes or (f"Les missions proposées chez {company} correspondent précisément au domaine dans lequel je souhaite "
                               f"approfondir mes compétences : le développement, le test et la validation de systèmes embarqués.")
        skills_txt = f" en {', '.join(skills)}" if skills else ""
        body = [
            f"Actuellement élève-ingénieur en cycle Master (M1) Électronique et Systèmes Embarqués à JUNIA ISEN Lille, et diplômé "
            f"d'un BSc en Génie Informatique de KNUST (Ghana, 2026), je vous adresse ma candidature pour le poste « {role} » chez {company}. {motivation}",
            f"Au fil de ma formation, j'ai acquis des compétences concrètes{skills_txt}. Parmi mes réalisations les plus proches de vos besoins :\n"
            + "\n".join(proj_lines),
            "En parallèle, la présidence de l'association ACES de KNUST (plus de 800 étudiants ingénieurs) et mon stage en développement "
            "logiciel et tests chez Spagard Technologies m'ont appris la rigueur, l'organisation et le travail en équipe pluridisciplinaire. "
            "Anglophone natif (C2), je progresse chaque jour en français grâce à mon immersion à Lille.",
            (f"Je suis disponible pour un {AVAIL[('fr', contract)]}. " if contract == "stage" else f"Je recherche une {AVAIL[('fr', contract)]}. ")
            + "Je serais ravi de vous présenter plus en détail mes projets lors d'un entretien.",
            "Je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées.",
        ]
        header = ("Hanz OFOSUHENE-SINTIM\nLille, France · +33 6 05 73 14 16 · hanzsintim@gmail.com\n"
                  "linkedin.com/in/hanzofosuhene-sintim · github.com/HanzSintim · hanzsintim.github.io")
        return f"{header}\n\n{company}\n{date}\n\n{objet}\n\n{greet}\n\n" + "\n\n".join(body) + "\n\nHanz OFOSUHENE-SINTIM\n"
    date = today.strftime("%d %B %Y").lstrip("0")
    greet = f"Dear {contact}," if contact else "Dear Hiring Team,"
    subject = f"Subject: Application — {role} ({AVAIL[('en', contract)]})"
    motivation = notes or (f"The responsibilities at {company} match exactly the area I want to grow in: developing, "
                           f"testing and validating embedded systems.")
    skills_txt = f" in {', '.join(skills)}" if skills else ""
    body = [
        f"I am an M1 engineering student in Electronics and Embedded Systems at JUNIA ISEN Lille and a BSc Computer Engineering "
        f"graduate from KNUST, Ghana (2026). I am writing to apply for the {role} position at {company}. {motivation}",
        f"Through my studies I have built hands-on skills{skills_txt}. The projects closest to your needs:\n" + "\n".join(proj_lines),
        "Alongside my studies, serving as President of the ACES association at KNUST (800+ engineering students) and my software "
        "development & testing internship at Spagard Technologies taught me rigour, organisation and multidisciplinary teamwork. "
        "I am a native English speaker (C2) and I am improving my French (A2) every day through immersion in Lille.",
        f"I am available for a {AVAIL[('en', contract)]}. I would welcome the chance to walk you through my projects in an interview.",
        "Kind regards,",
    ]
    header = ("Hanz OFOSUHENE-SINTIM\nLille, France · +33 6 05 73 14 16 · hanzsintim@gmail.com\n"
              "linkedin.com/in/hanzofosuhene-sintim · github.com/HanzSintim · hanzsintim.github.io")
    return f"{header}\n\n{company}\n{date}\n\n{subject}\n\n{greet}\n\n" + "\n\n".join(body) + "\n\nHanz Ofosuhene-Sintim\n"


def build_message(req: Dict[str, Any], tailored: Dict[str, Any], pool: List[Dict[str, Any]],
                  analysis: Dict[str, Any]) -> Dict[str, str]:
    lang, contract = req["lang"], req["contract"]
    company = req.get("company") or ("votre équipe" if lang == "fr" else "your team")
    role = req.get("role") or ("stage en systèmes embarqués" if lang == "fr" else "embedded systems internship")
    contact = req.get("contact") or ""
    by_id = {p["pid"]: p for p in pool}
    titles = [_short_title((by_id[i][lang].get("design") or by_id[i][lang].get("ats"))["title"])
              for i in tailored["project_ids"][:2] if i in by_id]
    skills = ", ".join(m["label"] for m in analysis["matched"][:3])
    if lang == "fr":
        hello = f"Bonjour {contact}," if contact else "Bonjour,"
        body = (f"{hello}\n\nÉlève-ingénieur M1 Électronique & Systèmes Embarqués à JUNIA ISEN Lille (BSc KNUST 2026), "
                f"je suis très intéressé par le poste « {role} » chez {company}. "
                f"J'ai notamment travaillé sur {' et '.join(titles)}{f' ({skills})' if skills else ''}. "
                f"Je suis disponible pour un {AVAIL[('fr', contract)]}.\n\n"
                f"Seriez-vous disponible pour un court échange ? Je vous joins mon CV.\n\n"
                f"Bien cordialement,\nHanz Ofosuhene-Sintim\nhanzsintim.github.io · +33 6 05 73 14 16")
        subject = f"Candidature {role} ({company}) — Hanz Ofosuhene-Sintim (JUNIA ISEN Lille)"
        linkedin_note = (f"{hello} Élève-ingénieur M1 Systèmes Embarqués à JUNIA ISEN Lille (BSc KNUST 2026), "
                         f"je candidate pour « {role} » chez {company} ({skills or 'C Embarqué, STM32'}). "
                         f"Ravi d'échanger ! — Hanz")[:295]
    else:
        hello = f"Hi {contact}," if contact else "Hello,"
        body = (f"{hello}\n\nI'm an M1 Electronics & Embedded Systems engineering student at JUNIA ISEN Lille (BSc KNUST 2026) "
                f"and I'm very interested in the {role} role at {company}. "
                f"I've worked on {' and '.join(titles)}{f' ({skills})' if skills else ''}, "
                f"and I'm available for a {AVAIL[('en', contract)]}.\n\n"
                f"Would you be open to a short call? My CV is attached.\n\n"
                f"Best regards,\nHanz Ofosuhene-Sintim\nhanzsintim.github.io · +33 6 05 73 14 16")
        subject = f"Application: {role} ({company}) — Hanz Ofosuhene-Sintim (JUNIA ISEN Lille)"
        linkedin_note = (f"{hello} I'm an M1 Embedded Systems student at JUNIA ISEN Lille (BSc KNUST 2026) "
                         f"applying for {role} at {company} ({skills or 'Embedded C, STM32'}). "
                         f"Would love to connect! — Hanz")[:295]
    return {"subject": subject, "body": body, "linkedin_note": linkedin_note}


# =============================================================================
# 8. ONE-PAGE FIT CHECK + PDF EXPORT (headless Edge / Chrome)
# =============================================================================
def find_browser() -> Optional[str]:
    for p in (r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
              r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
              r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"):
        if os.path.exists(p):
            return p
    return shutil.which("msedge") or shutil.which("chrome")


_FIT_PROBE = """<style>@media screen{%s}</style><script>
window.addEventListener('load',function(){var r={};var d=document.querySelector('.page');
if(d){var m=document.querySelector('.main'),s=document.querySelector('.sidebar');
r.over=Math.max(m.scrollHeight-m.clientHeight,s.scrollHeight-s.clientHeight);}
else{var x=document.createElement('div');x.style.height='%dmm';document.body.appendChild(x);var lim=x.offsetHeight;x.remove();
r.over=document.body.scrollHeight-lim;}
document.documentElement.setAttribute('data-overflow',String(r.over));});</script>"""


def measure_overflow(cv_html: str) -> Optional[int]:
    """Pixels of content beyond one A4 page (<= 0 means it fits). None if no browser available."""
    browser = find_browser()
    if not browser:
        return None
    width_rule = f"body{{width:{ATS_PRINT_WIDTH_MM}mm !important;max-width:{ATS_PRINT_WIDTH_MM}mm !important;}}" \
        if 'class="page"' not in cv_html else ""
    probe = _FIT_PROBE % (width_rule, ATS_PRINT_HEIGHT_MM)
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "fit.html")
        _write(p, cv_html.replace("</head>", probe + "</head>", 1))
        try:
            out = subprocess.run([browser, "--headless=new", "--disable-gpu", "--no-first-run",
                                  "--window-size=1240,1754", "--virtual-time-budget=2500", "--dump-dom",
                                  pathlib.Path(p).as_uri()], capture_output=True, timeout=60)
        except Exception:
            return None
    m = re.search(rb'data-overflow="(-?\d+)"', out.stdout)
    return int(m.group(1)) if m else None


def export_pdf(html_path: str, pdf_path: str) -> Tuple[bool, Optional[int], str]:
    browser = find_browser()
    if not browser:
        return False, None, "Edge/Chrome not found — HTML saved, print to PDF from the browser."
    try:
        subprocess.run([browser, "--headless=new", "--disable-gpu", "--no-first-run", "--no-pdf-header-footer",
                        f"--print-to-pdf={pdf_path}", pathlib.Path(html_path).as_uri()],
                       capture_output=True, timeout=90)
    except Exception as exc:
        return False, None, str(exc)
    if not os.path.exists(pdf_path):
        return False, None, "PDF not produced"
    with open(pdf_path, "rb") as f:
        pages = len(re.findall(rb"/Type\s*/Page(?!s)", f.read()))
    return True, pages, ""


def compact_to_fit(doc: Dict[str, Any], max_rounds: int = 4) -> Tuple[Dict[str, Any], Optional[int], List[str]]:
    """If a tailored CV overflows one page, trim the *last* projects' second bullet, one at a time."""
    notes: List[str] = []
    over = measure_overflow(render_doc(doc))
    rounds = 0
    while over is not None and over > 0 and rounds < max_rounds:
        sec = design_project_section(doc) if doc["kind"] == "design" else ats_project_section(doc)
        target = next((it for it in reversed(sec["items"]) if len(it.get("bullets", [])) > 1), None) if sec else None
        if not target:
            break
        target["bullets"] = target["bullets"][:1]
        notes.append(f"Trimmed 2nd bullet of “{_short_title(target['title'])}” to keep 1 page")
        over = measure_overflow(render_doc(doc))
        rounds += 1
    return doc, over, notes


# =============================================================================
# 9. WEBSITE ⇄ CV SYNC
# =============================================================================
SYNC_FIELDS = ("title_en", "title_fr", "status_en", "status_fr", "summary_en", "summary_fr",
               "architecture_en", "architecture_fr", "tech_stack", "repo_url")


def sync_state_path() -> str:
    return os.path.join(studio_dir(), "sync_state.json")


def load_website_projects(include_live: bool = False) -> Dict[str, Any]:
    local = _json_load(PROJECTS_JSON_PATH, {"projects": []})
    items = local.get("projects", local if isinstance(local, list) else [])
    website = {p.get("slug") or slugify(p.get("title_en", "")): p for p in items}
    live_info: Dict[str, Any] = {"checked": False}
    if include_live:
        try:
            with urllib.request.urlopen(urllib.request.Request(LIVE_PROJECTS_URL, headers={"User-Agent": "HanzStudio"}), timeout=5) as r:
                live = json.loads(r.read().decode("utf-8"))
            live_items = {p.get("slug"): _fingerprint(p) for p in live.get("projects", [])}
            local_fp = {s: _fingerprint(p) for s, p in website.items()}
            live_info = {"checked": True, "in_sync": live_items == local_fp,
                         "unpublished": sorted(s for s in local_fp if live_items.get(s) != local_fp[s])}
        except Exception as exc:
            live_info = {"checked": True, "error": str(exc)[:120]}
    return {"projects": website, "live": live_info}


def _snapshot(p: Dict[str, Any]) -> Dict[str, Any]:
    return {k: p.get(k) for k in SYNC_FIELDS}


def _fingerprint(p: Dict[str, Any]) -> str:
    return _sha(json.dumps(_snapshot(p), sort_keys=True, ensure_ascii=False))


def _stems(s: str) -> set:
    return {w[:5] for w in re.findall(r"[a-zà-ÿ0-9.]+", strip_tags(s).lower()) if len(w) >= 4}


def auto_link(pool: List[Dict[str, Any]], website: Dict[str, Any]) -> Dict[str, str]:
    links = {}
    for e in pool:
        if e.get("source_slug"):
            links[e["pid"]] = e["source_slug"]
            continue
        title = (e.get("en", {}).get("design") or e.get("en", {}).get("ats") or {}).get("title", "")
        best, best_score = None, 0
        for slug, p in website.items():
            score = len(_stems(_short_title(title)) & _stems(p.get("title_en", "")))
            if score > best_score:
                best, best_score = slug, score
        if best and best_score >= 2 and best not in links.values():
            links[e["pid"]] = best
    return links


def compute_sync(include_live: bool = False) -> Dict[str, Any]:
    masters = load_masters()
    pool = load_project_pool(masters)
    site = load_website_projects(include_live)
    website = site["projects"]
    state = _json_load(sync_state_path(), {"links": {}, "ack": {}, "ignored": []})
    if not state.get("links"):
        state["links"] = auto_link(pool, website)
    links = state["links"]
    first_run = not state.get("ack")
    if first_run:  # baseline: what is on the site today is what the master CVs already reflect
        state["ack"] = {slug: _snapshot(website[slug]) for slug in links.values() if slug in website}
    _json_save(sync_state_path(), state)

    linked_slugs = set(links.values())
    suggestions = []
    for slug, p in website.items():
        if slug in linked_slugs:
            old = state["ack"].get(slug)
            if old is not None and _fingerprint(old) != _fingerprint(p):
                pid = next(k for k, v in links.items() if v == slug)
                changed = [k for k in SYNC_FIELDS if old.get(k) != p.get(k)]
                prop = propose_entry_update(pool, pid, p, changed)
                suggestions.append({
                    "id": slug,
                    "type": "changed",
                    "slug": slug,
                    "pid": pid,
                    "title_en": p.get("title_en"),
                    "title_fr": p.get("title_fr"),
                    "changed_fields": changed,
                    "reason": f"Modified on website ({', '.join(changed)}) — ready to propagate to {len(find_cvs_with_project(pid, pool))} existing CV(s).",
                    "old": {k: old.get(k) for k in changed},
                    "new": {k: p.get(k) for k in changed},
                    "proposal": prop,
                    "proposed_fr_bullets": prop.get("fr", {}).get("bullets", []),
                    "proposed_en_bullets": prop.get("en", {}).get("bullets", []),
                    "affected": len(find_cvs_with_project(pid, pool)),
                })
        elif slug not in state.get("ignored", []):
            prop = propose_pool_entry(p)
            suggestions.append({
                "id": slug,
                "type": "new",
                "slug": slug,
                "title_en": p.get("title_en"),
                "title_fr": p.get("title_fr"),
                "tech_stack": p.get("tech_stack", []),
                "keywords": p.get("tech_stack", []),
                "status_en": p.get("status_en"),
                "reason": "Published on portfolio website (api/v1/projects.json) — not yet added to Hanz_CV_Hub project pool.",
                "proposal": prop,
                "proposed_fr_bullets": prop.get("fr", {}).get("bullets", []),
                "proposed_en_bullets": prop.get("en", {}).get("bullets", []),
            })
    return {
        "ok": True,
        "suggestions": suggestions,
        "links": links,
        "live": site["live"],
        "website_count": len(website),
        "local_website_count": len(website),
        "summary": {
            "new_project_suggestions": sum(1 for s in suggestions if s["type"] == "new"),
            "changed_project_updates": sum(1 for s in suggestions if s["type"] == "changed"),
        },
        "pool": [{
            "pid": e["pid"],
            "origin": e["origin"],
            "title_fr": strip_tags((e["fr"].get("ats") or {}).get("title", "")),
            "title_en": strip_tags((e["en"].get("ats") or {}).get("title", "")),
            "linked_slug": links.get(e["pid"]),
        } for e in pool],
    }


def _status_is_done(status: str) -> bool:
    return bool(re.search(r"complet|termin|production|livr|valid|deployed|finished|done", status or "", flags=re.I))


def propose_entry_update(pool, pid, site_p, changed) -> Dict[str, Any]:
    """Editable proposal: current CV wording, with deterministic adjustments derived from the website change."""
    entry = next((e for e in pool if e["pid"] == pid), None)
    prop = {}
    for lang in ("fr", "en"):
        cur = (entry or {}).get(lang, {}).get("ats") or {}
        cur_d = (entry or {}).get(lang, {}).get("design") or {}
        title = strip_tags(cur.get("title", ""))
        date = strip_tags(cur.get("date", ""))
        bullets = [strip_tags(b) for b in cur.get("bullets", [])]
        if f"title_{lang}" in changed and site_p.get(f"title_{lang}"):
            suffix = re.split(r"\s[—–]\s", title, maxsplit=1)
            title = site_p[f"title_{lang}"] + (f" — {suffix[1]}" if len(suffix) > 1 else "")
        if f"status_{lang}" in changed and _status_is_done(site_p.get(f"status_{lang}", "")):
            date = re.sub(r"\s*[–-]\s*(En cours|Présent|Present.*|Ongoing.*)$", f" – {_dt.date.today().year}", date, flags=re.I)
        arch = site_p.get(f"architecture_{lang}") or []
        if (f"architecture_{lang}" in changed or f"summary_{lang}" in changed) and arch:
            bullets = [a.rstrip(".") + "." for a in arch[:2]]
        prop[lang] = {"title": title, "date": date, "meta": strip_tags(cur_d.get("meta", "")), "bullets": bullets}
    return prop


def propose_pool_entry(p: Dict[str, Any]) -> Dict[str, Any]:
    prop = {}
    stack = ", ".join((p.get("tech_stack") or [])[:4])
    for lang in ("fr", "en"):
        arch = p.get(f"architecture_{lang}") or []
        summary = p.get(f"summary_{lang}") or ""
        bullets = [a.rstrip(".") + "." for a in arch[:2]] or [summary]
        prop[lang] = {"title": p.get(f"title_{lang}") or p.get("title_en", ""),
                      "date": "", "meta": stack, "bullets": bullets}
    return prop


def _entry_from_fields(fields: Dict[str, Any], kind: str, pid: str, old: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    esc = lambda s: html.escape(_clean(s), quote=False)
    bullets = [esc(b) for b in fields.get("bullets", []) if _clean(b)]
    if kind == "design":
        it = {"pid": pid, "title": esc(fields["title"]), "date": esc(fields.get("date", "")),
              "meta": esc(fields.get("meta", "")) if fields.get("meta") else (old or {}).get("meta", ""), "bullets": bullets}
    else:
        it = {"pid": pid, "title": esc(fields["title"]), "date": esc(fields.get("date", "")), "sub": None, "bullets": bullets}
    return it


def find_cvs_with_project(pid: str, pool: Optional[List[Dict[str, Any]]] = None) -> List[str]:
    """Every CV HTML in the hub that contains this project (by data-pid, or by its master title)."""
    pool = pool or load_project_pool()
    entry = next((e for e in pool if e["pid"] == pid), None)
    titles = set()
    if entry:
        for lang in ("fr", "en"):
            for kind in ("ats", "design"):
                if entry.get(lang, {}).get(kind):
                    titles.add(_clean(entry[lang][kind]["title"]))
    hits = []
    for path in _all_cv_html():
        try:
            src = _read(path)
        except Exception:
            continue
        if f'data-pid="{pid}"' in src or any(t and t in _clean(src) for t in titles):
            hits.append(path)
    return hits


def _all_cv_html() -> List[str]:
    out = []
    for root, dirs, files in os.walk(hub_root()):
        if "_studio" in root.split(os.sep):
            continue
        for f in files:
            if f.lower().endswith(".html"):
                out.append(os.path.join(root, f))
    return out


def _replace_project_in_doc(doc, pid, titles, new_item) -> bool:
    sec = design_project_section(doc) if doc["kind"] == "design" else ats_project_section(doc)
    if not sec:
        return False
    for i, it in enumerate(sec["items"]):
        if it.get("pid") == pid or _clean(it["title"]) in titles:
            sec["items"][i] = new_item
            return True
    return False


def apply_sync(action: Dict[str, Any], export_pdfs: bool = True) -> Dict[str, Any]:
    """action: {type: add|update|ignore|dismiss|link, slug, pid?, fields: {fr:{...}, en:{...}}}"""
    state = _json_load(sync_state_path(), {"links": {}, "ack": {}, "ignored": []})
    website = load_website_projects()["projects"]
    slug = action.get("slug")
    t = action.get("type")
    report: Dict[str, Any] = {"ok": True, "type": t, "updated_files": [], "pdfs": [], "skipped": []}

    if t == "ignore":
        state.setdefault("ignored", []).append(slug)
    elif t == "dismiss":
        state.setdefault("ack", {})[slug] = _snapshot(website.get(slug, {}))
    elif t == "add":
        fields = action["fields"]
        pid = slugify(fields["en"]["title"]) or slug
        entry = {"pid": pid, "source_slug": slug, "tech_stack": website.get(slug, {}).get("tech_stack", []),
                 "added_at": _dt.datetime.now().isoformat(timespec="seconds")}
        for lang in ("fr", "en"):
            entry[lang] = {"ats": _entry_from_fields(fields[lang], "ats", pid),
                           "design": _entry_from_fields(fields[lang], "design", pid)}
            # ATS title carries the stack (master style: "Title — Stack")
            if fields[lang].get("meta"):
                entry[lang]["ats"]["title"] = f'{entry[lang]["ats"]["title"]} — {html.escape(fields[lang]["meta"], quote=False)}'
        pool = _json_load(pool_path(), [])
        pool = [p for p in pool if p.get("pid") != pid] + [entry]
        _json_save(pool_path(), pool)
        state.setdefault("links", {})[pid] = slug
        state.setdefault("ack", {})[slug] = _snapshot(website.get(slug, {}))
        report["pid"] = pid
    elif t == "update":
        pid = action["pid"]
        pool = load_project_pool()
        entry = next((e for e in pool if e["pid"] == pid), None)
        titles = set()
        if entry:
            for lang in ("fr", "en"):
                for kind in ("ats", "design"):
                    if entry.get(lang, {}).get(kind):
                        titles.add(_clean(entry[lang][kind]["title"]))
        archive = os.path.join(studio_dir(), "archive", _dt.datetime.now().strftime("%Y%m%d_%H%M%S"))
        for path in find_cvs_with_project(pid, pool):
            src = _read(path)
            try:
                doc = parse_cv(src)
            except Exception:
                report["skipped"].append(os.path.relpath(path, hub_root()))
                continue
            lang = "en" if re.search(r'<html lang="en"', src) else "fr"
            old_item = None
            sec = design_project_section(doc) if doc["kind"] == "design" else ats_project_section(doc)
            if sec:
                old_item = next((it for it in sec["items"] if it.get("pid") == pid or _clean(it["title"]) in titles), None)
            new_item = _entry_from_fields(action["fields"][lang], doc["kind"], pid, old_item)
            if doc["kind"] == "ats" and old_item and " — " in strip_tags(old_item["title"]) and " — " not in action["fields"][lang]["title"]:
                new_item["title"] += " — " + html.escape(strip_tags(old_item["title"]).split(" — ", 1)[1], quote=False)
            if not _replace_project_in_doc(doc, pid, titles, new_item):
                report["skipped"].append(os.path.relpath(path, hub_root()))
                continue
            rel = os.path.relpath(path, hub_root())
            os.makedirs(os.path.dirname(os.path.join(archive, rel)), exist_ok=True)
            shutil.copy2(path, os.path.join(archive, rel))
            _write(path, render_doc(doc))
            report["updated_files"].append(rel)
            pdf = os.path.splitext(path)[0] + ".pdf"
            if export_pdfs and os.path.exists(pdf):
                ok, pages, err = export_pdf(path, pdf)
                report["pdfs"].append({"file": os.path.relpath(pdf, hub_root()), "ok": ok, "pages": pages, "error": err})
        # website-added projects live in the pool file — update them too
        extra = _json_load(pool_path(), [])
        for p in extra:
            if p.get("pid") == pid:
                for lang in ("fr", "en"):
                    p[lang] = {"ats": _entry_from_fields(action["fields"][lang], "ats", pid, p[lang].get("ats")),
                               "design": _entry_from_fields(action["fields"][lang], "design", pid, p[lang].get("design"))}
        _json_save(pool_path(), extra)
        state.setdefault("ack", {})[slug] = _snapshot(website.get(slug, {}))
        report["archive"] = os.path.relpath(archive, hub_root()) if report["updated_files"] else None
    elif t == "link":
        state.setdefault("links", {})[action["pid"]] = slug
        state.setdefault("ack", {})[slug] = _snapshot(website.get(slug, {}))
    else:
        return {"ok": False, "error": f"Unknown action {t}"}
    _json_save(sync_state_path(), state)
    return report


# =============================================================================
# 10. PUBLIC API — GENERATE + SAVE APPLICATION PACKS
# =============================================================================
def normalize_request(raw: Dict[str, Any]) -> Dict[str, Any]:
    text = raw.get("text", "") or ""
    company, role = raw.get("company", "").strip(), raw.get("role", "").strip()
    if not company or not role:
        c2, r2 = extract_company_role(text)
        company, role = company or c2, role or r2
    lang = raw.get("lang") or "auto"
    if lang == "auto":
        lang = detect_language(f"{role} {text}", default="fr")
    contract = raw.get("contract") or "auto"
    if contract == "auto":
        contract = detect_contract(f"{role} {text}")
    return {**raw, "text": text, "company": company, "role": role, "lang": lang, "contract": contract}


def generate_pack(raw: Dict[str, Any], fit_check: bool = False) -> Dict[str, Any]:
    req = normalize_request(raw)
    masters = load_masters()
    if masters["errors"] and (req["lang"], "ats") not in masters["docs"]:
        return {"ok": False, "error": "; ".join(masters["errors"])}
    pool = load_project_pool(masters)
    site = load_website_projects()["projects"]
    links = _json_load(sync_state_path(), {}).get("links") or auto_link(pool, site)
    analysis = analyze_offer(f"{req['role']} {req['text']}", masters, req["lang"])
    tailored = build_tailored_docs(masters, pool, req, analysis, links, site)
    notes: List[str] = []
    fit = {}
    if fit_check:
        for kind in ("ats", "design"):
            tailored[kind], over, n = compact_to_fit(tailored[kind])
            fit[kind] = over
            notes += n
    letter = build_cover_letter(req, tailored, pool, analysis)
    msg = build_message(req, tailored, pool, analysis)
    ranked = rank_pool(pool, analysis["matched"], req["lang"], links, site)
    return {
        "ok": True,
        "request": {k: req.get(k) for k in ("company", "role", "lang", "contract", "url", "contact", "notes")},
        "focus": tailored["focus"],
        "analysis": analysis,
        "project_ids": tailored["project_ids"],
        "pool": [{"pid": e["pid"], "origin": e["origin"], "score": round(s, 2),
                  "title": strip_tags((e[req["lang"]].get("ats") or {}).get("title", "")),
                  "selected": e["pid"] in tailored["project_ids"]} for s, e in ranked],
        "headline": tailored["ats"]["subtitle"],
        "ats_html": render_doc(tailored["ats"]),
        "design_html": render_doc(tailored["design"]),
        "docs": {"ats": tailored["ats"], "design": tailored["design"]},
        "letter": letter,
        "message": msg,
        "fit": fit,
        "fit_notes": notes,
        "masters_hash": masters["hash"],
    }


def _safe(s: str, n: int = 40) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", strip_tags(s)).strip("_")
    return s[:n] or "Company"


def save_pack(raw: Dict[str, Any], letter: Optional[str] = None, message: Optional[Dict[str, str]] = None,
              export_pdfs: bool = True) -> Dict[str, Any]:
    pack = generate_pack(raw, fit_check=export_pdfs)
    if not pack["ok"]:
        return pack
    req = pack["request"]
    lang = req["lang"].upper()
    folder = os.path.join(applications_dir(),
                          f"{_dt.date.today().isoformat()}_{_safe(req['company'] or 'Company', 30)}_{_safe(req['role'] or 'Role', 40)}_{lang}")
    os.makedirs(folder, exist_ok=True)
    name = f"Hanz_Ofosuhene_Sintim_{_safe(req['company'] or 'Company', 30)}"
    files = {}
    results = {}
    for kind, label in (("ats", "CV_ATS"), ("design", "CV_Design")):
        html_path = os.path.join(folder, f"{label}_{name}.html")
        _write(html_path, pack[f"{kind}_html"])
        files[f"{kind}_html"] = html_path
        if export_pdfs:
            ok, pages, err = export_pdf(html_path, os.path.splitext(html_path)[0] + ".pdf")
            results[kind] = {"ok": ok, "pages": pages, "error": err, "overflow_px": pack["fit"].get(kind)}
            if ok:
                files[f"{kind}_pdf"] = os.path.splitext(html_path)[0] + ".pdf"
    letter_text = letter if letter is not None else pack["letter"]
    msg = message or pack["message"]
    _write(os.path.join(folder, f"Cover_Letter_{name}.txt"), letter_text)
    files["letter"] = os.path.join(folder, f"Cover_Letter_{name}.txt")
    letter_html = _letter_html(letter_text, req["lang"])
    lp = os.path.join(folder, f"Cover_Letter_{name}.html")
    _write(lp, letter_html)
    if export_pdfs:
        ok, pages, err = export_pdf(lp, os.path.splitext(lp)[0] + ".pdf")
        results["letter"] = {"ok": ok, "pages": pages, "error": err}
        if ok:
            files["letter_pdf"] = os.path.splitext(lp)[0] + ".pdf"
    _write(os.path.join(folder, "Message.txt"), f"Subject: {msg['subject']}\n\n{msg['body']}\n")
    files["message"] = os.path.join(folder, "Message.txt")
    _json_save(os.path.join(folder, "application.json"), {
        "created_at": _dt.datetime.now().isoformat(timespec="seconds"),
        "request": {**req, "text": raw.get("text", "")},
        "project_ids": pack["project_ids"], "analysis": pack["analysis"], "focus": pack["focus"],
        "masters_hash": pack["masters_hash"], "exports": results, "fit_notes": pack["fit_notes"],
    })
    return {"ok": True, "folder": folder, "files": files, "exports": results, "fit_notes": pack["fit_notes"]}


def _letter_html(text: str, lang: str) -> str:
    paras = "".join(f"<p>{html.escape(p).replace(chr(10), '<br>')}</p>" for p in text.strip().split("\n\n"))
    return (f'<!DOCTYPE html><html lang="{lang}"><head><meta charset="UTF-8"><title>Cover Letter</title><style>'
            "*{margin:0;padding:0;box-sizing:border-box}@page{size:A4 portrait;margin:18mm 20mm}"
            "body{font-family:Arial,Helvetica,sans-serif;font-size:10.5pt;line-height:1.5;color:#111;max-width:210mm;margin:0 auto}"
            "p{margin-bottom:10px;text-align:justify}p:first-child{text-align:left;font-size:9.5pt;color:#163853}"
            f"</style></head><body>{paras}</body></html>")


def list_applications() -> List[Dict[str, Any]]:
    out = []
    root = applications_dir()
    for d in sorted(os.listdir(root), reverse=True):
        meta = _json_load(os.path.join(root, d, "application.json"), None)
        if meta:
            out.append({"folder": d, "company": meta["request"].get("company"), "role": meta["request"].get("role"),
                        "lang": meta["request"].get("lang"), "created_at": meta.get("created_at"),
                        "project_ids": meta.get("project_ids", []),
                        "files": sorted(f for f in os.listdir(os.path.join(root, d)) if f.endswith((".pdf", ".txt", ".html")))})
    return out


def resolve_hub_file(rel: str) -> Optional[str]:
    """Safe path join inside the hub (prevents path traversal)."""
    base = os.path.realpath(hub_root())
    full = os.path.realpath(os.path.join(base, rel))
    if not full.startswith(base + os.sep) or not os.path.isfile(full):
        return None
    return full


def studio_boot() -> Dict[str, Any]:
    masters = load_masters()
    sync_data = compute_sync(include_live=False)
    return {
        "hub_root": hub_root(),
        "masters": {f"{k[0]}_{k[1]}": {"file": os.path.relpath(p, hub_root()), "hash": masters["hash"].get(k)}
                    for k, p in masters["files"].items()},
        "master_errors": masters["errors"],
        "applications": list_applications(),
        "browser": bool(find_browser()),
        "sync": sync_data,
    }


def get_portrait_data_uri() -> str:
    """Return embedded base64 circular navy portrait from Hanz_CV_Hub master or static/images/Hans_circle_navy.jpg."""
    import base64
    for rel in (os.path.join("assets", "Hans_circle_navy.jpg"), os.path.join("assets", "Hans_circle_navy.png")):
        cand = os.path.join(hub_root(), rel)
        if os.path.exists(cand):
            mime = "image/png" if cand.endswith(".png") else "image/jpeg"
            with open(cand, "rb") as f:
                return f"data:{mime};base64," + base64.b64encode(f.read()).decode("ascii")
    static_jpg = os.path.join(BASE_DIR, "static", "images", "Hans_circle_navy.jpg")
    if os.path.exists(static_jpg):
        with open(static_jpg, "rb") as f:
            return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("ascii")
    return "/static/images/Hans_circle_navy.jpg"


def extract_text_from_image(image_bytes: bytes, filename: str = "offer.png") -> Dict[str, Any]:
    """
    Extract job/company text from an uploaded or pasted screenshot/photo using
    Windows Native WinRT OCR (Windows.Media.Ocr.OcrEngine), then parse company, role,
    language, contract, and matched skills.
    """
    if not image_bytes:
        return {"ok": False, "error": "Empty image payload"}

    ext = os.path.splitext(filename)[1].lower() or ".png"
    if ext not in (".png", ".jpg", ".jpeg", ".webp", ".bmp"):
        ext = ".png"

    uploads_dir = os.path.join(studio_dir(), "uploads")
    os.makedirs(uploads_dir, exist_ok=True)
    saved_path = os.path.join(uploads_dir, f"offer_{int(_dt.datetime.now().timestamp()*1000)}{ext}")
    with open(saved_path, "wb") as f:
        f.write(image_bytes)

    extracted = ""
    ocr_engine_used = "windows_winrt_ocr"

    # Run Windows 10/11 Native WinRT OcrEngine via PowerShell
    ps_script = f"""
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime]
$null = [Windows.Media.Ocr.OcrEngine,Windows.Foundation,ContentType=WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder,Windows.Foundation,ContentType=WindowsRuntime]
$asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {{ $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' }})[0]
function Await($WinRtTask, $ResultType) {{
    $asTask = $asTaskGeneric.MakeGenericMethod($ResultType)
    $netTask = $asTask.Invoke($null, @($WinRtTask))
    $netTask.Wait(-1) | Out-Null
    $netTask.Result
}}
$file = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync('{saved_path.replace("'", "''")}')) ([Windows.Storage.StorageFile])
$stream = Await ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
$decoder = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
$bitmap = Await ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
$result = Await ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Write-Output ($result.Lines | ForEach-Object {{ $_.Text }})
"""
    try:
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_script],
            capture_output=True,
            timeout=20,
        )
        if proc.returncode == 0:
            extracted = proc.stdout.decode("utf-8", errors="replace").strip()
    except Exception as exc:
        ocr_engine_used = f"fallback ({exc})"

    company, role = extract_company_role(extracted)
    lang = detect_language(extracted, default="fr")
    contract = detect_contract(extracted)
    masters = load_masters()
    analysis = analyze_offer(extracted, masters, lang)
    return {
        "ok": True,
        "extracted_text": extracted,
        "company": company,
        "role": role,
        "lang": lang,
        "contract": contract,
        "matched_skills": [m["label"] for m in analysis["matched"]],
        "warnings": analysis["warnings"],
        "ocr_engine": ocr_engine_used,
        "saved_image": saved_path,
    }


def propagate_validated_website_changes(export_pdfs: bool = False) -> Dict[str, Any]:
    """
    When Hanz modifies & validates projects on his website (api/v1/projects.json),
    automatically detect any linked project that changed and propagate the update
    to existing CVs in Hanz_CV_Hub (and workspace templates), returning a full report
    plus any newly added website project suggestions.
    """
    sync_state = compute_sync(include_live=False)
    auto_updated: List[Dict[str, Any]] = []
    new_suggestions: List[Dict[str, Any]] = []

    for sug in sync_state.get("suggestions", []):
        if sug.get("type") == "changed":
            res = apply_sync(
                {
                    "type": "update",
                    "slug": sug["slug"],
                    "pid": sug["pid"],
                    "fields": sug["proposal"],
                },
                export_pdfs=export_pdfs,
            )
            auto_updated.append({
                "slug": sug["slug"],
                "pid": sug["pid"],
                "changed_fields": sug.get("changed_fields", []),
                "updated_files": res.get("updated_files", []),
                "pdfs": res.get("pdfs", []),
            })
        elif sug.get("type") == "new":
            new_suggestions.append(sug)

    # Also keep workspace templates/cv_fr_ats.html & cv_en_ats.html synced with Hanz_CV_Hub masters
    for (lang, kind), rel in MASTER_FILES.items():
        hub_file = os.path.join(hub_root(), rel)
        if os.path.exists(hub_file) and kind == "ats":
            ws_target = os.path.join(BASE_DIR, "templates", f"cv_{lang}_ats.html")
            try:
                shutil.copy2(hub_file, ws_target)
            except Exception:
                pass

    return {
        "ok": True,
        "auto_updated": auto_updated,
        "new_suggestions": new_suggestions,
        "sync": compute_sync(include_live=False),
    }
