from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return '<h1> This is a URL shortener</h1>'


@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        return render_template('your_url.html', code=request.form['code'])
    else:
        error = 'Something went wrong. This is not valid URL.'
        return render_template('your_url.html', code=error)
