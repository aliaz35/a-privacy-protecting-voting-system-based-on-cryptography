from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

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

@app.route('/')
def query_database():
    return render_template('query_database.html')

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/authentication_keys')
def authentication_keys():
    authentication_keys = AuthenticationKey.query.all()
    return render_template('authentication_keys.html', authentication_keys=authentication_keys)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # generate_keys()
        # db.session.query(AuthenticationKey).delete()
        # db.session.commit()
    app.run(ssl_context="adhoc", debug = True)