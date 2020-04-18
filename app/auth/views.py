from . import auth_blueprint

from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User

class RegistrationView(MethodView):
    """This class registers a new user."""

    def post(self):
        """Handle POST request for the view. url --> /auth/register"""

        # Query to see if the user exists
        user = User.query.filter_by(email=request.data['email']).first()

        if not user:
            # There is no user so we try and register them
            try:
                post_data = request.data
                # Register the user
                email = post_data['email']
                password = post_data['password']
                user = User(email=email, password = password)
                user.save()

                response = {
                    'message': 'You registered successfully. Please Log in'
                }
                return make_response(jsonify(response)), 201
            except Exception as e:
                # An error occured so return a string message containing the error
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
            else:
                # There is an existing user. We dont want to register users twice
                # Return a message to the user telling them that they already exist
                response = {
                    'message': 'User already exists. Please login'
                }
                return make_response(jsonify(response)), 202

registration_view  = RegistrationView.as_view('register_view')
# Define the rule for registration url --> /auth/register
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods = ['POST']
)

