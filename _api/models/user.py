import uuid
from datetime import datetime

from _api import db
from _api.models.customer_group import CustomerGroupM


class UserM(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String, primary_key=True, nullable=False, unique=True, default=lambda: uuid.uuid4().hex)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    telephone = db.Column(db.String)
    nik_nrp = db.Column(db.String, unique=True)
    add_by = db.Column(db.String)
    add_time = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now())
    gender_id = db.Column(db.Integer, default=1)
    join_date = db.Column(db.DATE, default=datetime.now().date())
    profile_picture = db.Column(db.String)
    birth_date = db.Column(db.DATE)

    customer_group_id = db.Column(db.String, db.ForeignKey(CustomerGroupM.id))
    customer_group = db.relationship(CustomerGroupM, foreign_keys=customer_group_id)

    def __init__(self,
                 name,
                 telephone,
                 nik_nrp,
                 email,
                 customer_group_id,
                 gender_id,
                 profile_picture,
                 birth_date,
                 add_by):
        self.name = name
        self.telephone = telephone
        self.nik_nrp = nik_nrp
        self.email = email
        self.customer_group_id = customer_group_id
        self.gender_id = gender_id
        self.profile_picture = profile_picture
        self.birth_date = birth_date
        self.add_by = add_by

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

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "telephone": self.telephone,
            "nik_nrp": self.nik_nrp,
            "email": self.email,
            "customer_group_id": self.customer_group_id,
            "customer_group": self.customer_group.name if self.customer_group else "",
            "gender_id": self.gender_id,
            "gender": "Female" if self.gender_id == 2 else "Male",
            "profile_picture": self.profile_picture,
            "birth_date": self.birth_date,
            "join_date": self.join_date,
            "add_by": self.add_by,
        }
