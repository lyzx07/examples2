import os


from flask import Flask, flash, redirect, render_template, request, session, jsonify, url_for
import sqlite3
from datetime import datetime
import random
import requests
import json
import google.auth
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from validate_email import validate_email
from flask import flash
from googleapiclient.discovery import build
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
conn = sqlite3.connect('rate-app-real.db', check_same_thread=False)
c = conn.cursor()

""" c.execute('''CREATE TABLE IF NOT EXISTS tunes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    video_id TEXT NOT NULL);''')

conn.commit() """


DEVELOPER_KEY = "AIzaSyDHKne5gUlTY73VT5OlfmhsZBYJqDFgA_Q" # replace with your actual developer key
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def get_videos_from_playlists(youtube, playlist_ids):
    videos = {}
    for playlist_id in playlist_ids:
        video_list = []
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50
        )
        response = request.execute()
        for item in response['items']:
            video = {}
            video['title'] = item['snippet']['title']
            video['videoId'] = item['snippet']['resourceId']['videoId']
            video_list.append(video)
        videos[playlist_id] = video_list
    return videos


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

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    session_id = session.get("user_id")
    rows = c.execute('SELECT * FROM users WHERE id = ?', (session_id,)).fetchall()
    
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    
    if request.method == 'POST':
        # Get the username from the form data
        username = request.form['username']
        
        search_response = youtube.search().list(
            q=username,
            type='channel',
            part='id'
        ).execute()
        
        # Get channel id from search response
        channel_id = search_response['items'][0]['id']['channelId']
        
        # Call YouTube API to get channel statistics
        request_query = youtube.channels().list(
            part='statistics,snippet,contentDetails',
            id=channel_id
        )
        response = request_query.execute()
        
        # Extract necessary data from response
        video_count = response['items'][0]['statistics']['videoCount']
        subscriber_count = response['items'][0]['statistics']['subscriberCount']
        published_at = response['items'][0]['snippet']['publishedAt']
        formatted_date = '-'
        try:
            created_date = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%S%z")
            formatted_date = created_date.strftime('%m/%d/%Y')
        except ValueError:
            pass
        playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        videos_list_request = youtube.playlistItems().list(
            playlistId=playlist_id,
            part='snippet',
            maxResults=1
        )
        videos_list_response = videos_list_request.execute()
        last_video_date = videos_list_response['items'][0]['snippet']['publishedAt']
        created_date = '-'
        formatted_last_video_date = '-'
        try:
            last_video_date_obj = datetime.strptime(last_video_date, "%Y-%m-%dT%H:%M:%S%z")
            formatted_last_video_date = last_video_date_obj.strftime('%m/%d/%Y')
        except ValueError:
            pass
        
        # Pass all the necessary data to the Jinja template
        return render_template('index.html', 
                               video_count=video_count, 
                               subscriber_count=subscriber_count, 
                               created_date=created_date,
                               last_video_date=last_video_date_obj, 
                               formatted_date=formatted_date,
                               formatted_last_video_date=formatted_last_video_date)
        
    # Pass video count to the Jinja template
    return render_template("index.html", rows=rows, session_id=session_id)

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

        # Query database for username
        rows = c.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchall()

        # Ensure username does not already exist
        if len(rows) == 1:
            return apology("username already exists", 403)

        # Hash password
        hash = generate_password_hash(request.form.get("password"))

        # Insert into users table
        c.execute('INSERT INTO users (username, hash) VALUES (?, ?)', (username, hash))
        
        conn.commit()
        
        # Flash message
        flash('Registration successful. Please login.')
        
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
    
@app.route("/pentatonix", methods=["GET", "POST"])
@login_required
def pentatonix():
    session_id = session.get("user_id")
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    
    # Set channel id 
    channel_id = "UCmv1CLT6ZcFdTJMHxaR9XeA"
    must_watch = "PLWxNS1ipfyc8yXp2iu64HaUWByl0CmEEi"
    originals = "PLWxNS1ipfyc9isDBuA8RBIzU2R2mn8R7t"
    christmas = "PLWxNS1ipfyc_vJJt4CujWhG88dzFzBdIf"
    sing_off = "PLWxNS1ipfyc9My5y_XSANuS2ynybceM8A"
    live = "PLWxNS1ipfyc-JOjPUYomaKigWus1GCXUB"

    request_q = youtube.channels().list(
            part="statistics,snippet,contentDetails",
            id=channel_id
        )

    response = request_q.execute()
    

    # Extract necessary data from response
    video_count = response['items'][0]['statistics']['videoCount']
    subscriber_count = response['items'][0]['statistics']['subscriberCount']
    published_at = response['items'][0]['snippet']['publishedAt']
    created_date = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%S%z")
    formatted_date = created_date.strftime('%m/%d/%Y')
    playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    videos_list_request = youtube.playlistItems().list(
                           playlistId=playlist_id,
                           part="snippet",
                           maxResults=1)
    videos_list_response = videos_list_request.execute()
    last_video_date = videos_list_response['items'][0]['snippet']['publishedAt']
    last_video_date_obj = datetime.strptime(last_video_date, "%Y-%m-%dT%H:%M:%S%z")
    formatted_last_video_date = last_video_date_obj.strftime('%m/%d/%Y')
    
    playlist_items_request = youtube.playlistItems().list(
        part="snippet",
        playlistId=must_watch,
        maxResults=50
    )
    playlist_items_response = playlist_items_request.execute()

    # process the videos in the response and create a list of video titles and IDs
    videos = []

    while playlist_items_response:
        for item in playlist_items_response['items']:
            videos.append({
                "title": item['snippet']['title'],
                "videoId": item['snippet']['resourceId']['videoId']
            })

        nextPageToken = playlist_items_response.get('nextPageToken')

        if nextPageToken:
            playlist_items_response = youtube.playlistItems().list(
                part="snippet",
                playlistId=must_watch,
                maxResults=50,
                pageToken=nextPageToken
            ).execute()
        else:
            playlist_items_response = None
            
    for video in videos:
        title = video['title']
        video_id = video['videoId']
        c.execute('SELECT * FROM tunes WHERE title =? AND video_id =?', (title, video_id))
        result = c.fetchone()
        if result is None:
            c.execute('INSERT INTO tunes (title, video_id) VALUES (?,?)', (title, video_id))
            conn.commit()
            
    playlist_items_request = youtube.playlistItems().list(
        part="snippet",
        playlistId=originals,
        maxResults=50
    )
    playlist_items_response = playlist_items_request.execute()

    # process the videos in the response and create a list of video titles and IDs
    original = []

    for item in playlist_items_response['items']:
        original.append({
            "title": item['snippet']['title'],
            "videoId": item['snippet']['resourceId']['videoId']
        })  
        
    for origin in original:
        title = origin['title']
        video_id = origin['videoId']
        c.execute('SELECT * FROM tunes WHERE title =? AND video_id =?', (title, video_id))
        result = c.fetchone()
        if result is None:
            c.execute('INSERT INTO tunes (title, video_id) VALUES (?,?)', (title, video_id))
            conn.commit()
        
    playlist_items_request = youtube.playlistItems().list(
        part="snippet",
        playlistId=christmas,
        maxResults=50
    )
    playlist_items_response = playlist_items_request.execute()

    # process the videos in the response and create a list of video titles and IDs
    xmas = []

    for item in playlist_items_response['items']:
        xmas.append({
            "title": item['snippet']['title'],
            "videoId": item['snippet']['resourceId']['videoId']
        })  
        
    for x in xmas:
        title = x['title']
        video_id = x['videoId']
        c.execute('SELECT * FROM tunes WHERE title =? AND video_id =?', (title, video_id))
        result = c.fetchone()
        if result is None:
            c.execute('INSERT INTO tunes (title, video_id) VALUES (?,?)', (title, video_id))
            conn.commit()
            
    playlist_items_request = youtube.playlistItems().list(
        part="snippet",
        playlistId=sing_off,
        maxResults=50
    )
    playlist_items_response = playlist_items_request.execute()

    # process the videos in the response and create a list of video titles and IDs
    sing = []

    for item in playlist_items_response['items']:
        sing.append({
            "title": item['snippet']['title'],
            "videoId": item['snippet']['resourceId']['videoId']
        }) 
        
    for s in sing:
        title = s['title']
        video_id = s['videoId']
        c.execute('SELECT * FROM tunes WHERE title =? AND video_id =?', (title, video_id))
        result = c.fetchone()
        if result is None:
            c.execute('INSERT INTO tunes (title, video_id) VALUES (?,?)', (title, video_id))
            conn.commit() 
        
    playlist_items_request = youtube.playlistItems().list(
        part="snippet",
        playlistId=live,
        maxResults=50
    )
    playlist_items_response = playlist_items_request.execute()

    # process the videos in the response and create a list of video titles and IDs
    live_performance = []

    for item in playlist_items_response['items']:
        live_performance.append({
            "title": item['snippet']['title'],
            "videoId": item['snippet']['resourceId']['videoId']
        })
        
    for live in live_performance:
        title = live['title']
        video_id = live['videoId']
        c.execute('SELECT * FROM tunes WHERE title =? AND video_id =?', (title, video_id))
        result = c.fetchone()
        if result is None:
            c.execute('INSERT INTO tunes (title, video_id) VALUES (?,?)', (title, video_id))
            conn.commit()   
        
    channel_request = youtube.channels().list(
        part="snippet",
        id=channel_id,
        fields="items(snippet(thumbnails(medium)))"
    )
    channel_response = channel_request.execute()

    profile_picture_url = channel_response['items'][0]['snippet']['thumbnails']['medium']['url']
    
                        

    # Pass all the necessary data to the Jinja template
    return render_template("pentatonix.html", 
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
                            formatted_date=formatted_date)

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

conn.close

if __name__ == '__main__':
    app.run(debug=True)