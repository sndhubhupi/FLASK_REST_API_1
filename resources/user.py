from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity
)
from werkzeug.security import safe_str_cmp
from models.user import UserModel


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                    type=str,
                    required=True,
                    help='This field cannot be empty')
_user_parser.add_argument('password',
                    type=str,
                    required=True,
                    help='This field cannot be empty')

class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'Message': 'Username already exists'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"Message": "User created successfully."}, 201


class User(Resource):

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return{'message': 'user not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message' : 'user not found'}, 404
        user.delete_from_db()
        return {'message' : 'user deleted'}


class UserLogin(Resource):

    @classmethod
    def post(cls):
        # get data from parser
        data = _user_parser.parse_args()

        #find user in database
        user = UserModel.find_by_username(data['username'])

        #check password
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity= user.id, fresh= True )
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token' : access_token,
                'refresh_token' : refresh_token
            }

        return {'message' : 'Invalid credential'}, 401


class TokenRefresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        current_user =  get_jwt_identity()
        new_token = create_access_token(identity= current_user, fresh= False)
        return {'access_token' : new_token}, 200
