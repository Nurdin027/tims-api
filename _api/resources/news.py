from flask_restful import Resource

from _api.models.news import NewsM


class NewsList(Resource):
    @classmethod
    def get(cls):
        return [x.json() for x in NewsM.list_all()], 200
