import uuid
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from _api import db
from _api.models.auth import AuthM
from _api.models.user import UserM


class AccountM(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.String, primary_key=True, default=lambda: uuid.uuid4().hex)
    username = db.Column(db.String)
    password = db.Column(db.String)
    active = db.Column(db.Integer, default=1)
    add_by = db.Column(db.String)
    add_time = db.Column(db.DateTime, default=lambda: datetime.now())

    user_id = db.Column(db.String, db.ForeignKey(UserM.id))
    user = db.relationship(UserM, foreign_keys=user_id)
    auth_id = db.Column(db.String, db.ForeignKey(AuthM.id))
    auth = db.relationship(AuthM, foreign_keys=auth_id)

    def __init__(self,
                 username,
                 password,
                 user_id,
                 auth_id,
                 add_by):
        self.username = username
        self.hash_password = generate_password_hash(password)
        self.auth_id = auth_id
        self.user_id = user_id
        self.add_by = add_by

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by(cls, fieldna, isina, limitna="all"):
        q = "cls.query"
        if type(fieldna) == str:
            q += ".filter_by({}='{}')".format(fieldna, isina)
        elif type(fieldna) == list:
            for x, y in zip(fieldna, isina):
                q += ".filter_by({}='{}')".format(x, y)
        q += ".{}()".format(limitna)
        return eval(q)

    @classmethod
    def list_all(cls):
        return cls.query.order_by(cls.auth_id).all()

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "add_by": self.add_by,
            "add_time": str(self.add_time),
            "active": self.active,

            "auth_id": self.auth_id,
            "auth": self.auth.name if self.auth else "",
            "user_id": self.user_id,
            "user": self.user.name if self.user else "",
            "email": self.user.email if self.user else "",
            "telephone": self.user.telephone if self.user else "",
            "nik_nrp": self.user.nik_nrp if self.user else "",
            "customer_group_id": self.user.customer_group_id,
            "customer_group": self.user.customer_group.name if self.user.customer_group else "",
        }
