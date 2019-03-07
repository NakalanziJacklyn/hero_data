import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from books import app, db, bcrypt
from books.forms import RegistrationForm, LoginForm, ReviewForm, SearchForm
from books.models import User,Book,Review
from flask_login import login_user, current_user, logout_user, login_required



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
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('search'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)   
    


# Logout for the website
@app.route("/logout")
@login_required
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
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



# Comes after logging in
@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    return render_template("search.html")


# Page to show books as per search result
@app.route("/booklist", methods=["POST"])
@login_required
def booklist():
    if not current_user.is_authenticated:
        return render_template("login.html", error_message="Please Login First", work="Login")

    book_column = request.form.get("book_column")
    inputs = request.form.get("query")
   


    if book_column == "year":
        book_list=Book.query.filter_by(year=inputs)
        
        return render_template("booklist.html", book_list=book_list)

    elif book_column == "author":
        book_list=Book.query.filter_by(author=inputs)

        return render_template("booklist.html", book_list=book_list)

    elif book_column == "isbn":
        book_list=Book.query.filter_by(isbn=inputs)

        return render_template("booklist.html", book_list=book_list)

    elif book_column == "title":
        book_list=Book.query.filter_by(title=inputs)
        
        return render_template("booklist.html", book_list=book_list)

    else:
        return render_template("error.html", error_message="We didn't find any book with the year you typed."
                                                          " Please check for errors and try again.")

# Page to show details info about book
@app.route("/detail/<int:book_id>",methods=['GET','POST'])
@login_required
def detail(book_id):
    reviews=Review.query.filter_by(book_id=book_id).all()
    book=Book.query.get_or_404(book_id)
    return render_template("detail.html", success=True, book=book, reviews=reviews)
    

# user comments
@app.route("/detail/<int:book_id>/comment", methods=['GET', 'POST'])
@login_required
def comment(book_id):
    form=ReviewForm()
    if form.validate_on_submit():
        comment = Review(review=form.review.data, comment=form.comment.data, book_id=book_id, writer=current_user)
        db.session.add(comment)
        db.session.commit()
        flash('your comment has been added', 'success')
        return redirect(url_for('detail', book_id=book_id))
    return render_template('comment.html', title='Comment',
                           form=form, legend='Comment')


@app.route("/comment/<int:user_id>/delete", methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been deleted!', 'success')
    return redirect(url_for('detail'))