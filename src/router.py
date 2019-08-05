import datetime

from flask import Flask, request, render_template, url_for, redirect, flash, session, jsonify

from src.DAO.connection import SESSION
from src.DAO.entity import User, Message, Tag, Role

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.permanent_session_lifetime = datetime.timedelta(hours=12)

session_map = SESSION()


@app.route('/', methods=['GET'])
def index():
    if 'user_id' in session:
        messages = session_map.query(Message).filter_by(status=1).order_by(Message.id.desc())

        title = 'Выйти'
        link = '/sign_out'
        return render_template('pages/index.html', messages=messages, title=title, link=link)
    else:
        return redirect(url_for('login'))


#
# MESSAGE
#

@app.route('/send', methods=['POST'])
def send():
    user_id = session.get('user_id')
    title = request.form['title']
    text = request.form['text']
    tag = request.form['tag']
    color = request.form['color']

    session_map.add(Message(title, text, tag, user_id, color))
    session_map.commit()
    return redirect(url_for('posts'))


@app.route('/post/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    find_message_id = session_map.query(Message).filter_by(id=id).first()
    if find_message_id:
        session_map.delete(find_message_id)
        session_map.commit()
        flash('Сообщение удалено', 'alert-success')
        return redirect(url_for('posts'))
    else:
        flash('Не удалось удалить сообщение', 'alert-warning')
        return redirect(url_for('posts'))


@app.route('/post/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    title = 'Выйти'
    link = '/sign_out'

    find_message_id = session_map.query(Message).filter_by(id=id).first()
    find_tags = session_map.query(Tag).filter_by(message_id=id).all()

    if request.method == 'POST':
        message_title = request.form['title']
        text = request.form['text']

        find_message_id.title = message_title
        find_message_id.text = text

        session_map.commit()
        return redirect(url_for('posts'))

    else:
        if find_message_id:
            return render_template('pages/update-post.html',
                                   message=find_message_id,
                                   tag=find_tags,
                                   title=title,
                                   link=link)
        else:
            return redirect(url_for('posts'))


@app.route('/post/confirm/<int:id>', methods=['GET', 'POST'])
def confirm(id):
    if 'user_id' in session:
        find_message_id = session_map.query(Message).filter_by(id=id).first()

        if find_message_id:
            find_message_id.status = 1
            session_map.commit()
            flash('Пост подтвержден', 'alert-success')
            return redirect(url_for('posts'))
        else:
            flash('Пост не подтвержден', 'alert-warning')
            return redirect(url_for('index'))


#
# MESSAGE VIEW
#

@app.route('/posts', methods=['GET'])
def posts():
    if 'user_id' in session:
        user_id = session.get('user_id')
        messages = session_map.query(Message).filter_by(status=0).order_by(Message.id.desc())

        messages_in_review_admin = session_map.query(Message).filter_by(status=0).all()
        messages_in_review_user = session_map.query(Message).filter_by(status=0, user_id=user_id).all()

        message_cnt_user = 0
        for message in messages_in_review_user:
            message_cnt_user += 1

        message_cnt_admin = 0
        for message in messages_in_review_admin:
            message_cnt_admin += 1

        title = 'Выйти'
        link = '/sign_out'

        return render_template('pages/posts.html',
                               messages=messages,
                               message_cnt_user=message_cnt_user,
                               message_cnt_admin=message_cnt_admin,
                               title=title,
                               link=link
                               )
    else:
        return redirect(url_for('login'))


#
# USER
#


@app.route('/login/', methods=['GET'])
def login():
    if 'user_id' in session:
        user_id = format(session.get('user_id'))
        return redirect(url_for('posts', user_id=user_id))
    else:
        title = 'Регистрация'
        link = '/register'
        return render_template('pages/login.html', title=title, link=link)


@app.route('/check_login', methods=['POST'])
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
            return redirect(url_for('posts'))
        else:
            flash('Неверно введены логин или пароль', 'alert-warning')
            return redirect(url_for('login'))


@app.route('/register/', methods=['GET'])
def register():
    if 'user_id' in session:
        return redirect(url_for('posts'))
    else:
        title = 'Войти'
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


@app.route('/sign_out', methods=['GET'])
def sign_out():
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_login', None)
    session.pop('role_id', None)
    return redirect(url_for('login'))


@app.route('/users', methods=['GET'])
def users():
    if 'user_id' in session:
        title = 'Выйти'
        link = '/sign_out'

        get_all_users = session_map.query(User).all()
        get_all_roles = session_map.query(Role).all()
        return render_template('pages/users.html',
                               get_all_users=get_all_users,
                               get_all_roles=get_all_roles,
                               title=title,
                               link=link
                               )
    else:
        return redirect(url_for('login'))


@app.route('/api/user/info')
def user_info():
    user = {
        'id': session['user_id'],
        'username': session['user_name'],
        'login': session['user_login'],
        'role': session['role'],
        'role_id': session['role_id'],
    }
    return jsonify(user)


if __name__ == "__main__":
    app.run(debug=True)
