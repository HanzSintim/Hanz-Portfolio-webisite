"""Flask application with FR/EN i18n, JSON persistence, and Project Studio."""

import re
from flask import (
    Flask,
    abort,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)

from projects_data import load_projects, save_projects
from translations import UI_TEXT

app = Flask(__name__)

SUPPORTED_LANGS = ("fr", "en")
LOCAL_ADDRESSES = ("127.0.0.1", "::1")
VALID_STATUSES = ("in_progress", "completed")
VALID_TONES = ("copper", "navy", "forest", "bronze", "zinc", "steel")
COOKIE_MAX_AGE = 60 * 60 * 24 * 365  # 1 year in seconds


def is_local_request():
    """Return True when the request originates from localhost."""
    return request.remote_addr in LOCAL_ADDRESSES


def get_current_lang():
    """Determine the active UI language (`"fr"` or `"en"`).

    Priority order:
    1. Explicit user override stored in the `"lang"` request cookie.
    2. Browser `Accept-Language` header negotiation via `best_match`.
    3. Fallback default to `"en"`.
    """
    cookie_lang = request.cookies.get("lang")
    if cookie_lang in SUPPORTED_LANGS:
        return cookie_lang

    best_match = request.accept_languages.best_match(list(SUPPORTED_LANGS))
    if best_match == "fr":
        return "fr"
    return "en"


def _slugify(text):
    """Convert a project title into a URL-safe slug."""
    cleaned = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return cleaned or "custom-engineering-project"


def _split_list(raw_value, sep=","):
    """Split a string or list payload into a clean list of strings."""
    if isinstance(raw_value, list):
        return [str(item).strip() for item in raw_value if str(item).strip()]
    if not raw_value:
        return []
    return [part.strip() for part in str(raw_value).split(sep) if part.strip()]


@app.context_processor
def inject_localization():
    """Inject `t`, `current_lang`, and `is_local` into all templates."""
    lang = get_current_lang()
    return {
        "t": UI_TEXT[lang],
        "current_lang": lang,
        "is_local": is_local_request(),
    }


@app.route("/set-lang/<lang>")
def set_lang(lang):
    """Set the user's preferred language cookie and redirect back."""
    target = request.referrer or url_for("home")
    response = make_response(redirect(target))
    if lang in SUPPORTED_LANGS:
        response.set_cookie("lang", lang, max_age=COOKIE_MAX_AGE)
    return response


@app.route("/")
def home():
    """Render the App-Shell Dashboard home page with all persisted projects."""
    all_projects = load_projects()
    return render_template("index.html", projects=all_projects)


@app.route("/projects")
def projects():
    """Render the engineering projects catalog with category/status filters."""
    all_projects = load_projects()
    category = request.args.get("category")
    status_filter = request.args.get("status")

    filtered = all_projects
    if category:
        filtered = [p for p in filtered if p.get("category") == category]
    if status_filter in VALID_STATUSES:
        filtered = [p for p in filtered if p.get("status") == status_filter]

    return render_template(
        "projects.html",
        projects=filtered,
        current_category=category,
        current_status=status_filter,
    )


@app.route("/api/projects")
def api_projects():
    """Return machine-readable JSON representation of all projects."""
    return jsonify(load_projects())


@app.route("/about")
def about():
    """Render the About, Education, Experience, and Contact page."""
    return render_template("about.html")


@app.route("/projects/create", methods=["POST"])
def create_project():
    """Create a new project locally and persist it to `projects.json`."""
    if not is_local_request():
        abort(403)

    payload = (
        request.get_json(silent=True)
        if request.is_json
        else request.form.to_dict()
    ) or {}

    title_en = (
        payload.get("title_en") or payload.get("title") or "New Project"
    ).strip()
    title_fr = (payload.get("title_fr") or title_en).strip()
    category = payload.get("category") or "Embedded & Hardware"
    category_fr = (
        "Embarqué & Matériel"
        if category == "Embedded & Hardware"
        else "Logiciel & Systèmes"
    )
    status = payload.get("status", "in_progress")
    if status not in VALID_STATUSES:
        status = "in_progress"

    tone = payload.get("domain_tone", "copper")
    if tone not in VALID_TONES:
        tone = "copper"

    tech_stack = _split_list(payload.get("tech_stack"), sep=",") or [
        "C/C++",
        "Embedded Systems",
    ]
    block_diagram = _split_list(payload.get("block_diagram"), sep="|")
    if not block_diagram:
        block_diagram = _split_list(payload.get("block_diagram"), sep=",")
    if not block_diagram:
        block_diagram = [
            "Sensor / Input Stage",
            "Core Processing Unit",
            "Output & Telemetry Stage",
        ]

    summary_en = (
        payload.get("summary_en")
        or payload.get("summary")
        or "Engineering system prototype."
    ).strip()
    summary_fr = (payload.get("summary_fr") or summary_en).strip()

    highlights_en = _split_list(payload.get("highlights_en"), sep="|") or [
        summary_en
    ]
    highlights_fr = (
        _split_list(payload.get("highlights_fr"), sep="|") or highlights_en
    )

    team_raw = payload.get("team_acknowledgment", "")
    if isinstance(team_raw, dict):
        team_en = team_raw.get("en", "Hanz Ofosuhene-Sintim & Project Team")
        team_fr = team_raw.get("fr", team_en)
    else:
        team_en = (
            str(team_raw).strip() or "Hanz Ofosuhene-Sintim & Project Team"
        )
        team_fr = (
            payload.get("team_acknowledgment_fr") or team_en
        ).strip()

    all_projects = load_projects()
    existing_slugs = {p.get("slug") for p in all_projects}
    base_slug = _slugify(payload.get("slug") or title_en)
    slug = base_slug
    counter = 2
    while slug in existing_slugs:
        slug = f"{base_slug}-{counter}"
        counter += 1

    new_project = {
        "slug": slug,
        "status": status,
        "category": category,
        "domain_tone": tone,
        "title": title_en,
        "tech_stack": tech_stack,
        "block_diagram": block_diagram,
        "team_acknowledgment": {
            "en": team_en,
            "fr": team_fr,
        },
        "summary": summary_en,
        "highlights": highlights_en,
        "en": {
            "title": title_en,
            "category": category,
            "status_label": (
                "Completed"
                if status == "completed"
                else "In Progress — Active R&D"
            ),
            "tech_stack": tech_stack,
            "block_diagram": block_diagram,
            "summary": summary_en,
            "highlights": highlights_en,
        },
        "fr": {
            "title": title_fr,
            "category": category_fr,
            "status_label": (
                "Terminé"
                if status == "completed"
                else "En cours — R&D Active"
            ),
            "tech_stack": tech_stack,
            "block_diagram": block_diagram,
            "summary": summary_fr,
            "highlights": highlights_fr,
        },
    }

    all_projects.insert(0, new_project)
    save_projects(all_projects)

    if request.is_json:
        return jsonify({"ok": True, "project": new_project}), 201
    return redirect(request.referrer or url_for("projects"))


@app.route("/projects/toggle-status/<slug>", methods=["POST"])
def toggle_project_status(slug):
    """Flip a project's status between `in_progress` and `completed`."""
    if not is_local_request():
        abort(403)

    all_projects = load_projects()
    updated_project = None

    for project in all_projects:
        if project.get("slug") == slug:
            current = project.get("status", "completed")
            next_status = (
                "completed" if current == "in_progress" else "in_progress"
            )
            project["status"] = next_status
            if "en" in project and isinstance(project["en"], dict):
                project["en"]["status_label"] = (
                    "Completed"
                    if next_status == "completed"
                    else "In Progress — Active R&D"
                )
            if "fr" in project and isinstance(project["fr"], dict):
                project["fr"]["status_label"] = (
                    "Terminé"
                    if next_status == "completed"
                    else "En cours — R&D Active"
                )
            updated_project = project
            break

    if updated_project is None:
        abort(404)

    save_projects(all_projects)

    if request.is_json or request.headers.get("X-Requested-With") == "fetch":
        return jsonify({"ok": True, "project": updated_project})
    return redirect(request.referrer or url_for("projects"))


@app.route("/projects/update-team/<slug>", methods=["POST"])
def update_project_team(slug):
    """Update teammate acknowledgment credits in `projects.json`."""
    if not is_local_request():
        abort(403)

    payload = (
        request.get_json(silent=True)
        if request.is_json
        else request.form.to_dict()
    ) or {}
    team_text = (payload.get("team_acknowledgment") or "").strip()
    lang = get_current_lang()

    if not team_text:
        if request.is_json:
            return jsonify({"ok": False, "error": "Empty team text"}), 400
        return redirect(request.referrer or url_for("projects"))

    all_projects = load_projects()
    updated_project = None

    for project in all_projects:
        if project.get("slug") == slug:
            ack = project.get("team_acknowledgment")
            if not isinstance(ack, dict):
                ack = {"en": str(ack or ""), "fr": str(ack or "")}
            if "team_en" in payload or "team_fr" in payload:
                if payload.get("team_en"):
                    ack["en"] = payload["team_en"].strip()
                if payload.get("team_fr"):
                    ack["fr"] = payload["team_fr"].strip()
            else:
                ack[lang] = team_text
                if not ack.get("en"):
                    ack["en"] = team_text
                if not ack.get("fr"):
                    ack["fr"] = team_text
            project["team_acknowledgment"] = ack
            updated_project = project
            break

    if updated_project is None:
        abort(404)

    save_projects(all_projects)

    if request.is_json or request.headers.get("X-Requested-With") == "fetch":
        return jsonify({"ok": True, "project": updated_project})
    return redirect(request.referrer or url_for("projects"))


if __name__ == "__main__":
    app.run(debug=True)
