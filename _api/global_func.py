from pydoc import locate

from flask_restful import reqparse


def login_parser():
    parser = reqparse.RequestParser()
    parser.add_argument(
        'email',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    return parser.parse_args()


def global_parser(fields):
    parser = reqparse.RequestParser()
    for f in fields:
        parser.add_argument(
            f['name'],
            type=locate(f['type']),
            required='req' in f.keys(),  # required jika key 'req' ditambahkan
            help="This fields is required"
        )
    return parser.parse_args()


def hapus_field(field):
    from _api import db
    try:
        db.session.delete(field)
        db.session.commit()
        return {"message": "Success"}, 200
    except Exception as e:
        print("Error: {}".format(e))
        db.session.rollback()
        return {"message": "Fail"}, 400
