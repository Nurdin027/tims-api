import uuid
from datetime import datetime

from _api import db


class LogUnknownM(db.Model):
    __tablename__ = 'log_unknown'

    # region Column
    id = db.Column(db.String, primary_key=True, default=lambda: uuid.uuid4().hex)
    add_time = db.Column(db.DateTime, default=datetime.now())
    photo = db.Column(db.String)

    sub_device_id = db.Column(db.String)  # , db.ForeignKey(SubDeviceM.id))

    # sub_device = db.relationship(UserM, foreign_keys=sub_device_id)
    # endregion

    def __init__(self, photo, sub_device_id):
        self.photo = photo
        self.sub_device_id = sub_device_id

    @classmethod
    def list_all(cls):
        return cls.query.all()

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

    def json(self):
        return {
            "id": self.id,
            "photo": self.photo,
            "sub_device_id": self.sub_device_id,
            "add_time": str(self.add_time),
        }