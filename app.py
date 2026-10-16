from flask import Flask, jsonify, render_template, request

from projects_data import PROJECTS

app = Flask(__name__)


@app.route("/")
def home():
    # Home page: send only the top 3 projects to show on the hero page
    return render_template("index.html", projects=PROJECTS[:3])


@app.route("/projects")
def projects():
    # Read the "category" from the URL, e.g. /projects?category=Software & Systems
    # If nothing is in the URL, category is None and we show everything
    category = request.args.get("category")

    if category:
        # Keep only the projects whose category matches the one in the URL
        filtered_projects = [p for p in PROJECTS if p["category"] == category]
    else:
        filtered_projects = PROJECTS

    # current_category lets the template highlight the active filter link
    return render_template(
        "projects.html",
        projects=filtered_projects,
        current_category=category,
    )


@app.route("/api/projects")
def api_projects():
    # Machine-readable version of the same data (JSON)
    return jsonify(PROJECTS)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
