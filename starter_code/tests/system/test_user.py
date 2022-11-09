from starter_code.models.user import UserModel
from starter_code.tests.base_test import BaseTest
import json


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                request = client.post("/register", data={"username": "test", "password": "1234"})

                self.assertEqual(request.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_name("test"))

                self.assertDictEqual({"message": "User with username test created successfully"},
                                     # converts response to dictionary
                                     json.loads(request.data))

    def test_register_and_login(self):
        pass

    def test_user_exists(self):
        pass


