from _api.models.news import NewsM
from flask_jwt_extended import jwt_refresh_token_required
from flask_restful import Resource


class NewsList(Resource):
    @classmethod
    @jwt_refresh_token_required
    def get(cls):
        return [x.json() for x in NewsM.list_all()], 200
