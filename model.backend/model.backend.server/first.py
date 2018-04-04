from flask import Flask
from flask import jsonify

app = Flask(__name__)

@app.route('/')
def hello_word():
    d = {"hello": "world"}
    return jsonify(d)
    