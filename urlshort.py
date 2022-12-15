from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1> Hello World a</h1>'


@app.route('/about')
def about():
    return '<h1> This is a URL shortener</h1>'
