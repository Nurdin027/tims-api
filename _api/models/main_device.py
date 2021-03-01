import uuid

from _api import db
from _api.models.customer_group import CustomerGroupM


class MainDeviceM(db.Model):
    __tablename__ = 'main_device'
    id = db.Column(db.String, primary_key=True, default=lambda: uuid.uuid4().hex)
    name = db.Column(db.String)
    customer_group_id = db.Column(db.String, db.ForeignKey(CustomerGroupM.id))
    customer_group = db.relationship(CustomerGroupM, foreign_keys=customer_group_id)
    host = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    status = db.Column(db.Integer, default=1)
    add_by = db.Column(db.String)

    def __init__(self,
                 name,
                 customer_group_id,
                 host,
                 latitude,
                 longitude,
                 add_by,
                 ):
        self.name = name
        self.customer_group_id = customer_group_id
        self.host = host
        self.latitude = latitude
        self.longitude = longitude
        self.add_by = add_by

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.status.desc(), cls.name).all()

    @classmethod
    def get_filtered(cls, field, value, limit):
        q = "cls.query"
        if type(field) == str and type(value) == str:
            q += ".filter_by({}='{}')".format(field, value)
        else:
            for x, y in zip(field, value):
                q += ".filter_by({}='{}')".format(x, y)
        q += ".{}()".format(limit)
        return eval(q)

    @classmethod
    def by_id(cls, idna):
        return cls.query.filter_by(id=idna).first()

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "customer_group_id": self.customer_group_id,
            "customer_group": self.customer_group.name,
            "host": self.host,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "status": self.status,
        }
