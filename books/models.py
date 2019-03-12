from datetime import datetime
from books import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    reviews=db.relationship('Review', backref='writer', lazy=True)
    


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(50))
    author = db.Column(db.String(50))
    title = db.Column(db.String(50))
    year = db.Column(db.Integer) 
    reviews=db.relationship('Review', backref='read', lazy=True)  

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review= db.Column(db.Integer, nullable=False)
    book_id=db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment=db.Column(db.String(), nullable=False)

