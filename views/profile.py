from flask import Response, request
from flask_restful import Resource
import json
from models import db, User
import flask_jwt_extended

def get_path():
    return request.host_url + 'api/posts/'

class ProfileDetailEndpoint(Resource):

    @flask_jwt_extended.jwt_required()
    def __init__(self, current_user):
        self.current_user = current_user
    @flask_jwt_extended.jwt_required()
    def get(self):
        # Your code here:

        profile = User.query.filter(User.id.in_([self.current_user.id]))
        data = [
            item.to_dict() for item in profile.all()
        ]
        print("DATA in get profile is", data)

        return Response(json.dumps(data[0]), mimetype="application/json", status=200)

        
        #return Response(json.dumps({}), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        ProfileDetailEndpoint, 
        '/api/profile', 
        '/api/profile/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
