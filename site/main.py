import os, os.path
from flask import Flask, request, make_response, render_template
from flask.helpers import send_from_directory
import jinja_markdown
from datetime import datetime, timedelta
from sqlalchemy.sql.expression import select
from waitress import serve
import json
import jinja2
from flask_sqlalchemy import SQLAlchemy
from flask import send_from_directory
from flask_login import UserMixin

# Default puzzle directory may be overridden with env. variable
puzzle_path = os.environ.get('PUZZLE_PATH') or "coding_challenge"
db_uri = os.environ.get('DATABASE_URL') or 'sqlite:///scores.sqlite'

# puzzle_path + templates directory are both scanned for jinja content
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

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

db = SQLAlchemy(app)

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func

class Score(db.Model):
    id = Column('id', Integer, primary_key = True)
    player_name = Column(String(100)) # Deprecated - will be removed
    user_id = Column('user_id', Integer, ForeignKey('user.id'), nullable = False)
    puzzle_id = Column(Integer)
    timestamp = Column(DateTime, default=func.now())

    def __init__(self, player_name, puzzle_id):
        self.player_name = player_name
        self.puzzle_id = puzzle_id

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(64), nullable=False, unique=True)
    username = db.Column(db.String(64), nullable=False)
    # email = db.Column(db.String(64), nullable=True)

with app.app_context():
    db.create_all()

accept_new_answers = True

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
    name = request.cookies.get('userID')
    return render_template("index.html", username=name, puzzles=get_puzzle_range())

@app.route('/login')
def index():
    return render_template('login.html', hideusername=True)

@app.route('/setuser', methods = ['POST'])
def setuser():
    name = request.form['nm']
    if len(name) < 3 or len(name) > 20 or not name.isalnum():
        return make_response(render_template('logindenied.html', hideusername=True))
    else:
        resp = make_response(render_template('loginconfirm.html', hideusername=True))
        resp.set_cookie('userID', name, secure=True)
        return resp

@app.route('/getuser')
def getuser():
    # TODO -> userId is no longer equal to username
    name = request.cookies.get('userID')
    return '<p>username: ' + name + '</p>'

@app.route('/startacceptinganswers')
def start():
    global accept_new_answers
    accept_new_answers = True
    return render_template("confirm.html", hideusername=True)

@app.route('/stopacceptinganswers')
def stop():
    global accept_new_answers
    accept_new_answers = False
    return render_template("confirm.html", hideusername=True)

@app.route('/myscore')
def myscore():
    # TODO -> player_name no longer exsists
    name = request.cookies.get('userID')
    myscore = db.session.query(Score).filter(Score.player_name == name)
    return render_template("myscore.html", username=name, myscore=myscore)

@app.route("/puzzle/<number>")
def puzzle(number):
    # TODO -> userId is no longer equal to username
    name = request.cookies.get('userID')
    return render_template("puzzle.html", username=name, puzzle_number=number, puzzle_description=get_puzzle_description(number))

@app.route("/puzzleinput/<number>")
def puzzle_input(number):
    return send_from_directory(puzzle_path, get_puzzle_input(number), mimetype="text/plain")

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route("/submitanswer/<number>", methods = ['POST'])
def submit_answer(number):
    if (not accept_new_answers):
        return render_template("stop.html")

    name = request.cookies.get('userID')
    answered = request.form['answer_input']

    if (answered in answers.get(number)):
        score = Score(name, number)
        db.session.add(score)
        db.session.commit()
        template = "answercorrect.html"
    else:
        template = "answerincorrect.html"

    return make_response(render_template(template, puzzle_number=number, username=name))

def transform_leaderboard(results):
    # TODO -> player_name no longer exists
    matrix = {}
    leaderboard = {}
    for r in results:
        if r.player_name not in matrix:
            matrix[r.player_name] = {}
        matrix[r.player_name][r.puzzle_id] = True
    
    for player_name, solved in matrix.items():
        stars = ""
        count = 0
        for puzzle_id in get_puzzle_range():
            if puzzle_id in solved:
                stars += "<span class=\"solved\">*</span>"
                count += 1
            else:
                stars += "<span class=\"unsolved\">*</span>"
        leaderboard[player_name] = {"solvedcount": count, "stars": stars }
    return leaderboard

@app.route("/scoreboard")
def score_board_recent():
    # TODO -> player_name no longer exists
    six_months_ago = datetime.now() - timedelta(weeks=26)
    results = db.session.query(Score).order_by(Score.player_name, Score.puzzle_id).filter(Score.timestamp > six_months_ago).all()
    leaderboard = transform_leaderboard(results)
    return render_template("scoreboard.html", hideusername=True, autorefresh=True, leaderboard=leaderboard.items())

@app.route("/scoreboard/all")
def score_board_all():
    # TODO -> player_name no longer exists
    results = db.session.query(Score).order_by(Score.player_name, Score.puzzle_id).all()
    leaderboard = transform_leaderboard(results)
    return render_template("scoreboard.html", hideusername=True, autorefresh=True, leaderboard=leaderboard.items())

# def sort_count_date(tup):
#     key, d = tup
#     return -d["solvedcount"], d["date"]

# This ensures that we reload after login
@app.after_request
def add_header(response):
    response.vary = "Cookie"
    return response

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)
    