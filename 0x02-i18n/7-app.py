#!/usr/bin/env python3
"Basic Babel setup with timezone selector"

from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz
from pytz.exceptions import UnknownTimeZoneError

app = Flask(__name__)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

class Config:
    "class config"
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app.config.from_object(Config)

babel = Babel(app)

def get_user():
    "get user"
    user_id = request.args.get('login_as', type=int)
    if user_id is None or user_id not in users:
        return None
    return users[user_id]

@app.before_request
def before_request():
    "before"
    g.user = get_user()

@babel.localeselector
def get_locale():
    "Select the best language based on the user's locale, request, and headers."
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    if g.user and g.user['locale'] and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']
    return (request.accept_languages.best_match(app.config['LANGUAGES']) or
            app.config['BABEL_DEFAULT_LOCALE'])

@babel.timezoneselector
def get_timezone():
    "Select the best timezone based on the user's timezone, request, and headers."
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
    return render_template('7-index.html')

if __name__ == "__main__":
    app.run(debug=True)
