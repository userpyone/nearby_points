from geo import get_coordinates_by_address
from format import sort_by_admin_level, get_totals, content1
from osm import osm_request, get_osm_values, new_request, new_request2
from api import get_weather, weather_api_key

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
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
    user_input = session.pop('user_input', None)
    return render_template('main.html', error=error, user_input=user_input)

@app.route('/process_form', methods=['POST'])
def process_form():
    if request.method == 'POST':
        user_input = request.form['user_input']
        if user_input.strip() == "":
            return redirect(url_for('index'))
        if is_city(user_input):
            content, coord = content1(user_input)
            weather = get_weather(f'{coord}', weather_api_key)
            if content is not None:
                totals1000_1 = get_totals(new_request('1000', f'{coord}'))
                totals1000_2 = get_totals(new_request2('1000', f'{coord}'))
                session['coord'] = coord
                if totals1000_1 and totals1000_2:
                    return render_template('res.html',
                                           address=user_input,
                                           district=content[0],
                                           region=content[1],
                                           res1=totals1000_1,
                                           res2=totals1000_2,
                                           weather=weather)
                else:
                    session['error'] = "Произошла ошибка"
                    return redirect(url_for('index'))
            else:
                session['error'] = "Адрес некорректен"
                session['user_input'] = user_input
                return redirect(url_for('index'))
        else:
            session['error'] = "Адрес не содержит название города"
            session['user_input'] = user_input
            return redirect(url_for('index'))

@app.route('/get_more_data')
def get_more_data():
    coord = session.get('coord')
    if coord:
        totals2000_1 = get_totals(new_request('2000', f'{coord}'))
        totals2000_2 = get_totals(new_request2('2000', f'{coord}'))
        return jsonify(res3=totals2000_1, res4=totals2000_2)
    else:
        return jsonify(error="Coordinates not found"), 400

@app.route('/redirect')
def redirect_to_main():
    return redirect(url_for('index'))

@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('404.html'), 404

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True)
