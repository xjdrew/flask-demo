# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask import request, Response

from functools import wraps

app = Flask(__name__)

def check_auth(username, password):
    return username == 'xjdrew' and password == 'test1234'

def authenticate():
    '''Sends a 401 response that enables basic auth'''
    return Response('访问该页面需要授权',
            401, {'WWW-Authenticate': 'Basic realm="Login Requied"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    return 'index page'

@app.route("/about/")
def about():
    return "about page"

@app.route('/hello/')
@app.route('/hello/<name>')
@requires_auth
def hello_world(name = None):
    login_name = request.authorization.username
    return render_template('hello.html', name = name, login_name = login_name)

if __name__ == '__main__':
    app.debug = True
    app.run(port=3888)


