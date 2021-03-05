from _api import db, BLACKLIST
from _api.global_func import login_parser, global_parser, hapus_field, add_profile_pic
from _api.models.account import AccountM
from _api.models.user import UserM
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token, create_refresh_token, get_raw_jwt, \
    jwt_refresh_token_required
from flask_restful import Resource


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

        # region Cek Akun
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
        # endregion

        if lanjut and _account.check_password(data['password']):
            access_token = create_access_token(identity=_account.id, fresh=True, expires_delta=False)
            refresh_token = create_refresh_token(_account.id)

            if _account.active:
                akun = _account.json()
                return {
                           "access_token": access_token,
                           "refresh_token": refresh_token,
                           "user_detail": {
                               "id": akun['id'],
                               "auth_id": akun['auth_id'],
                               "auth_name": akun['auth'],
                               "user_id": akun['user_id'],
                               "full_name": akun['user'],
                               "nik_nrp": akun['nik_nrp'],
                               "telephone": akun['telephone'],
                               "active": akun['active'],
                               "notification": akun['notification'],
                               "customer_group_id": akun['customer_group_id'],
                               "customer_group": akun['customer_group'],
                               "gender_id": akun['gender_id'],
                               "gender": "Female" if akun['gender_id'] == 2 else "Male",
                               "profile_picture": akun['profile_picture'],
                               "birth_date": str(akun['birth_date']),
                               "join_date": str(akun['join_date']),
                               "add_by": akun['add_by'],
                               "add_time": str(akun['add_time'])
                           }
                       }, 200

        return {"message": "Wrong email or password."}, 400


class Logout(Resource):
    @classmethod
    @jwt_refresh_token_required
    def get(cls):
        jti = get_raw_jwt()['jti']  # jti is "JWT ID", a unique identifier for JWT
        BLACKLIST.add(jti)
        return {"message": "Success logged out"}, 200


class AccountAdd(Resource):
    @classmethod
    @jwt_refresh_token_required
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
    @jwt_refresh_token_required
    def get(cls):
        return [x.json() for x in AccountM.list_all()], 200


class AccountUpdate(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        par = global_parser([
            {"name": "id", "type": "str", "req": True},
            {"name": "user_id", "type": "str"},
            {"name": "username", "type": "str"},
            {"name": "password", "type": "str"},
            {"name": "auth_id", "type": "str"},
            {"name": "notification", "type": "int"},
        ])

        try:
            akun = AccountM.find_by_id(par['id']).json()
            if akun:
                akun.user_id = par['user_id'] if 'user_id' in par and par['user_id'] != "" else akun.user_id
                akun.username = par['username'] if 'username' in par and par['username'] != "" else akun.username
                akun.auth_id = par['auth_id'] if 'auth_id' in par and par['auth_id'] != "" else akun.auth_id
                akun.notification = par['notification'] if 'notification' in par and par[
                    'notification'] != "" else akun.notification
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
    @jwt_refresh_token_required
    def post(cls):
        par = global_parser([
            {"name": "id", "type": "str", "req": True}
        ])
        akun = AccountM.find_by_id(par['id'])
        if akun:
            hapus_field(akun)
        else:
            return {"message": "Account not found"}, 404


class ProfileUpdate(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        par = global_parser([
            {"name": "full_name", "type": "str"},  # user
            {"name": "nik_nrp", "type": "str"},  # user
            {"name": "telephone", "type": "str"},  # user
            {"name": "email", "type": "str"},  # user
            {"name": "username", "type": "str"},  # account
            {"name": "password", "type": "str"},  # account
            {"name": "notification", "type": "str"},  # account
            {"name": "profile_picture", "type": "str"},  # account
            {"name": "gender", "type": "str"},  # account
        ])

        akun = AccountM.find_by_id(get_jwt_identity())
        if akun:
            try:
                user = UserM.find_by_id(akun.user_id)
                if user:
                    user.name = par['full_name'] if par['full_name'] != "" and par[
                        'full_name'] is not None else user.name
                    user.nik_nrp = par['nik_nrp'] if par['nik_nrp'] != "" and par[
                        'nik_nrp'] is not None else user.nik_nrp
                    user.telephone = par['telephone'] if par['telephone'] != "" and par[
                        'telephone'] is not None else user.telephone
                    user.email = par['email'] if par['email'] != "" and par['email'] is not None else user.email
                    akun.username = par['username'] if par['username'] != "" and par[
                        'username'] is not None else akun.username
                    user.gender_id = par['gender'] if par['gender'] != "" and par[
                        'gender'] is not None else user.gender_id
                    akun.notification = par['notification'] if par['notification'] != "" and par[
                        'notification'] is not None else akun.notification
                    if par['profile_picture'] != "" and par['profile_picture'] is not None:
                        user.profile_picture = add_profile_pic(par['profile_picture'], akun.user_id)
                    pesan, kode = user.profile_picture, 200
                    db.session.commit()
                else:
                    pesan, kode = "User not found", 404
            except Exception as e:
                print("Error: {}".format(str(e)))
                db.session.rollback()
                pesan, kode = "Failed, \nError: " + str(e), 400
        else:
            pesan, kode = "User not found", 404
        return {"message": pesan}, kode
