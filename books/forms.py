from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField,IntegerField,SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from books.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ReviewForm(FlaskForm):
    review=SelectField('Rating', validators=[DataRequired()],  choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    comment = StringField('comment')
    submit = SubmitField('submit')

class SearchForm(FlaskForm):
    isbn=StringField('isbn_number', validators=[DataRequired()])
    title = StringField('title', validators=[DataRequired()])
    author = SubmitField('author', validators=[DataRequired()]) 
    year = SubmitField('year', validators=[DataRequired()]) 
    submit = SubmitField('search')    

# class CommentForm(FlaskForm):
#     comment = StringField("Comment", validators=[DataRequired()])
#     submit = SubmitField("submit")    