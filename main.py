import os, os.path
from flask import Flask, request, make_response, render_template
from jinja_markdown import MarkdownExtension
from datetime import datetime
from waitress import serve

app = Flask(__name__)
app.jinja_env.add_extension(MarkdownExtension)

answers = {
    "1": "(-107,35)",
    "2": "foo",
    "3": "foo",
    "4": "foo",
    "5": "foo",
    "6": "foo",
}
players = []
scoreboard = {}

@app.route("/")
def home():
    puzzle_list=os.listdir("templates/puzzles")
    name = request.cookies.get('userID')
    return render_template("index.html", username=name, puzzles=puzzle_list)

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
        scoreboard[name] = {}
        resp = make_response(render_template('loginconfirm.html', hideusername=True))
        resp.set_cookie('userID', name, secure=True)
        return resp

@app.route('/getuser')
def getuser():
    name = request.cookies.get('userID')
    print(scoreboard[name])
    return '<p>username: '+name+'</p>'

@app.route("/puzzle/<number>")
def puzzle(number):
    name = request.cookies.get('userID')
    return render_template("puzzle.html", username=name, puzzle_number=number)

@app.route("/puzzleinput/<number>")
def puzzle_input(number):
    return render_template("puzzleinput.html", puzzle_number=number)

@app.route("/submitanswer/<number>", methods = ['POST'])
def submit_answer(number):
    name = request.cookies.get('userID')
    answered = request.form['answer_input']

    if (answers.get(number) == answered):
        if (name not in scoreboard):
            scoreboard[name] = {}
        if (name not in players):
            players.append(name)
        scoreboard[name][number] = datetime.now()
        template = "answercorrect.html"
    else:
        template = "answerincorrect.html"

    return make_response(render_template(template, puzzle_number=number, username=name))

@app.route("/scoreboard")
def score_board():
    return render_template("scoreboard.html", hideusername=True, autorefresh=True, scores=scoreboard)

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)