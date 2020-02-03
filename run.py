#register endpoints inside the app
from flask import Flask
from flask_restful import Api #initialises the APIs
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager #json web token

app = Flask(__name__)
api = Api(app)

#SQLAlchemy configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'
db = SQLAlchemy(app)

#JWT secret key and initialisation
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

#blacklisting configuration
app.config['JWT_BLACKLIST_ENABLED'] = True #enable it
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh'] #will check access and refresh tokens

import views, models, resources

api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/secret')

#creates necessary tables in DB
@app.before_first_request
def create_tables():
    db.create_all()

#called every time client try to access secured endpoints
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti) #should return boolean