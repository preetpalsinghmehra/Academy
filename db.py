from itsdangerous import Serializer
from main import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    image_file = db.Column(db.String(100), nullable=False, default='default.jpg')
    email = db.Column(db.String(30), unique=True, nullable=False)
    mobile = db.Column(db.Integer, unique=True, nullable=False)
    password = db.Column(db.Text(20), nullable=False)
    address = db.Column(db.String(100), unique=False, nullable=False)
    city = db.Column(db.String(20), unique=False, nullable=False)
    state = db.Column(db.String(20), unique=False, nullable=False)
    zip = db.Column(db.Integer, unique=False, nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)

        return s.dumps({'user_id': self.id}).decode('utf-8')

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ques = db.Column(db.Text, nullable=False)
    ch1 = db.Column(db.String, nullable=False)
    ch2 = db.Column(db.String, nullable=False)
    ch3 = db.Column(db.String, nullable=False)
    ch4 = db.Column(db.String, nullable=False)
    ans = db.Column(db.String, nullable=False)