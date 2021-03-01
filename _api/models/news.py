import uuid
from datetime import datetime

from _api import db
from _api.models.category_news import CategoryNewsM


class NewsM(db.Model):
    __tablename__ = 'news'

    # region Column
    id = db.Column(db.String, primary_key=True, default=uuid.uuid4().hex)
    title = db.Column(db.String)
    description = db.Column(db.String)
    add_by = db.Column(db.String)
    add_time = db.Column(db.DateTime, default=datetime.now())

    category_id = db.Column(db.String, db.ForeignKey(CategoryNewsM.id))
    category = db.relationship(CategoryNewsM, foreign_keys=category_id)

    # endregion

    def __init__(self,
                 iden,
                 title,
                 description,
                 category_id,
                 add_by,
                 ):
        self.id = iden
        self.title = title
        self.description = description
        self.category_id = category_id
        self.add_by = add_by

    @classmethod
    def list_all(cls):
        return cls.query.order_by(cls.category_id, cls.title).all()

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
            "title": self.title,
            "description": self.description,
            "category_id": self.category_id,
            "category": self.category.name,
            "add_by": self.add_by,
            "add_time": str(self.add_time),
        }
