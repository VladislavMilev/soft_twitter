from collections import namedtuple

from flask import Flask, request, render_template, url_for, redirect

app = Flask(__name__)

Message = namedtuple('Message', 'name text tag')
messages = []


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')


@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html', messages=messages)


@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form['name']
    text = request.form['text']
    tag = request.form['tag']

    messages.append(Message(name, text, tag))
    return redirect(url_for('main'))
