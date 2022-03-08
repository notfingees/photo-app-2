
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS
from flask import render_template
import os
from models import db, User, ApiNavigator
from views import bookmarks, comments, followers, following, \
    posts, profile, stories, suggestions, post_likes

import flask_jwt_extended  
import decorators

# new views:
from views import authentication, token


app = Flask(__name__)


#JWT config variables and manager (add after app object created):
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET')
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
app.config["JWT_COOKIE_SECURE"] = False
jwt = flask_jwt_extended.JWTManager(app)

# Initialize routes of 2 new views




    
# CORS: allows anyone from anywhere to use your API:
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False    


db.init_app(app)
api = Api(app)

# set logged in user

  #  with app.app_context():
   #     app.current_user = User.query.filter_by(id=flask_jwt_extended.current_user).one()


# Initialize routes for all of your API endpoints:
bookmarks.initialize_routes(api)
comments.initialize_routes(api)
followers.initialize_routes(api)
following.initialize_routes(api)
posts.initialize_routes(api)
post_likes.initialize_routes(api)
profile.initialize_routes(api)
stories.initialize_routes(api)
suggestions.initialize_routes(api)

authentication.initialize_routes(app)
token.initialize_routes(api)

# Server-side template for the homepage:

ignore = '''
@jwt.unauthorized_loader
def custom_unauthorized_response(_err):
    print("in custom unauthorized response")
    return render_template(
            'login.html', 
            message='Please log in'
            )
'''

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    # print('JWT data:', jwt_data)
    # https://flask-jwt-extended.readthedocs.io/en/stable/automatic_user_loading/
    user_id = jwt_data["sub"]
    user = User.query.filter_by(id=user_id).one_or_none()
    return user

@app.route('/')
@flask_jwt_extended.jwt_required()
def home():

    user = flask_jwt_extended.get_jwt_identity()
    print("USER IS get jwt identity", user)
    if user:
        print("user is", user)
        print("flask_jwt_extended.current_user is", flask_jwt_extended.current_user)
        return render_template(
            'starter-client.html', 
            user=flask_jwt_extended.current_user
        )
    else:
        return render_template(
            'login.html', 
            message='Please log in'
            )

# Updated API endpoint includes a reference to 
# access_token and csrf token.
@app.route('/api')
@decorators.jwt_or_login
@flask_jwt_extended.jwt_required()
def api_docs():
    user = flask_jwt_extended.get_jwt_identity()
    print("user is", user)
    if user:
        print("USER IS TRUE")
        access_token = request.cookies.get('access_token_cookie')
        print("after access_token")
        csrf = request.cookies.get('csrf_access_token')
        print("after csrf")
        navigator = ApiNavigator(flask_jwt_extended.current_user)
        print("after navigator")
        rt = render_template(
            'api/api-docs.html', 
            user=flask_jwt_extended.current_user,  #TODO: change to flask_jwt_extended.current_user
            endpoints=navigator.get_endpoints(),
            access_token=access_token,
            csrf=csrf,
            url_root=request.url_root[0:-1] # trim trailing slash
        )
        print("render template is", rt)
        return rt
    else:
        return render_template(
            'login.html', 
            message='Please log in'
            )
    



# enables flask app to run using "python3 app.py"
if __name__ == '__main__':
    app.run()
