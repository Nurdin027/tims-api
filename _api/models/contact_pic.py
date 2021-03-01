import uuid

from _api import db
from _api.models.account import AccountM
from _api.models.customer_group import CustomerGroupM


class ContactPicM(db.Model):
    __tablename__ = "contact_pic"
    id = db.Column(db.String, primary_key=True, default=lambda: uuid.uuid4().hex)
    status = db.Column(db.String)

    group_id = db.Column(db.Integer, db.ForeignKey(CustomerGroupM.id))
    group = db.relationship(CustomerGroupM, foreign_keys=group_id)
    account_id = db.Column(db.String, db.ForeignKey(AccountM.id))
    account = db.relationship(AccountM, foreign_keys=account_id)

    def __init__(self,
                 iden,
                 group_id,
                 account_id,
                 status,
                 ):
        self.id = iden
        self.group_id = group_id
        self.account_id = account_id
        self.status = status

    @classmethod
    def get_all(cls):
        return cls.query.all()

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

    def json(self):
        return {
            "id": self.id,
            "group_id": self.group_id,
            "group": self.group.name if self.group else "",
            "account_id": self.account_id,
            "username": self.account.username if self.account else "",
            "status": self.status,
        }
