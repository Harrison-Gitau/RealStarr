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

class LoginView(MethodView):
    """This class based view handles user login and access token generation"""
    def post(self):
        """Handle post request for this view. Url --> /auth/login"""
        try:
            # get the user object using their email ( unique to every user )
            user = User.query.filter_by(email=request.data['email']).first()

            # try to authenticate the found user using their password
            if user and user.password_is_valid(request.data['password']):
                # generate the access token. this will be used as the authorization header
                access_token = user.generate_token(user.id)
                if access_token:
                    response = {
                        'message': 'You logged in successfully',
                        'access_token': access_token.decode()
                    }
                    return make_response(jsonify(response)), 200

                else:
                    # user doesn't exist so we return an error
                    response = {
                        'message': 'Invalid email or password. Please try again'
                    }
                    return make_response(jsonify(response)), 401

        except Exception as e:
            response = {
                'message': str(e)
            }
            # return a server error using the HTTP Error code 500 (internal server error)
            return make_response(jsonify(response)), 500
                
registration_view  = RegistrationView.as_view('register_view')
login_view = LoginView.as_view('login_view')
# Define the rule for registration url --> /auth/register
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST'])

# define the rule for login url --> /auth/login
# then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)

