
# from werkzeug.security import safe_str_cmp
import bcrypt

from starter_code.models.user import UserModel


def authenticate(username, password):
    """
    function that get called when user visits /auth with username and password
    :param username:
    :param password:
    :return User if authentication successful and None if not :
    """

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    user = UserModel.find_by_name(username)
    # using bcrypt
    # obtain the user's hashed password
    # has the password sent
    # compare if same then return appropriate message else return None

    if user and bcrypt.checkpw(user.password, hashed_password) == hashed_password:
        return user


def identity(payload):
    """
    gets called when the user is already authenticated with Flask jWT
    verify the user's authorization is correct
    :param payload: a dict with the identity key which is the user_id
    :return: A userModel object
    """
    user_id = payload["identity"]
    return UserModel.find_by_id(user_id)





