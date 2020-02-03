#API endpoints
from flask_restful import Resource, reqparse

#methods to work with tokens
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

#initialising parser and adding required parameters
parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

from models import UserModel

class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()#parsing of incoming data from POST

        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'. format(data['username'])}
            
        #create a new user with UserModel taking params username and password 
        #eturn access tokens on success   
        new_user = UserModel(
            username = data['username'],
            password = UserModel.generate_hash(data['password'])
        )
        try:
            new_user.save_to_db()
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'User {} was created'.format( data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        except:
            return {'message': 'Something went wrong'}, 500

class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()#parsing of incoming data from POST
        current_user = UserModel.find_by_username(data['username'])#do a lookup by username
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}
        
        #return access tokens on success
        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        else:
            return {'message': 'Wrong credentials'}
      
      
class UserLogoutAccess(Resource):
    def post(self):
        return {'message': 'User logout'}
      
      
class UserLogoutRefresh(Resource):
    def post(self):
        return {'message': 'User logout'}
      
      
class TokenRefresh(Resource):
    @jwt_refresh_token_required#can only access path with refresh token
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}
      
      
class AllUsers(Resource):
    def get(self):
        return UserModel.return_all()
    
    def delete(self):
        return UserModel.delete_all()


class SecretResource(Resource):
    @jwt_required #now the request header must have JWT
    def get(self):
        return {
            'answer': 42
        }
