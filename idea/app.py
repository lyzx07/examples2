import os

import sqlite3
import datetime
import random
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure SQLite database
conn = sqlite3.connect('rate-app.db', check_same_thread=False)
c = conn.cursor()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("login-username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("login-password"):
            return apology("must provide password", 403)
        
        username = request.form.get("login-username")

        # Query database for username
        rows = c.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchall()
        
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("login-password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/")
@login_required
def index():
    session_id = session.get("user_id")
    rows = c.execute('SELECT * FROM users WHERE id = ?', (session_id,)).fetchall()

    return render_template("index.html", rows=rows, session_id=session_id)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)
        
        elif len(request.form.get("username")) < 5 or len(request.form.get("username")) > 20:
            return apology("username must be at least 5 characters but less that 20", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        
        elif len(request.form.get("password")) < 8:
            return apology("password must be at least 8 characters", 403)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 403)

        # Ensure passwords match
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords must match", 403)
        
        username = request.form.get("username")

        # Query database for username
        rows = c.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchall()

        # Ensure username does not already exist
        if len(rows) == 1:
            return apology("username already exists", 403)

        # Hash password
        hash = generate_password_hash(request.form.get("password"))

        # Insert into users table
        c.execute('INSERT INTO users (username, hash) VALUES (?, ?)', (username, hash))
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
    
@app.route("/pentatonix", methods=["GET", "POST"])
@login_required
def pentatonix():
    return render_template("pentatonix.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")