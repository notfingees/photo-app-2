from flask import (
    request, make_response, render_template, redirect, Response, jsonify
)
from models import User, db
import flask_jwt_extended

def get_if_user_exists(username, password):
    sql = '''
        SELECT id
        FROM users
        WHERE username = '{username}' AND password_plaintext = '{password}'
        
    '''.format(username=username, password=password)
    rows = list(db.engine.execute(sql))
    if len(rows) > 0:
        return rows[0][0]
    else:
        return None

import json

def logout():
    # hint:  https://dev.to/totally_chase/python-using-jwt-in-cookies-with-a-flask-app-and-restful-api-2p75

    resp = make_response(redirect('/login', 302))
    flask_jwt_extended.unset_jwt_cookies(resp)
    return resp

def login():
    if request.method == 'POST':
        # authenticate user here. If the user sent valid credentials, set the
        # JWT cookies:
        # https://flask-jwt-extended.readthedocs.io/en/3.0.0_release/tokens_in_cookies/

        print(request)
        print(type(request))
        
        username = request.form['username']
        password = request.form['password']


        user_id = get_if_user_exists(username, password)
        
        if user_id != None:
            print("user exists")
            access_token = flask_jwt_extended.create_access_token(identity=user_id)
            refresh_token = flask_jwt_extended.create_refresh_token(identity=user_id)

            # Set the JWT cookies in the response

            resp = make_response(redirect('/', 302))
            flask_jwt_extended.set_access_cookies(resp, access_token)
            flask_jwt_extended.set_refresh_cookies(resp, refresh_token)

            return resp

        else:
            return render_template(
            'login.html', 
            message='Invalid password'
            )


        
        

        #return resp, 200
        

        
    else:
        return render_template(
            'login.html'
        )   

def initialize_routes(app):
    app.add_url_rule('/login', 
        view_func=login, methods=['GET', 'POST'])
    app.add_url_rule('/logout', view_func=logout)