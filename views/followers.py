from flask import Response, request
from flask_restful import Resource
from models import db, Following, User
import json
import flask_jwt_extended



def get_path():
    return request.host_url + 'api/posts/'


def user_followers(current_user):
    # query the "following" table to get the list of authorized users:
    user_ids_tuples = (
        db.session
            .query(Following.user_id)
            .filter(Following.following_id == current_user.id)
            .order_by(Following.user_id)
            .all()
    )
    # convert to a list of ints:
    user_ids = [id for (id,) in user_ids_tuples]
    return user_ids

class FollowerListEndpoint(Resource):
    @flask_jwt_extended.jwt_required()
    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def get(self):

        try:

            following_ids = (
                db.session
                .query(Following.id)
                .filter(Following.following_id == self.current_user.id)
                .order_by(Following.id)
                .all()
                )
                # convert to a list of ints:
            fids = [id for (id,) in following_ids]

                
            data = []

            # Your code here
            following = user_followers(self.current_user)
            users = User.query.filter(User.id.in_(following))
            index = 0
            for item in fids:
                temp = {}
                temp['id'] = item
                temp['follower'] = users.all()[index].to_dict()
                data.append(temp)
                index += 1

            return Response(json.dumps(data), mimetype="application/json", status=200)
        except Exception as e:
            print("eRROR in followers.py", e)

def initialize_routes(api):
    api.add_resource(
        FollowerListEndpoint, 
        '/api/followers', 
        '/api/followers/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
