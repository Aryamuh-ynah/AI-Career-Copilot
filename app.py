from flask import Flask, render_template, request, redirect, session
from db import Base, engine, SassionLocal
import models
import PyPDF2
import docx
import json

app = Flask(__name__)
app.secret_key = "123456789"

Base.metadata.create_all(bind=engine)


#Home
@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")

#signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    db = SessionLocal()

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = db.query(models.User).filter_by(email=email).first()
        if existing_user:
            return "User already exists"

        user = models.User(email=email, password=password)
        db.add(user)
        db.commit()

        return redirect("/login")

#login
@app.route("/login", methods=["GET", "POST"])
def login():
    db = SessionLocal()

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = db.query(models.User).filter_by(email=email, password=password).first()

        if user:
            session["user"] = user.email
            return redirect("/dashboard")
        
        else:
            return "Invalid Credentials"
        
    return render_template("login.html")

#Dashboard

@app.route("/dashboard", methods=["GET","POST"])
def dashboard():

    if "user" not in session:
        return redirect("/login")
    
    result = None

    if request.method == "POST":

        user_goal = request.form.get("role")
        resume_text = request.form.get("resume")

        file - request.files.get("file")

        #file handeling

        if file and file.name != "":
            if file.filename.endswith(".pdf"):
                try:
                    pdf_reader = PyPDF2.pdfReader(file)
                    text
                    for page in pdf_reader.pages:
                        text += page.extract_text() or ""
                    resume_text = text
                except Exception as e:
                    result = {"error": f"PDF error: {str(e)}"}

            elif file.filename.endswith(".docx"):

                try:
                    doc = docx.Document(file)
                    text = "" 
                    for para in doc.paragraphs:
                        text += para.text +"\n"
                    resume_text = text
                
                except Exception as e:
                    result = {"error:" f"Docx error: {str(e)}"}

        
    if resume_text and user_goal:
        try:
            result = analyze_resume(resume_text, user_goal)


             


if __name__ == "__main__":
    app.run(debug=True)