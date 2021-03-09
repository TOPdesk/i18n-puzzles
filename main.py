import os, os.path
from flask import Flask, request, make_response, render_template
from jinja_markdown import MarkdownExtension
from datetime import datetime
from waitress import serve

app = Flask(__name__)
app.jinja_env.add_extension(MarkdownExtension)

accept_new_answers = True
answers = {
    "1": "(-107,35)",
    "2": "495",
    "3": "711",
    "4": "3732",
    "5": "37",
    "6": "1177",
}
players = []
scores = {}

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
        scores[name] = {}
        resp = make_response(render_template('loginconfirm.html', hideusername=True))
        resp.set_cookie('userID', name, secure=True)
        return resp

@app.route('/getuser')
def getuser():
    name = request.cookies.get('userID')
    print(scores[name])
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
    global players
    global scores
    players = []
    scores = {}
    return render_template("confirm.html", hideusername=True)

@app.route('/myscore')
def myscore():
    name = request.cookies.get('userID')
    if (name not in scores):
        scores[name] = {}
    if (name not in players):
        players.append(name)
    return render_template("myscore.html", username=name, myscore=scores[name])

@app.route("/puzzle/<number>")
def puzzle(number):
    name = request.cookies.get('userID')
    return render_template("puzzle.html", username=name, puzzle_number=number)

@app.route("/puzzleinput/<number>")
def puzzle_input(number):
    return render_template("puzzleinput.html", puzzle_number=number)

@app.route("/submitanswer/<number>", methods = ['POST'])
def submit_answer(number):
    if (not accept_new_answers):
        return render_template("stop.html")

    name = request.cookies.get('userID')
    answered = request.form['answer_input']

    if (answers.get(number) == answered):
        if (name not in scores):
            scores[name] = {}
        if (name not in players):
            players.append(name)
        scores[name][number] = datetime.now()
        template = "answercorrect.html"
    else:
        template = "answerincorrect.html"

    return make_response(render_template(template, puzzle_number=number, username=name))

@app.route("/scoreboard")
def score_board():
    leaderboard = {}
    items = []
    for name, solved_times in scores.items():
        latest_solve = datetime.fromtimestamp(0)
        for puzzle_number, sovled_time in solved_times.items():
            if (sovled_time > latest_solve):
                latest_solve = sovled_time
        leaderboard[name] = {"solvedcount": len(scores[name]), "date": latest_solve.strftime("%H:%M:%S.%f")}
    
    items = sorted(leaderboard.items(), key = sort_count_date)
    return render_template("scoreboard.html", hideusername=True, autorefresh=True, leaderboard=items)

def sort_count_date(tup):
    key, d = tup
    return -d["solvedcount"], d["date"]

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)
