from _api import db


class AuthM(db.Model):
    __tablename__ = 'auth'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)

    @classmethod
    def find_by_name(cls, _name):
        return cls.query.filter_by(name=_name).first()

    @classmethod
    def list_all(cls):
        return cls.query.filter(cls.id != 1).all()

    def json(self):
        return {
            "id": self.id,
            "name": self.name
        }
