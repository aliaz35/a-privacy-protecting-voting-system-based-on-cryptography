from flask import Flask, render_template, request, redirect, url_for,jsonify,session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from phe import paillier
import pickle
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200))

class AuthenticationKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    authentication_key = db.Column(db.String(200), nullable=False)

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
            session['logged_in'] = True
            session['user_id'] = user.id
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

        return redirect(url_for('home'))
    return render_template('register.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))  # 如果未登录，重定向到登录页面
        return f(*args, **kwargs)  # 如果已登录，正常访问视图
    return decorated_function

@app.route('/vote', methods=['POST'])
@login_required  # 使用装饰器保护路由
def vote():
    data = request.json
    vote = data.get('vote')
    keys_in_db = AuthenticationKey.query.all()
    authKey = data.get('key')
    file_path_public = 'paillier_public_key.pkl'
    with open(file_path_public, 'rb') as file:
        public_key = pickle.load(file)
    for key_in_db in keys_in_db:
        if check_password_hash(key_in_db.authentication_key, authKey):
            try:
                db.session.delete(key_in_db)
                db.session.commit()
                file_path = 'result.pkl'
                with open(file_path, 'rb') as file:
                    res = pickle.load(file)
                res = res + public_key.encrypt(int(vote))
                with open(file_path, 'wb') as file:
                    pickle.dump(res, file)
                return jsonify({"message": "投票成功"})
            except Exception as e:
                db.session.rollback()
                return jsonify({"message": f"删除密钥时出错: {str(e)}"})
    return jsonify({"message": "无效的认证密钥"}), 401

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(ssl_context="adhoc", debug = True)