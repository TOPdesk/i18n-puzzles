import os, os.path
from flask import Flask, request, make_response, render_template, abort, send_from_directory
from flask.helpers import send_from_directory
import jinja_markdown
from datetime import datetime, timedelta
from sqlalchemy.sql.expression import select
from waitress import serve
import json
import jinja2
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user, LoginManager
from dotenv import load_dotenv

load_dotenv()

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

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    user = db.session.get(User, int(id))
    return user

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func

class Score(db.Model):
    id = Column('id', Integer, primary_key = True)
    player_name = Column(String(100)) # Deprecated - will be removed
    user_id = Column('user_id', Integer, ForeignKey('users.id'), nullable = False)
    puzzle_id = Column(Integer)
    timestamp = Column(DateTime, default=func.now())

    def __init__(self, user_id, player_name, puzzle_id):
        self.user_id = user_id
        self.player_name = player_name # TODO: deprecated
        self.puzzle_id = puzzle_id

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(64), nullable=False, unique=True)
    username = db.Column(db.String(64), nullable=False)
    # email = db.Column(db.String(64), nullable=True)

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

# we do not import anything (would be circular) - just make sure module is loaded https://flask.palletsprojects.com/en/1.1.x/patterns/packages/
import auth