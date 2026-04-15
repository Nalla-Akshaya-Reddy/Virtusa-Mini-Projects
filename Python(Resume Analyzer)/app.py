import os
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename

import resume_analyzer as ra

app = Flask(__name__)
app.secret_key = "resume-analyzer-secret-key"

UPLOAD_FOLDER = Path(__file__).parent / "uploads"
ALLOWED_EXTENSIONS = {"pdf"}
UPLOAD_FOLDER.mkdir(exist_ok=True)
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def index():
    history = ra.get_history()
    return render_template("index.html", history=history)


@app.route("/analyze", methods=["POST"])
def analyze():
    if "resume" not in request.files:
        flash("No file uploaded.")
        return redirect(url_for("index"))

    file = request.files["resume"]
    job_description = request.form.get("job_description", "").strip()
    job_role = request.form.get("job_role", "General").strip()

    if file.filename == "":
        flash("Please select a PDF file.")
        return redirect(url_for("index"))

    if not allowed_file(file.filename):
        flash("Only PDF files are supported.")
        return redirect(url_for("index"))

    if not job_description:
        flash("Please paste a job description.")
        return redirect(url_for("index"))

    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(save_path)

    try:
        result = ra.analyze(save_path, job_description, job_role)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("index"))
    finally:
        if os.path.exists(save_path):
            os.remove(save_path)

    return render_template("result.html", result=result, filename=filename, job_role=job_role)


@app.route("/history")
def history():
    data = ra.get_history()
    return jsonify(data)


if __name__ == "__main__":
    ra.init_db()
    print("\n Resume Analyzer is running → http://127.0.0.1:5000\n")
    app.run(debug=True)
