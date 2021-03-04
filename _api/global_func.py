import base64
import imghdr
import os
import random
import string
from pathlib import Path
from pydoc import locate

from flask import current_app
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


def rd_str(size=11, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def add_profile_pic(pic_upload, account_id):
    filename = base64.b64decode(pic_upload)
    extension = imghdr.what(None, h=filename)
    storage_filename = rd_str() + '.' + extension

    p = os.path.join(current_app.root_path, 'static/upload/profile/' + account_id)
    if not os.path.exists(p):
        os.makedirs(p)

    dir_name = Path(str(p) + '/' + storage_filename)
    with open(dir_name, 'wb') as f:
        f.write(filename)

    return storage_filename
