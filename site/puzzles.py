import os
import json
import jinja2
import jinja_markdown
from flask import request, make_response, render_template, abort, send_from_directory
from flask.helpers import send_from_directory
from datetime import datetime, timedelta
from flask_login import current_user
from model import db, User, Score

def add_puzzles(app):

    # Temporarily disabled - there is a caching bug in the footnotes extension
    # jinja_markdown.EXTENSIONS.append('pymdownx.extra') # To enable footnotes
    app.jinja_env.add_extension(jinja_markdown.MarkdownExtension)
    
    # Default puzzle directory may be overridden with env. variable
    puzzle_path = app.config['PUZZLE_PATH']
	# puzzle_path + templates directory are both scanned for jinja content
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
    def index():
        return render_template("index.html", puzzles=get_puzzle_range())

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route('/myscore')
    def myscore():
        userId = current_user.id
        myscore = db.session.query(Score).filter(Score.user_id == userId)
        return render_template("myscore.html", myscore=myscore)

    @app.route("/puzzle/<number>")
    def puzzle(number):
        return render_template("puzzle.html", puzzle_number=number, puzzle_description=get_puzzle_description(number))

    @app.route("/puzzle/<number>/input")
    def puzzle_input(number):
        return send_from_directory(puzzle_path, get_puzzle_input(number), mimetype="text/plain")

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
