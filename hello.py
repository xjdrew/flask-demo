# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask import session
from flask import request, Response, make_response
from flask import jsonify
from flask import json

from functools import wraps
from db import Server
from db import db_session

app = Flask(__name__)
app.secret_key = '!!!!!!!315gqaaga'

def check_auth(username, password):
    return username == 'xjdrew' and password == 'test123'

def authenticate():
    '''Sends a 401 response that enables basic auth'''
    return Response('访问该页面需要授权',
            401, {'WWW-Authenticate': 'Basic realm="Login Requied"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            # app.logger.debug("need authenticate")
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    if not 'username' in session:
        session['username'] = 'xjdrew'
    return session['username'] or __name__

@app.route("/about/")
def about():
    return "about page"

@app.route('/hello/')
@app.route('/hello/<name>')
@requires_auth
def hello_world(name = None):
    login_name = request.authorization.username
    return render_template('hello.html', name = name, login_name = login_name)

@app.route('/json/')
def json_data():
    a = {}
    a["name"] = "xjdrew"
    a["area"] = "gz.china"
    a["month"] = 12
    a["members"] = ["tracy", "esther"]
    b = {}
    b[0] = 10
    b[1] = 20
    b['a'] = a
    c = [1,2,3,4]
    # return app.response_class(json.dumps(b, indent = 2), mimetype='application/json')
    # return jsonify(b)
    return Response(json.dumps(b, indent = 2), mimetype='application/json') 

ret = []
@app.route('/static_servers/')
def static_servers():
    return Response(json.dumps(ret, indent = 2), mimetype='application/json') 

@app.route('/servers/')
def servers():
    ret = []
    for server in db_session.query(Server):
        ret.append({'ip':server.ip, 'name':server.name})
        if len(ret) > 100:
            break

    #return Response(json.dumps(ret, indent = 2), mimetype='application/json') 
    return Response('[]', mimetype='application/json') 

@app.route('/file')
def file():
    with app.open_resource('server_list.txt') as f:
        resp = make_response(f.read())
        resp.headers['Content-type'] = 'application/octet-stream'
        resp.headers['Content-Disposition'] = 'attachment; filename="test.txt"'
    return resp

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    for server in db_session.query(Server):
        ret.append({'ip':server.ip, 'name':server.name})
        if len(ret) > 100:
            break

    app.debug = True
    app.run(port=3888)


