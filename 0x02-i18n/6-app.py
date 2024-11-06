#!/usr/bin/env python3
"Basic Babel setup with user login emulation"

from flask import Flask, render_template, request, g
from flask_babel import Babel
from typing import Optional, Dict

app = Flask(__name__)


users: Dict[int, Dict[str, Optional[str]]] = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)

babel = Babel(app)


def get_user() -> Optional[Dict[str, Optional[str]]]:
    """Returns a user dictionary or None if no user is found"""
    user_id = request.args.get('login_as', type=int)
    if user_id is None or user_id not in users:
        return None
    return users[user_id]


@app.before_request
def before_request() -> None:
    """Sets the global user before each request"""
    g.user = get_user()


@babel.localeselector
def get_locale() -> str:
    """Returns the best locale according to the user preferences"""
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user.get('locale')
    locale = request.accept_languages.best_match(app.config['LANGUAGES'])
    if locale:
        return locale
    return app.config['BABEL_DEFAULT_LOCALE']


@app.context_processor
def inject_locale():
    """Inject get_locale into templates."""
    return dict(get_locale=get_locale)


@app.route('/')
def index() -> str:
    """Renders the index page"""
    return render_template('5-index.html')


if __name__ == "__main__":
    app.run(debug=True)
