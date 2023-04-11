import os

import sqlite3
import datetime
import random
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

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

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function




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
        
        username = request.form.get("login-username")
        password = request.form.get("login-password")
        stored_password = c.execute("SELECT hash FROM users WHERE username = ?", (username, )).fetchone()
        
        # Ensure username was submitted
        if username == '':
            return "must provide username"

        # Ensure password was submitted
        elif not password:
            return "must provide password"

        # Query database for username
        rows = c.execute("SELECT * FROM users WHERE username = ?", (username, )).fetchall()
        
        
        session["user_id"] = rows[0]["id"]
        
        if stored_password and check_password_hash(stored_password[0], password):
            return redirect("/")
        else:
            return "please try again"

        # Ensure username exists and password is correct
        #if len(rows) != 1 or not check_password_hash([0]["hash"], (password, )):
            #return "invalid username and/or password"

        # Remember which user has logged i

        # Redirect user to home page
        

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # get all form information submitted
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        # Execute SQL query to check if the username already exists
        if username == "" or password == "":
            return "Please enter user name"
        elif confirmation != password:
            return "Please enter same password again"
        
        
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        
        # If the username already exists, return an error
        if c.fetchone():
            return "Username already exists"
        
        # Otherwise, add the username to the database
        else:
            c.execute('INSERT INTO users (username, hash) VALUES (?, ?)', (username, generate_password_hash(password)))
            conn.commit()
            
        newUser = c.execute('SELECT * FROM users WHERE username = ?', (username,))    
        
        session["user_id"] = newUser[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")


