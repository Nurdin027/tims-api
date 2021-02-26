import uuid

from _api import db


class CustomerGroupM(db.Model):
    __tablename__ = "customer_group"
    id = db.Column(db.String, primary_key=True, default=lambda: uuid.uuid4().hex)
    name = db.Column(db.String)
    address = db.Column(db.String)
    email = db.Column(db.String)
    telephone = db.Column(db.String)
    status = db.Column(db.Integer)
    add_by = db.Column(db.String)

    def __init__(self,
                 name,
                 address,
                 email,
                 telephone,
                 status,
                 add_by,
                 ):
        self.name = name
        self.address = address
        self.email = email
        self.telephone = telephone
        self.status = status
        self.add_by = add_by

    @classmethod
    def list_all(cls):
        return cls.query.all()

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
            "address": self.address,
            "email": self.email,
            "telephone": self.telephone,
            "status": self.status,
            "add_by": self.add_by,
        }
