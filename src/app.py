from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('main.html')


@app.route('/url_map/')
def url_map():
    return str(app.url_map)


app.run()