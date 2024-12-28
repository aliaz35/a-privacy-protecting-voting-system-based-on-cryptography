from flask import Flask, render_template, request, redirect, url_for,jsonify,session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

votes = {
    "候选人1": 0,
    "候选人2": 0,
    "候选人3": 0
}
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200))  # 调整为能容纳加密后的密码

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(name=username).first()

        if user and check_password_hash(user.password, password):
            session['logged_in'] = True  # 标记用户已经登录
            session['user_id'] = user.id  # 存储用户ID
            return app.send_static_file('vote.html')
        else:
            error = 'Invalid credentials. Please try again.'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        user = User(name=name, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('users'))
    return render_template('register.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))  # 如果未登录，重定向到登录页面
        return f(*args, **kwargs)  # 如果已登录，正常访问视图
    return decorated_function

@app.route('/vote', methods=['GET', 'POST'])
@login_required  # 使用装饰器保护路由
def vote():
    data = request.json
    vote = data.get('vote')
    if vote in votes:
        votes[vote] += 1
        return jsonify({"message": "投票成功", "votes": votes})
    else:
        return jsonify({"message": "无效的投票选项"}), 400


@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)