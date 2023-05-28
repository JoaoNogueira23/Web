import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from datetime import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["FLASK_DEBUG"] = 1

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

#datetime variables
BithdaysToday = []


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        month = request.form.get("mounth")
        day = request.form.get("day")

        if name == '' or month == '' or day == '':
            return redirect("/")

        # TODO: Add the user's entry into the database
        db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", name, month, day)

        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html
        rows = db.execute("SELECT id, name, month, day FROM birthdays")
        day = datetime.now().day
        month = datetime.now().month
        for person in rows:
            if person['day'] == day and person['month'] == month:
                BithdaysToday.append(person)
        BithdaysToday.clear()
    
        return render_template("index.html", rows=rows)


