from src.DAO.entity import User, Message, Role, session_map
from flask import request, render_template, url_for, redirect, flash, session, Blueprint


auth_api = Blueprint('auth_api', __name__)


@auth_api.route('/login/', methods=['GET'])
def login():
    if 'user_id' in session:
        user_id = format(session.get('user_id'))
        return redirect(url_for('index', user_id=user_id))
    else:
        title = 'Регистрация'
        link = '/register'
        return render_template('pages/login.html', title=title, link=link)


@auth_api.route('/check_login', methods=['POST'])
def check_login():
    if request.method == 'POST':
        login = request.form['login']
        password_one = request.form['password']

        user = session_map.query(User).filter_by(login=login, password=password_one).first()
        if user:
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_login'] = user.login
            session['role'] = user.role.name
            session['role_id'] = user.role_id

            flash('Добро пожаловать ' + format(session.get('user_name')), 'alert-success')
            return redirect(url_for('index'))
        else:
            flash('Неверно введены логин или пароль', 'alert-warning')
            return redirect(url_for('auth_api.login'))


@auth_api.route('/register/', methods=['GET'])
def register():
    if 'user_id' in session:
        return redirect(url_for('auth_api.posts'))
    else:
        title = 'Вход'
        link = '/login'
        return render_template('pages/register.html', title=title, link=link)


@auth_api.route('/check_register', methods=['POST'])
def check_register():
    name = request.form['name']
    user_login = request.form['login']
    password_one = request.form['password_one']
    password_two = request.form['password_two']

    if password_one != password_two:
        flash('Пароли не совпадают', 'alert-warning')

        return redirect(url_for('auth_api.register'))
    else:
        check_user = session_map.query(User).filter_by(login=user_login).first()
        if check_user:
            flash('Юзер с таким логином уже существует', 'alert-warning')
            return redirect(url_for('auth_api.register'))
        else:
            user = User(name, user_login, password_one)
            session_map.add(user)
            session_map.commit()
            flash('Пользователь ' + user_login + ' успешно зарегистрирован', 'alert-success')
            return redirect(url_for('auth_api.login'))


@auth_api.route('/sign_out', methods=['GET'])
def sign_out():
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_login', None)
    session.pop('role_id', None)
    return redirect(url_for('auth_api.login'))

