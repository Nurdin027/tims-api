import uuid

from _api import db
from _api.models.main_device import MainDeviceM


class SubDeviceM(db.Model):
    __tablename__ = 'sub_device'
    id = db.Column(db.String, primary_key=True, default=lambda : uuid.uuid4().hex)
    channel = db.Column(db.Integer)
    desc = db.Column(db.String, comment="Deskripsi atau nama kamera")
    detect_stat = db.Column(db.Integer, default=1)
    add_by = db.Column(db.String)

    main_device_id = db.Column(db.String, db.ForeignKey(MainDeviceM.id))
    main_device = db.relationship(MainDeviceM, foreign_keys=main_device_id)

    def __init__(self,
                 channel,
                 desc,
                 main_device_id,
                 add_by,
                 ):
        self.channel = channel
        self.desc = desc
        self.main_device_id = main_device_id
        self.add_by = add_by

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

    @classmethod
    def by_id(cls, idna):
        return cls.query.filter_by(id=idna).first()

    @classmethod
    def by_main_device(cls, main_device):
        return cls.query.filter_by(main_device_id=main_device).all()

    def json(self):
        return {
            "id": self.id,
            "channel": self.channel,
            "desc": self.desc,
            "detect_stat": self.detect_stat,
            "main_device_id": self.main_device_id,
            "main_device": self.main_device.name if self.main_device else "",
            "customer_group_id": self.main_device.customer_group_id,
            "customer_group": self.main_device.customer_group.name if self.main_device and self.main_device.customer_group else "",
            "host": self.main_device.host if self.main_device else "",
        }
