from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import os
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200))  # 调整为能容纳加密后的密码

class AuthenticationKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    authentication_key = db.Column(db.String(200), nullable=False)

def generate_keys():
    for _ in range(10):
        key = str(uuid.uuid4())
        print(key)
        hashed_key = generate_password_hash(key)

        new_key = AuthenticationKey(authentication_key=hashed_key)
        db.session.add(new_key)

    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return []

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.session.query(AuthenticationKey).delete()
        generate_keys()
        db.session.commit()