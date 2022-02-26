from flask import Response, request
from flask_restful import Resource
from models import User, db, Following
from . import get_authorized_user_ids
import json

def get_user_not_following(current_user):
    # query the "following" table to get the list of authorized users:
    user_ids_tuples = (
        db.session
            .query(Following.following_id)
            .filter(Following.user_id == current_user.id)
            .order_by(Following.following_id)
            .all()
    )
    # convert to a list of ints:
    user_id_follows = get_authorized_user_ids(current_user)

    user_ids_tuples_2 = (
        db.session
            .query(User.id)
            .order_by(User.id)
            .all()
    )
    # convert to a list of ints:
    
    user_id_all = [id for (id,) in user_ids_tuples_2]

    print("user_id_follows is", user_id_follows)
    print("user_id_all is", user_id_all)


    user_not_following = list(set(user_id_all).difference(user_id_follows))

    print("user not following is", user_not_following)

    
    return user_not_following

class SuggestionsListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        # Your code here:
        not_following = get_user_not_following(self.current_user)
        users = User.query.filter(User.id.in_(not_following))
        #print(users)
        users = users.order_by(User.id.desc()).limit(7)
        data = [
            item.to_dict() for item in users.all()
        ]
        return Response(json.dumps(data), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        SuggestionsListEndpoint, 
        '/api/suggestions', 
        '/api/suggestions/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
