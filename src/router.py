import datetime

from flask import Flask, request, render_template, url_for, redirect, flash, make_response, session
from fastapi import Cookie, FastAPI

import auth
from DAO.connection import SESSION
from DAO.user.entity.userEntity import User, Message

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.permanent_session_lifetime = datetime.timedelta(days=1)


# app = FastAPI()


@app.route('/', methods=['GET'])
def index():

    if 'user_id' in session:
        return render_template('pages/main.html')
    else:
        return redirect(url_for('login'))


@app.route('/main', methods=['GET'])
def main():
    session_map = SESSION()

    if 'user_id' in session:
        messages = session_map.query(Message).order_by(Message.id)
        title = 'Sign out'
        link = '/sign_out'
        return render_template('pages/main.html', messages=messages, title=title, link=link)
    else:
        return redirect(url_for('login'))


#
# MESSAGE
#

@app.route('/send_message', methods=['POST'])
def send_message():
    session_map = SESSION()

    user_id = session.get('user_id')
    title = request.form['title']
    text = request.form['text']
    tag = request.form['tag']

    session_map.add(Message(title, text, tag, user_id))
    session_map.commit()

    return redirect(url_for('main'))


#
# USER
#


@app.route('/register/', methods=['GET'])
def register():
    if 'user_id' in session:
        return redirect(url_for('main'))
    else:
        title = 'Login'
        link = '/login'
        return render_template('pages/register.html', title=title, link=link)


@app.route('/check_register', methods=['POST'])
def check_register():
    name = request.form['name']
    user_login = request.form['login']
    password_one = request.form['password_one']
    password_two = request.form['password_two']

    if password_one != password_two:
        flash('Пароли не совпадают', 'alert-warning')

        return redirect(url_for('register'))
    else:
        session_map = SESSION()
        check_user = session_map.query(User).filter_by(login=user_login).first()
        if check_user:
            flash('Юзер с таким логином уже существует', 'alert-warning')
            return redirect(url_for('register'))
        else:
            user = User(name, user_login, password_one)
            session_map.add(user)
            session_map.commit()
            flash('Пользователь ' + user_login + ' успешно зарегистрирован', 'alert-success')
            return redirect(url_for('login'))


@app.route('/login/', methods=['GET'])
def login():
    if 'user_id' in session:
        user_id = format(session.get('user_id'))
        return redirect(url_for('main', user_id=user_id))
    else:
        title = 'Register'
        link = '/register'
        return render_template('pages/login.html', title=title, link=link)


@app.route('/check_login', methods=['POST'])
def check_login():
    if request.method == 'POST':
        session_map = SESSION()

        login = request.form['login']
        password_one = request.form['password']

        user = session_map.query(User).filter_by(login=login, password=password_one).first()
        if user:
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_login'] = user.login
            session['user_role'] = user.role

            flash('Добро пожаловать ' + format(session.get('user_name')), 'alert-success')
            return redirect(url_for('main'))
        else:
            flash('Неверно введены логин или пароль', 'alert-warning')
            return redirect(url_for('login'))


@app.route('/sign_out', methods=['GET'])
def sign_out():
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_login', None)
    session.pop('user_role', None)
    return redirect(url_for('login'))
