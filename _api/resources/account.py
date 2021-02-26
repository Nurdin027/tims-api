from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token, create_refresh_token
from flask_restful import Resource

from _api import db
from _api.global_func import login_parser, global_parser, hapus_field
from _api.models.account import AccountM
from _api.models.user import UserM


class TokenRefresh(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user)
        return {"access_token": new_token}, 200


class Login(Resource):
    @classmethod
    def post(cls):
        data = login_parser()
        lanjut = 0
        _account = AccountM.find_by('username', data['email'], 'first')
        if _account:
            lanjut = 1
        if not lanjut:
            _account = UserM.find_by('email', data['email'], 'first')
        if _account:
            lanjut = 1
        if not lanjut:
            _account = UserM.find_by('nik_nrp', data['email'], 'first')

        if lanjut and _account.check_password(data['password']):
            access_token = create_access_token(identity=_account.id, fresh=True, expires_delta=False)
            refresh_token = create_refresh_token(_account.id)

            if _account.auth_id == 1:
                akun = _account.json()
                return {
                           "access_token": access_token,
                           "refresh_token": refresh_token,
                           "user_detail": {
                               "id": akun['id'],
                               "auth_id": akun['auth_id'],
                               "auth_name": akun['auth'],
                               "full_name": akun['user'],
                               "nik_nrp": akun['nik_nrp'],
                               "telephone": akun['telephone'],
                               "active": akun['active'],
                               "customer_group_id": akun['customer_group_id'],
                               "customer_group": akun['customer_group'],
                               "add_by": akun['add_by'],
                               "add_time": str(akun['add_time'])
                           }
                       }, 200

        return {"message": "Wrong email or password."}, 400


class AccountAdd(Resource):
    @classmethod
    def post(cls):
        par = global_parser([
            {"name": "user_id", "type": "str", "req": True},
            {"name": "username", "type": "str", "req": True},
            {"name": "password", "type": "str", "req": True},
            {"name": "auth_id", "type": "str", "req": True},
            {"name": "add_by", "type": "str", "req": True},
        ])
        try:
            db.session.add(
                AccountM(par['username'], par['password'], par['user_id'], par['auth_id'], par['add_by'])
            )
            db.session.commit()
            return {"message": "Success"}, 200
        except Exception as e:
            print("Error: {}".format(e))
            db.session.rollback()
            return {"message": "Fail"}, 400


class AccountList(Resource):
    @classmethod
    def get(cls):
        return {"result": [x.json() for x in AccountM.list_all()]}, 200


class AccountUpdate(Resource):
    @classmethod
    def post(cls):
        par = global_parser([
            {"name": "id", "type": "str", "req": True},
            {"name": "user_id", "type": "str"},
            {"name": "username", "type": "str"},
            {"name": "password", "type": "str"},
            {"name": "auth_id", "type": "str"},
        ])

        try:
            akun = AccountM.find_by_id(par['id']).json()
            if akun:
                akun.user_id = par['user_id'] if par['user_id'] != "" else akun.user_id
                akun.username = par['username'] if par['username'] != "" else akun.username
                akun.password = par['password'] if par['password'] != "" else akun.password
                akun.auth_id = par['auth_id'] if par['auth_id'] != "" else akun.auth_id
                db.session.commit()
                return {"message": "Success"}, 200
            else:
                return {"message": "Account not found"}, 404
        except Exception as e:
            print("Error: {}".format(e))
            db.session.rollback()
            return {"message": "Fail"}, 400


class AccountDelete(Resource):
    @classmethod
    def post(cls):
        par = global_parser([
            {"name": "id", "type": "str", "req": True}
        ])
        akun = AccountM.find_by_id(par['id'])
        if akun:
            hapus_field(akun)
        else:
            return {"message": "Account not found"}, 404
