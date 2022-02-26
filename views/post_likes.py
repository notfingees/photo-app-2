from flask import Response
from flask_restful import Resource
from models import LikePost, db, Post
import json
from . import can_view_post, get_authorized_user_ids

class PostLikesListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def post(self, post_id):
        # Your code here
        try:
            user_id = self.current_user.id # id of the user who is logged in
            
            # create post:

            post = Post.query.get(post_id)
            if not post:
                return Response(json.dumps({'message': 'Invalid post ID'}), mimetype="application/json", status=404)

            ids_for_me_and_my_friends = get_authorized_user_ids(self.current_user)
            if can_view_post(post_id, self.current_user):

                newLike = LikePost(user_id, post_id)
                
                try:
                    db.session.add(newLike)
                    db.session.commit()
                    return Response(json.dumps(newLike.to_dict()), mimetype="application/json", status=201)


                except:
                    return Response(json.dumps({'message': 'Like already exists'}), mimetype="application/json", status=400)
            else:
                return Response(json.dumps({'message': 'You do not have access to this post'}), mimetype="application/json", status=404)
            
      
        except Exception as e:
            print("error in post likes", e)
            return Response(json.dumps({'message': 'Invalid query'}), mimetype="application/json", status=400)
        
            

class PostLikesDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, post_id, id):

        try:
            comment = LikePost.query.get(id)

            if not comment:
                return Response(json.dumps({'message': 'Error comment with that ID does not exist'}), mimetype="application/json", status=404)
            
            if comment.user_id != self.current_user.id:
                return Response(json.dumps({'message': 'Error you do not have access to this'}), mimetype="application/json", status=404)
            
            if comment:
                
                LikePost.query.filter_by(id=id).delete()
                db.session.commit()
                serialized_data = {
                    'message': 'Like {0} successfully deleted.'.format(id)
                }
                return Response(json.dumps(serialized_data), mimetype="application/json", status=200)

            else:
                return Response(json.dumps({'message': 'Error comment with that ID does not exist'}), mimetype="application/json", status=404)

        except:
            return Response(json.dumps({'message': 'Invalid query'}), mimetype="application/json", status=400)
        
        # Your code here
        



def initialize_routes(api):
    api.add_resource(
        PostLikesListEndpoint, 
        '/api/posts/<post_id>/likes', 
        '/api/posts/<post_id>/likes/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )

    api.add_resource(
        PostLikesDetailEndpoint, 
        '/api/posts/<post_id>/likes/<id>', 
        '/api/posts/<post_id>/likes/<id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
