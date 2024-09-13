import os
from flask import Flask
from waitress import serve
from dotenv import load_dotenv
from model import db
from oauth import add_authentication
from puzzles import add_puzzles

def create_app():
    load_dotenv()

    app = Flask(__name__)

    db_uri = os.environ.get('DATABASE_URL') or 'sqlite:///scores.sqlite'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['PUZZLE_PATH'] = os.path.abspath(os.environ.get('PUZZLE_PATH') or "coding_challenge")
    app.config['CONTACT_EMAIL'] = "m.van.iersel@topdesk.com"

    # url_for() should generate links with https protocol: https://stackoverflow.com/a/26636880/3306
    # Otherwise oauth provider will report callback url mismatch
    app.config['PREFERRED_URL_SCHEME'] = os.environ.get('PREFERRED_URL_SCHEME') or 'http'

    db.init_app(app)
    
    app.secret_key = os.environ.get('FLASK_SECRET_KEY')

    with app.app_context():
        db.create_all()

    add_puzzles(app)
    add_authentication(app)

    return app

app = create_app()

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
