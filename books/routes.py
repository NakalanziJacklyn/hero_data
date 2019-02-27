import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from books import app, db, bcrypt
from books.forms import RegistrationForm, LoginForm
from books.models import Users
from flask_login import login_user, current_user, logout_user, login_required
from flask_session import Session


# Homepage
@app.route("/")
def index():
     status = "Loggedout"
     try:
        user_email=["user_email"]
        status=""
     except KeyError:
        user_email=""
     return render_template("index.html")


# Login Page
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('search'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('search'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)   
    


# Logout for the website
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


# Register Page

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('search'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



# Comes after logging in
@login_required
@app.route("/search", methods=["GET", "POST"])
def search():
    return render_template("search.html")


# Page to show books as per search result
@app.route("/booklist", methods=["POST"])
def booklist():
    if not current_user.is_authenticated:
        return render_template("login.html", error_message="Please Login First", work="Login")

    book_column = request.form.get("book_column")
    query = request.form.get("query")

    if book_column == "year":
        book_list = db.execute("SELECT * FROM books WHERE year = :query", {"query": query}).fetchall()
    else:
        book_list = db.execute("SELECT * FROM books WHERE UPPER(" + book_column + ") = :query ORDER BY title",
                               {"query": query.upper()}).fetchall()

    # Is whole of the info i.e. ISBN, title matches...
    if len(book_list):
        return render_template("booklist.html", book_list=book_list)

    elif book_column != "year":
        error_message = "We couldn't find the books you searched for."
        book_list = db.execute("SELECT * FROM books WHERE UPPER(" + book_column + ") LIKE :query ORDER BY title",
                               {"query": "%" + query.upper() + "%"}).fetchall()
        if not len(book_list):
            return render_template("error.html", error_message=error_message)
        message = "You might be searching for:"
        return render_template("booklist.html", error_message=error_message, book_list=book_list, message=message,
                               )
    else:
        return render_template("error.html", error_message="We didn't find any book with the year you typed."
                                                          " Please check for errors and try again.")




