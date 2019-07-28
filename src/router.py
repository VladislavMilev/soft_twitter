from flask import Flask, request, render_template, url_for, redirect

from DAO.connection import SESSION, SESSION_SCOPE
from DAO.user.entity.userEntity import User, Message

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('main'))


@app.route('/main', methods=['GET'])
def main():
    session = SESSION()
    messages = session.query(Message).order_by(Message.id)

    return render_template('pages/main.html', messages=messages)


@app.route('/send_message', methods=['POST'])
def send_message():
    session = SESSION()

    title = request.form['title']
    text = request.form['text']
    tag = request.form['tag']

    session.add(Message(title, text, tag))
    session.commit()

    return redirect(url_for('main'))


@app.route('/register/', methods=['GET'])
def register():
    return render_template('pages/register.html')


@app.route('/check_register', methods=['POST'])
def check_register():
    name = request.form['name']
    login = request.form['login']
    password_1 = request.form['password_1']
    password_2 = request.form['password_2']
    return redirect(url_for('register'))


@app.route('/login/', methods=['GET'])
def login():
    return render_template('pages/login.html')


@app.route('/check_login', methods=['POST'])
def check_login():
    login = request.form['login']
    password = request.form['password_1']
    session = SESSION()

    user = session.query(User).filter_by(login=login, password=password).first()
    if user:
        user.login = SESSION_SCOPE
        return redirect(url_for('main'))
    else:
        return redirect(url_for('login'))
