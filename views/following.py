from flask import Response, request
from flask_restful import Resource
from models import Following, User, db
import json

def get_path():
    return request.host_url + 'api/posts/'

def user_follows(current_user):
    # query the "following" table to get the list of authorized users:
    user_ids_tuples = (
        db.session
            .query(Following.following_id)
            .filter(Following.user_id == current_user.id)
            .order_by(Following.following_id)
            .all()
    )
    # convert to a list of ints:
    user_ids = [id for (id,) in user_ids_tuples]
    return user_ids




class FollowingListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        try:
            following_ids = (
            db.session
                .query(Following.id)
                .filter(Following.user_id == self.current_user.id)
                .order_by(Following.id)
                .all()
            )
            # convert to a list of ints:
            fids = [id for (id,) in following_ids]

            
            data = []

            # Your code here
            following = user_follows(self.current_user)
            users = User.query.filter(User.id.in_(following))
            index = 0
            for item in fids:
                temp = {}
                temp['id'] = item
                temp['following'] = users.all()[index].to_dict()
                data.append(temp)
                index += 1


        #   data = [
        #       item.to_dict() for item in users.all()
        #   ]

            
            return Response(json.dumps(data), mimetype="application/json", status=200)
        except Exception as e:
            print("error in following get", e)
    def post(self):
        body = request.get_json()
        
        try:
            following_user_id = body.get('user_id')

            if not following_user_id:
                return Response(json.dumps({'message': 'Invalid query'}), mimetype="application/json", status=400)


            follow = User.query.get(following_user_id)
            if not follow:
                return Response(json.dumps({'message': 'User does not exist'}), mimetype="application/json", status=404)

            user_id = self.current_user.id # id of the user who is logged in
            
            # create post:

            temp = {}
            
            follow_record = Following(user_id, following_user_id)
            db.session.add(follow_record)
            db.session.commit()
            temp['id'] = follow_record.id
            temp['following'] = (self.current_user).to_dict()
            print("FOLLOWING id is", temp['id'])
            print("follower follower is", temp['following'])
            print("temp is", temp)

            return Response(json.dumps(temp), mimetype="application/json", status=201)

            # Your code here
        except Exception as e:
            print("in following wtih error as ", e)
            return Response(json.dumps({'message': 'Invalid query'}), mimetype="application/json", status=400)
        
       


class FollowingDetailEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, id):

        try:
        
            following_record = Following.query.get(id)

            if not following_record:
                return Response(json.dumps({'message': 'Error follow record with that ID does not exist'}), mimetype="application/json", status=404)
            
            if following_record.user_id != self.current_user.id:
                return Response(json.dumps({'message': 'Error you do not have access to this'}), mimetype="application/json", status=404)
            
            if following_record:
                
                Following.query.filter_by(id=id).delete()
                db.session.commit()
                serialized_data = {
                    'message': 'Following record {0} successfully deleted.'.format(id)
                }
                return Response(json.dumps(serialized_data), mimetype="application/json", status=200)

            else:
                return Response(json.dumps({'message': 'Error following record with that ID does not exist'}), mimetype="application/json", status=404)

            
        except:
            return Response(json.dumps({'message': 'Invalid query'}), mimetype="application/json", status=400)
        

def initialize_routes(api):
    api.add_resource(
        FollowingListEndpoint, 
        '/api/following', 
        '/api/following/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
    api.add_resource(
        FollowingDetailEndpoint, 
        '/api/following/<id>', 
        '/api/following/<id>/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
