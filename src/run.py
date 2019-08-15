from flask import Flask, render_template, url_for, redirect, session
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


@app.route('/', methods=['GET'])
def index():
    if 'user_id' in session:

        messages = session_map.query(Message).filter_by(status=message_statuses['aproved']).order_by(Message.id.desc())

        title = 'Выйти'
        link = '/sign_out'
        return render_template('pages/index.html', messages=messages, title=title, link=link)
    else:
        return redirect(url_for('auth_api.login'))



if __name__ == "__main__":
    app.run(debug=True)
