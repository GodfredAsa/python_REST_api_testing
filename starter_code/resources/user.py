from flask_restful import Resource, reqparse

from starter_code.models.user import UserModel


class UserRegister(Resource):
    """
    USERS REGISTER USING USERNAME AND PASSWORD
    """
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Password cannot be blank")

    def post(self):
        data = UserRegister.parser.parse_args()
        user = UserModel.find_by_name(data["username"])
        if user:
            return {"message": "User with {} all exists".format(data["username"])}, 400
        user = UserModel(**data)
        user.save_to_db()
        print(user.password, " hashed ==>")
        return {"message": "User with username {} created successfully".format(data["username"])}, 201

