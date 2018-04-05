from flask import Flask
from flask import jsonify

app = Flask(__name__)

d = {"hello": "worldd"}


@app.route('/')
def hello_word():
    return jsonify(d)



@app.route('/<userName>')
def print_userName(userName):
    d["userName"]= userName
    return jsonify(d)


if __name__=='__main__':
    app.run(debug=True)