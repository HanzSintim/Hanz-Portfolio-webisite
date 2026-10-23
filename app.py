"""
Hanz Ofosuhene-Sintim — Python Flask Portfolio Server & Static Compiler
=======================================================================
Run live server : python app.py
Build static    : python app.py --build-static
"""

from __future__ import annotations

import argparse
import json
import os
import time
from typing import Any, Dict

from flask import Flask, g, jsonify, render_template, request

from data_engine import (
    build_full_portfolio_payload,
    compute_euro_checkout_simulation,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
)
app.json.sort_keys = False


@app.before_request
def start_request_timer() -> None:
    g.t0 = time.perf_counter()


@app.after_request
def attach_telemetry_headers(response):
    t0 = getattr(g, "t0", None)
    if t0 is not None:
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        response.headers["X-Engine"] = "Python-3-Flask-LEAFE-Obsidian"
        response.headers["X-Response-Time"] = f"{elapsed_ms:.2f}ms"
        response.headers["Server-Timing"] = f"python_app;dur={elapsed_ms:.2f}"
    return response


@app.route("/")
def index():
    """Renders the redesigned LEAFE / Alpine-Obsidian Engineering Portfolio."""
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
    """Returns the 6 engineering systems with optional category filtering."""
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
    """Returns the 6-petal and 4-node radial proficiency vectors."""
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
def view_cv_en():
    """Renders the English Curriculum Vitae."""
    return render_template("cv_en.html")


@app.route("/cv/fr")
def view_cv_fr():
    """Renders the French Curriculum Vitae."""
    return render_template("cv_fr.html")


def build_static_bundle() -> None:
    """
    Compiles the Flask Jinja2 template and JSON API snapshots into root files
    so the repository runs both as a live Python Flask server AND on GitHub Pages.
    """
    payload = build_full_portfolio_payload()
    with app.app_context():
        rendered_html = render_template("index.html", data=payload, static_mode=True)
        rendered_cv_en = render_template("cv_en.html")
        rendered_cv_fr = render_template("cv_fr.html")

    output_html_path = os.path.join(BASE_DIR, "index.html")
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)

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

    print(f"[SUCCESS] Compiled static snapshot -> {output_html_path} and {len(endpoints)} API JSON files.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hanz Ofosuhene-Sintim Portfolio Server & Static Builder")
    parser.add_argument("--build-static", action="store_true", help="Compile static index.html and JSON API bundle")
    parser.add_argument("--port", type=int, default=5000, help="Port for Flask development server")
    args = parser.parse_args()

    if args.build_static:
        build_static_bundle()
    else:
        app.run(host="127.0.0.1", port=args.port, debug=True)
