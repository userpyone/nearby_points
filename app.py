from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from format import is_city
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_KEY')
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
@app.route('/')
def index():
    error = session.pop('error', None)
    return render_template('main.html', error=error)

@app.route('/process_form', methods=['POST'])
def process_form():
    if request.method == 'POST':
        user_input = request.form['user_input']
        if user_input.strip() == "":
            session['error'] = "Введите корректный адрес"
            return redirect(url_for('index'))
        if is_city(user_input):
            return render_template('res.html')
        else:
            session['error'] = "Адрес не содержит название города"
            return redirect(url_for('index'))

@app.route('/redirect')
def redirect_to_main():
    return redirect(url_for('index'))

@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('404.html'), 404

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)