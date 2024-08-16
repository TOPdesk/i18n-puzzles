from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

# Linked to app later:
# https://stackoverflow.com/a/9695045/3306
db = SQLAlchemy()

class Score(db.Model):
    id = Column('id', Integer, primary_key = True)
    user_id = Column('user_id', Integer, ForeignKey('users.id'), nullable = False)
    puzzle_id = Column(Integer)
    timestamp = Column(DateTime, default=func.now())

    def __init__(self, user_id, player_name, puzzle_id):
        self.user_id = user_id
        self.player_name = player_name # TODO: deprecated
        self.puzzle_id = puzzle_id

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    external_id = Column(String(64), nullable=False, unique=True)
    username = Column(String(64), nullable=False)
    # email = Column(String(64), nullable=True)
