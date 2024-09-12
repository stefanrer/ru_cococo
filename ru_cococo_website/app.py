from flask import redirect, request, render_template, jsonify, session
from flask_init import website, get_locale
from Backend.search import search


@website.route('/')
def hi():
    if 'language' not in session:
        session['language'] = get_locale()
    return redirect('main')


@website.route('/error')
def error():
    print("error")
    return redirect('main')


@website.route('/main')
def main():
    if 'language' not in session:
        session['language'] = get_locale()
    return render_template('main.html', lang=session['language'])


@website.route('/about')
def about():
    if 'language' not in session:
        session['language'] = get_locale()
    return render_template('about.html', lang=session['language'])


@website.route('/public/api/search', methods=['GET'])
def sql_search():
    return search(query=request.args)


@website.route('/change_lang/<current_lang>')
def set_language(current_lang):
    if current_lang in ["en", "ru"]:
        session['language'] = "ru" if current_lang == 'en' else "en"
        return jsonify(success=True)  # Return JSON success response
    else:
        return jsonify(success=False)


if __name__ == "__main__":
    website.run(host='0.0.0.0', port=15555, debug=True)

