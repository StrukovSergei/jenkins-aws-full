"""
A simple Flask application for a weather app.

This application provides functionality for user authentication, weather data retrieval,
and rendering weather information on a webpage.

"""

from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime, timedelta
from os import urandom
from googletrans import Translator
from modules import api
from modules.db_handler import add_user_to_file, login_user_from_file

app = Flask(__name__)
app.secret_key = "f10e2821bbbea527ea02200352313bc059445190"  # strong key
app.permanent_session_lifetime = timedelta(seconds=15)


@app.route("/", methods=['GET', 'POST'])
def index():
    """
    Route for the main page.

    If a user is logged in, it allows the user to search for weather data for a specific location.
    If a POST request is received, it retrieves weather data for the location provided by the user
    and renders the weather information on the webpage.
    If no user is logged in, it redirects to the login page.

    """
    if 'user' in session:
        if request.method == 'POST':
            location = request.form['location']
            if check_input(location):
                weather_data = api.get_weather(location)
                if weather_data:
                    return render_template('index.html', weather_data=weather_data, days=check_days(), filtered_location=check_location(weather_data))
                else:
                    return render_template('index.html', wrong_input=1)
            else:
                return render_template('index.html', wrong_input=1)
        else:
            return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Route for user signup.

    If a POST request is received with valid user credentials, it adds the user to the system
    and redirects to the main page.
    If no POST request is received, it renders the signup page.

    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if add_user_to_file(username, password):
            session['user'] = username
            return redirect(url_for('index'))
        else:
            return render_template('signup.html', info="User already exists or incorrect")
    else:
        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route for user login.

    If a POST request is received with valid user credentials, it logs the user in
    and redirects to the main page.
    If no POST request is received, it renders the login page.

    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_user_from_file(username, password):
            session['user'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', info="Invalid Username or Password")
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    """
    Route for user logout.

    Logs out the user and redirects to the login page.

    """
    session.pop('user', None)
    return redirect(url_for('login'))

def check_input(input):
    """
    Check the validity of user input.

    """
    special = {'@', '#', '%', '&', '!', '^', '*', '(', ')', '~', '[', ']', '=', '+'}
    if input is None or len(input) > 20 or any(char.isdigit() for char in input) or any(char in special for char in input):
        return False
    else:
        return True
    
def check_days():
    """
    Get rearranged days of the week starting from the current day.

    """
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    today = datetime.today().strftime('%A')
    today_index = days.index(today)
    rearranged_days = days[today_index:] + days[:today_index]
    return rearranged_days

def check_location(data):
    """
    Translate the resolved address to the user's language.

    """
    return Translator().translate(data['resolvedAddress']).text

if __name__ == '__main__':
    app.run(host='0.0.0.0')
