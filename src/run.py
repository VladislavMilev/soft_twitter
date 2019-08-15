import json
import os
import random

from flask import Flask, render_template, url_for, redirect, session, send_file, request
import datetime
from src.DAO.connection import SESSION
from src.DAO.entity import Message

from src.api.user import user_api
from src.api.message import message_api
from src.api.auth import auth_api

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.permanent_session_lifetime = datetime.timedelta(hours=1)

app.register_blueprint(user_api)
app.register_blueprint(message_api)
app.register_blueprint(auth_api)


session_map = SESSION()


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


FILE_FOLDER = 'src/files/'
rnd = 'qwertyuiopasdfghjklzxcvbnm1234567890'
ls = list(rnd)

file_name = ''.join([random.choice(ls) for x in range(12)])


@app.route('/', methods=['GET'])
def index():
    if 'user_id' in session:

        messages = session_map.query(Message).filter_by(status=message_statuses['aproved']).order_by(Message.id.desc())

        title = 'Выйти'
        link = '/sign_out'
        return render_template('pages/index.html', messages=messages, title=title, link=link)
    else:
        return redirect(url_for('auth_api.login'))



#
# GENERATE USER-KEY
#

@app.route('/create', methods=['GET', 'POST'])
def create():
    return render_template('pages/create.html')


@app.route('/createfile', methods=['GET', 'POST'])
def createfile():
    token = ''.join([random.choice(ls) for x in range(29)])

    name = session.get('user_name')
    login = session.get('user_login')

    user = {
        'name': name,
        'login': login,
        'token': token
    }

    file_create = open(FILE_FOLDER + str(file_name + '.txt'), 'w')
    file_create.write(json.dumps(user))
    file_create.close()

    # file_read = open(FILE_FOLDER + str(file_name), 'r')
    # f = json.loads(file_read.read())

    # return render_template('pages/create.html')
    return send_file('files/' + file_name + '.txt', attachment_filename=file_name)


@app.route('/getfile')
def getfile():
    return send_file(FILE_FOLDER + file_name, attachment_filename=file_name)


def remove():
    scan = os.scandir(FILE_FOLDER)
    file_name = list(scan)

    for item in file_name:
        os.remove(item)
    return redirect(url_for('index'))


@app.route('/key')
def key():
    title = 'Выйти'
    link = '/sign_out'
    return render_template('pages/key.html',
                           title=title,
                           link=link
                           )


@app.route('/get-key')
def get_key():
    pass


if __name__ == "__main__":
    app.run(debug=True)
