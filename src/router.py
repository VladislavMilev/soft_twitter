from flask import Flask, request, render_template, url_for, redirect, flash, make_response
from fastapi import Cookie, FastAPI

import cookies
from DAO.connection import SESSION
from DAO.user.entity.userEntity import User, Message

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# app = FastAPI()


@app.route('/', methods=['GET'])
def index():
    return render_template('pages/index.html')


@app.route('/main', methods=['GET'])
def main():
    session = SESSION()
    messages = session.query(Message).order_by(Message.id)

    return render_template('pages/main.html', messages=messages)


#
# MESSAGE
#

@app.route('/send_message', methods=['POST'])
def send_message():
    session = SESSION()

    title = request.form['title']
    text = request.form['text']
    tag = request.form['tag']

    session.add(Message(title, text, tag))
    session.commit()

    return redirect(url_for('main'))


#
# USER
#


@app.route('/register/', methods=['GET'])
def register():
    return render_template('pages/register.html')


@app.route('/check_register', methods=['POST'])
def check_register():
    name = request.form['name']
    login = request.form['login']
    password_one = request.form['password_one']
    password_two = request.form['password_two']

    if password_one != password_two:
        flash('Пароли не совпадают', 'alert-warning')

        return redirect(url_for('register'))
    else:
        session = SESSION()
        check_user = session.query(User).filter_by(login=login).first()
        if check_user:
            flash('Юзер с таким логином уже существует', 'alert-warning')
            return redirect(url_for('register'))
        else:
            user = User(name, login, password_one)
            session.add(user)
            session.commit()
            flash('Пользователь ' + login + ' успешно зарегистрирован', 'alert-success')
            return redirect(url_for('login'))


@app.route('/login/', methods=['GET'])
def login():
    return render_template('pages/login.html')


@app.route('/check_login', methods=['GET', 'POST'])
def check_login():
    login = request.form['login']
    password_one = request.form['password']

    session = SESSION()
    user = session.query(User).filter_by(login=login, password=password_one).first()

    if user:
        flash('Добро пожаловать ' + login, 'alert-success')
        return redirect(url_for('set_cookie'))
    else:
        flash('Неверно введены логин или пароль', 'alert-warning')
        return redirect(url_for('login'))


#
# COOKIES
#

@app.route('/set_cookie', methods=['GET', 'POST'])
def set_cookie():
    res = make_response("Setting a cookie")
    res.set_cookie('foo', max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route('/delete_cookie', methods=['GET', 'POST'])
def delete_cookie():
    res = make_response("Setting a cookie")
    res.set_cookie('session', max_age=0)
    return res


@app.route('/check_cookies', methods=['POST'])
def check_cookies():
    res = make_response(format(request.cookies.get('foo')))
    return res
