import os, os.path
from flask import Flask, request, make_response, render_template
from jinja_markdown import MarkdownExtension
from datetime import datetime
from sqlalchemy.sql.expression import select
from waitress import serve
import json
import jinja2
from flask_sqlalchemy import SQLAlchemy

# Default puzzle directory may be overridden with env. variable
puzzle_path = os.environ.get('PUZZLE_PATH') or "coding_challenge"
db_uri = os.environ.get('DATABASE_URL') or 'sqlite:///scores.sqlite'

# puzzle_path + templates directory are both scanned for jinja content
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

app.jinja_env.add_extension(MarkdownExtension)
my_loader = jinja2.ChoiceLoader([
        app.jinja_loader, jinja2.FileSystemLoader([puzzle_path]),
    ])
app.jinja_loader = my_loader

# config.json found in root of puzzle path.
config_file = os.path.join(puzzle_path, "config.json")
with open(config_file, encoding="utf-8") as infile:
    puzzle_data = json.load(infile)
answers = puzzle_data["answers"]

db = SQLAlchemy(app)

from sqlalchemy import Column, DateTime, String, Integer, func

class Score(db.Model):
    id = Column('id', Integer, primary_key = True)
    player_name = Column(String(100))
    puzzle_id = Column(Integer)
    timestamp = Column(DateTime, default=func.now())

    def __init__(self, player_name, puzzle_id):
        self.player_name = player_name
        self.puzzle_id = puzzle_id

db.create_all()

accept_new_answers = True

players = []

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
    if len(name) < 3 or len(name) > 20 or not name.isalnum() or name.upper() in (player.upper() for player in players):
        return make_response(render_template('logindenied.html', hideusername=True))
    else:
        players.append(name)
        resp = make_response(render_template('loginconfirm.html', hideusername=True))
        resp.set_cookie('userID', name, secure=True)
        return resp

@app.route('/getuser')
def getuser():
    name = request.cookies.get('userID')
    scores = db.session.query(Score).filter(Score.player_name == name)
    print(scores)
    return '<p>username: '+name+'</p>'

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

@app.route('/resetscoresandplayers')
def reset():
    players = []
    # scores can not be reset this way...
    return render_template("confirm.html", hideusername=True)

@app.route('/myscore')
def myscore():
    name = request.cookies.get('userID')
    if (name not in players):
        players.append(name)
    myscore = db.session.query(Score).filter(Score.player_name == name)
    return render_template("myscore.html", username=name, myscore=myscore)

@app.route("/puzzle/<number>")
def puzzle(number):
    name = request.cookies.get('userID')
    return render_template("puzzle.html", username=name, puzzle_number=number, puzzle_description=get_puzzle_description(number))

@app.route("/puzzleinput/<number>")
def puzzle_input(number):
    return render_template("puzzleinput.html", puzzle_input=get_puzzle_input(number))

@app.route("/submitanswer/<number>", methods = ['POST'])
def submit_answer(number):
    if (not accept_new_answers):
        return render_template("stop.html")

    name = request.cookies.get('userID')
    answered = request.form['answer_input']

    if (answered in answers.get(number)):
        if (name not in players):
            players.append(name)
        score = Score(name, number)
        db.session.add(score)
        db.session.commit()
        template = "answercorrect.html"
    else:
        template = "answerincorrect.html"

    return make_response(render_template(template, puzzle_number=number, username=name))

@app.route("/scoreboard")
def score_board():
    matrix = {}
    leaderboard = {}
    results = db.session.query(Score).order_by(Score.player_name, Score.puzzle_id).all()

    for r in results:
        if r.player_name not in matrix:
            matrix[r.player_name] = {}
        matrix[r.player_name][r.puzzle_id] = True
    
    for player_name, solved in matrix.items():
        stars = ""
        count = 0
        for puzzle_id in get_puzzle_range():
            if puzzle_id in solved:
                stars += "*"
                count += 1
            else:
                stars += " "
        leaderboard[player_name] = {"solvedcount": count, "stars": stars }
    
    # items = sorted(results, key = sort_count_date)
    return render_template("scoreboard.html", hideusername=True, autorefresh=True, leaderboard=leaderboard.items())

# def sort_count_date(tup):
#     key, d = tup
#     return -d["solvedcount"], d["date"]

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)
    