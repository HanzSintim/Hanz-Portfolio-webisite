"""
Hanz Ofosuhene-Sintim — Python Flask Portfolio Server, CMS & Static Compiler
============================================================================
Run live server : python app.py
Build static    : python app.py --build-static
Admin Login     : http://127.0.0.1:5000/admin/login
Admin CMS       : http://127.0.0.1:5000/admin/dashboard
"""

from __future__ import annotations

import argparse
from functools import wraps
import hmac
import json
import os
import shutil
import time
from typing import Any, Callable, Dict, List

from flask import (
    Flask,
    abort,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from werkzeug.utils import secure_filename

from data_engine import (
    PROJECTS_JSON_PATH,
    build_full_portfolio_payload,
    compute_euro_checkout_simulation,
    load_or_seed_projects,
)
from internship_hunter import (
    REGION_CONFIGS,
    SOURCE_CONFIGS,
    TAILORED_APPLICATIONS_DIR,
    analyze_job_relevance_and_contract,
    determine_ats_policy,
    generate_tailored_cv_draft,
    load_hunter_state,
    run_multi_region_hunt,
    save_hunter_state,
    save_validated_cv_bundle,
    start_autonomous_hunter_daemon,
    tailor_cv_for_job,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def _load_dotenv_file() -> None:
    """Lightweight .env loader so no extra external package is required."""
    env_path = os.path.join(BASE_DIR, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                clean = line.strip()
                if clean and not clean.startswith("#") and "=" in clean:
                    k, v = clean.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


_load_dotenv_file()

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
)
app.json.sort_keys = False
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0


@app.after_request
def _disable_dev_cache(response):
    """Ensure local browser refreshes always load the latest CSS, JS, and HTML."""
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# ==============================================================================
# 3. FLASK FILE UPLOAD & SECURITY CONFIGURATION
# ==============================================================================
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY", "hanz-obsidian-cms-secret-key-2026-junia-knust"
)
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "HanzAdmin2026!")

app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max limit to prevent payload attacks

ABS_UPLOAD_FOLDER = os.path.join(BASE_DIR, app.config["UPLOAD_FOLDER"])
ABS_IMAGES_FOLDER = os.path.join(BASE_DIR, "static", "images")
ABS_CV_ARCHIVE_FOLDER = os.path.join(BASE_DIR, "static", "cv")

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".svg"}

# Ensure static/uploads, static/images, and api/v1 exist automatically on boot
os.makedirs(ABS_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ABS_IMAGES_FOLDER, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "api", "v1"), exist_ok=True)

# Seed static/uploads/resume.pdf on first boot from existing Engineering CV if missing
_default_resume_dest = os.path.join(ABS_UPLOAD_FOLDER, "resume.pdf")
_default_resume_src = os.path.join(
    ABS_CV_ARCHIVE_FOLDER, "CV_Engineering_EN_Hanz_Ofosuhene_Sintim.pdf"
)
if not os.path.exists(_default_resume_dest) and os.path.exists(_default_resume_src):
    shutil.copy2(_default_resume_src, _default_resume_dest)


@app.before_request
def start_request_timer() -> None:
    g.t0 = time.perf_counter()


@app.after_request
def attach_telemetry_headers(response):
    t0 = getattr(g, "t0", None)
    if t0 is not None:
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        response.headers["X-Engine"] = "Python-3-Flask-LEAFE-Obsidian-CMS"
        response.headers["X-Response-Time"] = f"{elapsed_ms:.2f}ms"
        response.headers["Server-Timing"] = f"python_app;dur={elapsed_ms:.2f}"
    return response


# ==============================================================================
# 1. SECURE ADMIN AUTHENTICATION (THE GATEKEEPER)
# ==============================================================================
def admin_required(view_func: Callable) -> Callable:
    """
    Protects all /admin/* routes.
    Unauthorized access redirects browsers to /admin/login or returns 403 Forbidden.
    """
    @wraps(view_func)
    def wrapped(*args: Any, **kwargs: Any):
        if not session.get("admin_logged_in"):
            if (
                request.args.get("format") == "json"
                or (
                    request.accept_mimetypes.accept_json
                    and not request.accept_mimetypes.accept_html
                )
            ):
                abort(403)
            return redirect(url_for("admin_login", next=request.path))
        return view_func(*args, **kwargs)

    return wrapped


@app.route("/admin")
def admin_root():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """Renders the centered glass-morphic login card and validates ADMIN_PASSWORD."""
    if session.get("admin_logged_in"):
        return redirect(url_for("admin_dashboard"))

    error = None
    if request.method == "POST":
        submitted_pw = request.form.get("password", "")
        if hmac.compare_digest(submitted_pw, ADMIN_PASSWORD):
            session["admin_logged_in"] = True
            flash("Gatekeeper unlocked. Welcome to HanzCraft Admin CMS.", "success")
            next_url = request.args.get("next") or url_for("admin_dashboard")
            return redirect(next_url)
        error = "Invalid administrator password. Access denied (403)."

    return render_template("admin_login.html", error=error)


@app.route("/admin/logout", methods=["POST", "GET"])
def admin_logout():
    session.clear()
    flash("Administrator session locked.", "info")
    return redirect(url_for("admin_login"))


# ==============================================================================
# 2. THE ADMIN DASHBOARD (/admin/dashboard) & CMS MUTATION ENDPOINTS
# ==============================================================================
@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    """Renders the secure Admin Bento Grid CMS & Internship Command Center."""
    projects = load_or_seed_projects()
    raw_projects_json = json.dumps(
        {"count": len(projects), "projects": projects}, indent=2, ensure_ascii=False
    )

    uploaded_images = sorted(
        f
        for f in os.listdir(ABS_IMAGES_FOLDER)
        if os.path.splitext(f)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
    )

    archive_cvs: List[str] = []
    if os.path.exists(ABS_CV_ARCHIVE_FOLDER):
        archive_cvs = sorted(
            f for f in os.listdir(ABS_CV_ARCHIVE_FOLDER) if f.lower().endswith(".pdf")
        )

    resume_path = os.path.join(ABS_UPLOAD_FOLDER, "resume.pdf")
    resume_meta = {
        "exists": os.path.exists(resume_path),
        "size_kb": round(os.path.getsize(resume_path) / 1024, 1)
        if os.path.exists(resume_path)
        else 0,
        "updated_at": (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(resume_path)))
            if os.path.exists(resume_path)
            else "Never"
        ),
    }

    start_autonomous_hunter_daemon()
    hunter_state = load_hunter_state()

    return render_template(
        "admin_dashboard.html",
        projects=projects,
        raw_projects_json=raw_projects_json,
        uploaded_images=uploaded_images,
        archive_cvs=archive_cvs,
        resume_meta=resume_meta,
        hunter_state=hunter_state,
        region_configs=REGION_CONFIGS,
        source_configs=SOURCE_CONFIGS,
    )


@app.route("/admin/upload-resume", methods=["POST"])
@admin_required
def admin_upload_resume():
    """Section 1: Uploads a new .pdf and overwrites static/uploads/resume.pdf."""
    promote_cv = request.form.get("promote_archive_cv", "").strip()
    dest_path = os.path.join(ABS_UPLOAD_FOLDER, "resume.pdf")

    if promote_cv:
        safe_archive = secure_filename(promote_cv)
        src_candidate = os.path.join(ABS_CV_ARCHIVE_FOLDER, promote_cv)
        if os.path.exists(src_candidate) and promote_cv.lower().endswith(".pdf"):
            shutil.copy2(src_candidate, dest_path)
            build_static_bundle()
            flash(
                f"Promoted '{promote_cv}' -> /static/uploads/resume.pdf and updated static snapshot.",
                "success",
            )
            return redirect(url_for("admin_dashboard"))
        flash(f"Archive CV '{safe_archive}' not found.", "error")
        return redirect(url_for("admin_dashboard"))

    uploaded_file = request.files.get("resume_pdf")
    if not uploaded_file or uploaded_file.filename == "":
        flash("No PDF file selected.", "error")
        return redirect(url_for("admin_dashboard"))

    safe_name = secure_filename(uploaded_file.filename)
    if not safe_name.lower().endswith(".pdf"):
        flash("Security Rejection: Only .pdf files are allowed for resume.pdf.", "error")
        return redirect(url_for("admin_dashboard"))

    uploaded_file.save(dest_path)
    build_static_bundle()
    flash(
        f"Uploaded '{safe_name}' -> overwritten /static/uploads/resume.pdf and recompiled static site.",
        "success",
    )
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/upload-image", methods=["POST"])
@admin_required
def admin_upload_image():
    """Section 2: Sanitizes filename and saves hardware/project images to static/images/."""
    image_file = request.files.get("project_image")
    if not image_file or image_file.filename == "":
        flash("No image file selected.", "error")
        return redirect(url_for("admin_dashboard"))

    safe_name = secure_filename(image_file.filename)
    ext = os.path.splitext(safe_name)[1].lower()
    if not safe_name or ext not in ALLOWED_IMAGE_EXTENSIONS:
        flash(
            "Security Rejection: Allowed image formats are .jpg, .jpeg, .png, .webp, .svg",
            "error",
        )
        return redirect(url_for("admin_dashboard"))

    dest_path = os.path.join(ABS_IMAGES_FOLDER, safe_name)
    image_file.save(dest_path)
    flash(f"Saved sanitized project image -> /static/images/{safe_name}", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/update-projects", methods=["POST"])
@admin_required
def admin_update_projects():
    """
    Section 3: Mutates api/v1/projects.json from structured bilingual cards or raw JSON,
    preserving the E.Leclerc C++17 entry and EN/FR fields, then rebuilds index.html.
    """
    mode = request.form.get("editor_mode", "structured")
    projects = load_or_seed_projects()

    if mode == "raw_json":
        raw_payload = request.form.get("raw_projects_json", "")
        try:
            parsed = json.loads(raw_payload)
            mutated_list = (
                parsed.get("projects", parsed) if isinstance(parsed, dict) else parsed
            )
            if not isinstance(mutated_list, list) or len(mutated_list) == 0:
                raise ValueError("JSON payload must contain a non-empty list of projects.")
            projects = mutated_list
        except Exception as exc:
            flash(f"JSON Parse / Validation Error: {exc}", "error")
            return redirect(url_for("admin_dashboard"))
    else:
        for idx, proj in enumerate(projects):
            proj["title_en"] = request.form.get(f"title_en_{idx}", proj.get("title_en", "")).strip()
            proj["title_fr"] = request.form.get(f"title_fr_{idx}", proj.get("title_fr", "")).strip()
            proj["status_en"] = request.form.get(f"status_en_{idx}", proj.get("status_en", "")).strip()
            proj["status_fr"] = request.form.get(f"status_fr_{idx}", proj.get("status_fr", "")).strip()
            proj["summary_en"] = request.form.get(f"summary_en_{idx}", proj.get("summary_en", "")).strip()
            proj["summary_fr"] = request.form.get(f"summary_fr_{idx}", proj.get("summary_fr", "")).strip()
            proj["repo_url"] = request.form.get(f"repo_url_{idx}", proj.get("repo_url", "")).strip()
            custom_img = request.form.get(f"image_url_{idx}", proj.get("image_url", "")).strip()
            if custom_img:
                proj["image_url"] = custom_img
            elif "image_url" in proj:
                del proj["image_url"]

            arch_en_raw = request.form.get(f"architecture_en_{idx}", "")
            if arch_en_raw.strip():
                proj["architecture_en"] = [
                    line.strip() for line in arch_en_raw.splitlines() if line.strip()
                ]

            arch_fr_raw = request.form.get(f"architecture_fr_{idx}", "")
            if arch_fr_raw.strip():
                proj["architecture_fr"] = [
                    line.strip() for line in arch_fr_raw.splitlines() if line.strip()
                ]

    with open(PROJECTS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(
            {"count": len(projects), "projects": projects},
            f,
            indent=2,
            ensure_ascii=False,
        )

    build_static_bundle()
    flash(
        "Successfully saved mutated projects.json and recompiled static index.html.",
        "success",
    )
    return redirect(url_for("admin_dashboard"))


# ==============================================================================
# 3B. AUTONOMOUS INTERNSHIP & ALTERNANCE HUNTER ENDPOINTS (/admin/hunter/*)
# ==============================================================================
@app.route("/admin/hunter/run", methods=["POST"])
@admin_required
def admin_hunter_run():
    """Executes the Concurrent Multi-Region x Multi-Site Hunter & Auto-Tailoring Engine."""
    selected_regions = request.form.getlist("regions")
    selected_sources = request.form.getlist("sources")
    contract_filter = request.form.get("contract_filter", "all").strip()
    try:
        tpr_seconds = int(request.form.get("tpr_seconds", "86400"))
    except ValueError:
        tpr_seconds = 86400
    auto_tailor_top = request.form.get("auto_tailor_top") == "1"

    state = run_multi_region_hunt(
        selected_regions=selected_regions,
        selected_sources=selected_sources,
        contract_filter=contract_filter,
        tpr_seconds=tpr_seconds,
        auto_tailor_top=auto_tailor_top,
        enable_live_network=True,
    )
    flash(
        f"Hunter scanned {len(state['selected_regions'])} regions x {len(state['selected_sources'])} sources "
        f"in {state['execution_ms']}ms -> {state['total_discovered']} roles found "
        f"({state['alternance_count']} Alternance Sept 2027, {state['tailored_ready_count']} CVs auto-tailored to Hanz_CV_Hub).",
        "success",
    )
    return redirect(url_for("admin_dashboard") + "#section-hunter")


@app.route("/admin/hunter/tailor", methods=["POST"])
@admin_required
def admin_hunter_tailor():
    """
    Honest Auto-Tailoring endpoint:
    - Either tailors a discovered job by `job_id`
    - Or tailors a custom pasted job offer (detecting ATS vs. Design & Alternance Sept 2027 vs. Stage Apr 2027)
    Saves HTML + 1-page A4 PDF + Cover Letter into C:\\Users\\hanzs\\Desktop\\Hanz_CV_Hub\\Tailored_Applications\\
    """
    state = load_hunter_state()
    job_id = request.form.get("job_id", "").strip()
    override_policy = request.form.get("override_ats_policy", "").strip() or None

    target_job = None
    if job_id:
        for j in state.get("jobs", []):
            if j.get("id") == job_id:
                target_job = j
                break

    if not target_job:
        # Custom pasted job description tailoring
        company = request.form.get("custom_company", "").strip() or "Target Employer"
        title = request.form.get("custom_title", "").strip() or "Embedded Systems Engineering Intern / Alternant"
        location = request.form.get("custom_location", "").strip() or "Lille, France"
        region = request.form.get("custom_region", "lille").strip()
        url = request.form.get("custom_url", "").strip() or "https://www.linkedin.com/jobs/"
        description = request.form.get("custom_description", "").strip()
        contract_type = request.form.get("custom_contract", "alternance_2027").strip()

        rel = analyze_job_relevance_and_contract(
            title=title,
            company=company,
            location=location,
            description=description,
            region=region,
            posted_minutes_ago=10,
            default_contract_type=contract_type,
        )
        if rel.get("excluded"):
            flash("Geographical Guardrail: African locations are excluded per your configuration.", "error")
            return redirect(url_for("admin_dashboard") + "#section-hunter")

        ats_info = determine_ats_policy(
            company=company,
            title=title,
            location=location,
            region=region,
            url=url,
            source_id="direct_ats",
            explicit_policy=override_policy,
        )
        custom_id = f"custom_{int(time.time())}"
        target_job = {
            "id": custom_id,
            "company": company,
            "title": title,
            "location": location,
            "region": region,
            "region_label": REGION_CONFIGS.get(region, {}).get("short_label", region),
            "source_id": "direct_ats",
            "source_badge": "Custom Target",
            "posted_minutes_ago": 1,
            "url": url,
            "description": description or f"Custom tailored application for {company} ({title}).",
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
        }
        state.setdefault("jobs", []).insert(0, target_job)
    elif override_policy:
        ats_info = determine_ats_policy(
            company=target_job["company"],
            title=target_job["title"],
            location=target_job["location"],
            region=target_job["region"],
            url=target_job["url"],
            source_id=target_job["source_id"],
            explicit_policy=override_policy,
        )
        target_job["ats_policy"] = ats_info["ats_policy"]
        target_job["primary_format_label"] = ats_info["primary_format_label"]
        target_job["ats_warning"] = ats_info["warning_text"]
        target_job["badge_tone"] = ats_info["badge_tone"]

    bundle = tailor_cv_for_job(target_job)
    target_job["tailored_bundle"] = bundle
    state["tailored_ready_count"] = sum(1 for j in state.get("jobs", []) if j.get("tailored_bundle"))
    save_hunter_state(state)

    flash(
        f"Honest Tailored CV & Cover Letter saved to {bundle['folder_path']} "
        f"[{target_job['primary_format_label']}] -> {bundle['pdf_filename']}",
        "success",
    )
    return redirect(url_for("admin_dashboard") + "#section-hunter")


@app.route("/admin/hunter/toggle-auto", methods=["POST"])
@admin_required
def admin_hunter_toggle_auto():
    """Toggles Autonomous Background Hunter Mode ON/OFF and updates scan interval."""
    state = load_hunter_state()
    enable_flag = request.form.get("autonomous_enabled") == "1"
    try:
        interval_mins = max(5, min(240, int(request.form.get("interval_minutes", "30"))))
    except ValueError:
        interval_mins = 30

    state["autonomous_enabled"] = enable_flag
    state["interval_minutes"] = interval_mins
    save_hunter_state(state)
    start_autonomous_hunter_daemon()

    status_label = f"ENABLED (Scanning every {interval_mins} mins)" if enable_flag else "PAUSED (Manual Trigger Only)"
    flash(f"Autonomous Internship & Alternance Hunter is now {status_label}.", "success")
    return redirect(url_for("admin_dashboard") + "#section-hunter")


@app.route("/admin/hunter/api/search", methods=["POST"])
@admin_required
def admin_hunter_api_search():
    """AJAX JSON endpoint: runs the multi-region x multi-site hunt without reloading the page."""
    payload = request.get_json(silent=True) or {}
    selected_regions = payload.get("regions") or ["lille", "france", "europe"]
    selected_sources = payload.get("sources") or ["linkedin_guest", "alternance_france", "direct_ats", "wttj_jobteaser"]
    contract_filter = payload.get("contract_filter", "all")
    try:
        tpr_seconds = int(payload.get("tpr_seconds", 86400))
    except ValueError:
        tpr_seconds = 86400
    auto_tailor_top = bool(payload.get("auto_tailor_top", False))

    state = run_multi_region_hunt(
        selected_regions=selected_regions,
        selected_sources=selected_sources,
        contract_filter=contract_filter,
        tpr_seconds=tpr_seconds,
        auto_tailor_top=auto_tailor_top,
        enable_live_network=True,
    )
    return jsonify({"ok": True, "state": state})


@app.route("/admin/hunter/api/prepare-cv", methods=["POST"])
@admin_required
def admin_hunter_api_prepare_cv():
    """
    AJAX JSON endpoint: returns a tailored CV draft (HTML + Subtitle + Profile + Cover Letter)
    for either an existing `job_id` or a custom pasted job offer so Hanz can edit it before saving.
    """
    payload = request.get_json(silent=True) or {}
    state = load_hunter_state()
    job_id = (payload.get("job_id") or "").strip()
    override_policy = (payload.get("override_ats_policy") or "").strip() or None
    override_lang = (payload.get("override_lang") or "").strip() or None
    override_lead_project = (payload.get("override_lead_project") or "").strip() or None

    target_job = None
    if job_id:
        for j in state.get("jobs", []):
            if j.get("id") == job_id:
                target_job = j
                break

    if not target_job:
        company = (payload.get("custom_company") or "Target Employer").strip()
        title = (payload.get("custom_title") or "Embedded Systems Engineering Intern / Alternant").strip()
        location = (payload.get("custom_location") or "Lille, France").strip()
        region = (payload.get("custom_region") or "lille").strip()
        url = (payload.get("custom_url") or "https://www.linkedin.com/jobs/").strip()
        description = (payload.get("custom_description") or "").strip()
        contract_type = (payload.get("custom_contract") or "alternance_2027").strip()

        rel = analyze_job_relevance_and_contract(
            title=title,
            company=company,
            location=location,
            description=description,
            region=region,
            posted_minutes_ago=5,
            default_contract_type=contract_type,
        )
        if rel.get("excluded"):
            return jsonify({"ok": False, "error": "African locations are excluded per your guardrail."}), 400

        ats_info = determine_ats_policy(
            company=company,
            title=title,
            location=location,
            region=region,
            url=url,
            source_id="direct_ats",
            explicit_policy=override_policy,
        )
        custom_id = f"custom_{int(time.time())}"
        target_job = {
            "id": custom_id,
            "company": company,
            "title": title,
            "location": location,
            "region": region,
            "region_label": REGION_CONFIGS.get(region, {}).get("short_label", region),
            "source_id": "direct_ats",
            "source_badge": "Custom Target",
            "posted_minutes_ago": 1,
            "url": url,
            "linkedin_apply_url": url,
            "description": description or f"Custom tailored application for {company} ({title}).",
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
        }
        state.setdefault("jobs", []).insert(0, target_job)
        save_hunter_state(state)

    draft = generate_tailored_cv_draft(
        target_job,
        override_ats_policy=override_policy,
        override_lang=override_lang,
        override_lead_project=override_lead_project,
    )
    return jsonify({"ok": True, "draft": draft, "job": target_job})


@app.route("/admin/hunter/api/save-validated-cv", methods=["POST"])
@admin_required
def admin_hunter_api_save_validated_cv():
    """
    AJAX JSON endpoint: compiles Hanz's edited/validated CV HTML & Cover Letter into a 1-page A4 PDF
    and writes it to C:\\Users\\hanzs\\Desktop\\Hanz_CV_Hub\\Tailored_Applications\\
    """
    payload = request.get_json(silent=True) or {}
    job_id = (payload.get("job_id") or "").strip()
    validated_html = payload.get("html_content") or ""
    cover_letter_text = payload.get("cover_letter_text") or ""
    ats_policy = (payload.get("ats_policy") or "STRICT_ATS").strip()
    cv_lang = (payload.get("cv_lang") or "EN").strip().upper()

    if not validated_html.strip():
        return jsonify({"ok": False, "error": "CV HTML content cannot be empty."}), 400

    state = load_hunter_state()
    target_job = None
    for j in state.get("jobs", []):
        if j.get("id") == job_id:
            target_job = j
            break

    if not target_job:
        target_job = {
            "id": job_id or f"custom_{int(time.time())}",
            "company": payload.get("company", "Target_Employer"),
            "title": payload.get("title", "Embedded_Systems_Role"),
            "location": payload.get("location", "Lille, France"),
            "url": payload.get("url", ""),
        }

    bundle = save_validated_cv_bundle(
        job=target_job,
        validated_html=validated_html,
        cover_letter_text=cover_letter_text,
        ats_policy=ats_policy,
        cv_lang=cv_lang,
    )
    target_job["tailored_bundle"] = bundle
    target_job["ats_policy"] = ats_policy
    target_job["cv_lang"] = cv_lang
    state["tailored_ready_count"] = sum(1 for j in state.get("jobs", []) if j.get("tailored_bundle"))
    save_hunter_state(state)

    return jsonify({"ok": True, "bundle": bundle, "job_id": target_job["id"], "tailored_ready_count": state["tailored_ready_count"]})



# ==============================================================================
# 4. PUBLIC FRONTEND & REST API ROUTES (DYNAMICALLY BOUND TO PROJECTS.JSON)
# ==============================================================================
@app.route("/")
@app.route("/about")
@app.route("/projects")
def index():
    """Renders the bilingual Engineering Portfolio dynamically bound to projects.json & resume.pdf."""
    payload = build_full_portfolio_payload()
    return render_template("index.html", data=payload, static_mode=False)


@app.route("/api/v1/profile")
def api_profile():
    """Returns engineer identity, telemetry summary, and leadership dossier."""
    payload = build_full_portfolio_payload()
    return jsonify({
        "engineer": payload["engineer"],
        "telemetry_summary": payload["telemetry_summary"],
        "leadership": payload["leadership"],
    })


@app.route("/api/v1/projects")
def api_projects():
    """Returns the engineering systems dynamically from projects.json with optional category filtering."""
    payload = build_full_portfolio_payload()
    category = request.args.get("category", "").strip().lower()
    projects = payload["projects"]
    if category and category != "all":
        projects = [p for p in projects if p["category"].lower() == category]
    return jsonify({
        "count": len(projects),
        "projects": projects,
    })


@app.route("/api/v1/infographics")
def api_infographics():
    """Returns the 6-petal radial proficiency vectors."""
    payload = build_full_portfolio_payload()
    return jsonify({
        "average_proficiency_pct": payload["telemetry_summary"]["average_proficiency_pct"],
        "skill_petals": payload["skill_petals"],
    })


@app.route("/api/v1/corridor")
def api_corridor():
    """Returns the Ghana (Accra / Kumasi) <-> France (Lille) academic & leadership corridor."""
    payload = build_full_portfolio_payload()
    return jsonify({
        "corridor": payload["corridor"],
    })


@app.route("/api/v1/pos-simulator")
def api_pos_simulator():
    """Live Python endpoint executing the E.Leclerc Euro Greedy Change & TVA 20% algorithm."""
    try:
        amount = float(request.args.get("amount", "47.97"))
        tendered = float(request.args.get("tendered", "60.00"))
    except ValueError:
        return jsonify({"error": "Invalid numeric parameters"}), 400

    amount = max(0.01, min(amount, 10000.0))
    tendered = max(amount, min(tendered, 20000.0))
    result = compute_euro_checkout_simulation(amount, tendered)
    return jsonify(result)


@app.route("/cv/en")
@app.route("/cv_en.html")
def view_cv_en():
    """Renders the English Curriculum Vitae."""
    return render_template("cv_en.html")


@app.route("/cv/fr")
@app.route("/cv_fr.html")
def view_cv_fr():
    """Renders the French Curriculum Vitae."""
    return render_template("cv_fr.html")


@app.route("/cv_general_fr.html")
def view_cv_general_fr():
    """Serves the French General CV HTML."""
    return send_from_directory(BASE_DIR, "cv_general_fr.html")


@app.route("/cv_ing_teal_fr.html")
def view_cv_ing_teal_fr():
    """Serves the Teal French Engineering CV HTML."""
    return send_from_directory(BASE_DIR, "cv_ing_teal_fr.html")


@app.route("/admin.html")
def view_admin_html_redirect():
    """Redirects /admin.html on localhost to the Flask Admin Gatekeeper."""
    return redirect(url_for("admin_login"))


def build_static_bundle() -> None:
    """
    Compiles the Flask Jinja2 template and JSON API snapshots into root files
    so the repository runs both as a live Python Flask server AND on GitHub Pages.
    """
    payload = build_full_portfolio_payload()

    # Refresh hunter_state.json with direct application requisition links
    hunter_state = run_multi_region_hunt(
        selected_regions=["lille", "france", "europe", "uk_ch", "north_america", "australia"],
        selected_sources=["linkedin_guest", "alternance_france", "direct_ats", "wttj_jobteaser"],
        contract_filter="all",
        tpr_seconds=86400,
        auto_tailor_top=False,
        enable_live_network=False,
    )
    precomputed_drafts = {
        j["id"]: generate_tailored_cv_draft(j)
        for j in hunter_state.get("jobs", [])
    }
    projects_list = load_or_seed_projects()
    raw_json_str = json.dumps(projects_list, indent=2, ensure_ascii=False)

    with app.test_request_context():
        rendered_html = render_template("index.html", data=payload, static_mode=True)
        rendered_cv_en = render_template("cv_en.html")
        rendered_cv_fr = render_template("cv_fr.html")
        rendered_admin = render_template(
            "admin_dashboard.html",
            data=payload,
            projects=projects_list,
            raw_projects_json=raw_json_str,
            uploaded_images=[],
            resume_exists=True,
            resume_meta={"exists": True, "size_kb": 124.0, "updated_at": "2026-11-04"},
            hunter_state=hunter_state,
            region_configs=REGION_CONFIGS,
            source_configs=SOURCE_CONFIGS,
            tailored_dir=TAILORED_APPLICATIONS_DIR,
            precomputed_drafts=precomputed_drafts,
            static_mode=True,
        )

    output_html_path = os.path.join(BASE_DIR, "index.html")
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)

    with open(os.path.join(BASE_DIR, "admin.html"), "w", encoding="utf-8") as f:
        f.write(rendered_admin)

    with open(os.path.join(BASE_DIR, "cv_en.html"), "w", encoding="utf-8") as f:
        f.write(rendered_cv_en)

    with open(os.path.join(BASE_DIR, "cv_fr.html"), "w", encoding="utf-8") as f:
        f.write(rendered_cv_fr)

    api_dir = os.path.join(BASE_DIR, "api", "v1")
    os.makedirs(api_dir, exist_ok=True)

    endpoints: Dict[str, Any] = {
        "profile.json": {
            "engineer": payload["engineer"],
            "telemetry_summary": payload["telemetry_summary"],
            "leadership": payload["leadership"],
        },
        "projects.json": {
            "count": len(payload["projects"]),
            "projects": payload["projects"],
        },
        "infographics.json": {
            "average_proficiency_pct": payload["telemetry_summary"]["average_proficiency_pct"],
            "skill_petals": payload["skill_petals"],
        },
        "corridor.json": {
            "corridor": payload["corridor"],
        },
        "pos-simulator.json": payload["sample_pos_simulation"],
    }

    for filename, content in endpoints.items():
        with open(os.path.join(api_dir, filename), "w", encoding="utf-8") as f:
            json.dump(content, f, indent=2, ensure_ascii=False)

    print(f"[SUCCESS] Compiled static snapshot -> {output_html_path}, admin.html, and {len(endpoints)} API JSON files.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Hanz Ofosuhene-Sintim Portfolio Server, CMS & Static Builder"
    )
    parser.add_argument(
        "--build-static",
        action="store_true",
        help="Compile static index.html and JSON API bundle",
    )
    parser.add_argument(
        "--port", type=int, default=5000, help="Port for Flask development server"
    )
    args = parser.parse_args()

    if args.build_static:
        build_static_bundle()
    else:
        app.run(host="127.0.0.1", port=args.port, debug=True)
