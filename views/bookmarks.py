from flask import Response, request
from flask_restful import Resource
from models import Bookmark, db, Post
import json
from . import can_view_post
import flask_jwt_extended



def user_follows(current_user):
    # query the "following" table to get the list of authorized users:
    bookmark_ids = (
        db.session
            .query(Bookmark.id)
            .filter(Bookmark.user_id == current_user.id)
            .order_by(Bookmark.id)
            .all()
    )
    # convert to a list of ints:
    user_ids = [id for (id,) in bookmark_ids]
    return user_ids


class BookmarksListEndpoint(Resource):

    @flask_jwt_extended.jwt_required()
    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def get(self):
        # Your code here

        b = user_follows(self.current_user)
        bookmarks = Bookmark.query.filter(Bookmark.id.in_(b))
        data = [
            item.to_dict() for item in bookmarks.all()
        ]
        return Response(json.dumps(data), mimetype="application/json", status=200)

    @flask_jwt_extended.jwt_required()
    def post(self):


        body = request.get_json()
        post_id = body.get('post_id')
        if not post_id:
            return Response(json.dumps({'message': 'Invalid query'}), mimetype="application/json", status=400)

        try:
            post = Post.query.get(post_id)

        
            if post:

                if can_view_post(post_id, self.current_user):
            

                    bookmark = Bookmark(self.current_user.id, post_id)
                    db.session.add(bookmark)
                    # commit changes:
                    db.session.commit()        
                    return Response(json.dumps(bookmark.to_dict()), mimetype="application/json", status=201)
                else:
                    return Response(json.dumps({'message': 'No access'}), mimetype="application/json", status=404)
            else:
                return Response(json.dumps({'message': 'Error post with that ID does not exist'}), mimetype="application/json", status=404)
        except:
            return Response(json.dumps({'message': 'Invalid query'}), mimetype="application/json", status=400)
        

class BookmarkDetailEndpoint(Resource):

    @flask_jwt_extended.jwt_required()
    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def delete(self, id):

        bookmark = Bookmark.query.get(id)
        
        if bookmark.user_id != self.current_user.id:
            return Response(json.dumps({'message': 'Error you do not have access to this'}), mimetype="application/json", status=404)
        
        if bookmark:
            
            Bookmark.query.filter_by(id=id).delete()
            db.session.commit()
            serialized_data = {
                'message': 'Bookmark {0} successfully deleted.'.format(id)
            }
            return Response(json.dumps(serialized_data), mimetype="application/json", status=200)

        else:
            return Response(json.dumps({'message': 'Error bookmark with that ID does not exist'}), mimetype="application/json", status=404)



def initialize_routes(api):
    api.add_resource(
        BookmarksListEndpoint, 
        '/api/bookmarks', 
        '/api/bookmarks/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )

    api.add_resource(
        BookmarkDetailEndpoint, 
        '/api/bookmarks/<id>', 
        '/api/bookmarks/<id>',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
