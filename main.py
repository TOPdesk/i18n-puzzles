import os, os.path
from flask import Flask, request, make_response, render_template
from jinja_markdown import MarkdownExtension

app = Flask(__name__)
app.jinja_env.add_extension(MarkdownExtension)

@app.route("/")
def home():
    puzzle_list=os.listdir("templates/puzzles")
    name = request.cookies.get('userID')
    return render_template("index.html", username=name, puzzles=puzzle_list)

@app.route('/login')
def index():
   return render_template('login.html')

@app.route('/setuser', methods = ['POST', 'GET'])
def setuser():
   if request.method == 'POST':
    user = request.form['nm']
    resp = make_response(render_template('loginconfirm.html'))
    resp.set_cookie('userID', user)
    return resp

@app.route('/getuser')
def getuser():
   name = request.cookies.get('userID')
   return '<p>username: '+name+'</p>'

@app.route("/puzzle/<number>")
def puzzle(number):
    name = request.cookies.get('userID')
    return render_template("puzzle.html", username=name, puzzle_number=number)

@app.route("/puzzleinput/<number>")
def puzzle_input(number):
    return render_template("puzzleinput.html", puzzle_number=number)

if __name__ == "__main__":
    app.run()