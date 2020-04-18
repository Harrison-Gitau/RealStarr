import json
from flask_api import FlaskAPI, status
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response

# local import
from instance.config import app_config

# for password hashing
from flask_bcrypt import Bcrypt

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):

    from app.models import Post, User

    app = FlaskAPI(__name__, instance_relative_config=True)

    # overriding werkzeugs built-in password hashing utilities using Bcrypt
    bcrypt = Bcrypt(app)


    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/posts/', methods=['POST', 'GET'])
    def posts():
        # get the access token
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                if request.method == "POST":
                    name = str(request.data.get('name', ''))
                    if name:
                        post = Post(name=name, created_by=user_id)
                        post.save()
                        response = jsonify({
                            'id': post.id,
                            'name': post.name,
                            'message': post.message,
                            'date_created': post.date_created,
                            'date_modified': post.date_modified,
                            'created_by': user_id
                        })
                        return make_response(response), 201
                else:
                    #GET
                    posts = Post.get_all(user_id)
                    results = []

                    for post in posts:
                        obj = {
                            'id': post.id,
                            'name': post.name,
                            'message': post.message,
                            'date_created': post.date_created,
                            'date_modified': post.date_modified,
                            'created_by': post.created_by
                        }
                        results.append(obj)

                    return make_response(jsonify(response)), 200
            else:
                # User is not legit so the payload is an error
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

    @app.route('/posts/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def post_manipulation(id, **kwargs):

        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):

                # retrieve a post using its id
                post = Post.query.filter_by(id=id).first()
                if not post:
                    # Raise an HTTPexception error with a 404 not found status code
                    abort(404) 

                if request.method == 'DELETE':
                    post.delete()
                    return {
                    "message": "post {} deleted".format(post.id)
                    }, 200

                elif request.method == 'PUT':
                    name = str(request.data.get('name', ''))
                    post.name = name
                    post.save()
                    response = {
                        'id': post.id,
                        'name': post.name,
                        'message': post.message,
                        'date_created': post.date_created,
                        'date_modified': post.date_modified,
                        'created_by': post.created_by
                    }

                    return make_response(jsonify(response)), 200
                else:

                    # GET
                    response = jsonify({
                        'id': post.id,
                        'name': post.name,
                        'message': post.message,
                        'date_created': post.date_created,
                        'date_modified': post.date_modified,
                        'created_by': post.created_by

                    })
                    return make_response(response), 200

    # Import the authentication blueprint and register it on the app
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
