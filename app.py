import json
import os
from functools import wraps

import docx
import PyPDF2
from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from ai import analyze_resume
from db import Base, SessionLocal, engine
from models import Report, User

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-me")

Base.metadata.create_all(bind=engine)


def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first.", "error")
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    return wrapper


def extract_text_from_upload(file):
    if not file or file.filename == "":
        return ""

    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file.stream)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    if filename.endswith(".docx"):
        document = docx.Document(file.stream)
        return "\n".join(paragraph.text for paragraph in document.paragraphs)

    raise ValueError("Only PDF and DOCX files are supported.")


@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""

    if not email or not password:
        flash("Email and password are required.", "error")
        return redirect(url_for("signup"))

    if len(password) < 6:
        flash("Password must be at least 6 characters.", "error")
        return redirect(url_for("signup"))

    db = SessionLocal()

    try:
        existing_user = db.query(User).filter_by(email=email).first()

        if existing_user:
            flash("User already exists. Please login.", "error")
            return redirect(url_for("login"))

        user = User(
            email=email,
            password_hash=generate_password_hash(password),
        )

        db.add(user)
        db.commit()

        flash("Account created successfully. Please login.", "success")
        return redirect(url_for("login"))

    finally:
        db.close()


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""

    db = SessionLocal()

    try:
        user = db.query(User).filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash("Invalid email or password.", "error")
            return redirect(url_for("login"))

        session.clear()
        session["user_id"] = user.id
        session["user_email"] = user.email

        return redirect(url_for("dashboard"))

    finally:
        db.close()


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    result = None

    if request.method == "POST":
        user_goal = (request.form.get("role") or "").strip()
        resume_text = (request.form.get("resume") or "").strip()
        uploaded_file = request.files.get("file")

        try:
            uploaded_text = extract_text_from_upload(uploaded_file)
            if uploaded_text:
                resume_text = uploaded_text

            if not user_goal:
                flash("Please enter your target role.", "error")
                return redirect(url_for("dashboard"))

            if not resume_text:
                flash("Please paste your resume or upload a PDF/DOCX file.", "error")
                return redirect(url_for("dashboard"))

            provider = request.form.get("provider", "mock")
            result = analyze_resume(resume_text, user_goal, provider)

            db = SessionLocal()

            try:
                report = Report(
                    user_id=session["user_id"],
                    goal=user_goal,
                    resume_text=resume_text,
                    result_json=json.dumps(result),
                )

                db.add(report)
                db.commit()

            finally:
                db.close()

        except Exception as e:
            result = {"error": str(e)}

    return render_template(
        "dashboard.html",
        user=session.get("user_email"),
        result=result,
    )


@app.route("/history")
@login_required
def history():
    db = SessionLocal()

    try:
        reports = (
            db.query(Report)
            .filter_by(user_id=session["user_id"])
            .order_by(Report.created_at.desc())
            .all()
        )

        report_items = []

        for report in reports:
            report_items.append(
                {
                    "report": report,
                    "result": json.loads(report.result_json),
                }
            )

        return render_template("history.html", report_items=report_items)

    finally:
        db.close()


if __name__ == "__main__":
    app.run(debug=True)