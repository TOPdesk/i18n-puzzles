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

scoreboard = {}

@app.route("/")
def home():
    puzzle_list=os.listdir("templates/puzzles")
    name = request.cookies.get('userID')
    return render_template("index.html", username=name, puzzles=puzzle_list)

@app.route('/login')
def index():
    return render_template('login.html')

@app.route('/setuser', methods = ['POST'])
def setuser():
    name = request.form['nm']
    scoreboard[name] = {}
    resp = make_response(render_template('loginconfirm.html'))
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
        scoreboard[name][number] = datetime.now()
        template = "correct.html"
    else:
        template = "incorrect.html"

    return make_response(render_template(template, puzzle_number=number, username=name))

@app.route("/scoreboard")
def score_board():
    return render_template("scoreboard.html", scores=scoreboard)

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)