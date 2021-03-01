import os
from datetime import timedelta

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://teda:m0n0w4ll@192.168.5.8/tims'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = os.urandom(64)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_USERNAME'] = 'teda@opa-group.com'
app.config['MAIL_PASSWORD'] = 'ARQ*X!bz9Rv!Bh'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

api = Api(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)
mail = Mail(app)

from _api.blacklist import BLACKLIST

from _api.resources.account import Login, AccountList, ProfileUpdate, Logout
from _api.resources.log import LogUnknownList, ViewImage
from _api.resources.news import NewsList


#  region Region JWT function
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


@jwt.user_claims_loader
def add_claims_go_jwt(identity):
    if identity == 1:
        return {"is_admin": True}

    return {"is_admin": False}


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify(
        {
            "description": "The token has expired.",
            "error": "token_expired"
        }
    ), 401


@jwt.invalid_token_loader
def invalid_token_callback():
    return jsonify(
        {
            "description": "Signature verification failed.",
            "error": "invalid_token"
        }
    ), 401


@jwt.unauthorized_loader
def missing_token_callback():
    return jsonify(
        {
            "description": "Request does not contain an access token.",
            "error": "authorization_required"
        }
    ), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify(
        {
            "description": "The token is not fresh.",
            "error": "fresh_token_required"
        }
    ), 401


@jwt.revoked_token_loader
def revoke_token_callback():
    return jsonify(
        {
            "description": "The token has been revoked.",
            "error": "token_revoked"
        }
    ), 401


#  endregion


# region account
api.add_resource(Login, '/api/account/login')
api.add_resource(Logout, '/api/account/logout')
api.add_resource(AccountList, '/api/account/list')
api.add_resource(ProfileUpdate, '/api/profile/update')
# endregion

# region log_unknown
api.add_resource(LogUnknownList, '/api/log_unknown/list')
api.add_resource(ViewImage, '/api/view/image')
# endregion

# region news
api.add_resource(NewsList, '/api/news/list')
# endregion
