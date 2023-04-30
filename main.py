from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
import unittest
from app import create_app
from app.firestore_service import get_users, get_todos
from app.firestore_service import *
from flask_login import login_required

app = create_app()


app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

    
@app.errorhandler(404)

def not_found(error):
    return render_template('404.html', error = error)

@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip
    return response


@app.route('/hello', methods=['GET'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = session.get('username')

    context = {
        'user_ip': user_ip,
        'todos' : get_todos(user_id = username),
        'username': username
    }

    return render_template('hello.html', **context)


if __name__ == '__main__':
    app.debug = True
    app.run(port=5003)
