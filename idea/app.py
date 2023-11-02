import os


from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    jsonify,
    url_for,
)
import sqlite3
from datetime import datetime
import random
import requests
import json
import google.auth
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import bcrypt
from functools import wraps
from validate_email import validate_email
from flask import flash
from googleapiclient.discovery import build
from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_COOKIE_SECURE"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure SQLite database
conn = sqlite3.connect("rate-app-real.db", check_same_thread=False)
c = conn.cursor()

DEVELOPER_KEY = (
    "AIzaSyDHKne5gUlTY73VT5OlfmhsZBYJqDFgA_Q"  # replace with your actual developer key
)
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


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
        password = request.form.get("login-password")

        # Query database for user
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()

        if user:
            # Check if password_bcrypt exists
            if user[3]:
                # Verify password using bcrypt
                if bcrypt.checkpw(password.encode("utf-8"), user[3]):
                    session["user_id"] = user[0]
                    session["username"] = username
                    return redirect(url_for("index"))
            else:
                # Verify password using werkzeug.security
                if check_password_hash(user[2], password):
                    session["user_id"] = user[0]
                    session["username"] = username

        # Redirect to the index route with the username as a query parameter
        return redirect(url_for("index", username=username))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/add_creator", methods=["POST"])
def add_creator():
    youtube = build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY
    )
    
    ### still need to add first and last video dates to this
    
    session_id = session.get("user_id")

    form_name = request.form.get("form_name")

    if form_name == "form1":
        username = request.form["username"]

        if not request.form.get("username"):
            return apology("must provide YouTube Creator", 403)

        search_response = (
            youtube.search().list(q=username, type="channel", part="id").execute()
        )

        # Get channel id from search response
        channelId = search_response["items"][0]["id"]["channelId"]

        # Call YouTube API to get channel statistics
        request_query = youtube.channels().list(
            part="statistics,snippet,contentDetails", id=channelId
        )
        response = request_query.execute()

        # Extract necessary data from response
        video_count = response["items"][0]["statistics"]["videoCount"]
        subscriber_count = response["items"][0]["statistics"]["subscriberCount"]
        channel_description = response["items"][0]["snippet"]["description"]
        channel_name = response["items"][0]["snippet"]["title"]
        channel_thumbnail = response["items"][0]["snippet"]["thumbnails"]["default"][
            "url"
        ]
        published_at = response["items"][0]["snippet"]["publishedAt"]
        created_date = "-"
        formatted_date = "-"
        try:
            created_date = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%S%z")
            formatted_date = created_date.strftime("%m/%d/%Y")
        except ValueError:
            pass
        playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"][
            "uploads"
        ]
        videos_list_request = youtube.playlistItems().list(
            playlistId=playlist_id, part="snippet", maxResults=1
        )
        videos_list_response = videos_list_request.execute()
        last_video_date = videos_list_response["items"][0]["snippet"]["publishedAt"]
        formatted_last_video_date = "-"
        try:
            last_video_date_obj = datetime.strptime(
                last_video_date, "%Y-%m-%dT%H:%M:%S%z"
            )
            formatted_last_video_date = last_video_date_obj.strftime("%m/%d/%Y")
        except ValueError:
            pass

        c.execute(
            "SELECT * FROM creators WHERE channel_id=? AND user_id=?",
            (channelId, session_id),
        )
        check = c.fetchone()
        if check is not None:
            # If the creator already exists, return the creator ID in the response
            pass
        else:
            # If the creator doesn't exist, add it to the 'creators' variable and return the updated 'creators' variable in the response
            c.execute(
                "INSERT INTO creators (videoCount, subscriberCount, description, thumbnail, username, channel_id, user_id) VALUES (?,?,?,?,?,?,?)",
                (
                    video_count,
                    subscriber_count,
                    channel_description,
                    channel_thumbnail,
                    channel_name,
                    channelId,
                    session_id,
                ),
            )
            conn.commit()

        c.execute(
            "SELECT highlighted_note, created_at, channel_id FROM highlight_notes WHERE user_id = ? ORDER BY created_at DESC LIMIT 1",
            (session_id,),
        )
        highlighted_note = c.fetchone()

        c.execute(
            "SELECT note, created_at, channel_id FROM notes WHERE user_id =?",
            (session_id,),
        )
        notes = c.fetchall()

        # Fetch the updated 'creators' variable
        c.execute(
            "SELECT * FROM creators WHERE user_id=? ORDER BY id DESC", (session_id,)
        )
        creators = c.fetchall()

        aspects = [
            "Likeability",
            "Humor",
            "Pity Subscription",
            "Informative",
            "Silly",
            "Funny",
            "Serious",
            "Deadpan",
            "Let's Be Friends",
            "Genuine",
            "Fake",
            "Relatable",
            "Emotional",
            "Inspirational",
            "Controversial",
        ]

        c.execute(
            "SELECT rate_value, likeability, humor, pity_subscription, informative, silly, funny, serious, deadpan, lets_be_friends, genuine, fake, relatable, emotional, inspirational, controversial, channel_id FROM ratings WHERE user_id =?",
            (session_id,),
        )
        ratings = c.fetchall()

        c.execute(
            "SELECT rate_value, likeability, humor, pity_subscription, informative, silly, funny, serious, deadpan, lets_be_friends, genuine, fake, relatable, emotional, inspirational, controversial, channel_id FROM ratings WHERE user_id =?",
            (session_id,),
        )
        columns = [column[0] for column in c.description]

        for i in range(len(columns)):
            columns[i] = columns[i].title()
            columns[i] = columns[i].replace("_", " ")

        return render_template(
            "index.html",
            exists=False,
            channelId=channelId,
            creators=creators,
            video_count=video_count,
            subscriber_count=subscriber_count,
            formatted_date=formatted_date,
            channel_description=channel_description,
            channel_thumbnail=channel_thumbnail,
            channel_name=channel_name,
            formatted_last_video_date=formatted_last_video_date,
            aspects=aspects,
            highlighted_note=highlighted_note,
            notes=notes,
            columns=columns,
            ratings=ratings,
            session_id=session_id,
        )

        # need to change username variable back from channel id .
        """return jsonify({
            "status": "success",
            "exists": False,
            "channelId": channelId,
            "creators": creators,
            "video_count": video_count,
            "subscriber_count": subscriber_count,
            "formatted_date": formatted_date,
            "channel_description": channel_description,
            "channel_thumbnail": channel_thumbnail,
            "channel_name": channel_name,
            "formatted_last_video_date": formatted_last_video_date,
            "aspects": aspects,
            "highlighted_note": highlighted_note,
            "notes": notes,
            "columns": columns,
            "ratings": ratings,
            "session_id": session_id
        })"""


@app.route("/delete_creator", methods=["POST"])
def delete_creator():
    youtube = build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY
    )

    form_name = request.form.get("form_name")
    session_id = session.get("user_id")

    if form_name == "form2":
        channelId = request.form.get("channel_id")
        c.execute(
            "DELETE FROM creators WHERE channel_id =? AND user_id=?",
            (channelId, session_id),
        )
        conn.commit()

        c.execute(
            "DELETE FROM notes WHERE channel_id =? AND user_id=?",
            (channelId, session_id),
        )
        conn.commit()

        c.execute(
            "DELETE FROM highlight_notes WHERE channel_id =? AND user_id=?",
            (channelId, session_id),
        )
        conn.commit()

        c.execute(
            "DELETE FROM ratings WHERE channel_id =? AND user_id=?",
            (channelId, session_id),
        )
        conn.commit()

        # Retrieve data from the "creators" table
        c.execute(
            "SELECT * FROM creators WHERE user_id =? ORDER BY id DESC",
            (session_id,),
        )
        creators = c.fetchall()

        c.execute(
            "SELECT highlighted_note, created_at, channel_id FROM highlight_notes WHERE user_id = ? ORDER BY created_at DESC LIMIT 1",
            (session_id,),
        )
        highlighted_note = c.fetchone()

        c.execute(
            "SELECT note, created_at, channel_id FROM notes WHERE user_id =?",
            (session_id,),
        )
        notes = c.fetchall()

        c.execute(
            "SELECT rate_value, likeability, humor, pity_subscription, informative, silly, funny, serious, deadpan, lets_be_friends, genuine, fake, relatable, emotional, inspirational, controversial, channel_id FROM ratings WHERE user_id =?",
            (session_id,),
        )
        ratings = c.fetchall()

        c.execute(
            "SELECT rate_value, likeability, humor, pity_subscription, informative, silly, funny, serious, deadpan, lets_be_friends, genuine, fake, relatable, emotional, inspirational, controversial, channel_id FROM ratings WHERE user_id =?",
            (session_id,),
        )
        columns = [column[0] for column in c.description]

        for i in range(len(columns)):
            columns[i] = columns[i].title()
            columns[i] = columns[i].replace("_", " ")

        aspects = [
            "Likeability",
            "Humor",
            "Pity Subscription",
            "Informative",
            "Silly",
            "Funny",
            "Serious",
            "Deadpan",
            "Let's Be Friends",
            "Genuine",
            "Fake",
            "Relatable",
            "Emotional",
            "Inspirational",
            "Controversial",
        ]

        response = {
            "status": "success",
            "creators": creators,
            "notes": notes,
            "session_id": session_id,
            "channelId": channelId,
            "aspects": aspects,
            "ratings": ratings,
            "highlighted_note": highlighted_note,
            "columns": columns,
        }
        return json.dumps(response)


@app.route("/add_note", methods=["POST"])
def add_note():
    youtube = build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY
    )
    
    c.execute(
        "SELECT DISTINCT channel_id FROM creators WHERE user_id =?", (session_id,)
    )
    creator_ids = c.fetchall()
    
    creator_video_dates = []

    # Call YouTube API to get channel statistics
    for channel_id in creator_ids:
        request_query = youtube.channels().list(
            part="statistics,snippet,contentDetails", id=channel_id[0]
        )
        response = request_query.execute()

        # Extract necessary data from response
        published_at = response["items"][0]["snippet"]["publishedAt"]
        created_date = "-"
        formatted_date = "-"
        try:
            created_date = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%S%z")
            formatted_date = created_date.strftime("%m/%d/%Y")
        except ValueError:
            pass
        playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"][
            "uploads"
        ]
        videos_list_request = youtube.playlistItems().list(
            playlistId=playlist_id, part="snippet", maxResults=1
        )
        videos_list_response = videos_list_request.execute()
        last_video_date = videos_list_response["items"][0]["snippet"]["publishedAt"]
        formatted_last_video_date = "-"
        try:
            last_video_date_obj = datetime.strptime(
                last_video_date, "%Y-%m-%dT%H:%M:%S%z"
            )
            formatted_last_video_date = last_video_date_obj.strftime("%m/%d/%Y")
        except ValueError:
            pass

        creator_video_dates.append({
            "channel_id": channel_id[0],
            "created_date": formatted_date,
            "last_video_date": formatted_last_video_date
        })

    form_name = request.form.get("form_name")
    session_id = session.get("user_id")

    if form_name == "form3":
        channelId = request.form.get("channel_id")
        note = request.form.get("message")
        highlighted_note = request.form.get("saved_notes")

        # Check if the exact note already exists in the database
        c.execute(
            "SELECT COUNT(*) FROM notes WHERE user_id = ? AND channel_id = ? AND note = ?",
            (session_id, channelId, note),
        )
        existing_note_count = c.fetchone()[0]

        # Check if the highlighted note already exists in the database
        c.execute(
            "SELECT COUNT(*) FROM highlight_notes WHERE user_id = ? AND channel_id = ? AND highlighted_note = ?",
            (session_id, channelId, highlighted_note),
        )
        existing_highlighted_note_count = c.fetchone()[0]

        if not highlighted_note and not note:
            return apology("must provide note or highlighted note", 403)

        if existing_note_count == 0:
            if highlighted_note and note:
                if existing_highlighted_note_count == 0:
                    c.execute(
                        "INSERT INTO notes (user_id, channel_id, note) VALUES (?,?,?)",
                        (session_id, channelId, note),
                    )
                    conn.commit()
                    c.execute(
                        "INSERT INTO highlight_notes (user_id, channel_id, highlighted_note) VALUES (?,?,?)",
                        (session_id, channelId, highlighted_note),
                    )
                    conn.commit()
                else:
                    c.execute(
                        "UPDATE highlight_notes SET highlighted_note = ? WHERE user_id = ? AND channel_id = ?",
                        (highlighted_note, session_id, channelId),
                    )
                    conn.commit()
            elif note and not highlighted_note:
                c.execute(
                    "INSERT INTO notes (user_id, channel_id, note) VALUES (?,?,?)",
                    (session_id, channelId, note),
                )
                conn.commit()
            elif highlighted_note and not note:
                if existing_highlighted_note_count == 0:
                    c.execute(
                        "INSERT INTO highlight_notes (user_id, channel_id, highlighted_note) VALUES (?,?,?)",
                        (session_id, channelId, highlighted_note),
                    )
                    conn.commit()
                else:
                    c.execute(
                        "UPDATE highlight_notes SET highlighted_note = ? WHERE user_id = ? AND channel_id = ?",
                        (highlighted_note, session_id, channelId),
                    )
                    conn.commit()
        else:
            pass

        # Retrieve the most recent saved highlighted note for the specific channel ID
        c.execute(
            "SELECT highlighted_note, created_at, channel_id FROM highlight_notes WHERE user_id = ? AND channel_id = ?",
            (session_id, channelId),
        )
        highlighted_note = c.fetchone()

        c.execute(
            "SELECT note, created_at, channel_id FROM notes WHERE user_id =?",
            (session_id,),
        )
        notes = c.fetchall()

        # Retrieve data from the "creators" table
        c.execute(
            "SELECT * FROM creators WHERE user_id =? ORDER BY id DESC",
            (session_id,),
        )
        creators = c.fetchall()

        c.execute(
            "SELECT rate_value, likeability, humor, pity_subscription, informative, silly, funny, serious, deadpan, lets_be_friends, genuine, fake, relatable, emotional, inspirational, controversial, channel_id FROM ratings WHERE user_id =?",
            (session_id,),
        )
        ratings = c.fetchall()

        c.execute(
            "SELECT rate_value, likeability, humor, pity_subscription, informative, silly, funny, serious, deadpan, lets_be_friends, genuine, fake, relatable, emotional, inspirational, controversial, channel_id FROM ratings WHERE user_id =?",
            (session_id,),
        )
        columns = [column[0] for column in c.description]

        for i in range(len(columns)):
            columns[i] = columns[i].title()
            columns[i] = columns[i].replace("_", " ")

        aspects = [
            "Likeability",
            "Humor",
            "Pity Subscription",
            "Informative",
            "Silly",
            "Funny",
            "Serious",
            "Deadpan",
            "Let's Be Friends",
            "Genuine",
            "Fake",
            "Relatable",
            "Emotional",
            "Inspirational",
            "Controversial",
        ]

        print(highlighted_note)

        return render_template(
            "index.html",
            creators=creators,
            notes=notes,
            session_id=session_id,
            channelId=channelId,
            aspects=aspects,
            ratings=ratings,
            columns=columns,
            highlighted_note=highlighted_note,
            creator_video_dates=creator_video_dates,
        )


@app.route("/add_ratings", methods=["POST"])
def add_ratings():
    youtube = build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY
    )

    form_name = request.form.get("form_name")
    session_id = session.get("user_id")
    
    c.execute(
        "SELECT DISTINCT channel_id FROM creators WHERE user_id =?", (session_id,)
    )
    creator_ids = c.fetchall()
    
    creator_video_dates = []

    # Call YouTube API to get channel statistics
    for channel_id in creator_ids:
        request_query = youtube.channels().list(
            part="statistics,snippet,contentDetails", id=channel_id[0]
        )
        response = request_query.execute()

        # Extract necessary data from response
        published_at = response["items"][0]["snippet"]["publishedAt"]
        created_date = "-"
        formatted_date = "-"
        try:
            created_date = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%S%z")
            formatted_date = created_date.strftime("%m/%d/%Y")
        except ValueError:
            pass
        playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"][
            "uploads"
        ]
        videos_list_request = youtube.playlistItems().list(
            playlistId=playlist_id, part="snippet", maxResults=1
        )
        videos_list_response = videos_list_request.execute()
        last_video_date = videos_list_response["items"][0]["snippet"]["publishedAt"]
        formatted_last_video_date = "-"
        try:
            last_video_date_obj = datetime.strptime(
                last_video_date, "%Y-%m-%dT%H:%M:%S%z"
            )
            formatted_last_video_date = last_video_date_obj.strftime("%m/%d/%Y")
        except ValueError:
            pass

        creator_video_dates.append({
            "channel_id": channel_id[0],
            "created_date": formatted_date,
            "last_video_date": formatted_last_video_date
        })

    aspects = [
        "Likeability",
        "Humor",
        "Pity Subscription",
        "Informative",
        "Silly",
        "Funny",
        "Serious",
        "Deadpan",
        "Let's Be Friends",
        "Genuine",
        "Fake",
        "Relatable",
        "Emotional",
        "Inspirational",
        "Controversial",
    ]

    if form_name == "form4":
        channelId = request.form.get("channel_id")
        ratings = int(request.form.get("rating"))

        rates = {}
        for aspect in aspects:
            rate = request.form.get(aspect.lower())
            rates[aspect] = rate

        if not request.form.get("rating"):
            return apology("must choose rating 1-10", 403)

        c.execute(
            "SELECT COUNT(*) FROM ratings WHERE user_id =? AND channel_id =?",
            (session_id, channelId),
        )
        count = c.fetchone()[0]

        if count == 0:
            # Insert a new row with default values
            c.execute(
                "INSERT INTO ratings (user_id, channel_id, rate_value, likeability, humor, pity_subscription, informative, silly, funny, serious, deadpan, lets_be_friends, genuine, fake, relatable, emotional, inspirational, controversial) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    session_id,
                    channelId,
                    0,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                ),
            )

        c.execute(
            "UPDATE ratings SET rate_value =?, likeability = CASE WHEN likeability IS NULL OR likeability <>? THEN? ELSE likeability END, humor = CASE WHEN humor IS NULL OR humor <>? THEN? ELSE humor END, pity_subscription = CASE WHEN pity_subscription IS NULL OR pity_subscription <>? THEN? ELSE pity_subscription END, informative = CASE WHEN informative IS NULL OR informative <>? THEN? ELSE informative END, silly = CASE WHEN silly IS NULL OR silly <>? THEN? ELSE silly END, funny = CASE WHEN funny IS NULL OR funny <>? THEN? ELSE funny END, serious = CASE WHEN serious IS NULL OR serious <>? THEN? ELSE serious END, deadpan = CASE WHEN deadpan IS NULL OR deadpan <>? THEN? ELSE deadpan END, lets_be_friends = CASE WHEN lets_be_friends IS NULL OR lets_be_friends <>? THEN? ELSE lets_be_friends END, genuine = CASE WHEN genuine IS NULL OR genuine <>? THEN? ELSE genuine END, fake = CASE WHEN fake IS NULL OR fake <>? THEN? ELSE fake END, relatable = CASE WHEN relatable IS NULL OR relatable <>? THEN? ELSE relatable END, emotional = CASE WHEN emotional IS NULL OR emotional <>? THEN? ELSE emotional END, inspirational = CASE WHEN inspirational IS NULL OR inspirational <>? THEN? ELSE inspirational END, controversial = CASE WHEN controversial IS NULL OR controversial <>? THEN? ELSE controversial END WHERE user_id =? AND channel_id =?",
            (
                ratings,
                rates["Likeability"],
                rates["Likeability"] if rates["Likeability"] is not None else None,
                rates["Humor"],
                rates["Humor"] if rates["Humor"] is not None else None,
                rates["Pity Subscription"],
                rates["Pity Subscription"]
                if rates["Pity Subscription"] is not None
                else None,
                rates["Informative"],
                rates["Informative"] if rates["Informative"] is not None else None,
                rates["Silly"],
                rates["Silly"] if rates["Silly"] is not None else None,
                rates["Funny"],
                rates["Funny"] if rates["Funny"] is not None else None,
                rates["Serious"],
                rates["Serious"] if rates["Serious"] is not None else None,
                rates["Deadpan"],
                rates["Deadpan"] if rates["Deadpan"] is not None else None,
                rates["Let's Be Friends"],
                rates["Let's Be Friends"]
                if rates["Let's Be Friends"] is not None
                else None,
                rates["Genuine"],
                rates["Genuine"] if rates["Genuine"] is not None else None,
                rates["Fake"],
                rates["Fake"] if rates["Fake"] is not None else None,
                rates["Relatable"],
                rates["Relatable"] if rates["Relatable"] is not None else None,
                rates["Emotional"],
                rates["Emotional"] if rates["Emotional"] is not None else None,
                rates["Inspirational"],
                rates["Inspirational"] if rates["Inspirational"] is not None else None,
                rates["Controversial"],
                rates["Controversial"] if rates["Controversial"] is not None else None,
                session_id,
                channelId,
            ),
        )
        conn.commit()

        c.execute(
            "SELECT rate_value, likeability, humor, pity_subscription, informative, silly, funny, serious, deadpan, lets_be_friends, genuine, fake, relatable, emotional, inspirational, controversial, channel_id FROM ratings WHERE user_id =?",
            (session_id,),
        )
        ratings = c.fetchall()

        c.execute(
            "SELECT rate_value, likeability, humor, pity_subscription, informative, silly, funny, serious, deadpan, lets_be_friends, genuine, fake, relatable, emotional, inspirational, controversial, channel_id FROM ratings WHERE user_id =?",
            (session_id,),
        )
        columns = [column[0] for column in c.description]

        for i in range(len(columns)):
            columns[i] = columns[i].title()
            columns[i] = columns[i].replace("_", " ")

        # Print the column names
        print(columns)

        print("ratings after:", ratings[0][0])

        c.execute(
            "SELECT highlighted_note, created_at, channel_id FROM highlight_notes WHERE user_id = ? ORDER BY created_at DESC LIMIT 1",
            (session_id,),
        )
        highlighted_note = c.fetchone()

        c.execute(
            "SELECT note, created_at, channel_id FROM notes WHERE user_id =?",
            (session_id,),
        )
        notes = c.fetchall()

        # Retrieve data from the "creators" table
        c.execute(
            "SELECT * FROM creators WHERE user_id =? ORDER BY id DESC",
            (session_id,),
        )
        creators = c.fetchall()

        return render_template(
            "index.html",
            creators=creators,
            notes=notes,
            session_id=session_id,
            channelId=channelId,
            ratings=ratings,
            aspects=aspects,
            highlighted_note=highlighted_note,
            columns=columns,
            creator_video_dates=creator_video_dates,
        )


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    session_id = session.get("user_id")

    # Retrieve the username from the query parameter
    """ username = request.args.get("username") """

    youtube = build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY
    )

    aspects = [
        "Likeability",
        "Humor",
        "Pity Subscription",
        "Informative",
        "Silly",
        "Funny",
        "Serious",
        "Deadpan",
        "Let's Be Friends",
        "Genuine",
        "Fake",
        "Relatable",
        "Emotional",
        "Inspirational",
        "Controversial",
    ]

    c.execute(
        "SELECT DISTINCT channel_id FROM creators WHERE user_id =?", (session_id,)
    )
    creator_ids = c.fetchall()
    
    creator_video_dates = []

    # Call YouTube API to get channel statistics
    for channel_id in creator_ids:
        request_query = youtube.channels().list(
            part="statistics,snippet,contentDetails", id=channel_id[0]
        )
        response = request_query.execute()

        # Extract necessary data from response
        video_count = response["items"][0]["statistics"]["videoCount"]
        subscriber_count = response["items"][0]["statistics"]["subscriberCount"]
        channel_description = response["items"][0]["snippet"]["description"]
        channel_name = response["items"][0]["snippet"]["title"]
        channel_thumbnail = response["items"][0]["snippet"]["thumbnails"]["default"][
            "url"
        ]
        published_at = response["items"][0]["snippet"]["publishedAt"]
        created_date = "-"
        formatted_date = "-"
        try:
            created_date = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%S%z")
            formatted_date = created_date.strftime("%m/%d/%Y")
        except ValueError:
            pass
        playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"][
            "uploads"
        ]
        videos_list_request = youtube.playlistItems().list(
            playlistId=playlist_id, part="snippet", maxResults=1
        )
        videos_list_response = videos_list_request.execute()
        last_video_date = videos_list_response["items"][0]["snippet"]["publishedAt"]
        formatted_last_video_date = "-"
        try:
            last_video_date_obj = datetime.strptime(
                last_video_date, "%Y-%m-%dT%H:%M:%S%z"
            )
            formatted_last_video_date = last_video_date_obj.strftime("%m/%d/%Y")
        except ValueError:
            pass

        creator_video_dates.append({
            "channel_id": channel_id[0],
            "created_date": formatted_date,
            "last_video_date": formatted_last_video_date
        })

        c.execute(
            "UPDATE creators SET videoCount =?, subscriberCount =?, description =?, username =?, thumbnail =? WHERE channel_id =?",
            (
                video_count,
                subscriber_count,
                channel_description,
                channel_name,
                channel_thumbnail,
                channel_id[0],
            ),
        )
        conn.commit()

    # Retrieve data from the "creators" table
    c.execute("SELECT * FROM creators WHERE user_id =? ORDER BY id DESC", (session_id,))
    creators = c.fetchall()

    c.execute(
        "SELECT note, created_at, channel_id FROM notes WHERE user_id =?", (session_id,)
    )
    notes = c.fetchall()

    c.execute(
        "SELECT highlighted_note, created_at, channel_id FROM highlight_notes WHERE user_id = ? ORDER BY created_at DESC LIMIT 1",
        (session_id,),
    )
    highlighted_note = c.fetchone()

    c.execute(
        "SELECT rate_value, likeability, humor, pity_subscription, informative, silly, funny, serious, deadpan, lets_be_friends, genuine, fake, relatable, emotional, inspirational, controversial, channel_id FROM ratings WHERE user_id =?",
        (session_id,),
    )
    ratings = c.fetchall()

    c.execute(
        "SELECT rate_value, likeability, humor, pity_subscription, informative, silly, funny, serious, deadpan, lets_be_friends, genuine, fake, relatable, emotional, inspirational, controversial, channel_id FROM ratings WHERE user_id =?",
        (session_id,),
    )
    columns = [column[0] for column in c.description]

    for i in range(len(columns)):
        columns[i] = columns[i].title()
        columns[i] = columns[i].replace("_", " ")

    if request.method == "GET":
        return render_template(
            "index.html",
            session_id=session_id,
            creators=creators,
            ratings=ratings,
            aspects=aspects,
            columns=columns,
            notes=notes,
            highlighted_note=highlighted_note,
            creator_video_dates=creator_video_dates,
        )


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide email address", 403)

        # Ensure email is valid
        elif not validate_email(request.form.get("username")):
            return apology("invalid email", 403)

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
        password = request.form.get("password")

        # Query database for username
        rows = c.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchall()

        # Ensure username does not already exist
        if len(rows) == 1:
            return apology("username already exists", 403)

        # Hash password
        password_hash = generate_password_hash(password)

        # Generate password hash using bcrypt
        password_bcrypt = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # Save both password hashes in the users table
        c.execute(
            "INSERT INTO users (username, hash, password_bcrypt) VALUES (?, ?, ?)",
            (username, password_hash, password_bcrypt),
        )

        conn.commit()

        # Flash message
        flash("Registration successful. Please login.")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/save-song", methods=["POST"])
def save_song():
    session_id = session.get("user_id")
    data = request.get_json()
    title = data["title"]
    videoId = data["videoId"]

    c.execute(
        "SELECT * FROM watched WHERE video_id=? AND user_id=?",
        (videoId, session_id),
    )
    check = c.fetchone()
    if check is not None:
        # If the video id already exists do nothing
        pass
    else:
        # If the video id doesn't exist, add it to the 'watched' variable and return the updated 'watched' variable in the response
        c.execute(
            "INSERT INTO watched (title, video_id, user_id) VALUES (?,?,?)",
            (
                title,
                videoId,
                session_id,
            ),
        )
        conn.commit()

    print(title)
    print(videoId)

    c.execute(
        "SELECT * FROM watched WHERE video_id=? AND user_id=?",
        (videoId, session_id),
    )
    watched = c.fetchall()
    # Save the song with the title and video ID to the database
    return jsonify({"message": "Song saved successfully!", "watched": watched})


@app.route("/remove-song", methods=["POST"])
def remove_song():
    session_id = session.get("user_id")
    data = request.get_json()
    """ title = data["title"] """
    videoId = data["videoId"]

    c.execute(
        "DELETE FROM watched WHERE video_id =? AND user_id=?",
        (videoId, session_id),
    )
    conn.commit()

    c.execute(
        "SELECT * FROM watched WHERE video_id=? AND user_id=?",
        (videoId, session_id),
    )
    watched = c.fetchall()

    # Remove the song with the title and video ID from the database
    return jsonify({"message": "Song removed successfully!", "watched": watched})


@app.route("/watched", methods=["GET", "POST"])
def watched():
    session_id = session.get("user_id")

    c.execute(
        "SELECT video_id FROM watched WHERE user_id=?",
        (session_id,),
    )
    watched_songs = c.fetchall()

    c.execute(
        "SELECT * FROM watched WHERE user_id=?",
        (session_id,),
    )
    watched = c.fetchall()

    print(watched)

    response = {
        "status": "success",
        "watched": watched,
        "watched_songs": watched_songs,
    }
    return jsonify(response)


@app.route("/pentatonix", methods=["GET", "POST"])
@login_required
def pentatonix():
    session_id = session.get("user_id")
    youtube = build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY
    )

    # Set channel id
    channel_id = "UCmv1CLT6ZcFdTJMHxaR9XeA"
    must_watch = "PLWxNS1ipfyc8yXp2iu64HaUWByl0CmEEi"
    originals = "PLWxNS1ipfyc9isDBuA8RBIzU2R2mn8R7t"
    christmas = "PLWxNS1ipfyc_vJJt4CujWhG88dzFzBdIf"
    sing_off = "PLWxNS1ipfyc9My5y_XSANuS2ynybceM8A"
    live = "PLWxNS1ipfyc-JOjPUYomaKigWus1GCXUB"

    c.execute(
        "SELECT * FROM watched WHERE user_id=?",
        (session_id,),
    )
    watched = c.fetchall()

    request_q = youtube.channels().list(
        part="statistics,snippet,contentDetails", id=channel_id
    )

    response = request_q.execute()

    # Extract necessary data from response
    video_count = response["items"][0]["statistics"]["videoCount"]
    """ view_count = response["items"][0]["statistics"]["viewCount"] """
    subscriber_count = response["items"][0]["statistics"]["subscriberCount"]
    published_at = response["items"][0]["snippet"]["publishedAt"]
    created_date = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%S%z")
    formatted_date = created_date.strftime("%m/%d/%Y")
    playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    videos_list_request = youtube.playlistItems().list(
        playlistId=playlist_id, part="snippet", maxResults=1
    )
    videos_list_response = videos_list_request.execute()

    last_video_date = videos_list_response["items"][0]["snippet"]["publishedAt"]
    last_video_date_obj = datetime.strptime(last_video_date, "%Y-%m-%dT%H:%M:%S%z")
    formatted_last_video_date = last_video_date_obj.strftime("%m/%d/%Y")

    playlist_items_request = youtube.playlistItems().list(
        part="snippet", playlistId=must_watch, maxResults=50
    )
    playlist_items_response = playlist_items_request.execute()

    # process the videos in the response and create a list of video titles and IDs
    videos = []

    while playlist_items_response:
        for item in playlist_items_response["items"]:
            videos.append(
                {
                    "title": item["snippet"]["title"],
                    "videoId": item["snippet"]["resourceId"]["videoId"],
                }
            )

        nextPageToken = playlist_items_response.get("nextPageToken")

        if nextPageToken:
            playlist_items_response = (
                youtube.playlistItems()
                .list(
                    part="snippet",
                    playlistId=must_watch,
                    maxResults=50,
                    pageToken=nextPageToken,
                )
                .execute()
            )
        else:
            playlist_items_response = None

    for video in videos:
        title = video["title"]
        video_id = video["videoId"]
        c.execute(
            "SELECT * FROM tunes WHERE title =? AND video_id =?", (title, video_id)
        )
        result = c.fetchone()
        if result is None:
            c.execute(
                "INSERT INTO tunes (title, video_id) VALUES (?,?)", (title, video_id)
            )
            conn.commit()

    playlist_items_request = youtube.playlistItems().list(
        part="snippet", playlistId=originals, maxResults=50
    )
    playlist_items_response = playlist_items_request.execute()

    # process the videos in the response and create a list of video titles and IDs
    original = []

    for item in playlist_items_response["items"]:
        original.append(
            {
                "title": item["snippet"]["title"],
                "videoId": item["snippet"]["resourceId"]["videoId"],
            }
        )

    for origin in original:
        title = origin["title"]
        video_id = origin["videoId"]
        c.execute(
            "SELECT * FROM tunes WHERE title =? AND video_id =?", (title, video_id)
        )
        result = c.fetchone()
        if result is None:
            c.execute(
                "INSERT INTO tunes (title, video_id) VALUES (?,?)", (title, video_id)
            )
            conn.commit()

    playlist_items_request = youtube.playlistItems().list(
        part="snippet", playlistId=christmas, maxResults=50
    )
    playlist_items_response = playlist_items_request.execute()

    # process the videos in the response and create a list of video titles and IDs
    xmas = []

    for item in playlist_items_response["items"]:
        xmas.append(
            {
                "title": item["snippet"]["title"],
                "videoId": item["snippet"]["resourceId"]["videoId"],
            }
        )

    for x in xmas:
        title = x["title"]
        video_id = x["videoId"]
        c.execute(
            "SELECT * FROM tunes WHERE title =? AND video_id =?", (title, video_id)
        )
        result = c.fetchone()
        if result is None:
            c.execute(
                "INSERT INTO tunes (title, video_id) VALUES (?,?)", (title, video_id)
            )
            conn.commit()

    playlist_items_request = youtube.playlistItems().list(
        part="snippet", playlistId=sing_off, maxResults=50
    )
    playlist_items_response = playlist_items_request.execute()

    # process the videos in the response and create a list of video titles and IDs
    sing = []

    for item in playlist_items_response["items"]:
        sing.append(
            {
                "title": item["snippet"]["title"],
                "videoId": item["snippet"]["resourceId"]["videoId"],
            }
        )

    for s in sing:
        title = s["title"]
        video_id = s["videoId"]
        c.execute(
            "SELECT * FROM tunes WHERE title =? AND video_id =?", (title, video_id)
        )
        result = c.fetchone()
        if result is None:
            c.execute(
                "INSERT INTO tunes (title, video_id) VALUES (?,?)", (title, video_id)
            )
            conn.commit()

    playlist_items_request = youtube.playlistItems().list(
        part="snippet", playlistId=live, maxResults=50
    )
    playlist_items_response = playlist_items_request.execute()

    # process the videos in the response and create a list of video titles and IDs
    live_performance = []

    for item in playlist_items_response["items"]:
        live_performance.append(
            {
                "title": item["snippet"]["title"],
                "videoId": item["snippet"]["resourceId"]["videoId"],
            }
        )

    for live in live_performance:
        title = live["title"]
        video_id = live["videoId"]
        c.execute(
            "SELECT * FROM tunes WHERE title =? AND video_id =?", (title, video_id)
        )
        result = c.fetchone()
        if result is None:
            c.execute(
                "INSERT INTO tunes (title, video_id) VALUES (?,?)", (title, video_id)
            )
            conn.commit()

    channel_request = youtube.channels().list(
        part="snippet", id=channel_id, fields="items(snippet(thumbnails(medium)))"
    )
    channel_response = channel_request.execute()

    profile_picture_url = channel_response["items"][0]["snippet"]["thumbnails"][
        "medium"
    ]["url"]

    # Pass all the necessary data to the Jinja template
    return render_template(
        "pentatonix.html",
        video_count=video_count,
        subscriber_count=subscriber_count,
        created_date=created_date,
        last_video_date=last_video_date_obj,
        videos=videos,
        original=original,
        xmas=xmas,
        sing=sing,
        live_performance=live_performance,
        profile_picture_url=profile_picture_url,
        session_id=session_id,
        formatted_last_video_date=formatted_last_video_date,
        formatted_date=formatted_date,
        watched=watched,
    )


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


conn.close

if __name__ == "__main__":
    app.run(debug=True)
