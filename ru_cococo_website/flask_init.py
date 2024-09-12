from flask import Flask, session, request


def get_locale():
    session['language'] = request.accept_languages.best_match(['ru', 'en'])
    # session['lang'] = 'ru'
    return session.get('language', 'ru')


website = Flask(__name__)
# configure secret key for sessions
website.secret_key = 'H*&g*G*G8yGy8g87g87g8yG8^&TG7tyf7G0JUG5e6%F%^er8yuh0j'