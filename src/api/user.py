from src.DAO.entity import User, Message, Role, session_map
from flask import request, render_template, url_for, redirect, flash, session, Blueprint

import base64
import requests



message_statuses = {
    'inreview': 0,
    'aproved': 1,
    'rejected': 2
}

user_statuses = {
    'admin': 1,
    'new': 2,
    'redactor': 3,
    'rejected': 4,
}


user_api = Blueprint('user_api', __name__)


@user_api.route('/users', methods=['GET'])
def users():
    if 'user_id' in session:
        if session.get('role') == 'admin':
            title = 'Выйти'
            link = '/sign_out'

            status_color = {
                'admin': 'dark',
                'redactor': 'success',
                'rejected': 'danger',
                'new': 'primary',
            }

            get_all_users = session_map.query(User).all()
            get_all_roles = session_map.query(Role).all()
            return render_template('pages/users.html',
                                   get_all_users=get_all_users,
                                   get_all_roles=get_all_roles,
                                   title=title,
                                   link=link,
                                   status_color=status_color
                                   )
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@user_api.route('/set-role/<string:role>/<int:id>', methods=['GET', 'POST'])
def set_role(role, id):
    find_id = session_map.query(User).filter_by(id=id).first()

    if find_id:
        if role == 'admin':
            find_id.role_id = user_statuses['admin']
        elif role == 'new':
            find_id.role_id = user_statuses['new']
        elif role == 'redactor':
            find_id.role_id = user_statuses['redactor']
        elif role == 'rejected':
            find_id.role_id = user_statuses['rejected']

        session_map.commit()
        flash('Статус пользователя "' + find_id.name + '" изменен на ' + find_id.role.name, 'alert-success')
        return redirect(url_for('user_api.users'))

    else:
        flash('Статус пользователя ' + find_id.name + ' не изменен', 'alert-warning')
        return redirect(url_for('user_api.users'))


@user_api.route('/user/<int:id>')
def user(id):
    if session.get('role') == 'admin' or session.get('user_id') == id:
        title = 'Выйти'
        link = '/sign_out'

        user = session_map.query(User).filter_by(id=id).first()
        message_count = session_map.query(Message).filter_by(user_id=id).all()

        mc = 0
        for messages in message_count:
            mc += 1

        return render_template('pages/user.html',
                               user=user,
                               mc=mc,
                               title=title,
                               link=link,
                               )
    else:
        flash('Отказано в доступе', 'alert-warning')
        return redirect(url_for('index'))


@user_api.route('/user/edit/<int:id>', methods=['GET'])
def user_edit(id):
    title = 'Выйти'
    link = '/sign_out'

    user = session_map.query(User).filter_by(id=id).first()

    if user:
        return render_template('pages/user-edit.html',
                               user=user,
                               title=title,
                               link=link
                               )
    else:
        flash('Отказано в доступе', 'alert-warning')
        return redirect(url_for('index'))


@user_api.route('/user_image_upload/<int:id>', methods=['POST'])
def user_image_uploads(id):
    image = request.files['image']
    token = 'WebKitFormBoundaryjKbhzxJawAgnCDuK'

    image_string = base64.b64encode(image.read()).decode("utf-8")

    res = requests.post('https://api.imgbb.com/1/upload?key=' + token, {
        'image': image_string
    })
    data = res.json()
    get_image = data['data']['url']
    return render_template('pages/user-edit.html',
                           res=res,
                           image_string=image_string,
                           get_image=get_image
                           )


@user_api.route('/user/update/<int:id>', methods=['GET', 'POST'])
def user_update(id):
    title = 'Выйти'
    link = '/sign_out'

    find_user_id = session_map.query(User).filter_by(id=id).first()

    if request.method == 'POST':
        user_name = request.form['name']
        user_login = request.form['login']
        image = request.files['image']

        if image == None:
            image = 'https://avatars.servers.getgo.com/2205256774854474505_medium.jpg'

        token = 'WebKitFormBoundaryjKbhzxJawAgnCDuK'

        image_string = base64.b64encode(image.read()).decode("utf-8")

        res = requests.post('https://api.imgbb.com/1/upload?key=' + token, {
            'image': image_string
        })
        data = res.json()
        get_image = data['data']['url']

        find_user_id.name = user_name
        find_user_id.login = user_login
        find_user_id.user_image = get_image

        session_map.commit()
        flash('Данные обновлены', 'alert-success')
        return redirect(url_for('user_api.users'))

    else:
        flash('Отказано в доступе', 'alert-warning')
        return redirect(url_for('user_api.users'))