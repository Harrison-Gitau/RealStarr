from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    from app.models import Post, User
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/posts/', methods=['POST', 'GET'])
    def posts():
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            if name:
                post = Post(name=name)
                post.save()
                response = jsonify({
                    'id': post.id,
                    'name': post.name,
                    'message': post.message,
                    'date_created': post.date_created,
                    'date_modified': post.date_modified,
                })
                response.status_code = 201
                return response
        else:
            #GET
            posts = Post.get_all()
            results = []

            for post in posts:
                obj = {
                    'id': post.id,
                    'name': post.name,
                    'message': post.message,
                    'date_created': post.date_created,
                    'date_modified': post.date_modified
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/posts/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def post_manipulation(id, **kwargs):
        # retrieve a post using its id
        post = Post.query.filter_by(id=id).first()
        if not post:
            # Raise an HTTPexception error with a 404 not found status code
            abort(404) 

        if request.method == 'DELETE':
            post.delete()
            return {
            "message": "post {} deleted successfully".format(post.id)
            }, 200

        elif request.method == 'PUT':
            name = str(request.data.get('name', ''))
            post.name = name
            post.save()
            response = jsonify({
                'id': post.id,
                'name': post.name,
                'message': post.message,
                'date_created': post.date_created,
                'date_modified': post.date_modified
            })

            response.status_code = 200
            return response
        else:

            # GET
            response = jsonify({
                'id': post.id,
                'name': post.name,
                'message': post.message,
                'date_created': post.date_created,
                'date_modified': post.date_modified

            })
            response.status_code = 200
            return response

    # Import the authentication blueprint and register it on the app
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
