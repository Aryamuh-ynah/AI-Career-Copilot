from flask import Flask, render_template, request, redirect, session
from db import Base, engine, SassionLocal
import models
import PyPDF2
import docx
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "App is ON"


if __name__ == "__main__":
    app.run(debug=True)