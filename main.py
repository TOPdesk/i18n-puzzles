import os, os.path
from flask import Flask, render_template
from jinja_markdown import MarkdownExtension

app = Flask(__name__)
app.jinja_env.add_extension(MarkdownExtension)

@app.route("/")
def home():
    puzzle_list=os.listdir("templates/puzzles")
    return render_template("index.html", puzzles=puzzle_list)

@app.route("/puzzle/<number>")
def puzzle(number):
    return render_template("puzzle.html", puzzle_number=number)

@app.route("/puzzleinput/<number>")
def puzzle_input(number):
    return render_template("puzzleinput.html", puzzle_number=number)

if __name__ == "__main__":
    app.run()