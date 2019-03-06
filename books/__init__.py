from flask import Flask,  request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_session import Session
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, Column
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = '57c55221dc0f2eb9e4de954dba0393fd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://dvzeebgbtgejnj:8fd31663266b81198d9b6eed848c39a1100adb5982afc1306c4ea34b290d6a0f@ec2-54-163-234-88.compute-1.amazonaws.com:5432/d9uk68nilkcqn4'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# POSTGRES = {
#     'user':'postgres',
#     'pw':'project123',
#     'db':'project1',
#     'host':'localhost',
#     'port':'5432',
# }

# app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{POSTGRES['user']}:{POSTGRES['pw']}@{POSTGRES['host']}:{POSTGRES['port']}/{POSTGRES['db']}"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
Session(app)


db = SQLAlchemy(app)
# migrate=Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from books import routes