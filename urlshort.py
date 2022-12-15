from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', cash='Show me the money!')


@app.route('/about')
def about():
    return '<h1> This is a URL shortener</h1>'
