from flask import send_file
from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity
from flask_restful import Resource

from _api.global_func import global_parser
from _api.models.log_unknown import LogUnknownM


class LogUnknownList(Resource):
    @classmethod
    @jwt_refresh_token_required
    def get(cls):
        account_id = get_jwt_identity()
        print(account_id)

        data = [x.json() for x in LogUnknownM.list_all()]
        return data, 200


class ViewImage(Resource):
    @classmethod
    def get(cls):
        par = global_parser([{"name": "filename", "type": "str", "req": True}])
        return send_file(par['filename'], mimetype='image/*')
