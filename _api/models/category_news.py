import uuid

from _api import db


class CategoryNewsM(db.Model):
    __tablename__ = 'category_news'

    # region Column
    id = db.Column(db.String, primary_key=True, default=uuid.uuid4().hex)
    name = db.Column(db.String)

    # endregion

    @classmethod
    def list_all(cls):
        return cls.query.order_by(cls.name).all()

    @classmethod
    def find_by(cls, field, value, limit):
        q = "cls.query"
        if type(field) == str and type(value) == str:
            q += ".filter_by({}='{}')".format(field, value)
        else:
            for x, y in zip(field, value):
                q += ".filter_by({}='{}')".format(x, y)
        q += ".{}()".format(limit)
        return eval(q)

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
        }
