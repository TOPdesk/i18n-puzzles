from flask import Flask, render_template
from jinja_markdown import MarkdownExtension

app = Flask(__name__)
app.jinja_env.add_extension(MarkdownExtension)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/puzzle/<number>")
def puzzle(number):
    return render_template("index.html", puzzle_number=number)

if __name__ == "__main__":
    app.run()