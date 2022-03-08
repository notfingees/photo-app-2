from models import User, db
import flask_jwt_extended
from flask import Response, request
from flask_restful import Resource
import json
from datetime import timezone, datetime, timedelta


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

class AccessTokenEndpoint(Resource):

    def post(self):
        body = request.get_json() or {}
        print(body)
        username = body.get('username')
        password = body.get('password')

        user_id = get_if_user_exists(username, password)
        
        if user_id != None:
            print("user exists")
            access_token = flask_jwt_extended.create_access_token(identity=user_id)
            refresh_token = flask_jwt_extended.create_refresh_token(identity=user_id)

            # Set the JWT cookies in the response

            return Response(json.dumps({ 
            "access_token": access_token, 
            "refresh_token": refresh_token
            }), mimetype="application/json", status=200)



        else:
            return Response(json.dumps({ 
            "access_token": "???", 
            "refresh_token": "???"
            }), mimetype="application/json", status=401)

        
        # check username and log in credentials. If valid, return tokens
        
@flask_jwt_extended.jwt_required()
def generate_new_token(refresh_token):
    ignore = '''
    decoded_token = flask_jwt_extended.decode_token(refresh_token)
    flask_jwt_extended.set_access_cookies({"login": True}, access_token)
    flask_jwt_extended.set_refresh_cookies({"login": True}, refresh_token) 
    print("decoded token is", decoded_token)
    '''
    
    access_token = flask_jwt_extended.create_access_token(identity=flask_jwt_extended.get_jwt_identity())
    flask_jwt_extended.set_access_cookies({"login": True}, access_token)
    #flask_jwt_extended.set_access_cookies(response, access_token)

    return access_token
   # return response


class RefreshTokenEndpoint(Resource):

    @flask_jwt_extended.jwt_required()
    def generate_new_token(refresh_token):
        decoded_token = flask_jwt_extended.decode_token(refresh_token)
        access_token = flask_jwt_extended.create_access_token(identity=flask_jwt_extended.get_jwt_identity())
        #flask_jwt_extended.set_access_cookies(response, access_token)

        return access_token

    
    
    def post(self):

        body = request.get_json() or {}
        refresh_token = body.get('refresh_token')
        print(refresh_token)

       # https://flask-jwt-extended.readthedocs.io/en/latest/refreshing_tokens/
       # Hint: To decode the refresh token and see if it expired:
        try:
            decoded_token = flask_jwt_extended.decode_token(refresh_token)
            print("decoded token is", decoded_token)
            exp_timestamp = decoded_token.get("exp")
            current_timestamp = datetime.timestamp(datetime.now(timezone.utc))
            if current_timestamp > exp_timestamp:
                # token has expired:
                return Response(json.dumps({ 
                        "message": "refresh_token has expired"
                    }), mimetype="application/json", status=401)
            else:
                # issue new token:
                #access_token = flask_jwt_extended.create_access_token(identity=flask_jwt_extended.get_jwt_identity())
                new_generated_token = self.generate_new_token(refresh_token)
                #print("new generated token is", new_generated_token)

                r = Response(json.dumps({ 
                        "access_token": new_generated_token
                    }), mimetype="application/json", status=200)
                return r

                #return generate_new_token(refresh_token)
        except Exception as e:
            print(e)
            return Response(json.dumps({"message": "error"}), mimetype="application/json", status=400)

#        return Response(json.dumps({ 
 #               "access_token": "new access token goes here"
  #          }), mimetype="application/json", status=200)
        


def initialize_routes(api):
    api.add_resource(
        AccessTokenEndpoint, 
        '/api/token', '/api/token/'
    )

    api.add_resource(
        RefreshTokenEndpoint, 
        '/api/token/refresh', '/api/token/refresh/'
    )