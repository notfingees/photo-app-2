from flask import Response, request
from flask_restful import Resource
from . import can_view_post
import json
from models import db, Comment, Post

class CommentListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def post(self):
        # Your code here

        body = request.get_json()
        post_id = body.get('post_id')
        text = body.get('text')
        user_id = self.current_user.id # id of the user who is logged in

        try:

            post = Post.query.get(post_id)
            if not post:
                return Response(json.dumps({'message': 'Invalid post ID'}), mimetype="application/json", status=404)
        
        # create post:
            if can_view_post(post_id, self.current_user):
                comment = Comment(text, user_id, post_id) 
                db.session.add(comment)
                db.session.commit()
                return Response(json.dumps(comment.to_dict()), mimetype="application/json", status=201)
            else:
                return Response(json.dumps({'message': 'No access'}), mimetype="application/json", status=404)

        except:
            return Response(json.dumps({'message': 'Invalid query'}), mimetype="application/json", status=400)
        

        
class CommentDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
  
    def delete(self, id):

        try:
            
            comment = Comment.query.get(id)

            if not comment:
                return Response(json.dumps({'message': 'Error comment with that ID does not exist'}), mimetype="application/json", status=404)
            
            if comment:

                if comment.user_id == self.current_user.id:
                    Comment.query.filter_by(id=id).delete()
                    db.session.commit()
                    serialized_data = {
                        'message': 'Comment {0} successfully deleted.'.format(id)
                    }
                    return Response(json.dumps(serialized_data), mimetype="application/json", status=200)
                else:
                    return Response(json.dumps({'message': 'You cant access that data'}), mimetype="application/json", status=404)


        except:
            return Response(json.dumps({'message': 'Invalid query'}), mimetype="application/json", status=400)
        

def initialize_routes(api):
    api.add_resource(
        CommentListEndpoint, 
        '/api/comments', 
        '/api/comments/',
        resource_class_kwargs={'current_user': api.app.current_user}

    )
    api.add_resource(
        CommentDetailEndpoint, 
        '/api/comments/<id>', 
        '/api/comments/<id>',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
