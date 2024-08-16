import os
import json
import jinja2
import jinja_markdown
from flask import Flask, request, redirect, current_app, session, make_response, render_template, abort, send_from_directory, flash, url_for
from flask.helpers import send_from_directory
from datetime import datetime, timedelta
from waitress import serve
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, LoginManager, login_user, logout_user
from dotenv import load_dotenv
import secrets
import requests
from urllib.parse import urlencode
from model import db, User, Score
from oauth import OAUTH2_PROVIDERS

load_dotenv()

# Default puzzle directory may be overridden with env. variable
puzzle_path = os.environ.get('PUZZLE_PATH') or "coding_challenge"
db_uri = os.environ.get('DATABASE_URL') or 'sqlite:///scores.sqlite'

# puzzle_path + templates directory are both scanned for jinja content
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db.init_app(app)

# url_for() should generate links with https protocol: https://stackoverflow.com/a/26636880/3306
# Otherwise oauth provider will report callback url mismatch
# Note that app.config['PREFERRED_URL_SCHEME'] does not do what you expect: https://stackoverflow.com/a/43288737/3306
PREFERRED_URL_SCHEME = os.environ.get('PREFERRED_URL_SCHEME') or 'http'

# Temporarily disabled - there is a caching bug in the footnotes extension
# jinja_markdown.EXTENSIONS.append('pymdownx.extra') # To enable footnotes

app.jinja_env.add_extension(jinja_markdown.MarkdownExtension)
my_loader = jinja2.ChoiceLoader([
        app.jinja_loader, jinja2.FileSystemLoader([puzzle_path]),
    ])
app.jinja_loader = my_loader

# config.json found in root of puzzle path.
config_file = os.path.join(puzzle_path, "config.json")
with open(config_file, encoding="utf-8") as infile:
    puzzle_data = json.load(infile)

answers_file = os.path.join(puzzle_path, "answers.json")
with open(answers_file, encoding="utf-8") as infile:
    answers = json.load(infile)

app.secret_key = os.environ.get('FLASK_SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    user = db.session.get(User, int(id))
    return user

with app.app_context():
    db.create_all()

@app.context_processor
def inject_title():
    return dict(title=puzzle_data["title"])

def get_puzzle_description(puzzle_number):
    return puzzle_data['descriptions_filepattern'] % int(puzzle_number)

def get_puzzle_input(puzzle_number):
    return puzzle_data['inputs_filepattern'] % int(puzzle_number)

# Extract list of puzzles based on configured answers. They don't even have to be consecutive...
def get_puzzle_range():
    result = [int(x) for x in answers.keys()]
    result.sort()
    return result

@app.route("/")
def home():
    return render_template("index.html", puzzles=get_puzzle_range())

@app.route('/myscore')
def myscore():
    userId = current_user.id
    myscore = db.session.query(Score).filter(Score.user_id == userId)
    return render_template("myscore.html", myscore=myscore)

@app.route("/puzzle/<number>")
def puzzle(number):
    return render_template("puzzle.html", puzzle_number=number, puzzle_description=get_puzzle_description(number))

@app.route("/puzzleinput/<number>")
def puzzle_input(number):
    return send_from_directory(puzzle_path, get_puzzle_input(number), mimetype="text/plain")

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route("/submitanswer/<number>", methods = ['POST'])
def submit_answer(number):
    if current_user.is_anonymous:
        abort(401)
    
    userId = current_user.id
    name = current_user.username
    answered = request.form['answer_input']

    if (answered in answers.get(number)):
        score = Score(userId, name, number)
        db.session.add(score)
        db.session.commit()
        template = "answercorrect.html"
    else:
        template = "answerincorrect.html"

    return make_response(render_template(template, puzzle_number=number, username=name))

def transform_leaderboard(results):
    matrix = {}
    leaderboard = {}
    for r in results:
        if r.user_id not in matrix:
            matrix[r.user_id] = {}
        matrix[r.user_id][r.puzzle_id] = True

    usernames = {}
    for r in results:
        if r.user_id not in usernames:
            usernames[r.user_id] = r.username
    
    for user_id, solved in matrix.items():
        stars = ""
        count = 0
        for puzzle_id in get_puzzle_range():
            if puzzle_id in solved:
                stars += "<span class=\"solved\">*</span>"
                count += 1
            else:
                stars += "<span class=\"unsolved\">*</span>"
        leaderboard[user_id] = {"username": usernames[user_id], "solvedcount": count, "stars": stars }
    return leaderboard

@app.route("/scoreboard")
def score_board_recent():
    six_months_ago = datetime.now() - timedelta(weeks=26)
    results = (db.session.query(Score.puzzle_id, Score.user_id, User.username)
               .join(User, Score.user_id == User.id)
               .order_by(User.username, Score.puzzle_id)
               .filter(Score.timestamp > six_months_ago)
               .all())
    leaderboard = transform_leaderboard(results)
    return render_template("scoreboard.html", hideusername=True, autorefresh=True, leaderboard=leaderboard.items())

@app.route("/scoreboard/all")
def score_board_all():
    results = (db.session.query(Score.puzzle_id, Score.user_id, User.username)
               .join(User, Score.user_id == User.id)
               .order_by(User.username, Score.puzzle_id)
               .all())
    leaderboard = transform_leaderboard(results)
    return render_template("scoreboard.html", hideusername=True, autorefresh=True, leaderboard=leaderboard.items())

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/authorize/<provider>')
def oauth2_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    provider_data = OAUTH2_PROVIDERS.get(provider)
    if provider_data is None:
        abort(404)

    # generate a random string for the state parameter
    session['oauth2_state'] = secrets.token_urlsafe(16)

    # create a query string with all the OAuth2 parameters
    qs = urlencode({
        'client_id': provider_data['client_id'],
        'redirect_uri': url_for('oauth2_callback', provider=provider,
                                _scheme=PREFERRED_URL_SCHEME,
                                _external=True),
        'response_type': 'code',
        'scope': ' '.join(provider_data['scopes']),
        'state': session['oauth2_state'],
    })

    # redirect the user to the OAuth2 provider authorization URL
    return redirect(provider_data['authorize_url'] + '?' + qs)

@app.route('/callback/<provider>')
def oauth2_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    provider_data = OAUTH2_PROVIDERS.get(provider)
    if provider_data is None:
        abort(404)

    # if there was an authentication error, flash the error messages and exit
    if 'error' in request.args:
        for k, v in request.args.items():
            if k.startswith('error'):
                flash(f'{k}: {v}')
        return redirect(url_for('index'))

    # make sure that the state parameter matches the one we created in the
    # authorization request
    if request.args['state'] != session.get('oauth2_state'):
        abort(401)

    # make sure that the authorization code is present
    if 'code' not in request.args:
        abort(401)

    # exchange the authorization code for an access token
    response = requests.post(provider_data['token_url'], data={
        'client_id': provider_data['client_id'],
        'client_secret': provider_data['client_secret'],
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': url_for('oauth2_callback', provider=provider,
                                _scheme=PREFERRED_URL_SCHEME,
                                _external=True),
    }, headers={'Accept': 'application/json'})
    if response.status_code != 200:
        abort(401)
    oauth2_token = response.json().get('access_token')
    if not oauth2_token:
        abort(401)

    # use the access token to get the user's email address
    response = requests.get(provider_data['userinfo']['url'], headers={
        'Authorization': 'Bearer ' + oauth2_token,
        'Accept': 'application/json',
    })
    if response.status_code != 200:
        abort(401)

    name = provider_data['userinfo']['displayName'](response.json())
    external_id = provider + ':' + provider_data['userinfo']['id'](response.json())

    # find or create the user in the database
    user = db.session.scalar(db.select(User).where(User.external_id == external_id))
    if user is None:
        user = User(external_id = external_id, username=name)
        db.session.add(user)
        db.session.commit()

    # log the user in
    login_user(user)
    return redirect(url_for('index'))

# This ensures that we reload after login
@app.after_request
def add_header(response):
    response.vary = "Cookie"
    return response

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
