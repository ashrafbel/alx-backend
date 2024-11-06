#!/usr/bin/env python3
from flask import Flask, render_template, request, g
from flask_babel import Babel, _
from pytz.exceptions import UnknownTimeZoneError
from datetime import datetime
import pytz

app = Flask(__name__)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

class Config:
    """Configuration class for the application."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app.config.from_object(Config)

babel = Babel(app)

def get_user():
    """
    Get the current user based on the 'login_as' URL parameter.

    Returns:
        dict: User data if the user ID is valid, else None.
    """
    user_id = request.args.get('login_as', type=int)
    if user_id is None or user_id not in users:
        return None
    return users[user_id]

@app.before_request
def before_request():
    """
    Store the current user in the global `g` object.
    
    This function is executed before each request.
    """
    g.user = get_user()

@babel.localeselector
def get_locale():
    """
    Select the best language based on the user's locale, request, and headers.

    Returns:
        str: The selected language code (e.g., 'en', 'fr').
    """
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    if g.user and g.user['locale'] and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']
    return (request.accept_languages.best_match(app.config['LANGUAGES']) or
            app.config['BABEL_DEFAULT_LOCALE'])

@babel.timezoneselector
def get_timezone():
    """
    Select the best timezone based on the user's timezone, request, and headers.

    Returns:
        str: The selected timezone (e.g., 'UTC', 'Europe/Paris').
    """
    timezone = request.args.get('timezone')
    if timezone:
        try:
            pytz.timezone(timezone)
            return timezone
        except UnknownTimeZoneError:
            pass

    if g.user and g.user['timezone']:
        try:
            pytz.timezone(g.user['timezone'])
            return g.user['timezone']
        except UnknownTimeZoneError:
            pass

    return app.config['BABEL_DEFAULT_TIMEZONE']

@app.route('/')
def index():
    """
    Render the home page, displaying the current time in the selected timezone.

    The current time is displayed based on the user's locale and timezone.
    
    Returns:
        Response: The rendered HTML template with the current time.
    """
    tz = get_timezone()
    current_time = datetime.now(pytz.timezone(tz))
    formatted_time = current_time.strftime("%b %d, %Y, %I:%M:%S %p")
    
    return render_template('index.html', current_time=formatted_time)

if __name__ == "__main__":
    """
    Run the Flask application with debugging enabled.
    """
    app.run(debug=True)
