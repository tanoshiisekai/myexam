from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    admin_username = db.Column(db.String(30), unique=True)
    admin_password = db.Column(db.String(30))

    def __init__(self, admin_username, admin_password):
        self.admin_username = admin_username
        self.admin_password = admin_password


class Problem(db.Model):
    problem_id = db.Column(db.Integer, primary_key=True)
    problem_typestring = db.Column(db.String(20))
    problem_description = db.Column(db.String(200))
    problem_picpath = db.Column(db.String(100))
    problem_choiceA = db.Column(db.String(100))
    problem_choiceB = db.Column(db.String(100))
    problem_choiceC = db.Column(db.String(100))
    problem_choiceD = db.Column(db.String(100))
    problem_answer = db.Column(db.String(10))

    def __init__(self, problem_typestring, problem_description,
                 problem_picpath, problem_choiceA, problem_choiceB,
                 problem_choiceC, problem_choiceD, problem_answer):
        self.problem_typestring = problem_typestring
        self.problem_description = problem_description
        self.problem_picpath = problem_picpath
        self.problem_choiceA = problem_choiceA
        self.problem_choiceB = problem_choiceB
        self.problem_choiceC = problem_choiceC
        self.problem_choiceD = problem_choiceD
        self.problem_answer = problem_answer


class UserLog(db.Model):
    userlog_id = db.Column(db.Integer, primary_key=True)
    userlog_userid = db.Column(db.Integer)
    userlog_right = db.Column(db.Integer)
    userlog_wrong = db.Column(db.Integer)
    userlog_timeduring = db.Column(db.Integer)
    userlog_status = db.Column(db.Integer)
    userlog_choicelog = db.Column(db.String(1000))

    def __init__(self, userlog_userid, userlog_right, userlog_wrong,
                 userlog_timeduring, userlog_status, userlog_choicelog):
        self.userlog_userid = userlog_userid
        self.userlog_right = userlog_right
        self.userlog_wrong = userlog_wrong
        self.userlog_timeduring = userlog_timeduring
        self.userlog_status = userlog_status
        self.userlog_choicelog = userlog_choicelog


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_username = db.Column(db.String(30))
    user_password = db.Column(db.String(30))
    user_token = db.Column(db.String(1000))
    user_ip = db.Column(db.String(30))

    def __init__(self, user_username, user_password, user_token="", user_ip=""):
        self.user_username = user_username
        self.user_password = user_password
        self.user_token = user_token
        self.user_ip = user_ip


db.create_all()

ad = Admin("admin", "longlong")
try:
    db.session.add(ad)
    db.session.commit()
except Exception as e:
    pass

