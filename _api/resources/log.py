from flask import send_file
from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity
from flask_restful import Resource

from _api import db
from _api.global_func import global_parser
from _api.models.contact_pic import ContactPicM
from _api.models.customer_group import CustomerGroupM
from _api.models.log_unknown import LogUnknownM
from _api.models.main_device import MainDeviceM
from _api.models.sub_device import SubDeviceM


class LogUnknownList(Resource):
    @classmethod
    @jwt_refresh_token_required
    def get(cls):
        account_id = get_jwt_identity()
        logna = db.session.query(LogUnknownM) \
            .join(SubDeviceM, SubDeviceM.id == LogUnknownM.sub_device_id) \
            .join(MainDeviceM, MainDeviceM.id == SubDeviceM.main_device_id) \
            .join(CustomerGroupM, CustomerGroupM.id == MainDeviceM.customer_group_id) \
            .join(ContactPicM, ContactPicM.group_id == CustomerGroupM.id) \
            .filter(ContactPicM.account_id == account_id) \
            .order_by(LogUnknownM.add_time.desc()) \
            .all()
        return [x.json() for x in logna], 200


class ViewImage(Resource):
    @classmethod
    def get(cls):
        par = global_parser([{"name": "filename", "type": "str", "req": True}])
        return send_file(par['filename'], mimetype='image/*')
