from flask import Flask

app = Flask(__name__)

from app import rout
app.run(debug=True)