from starter_code.models.user import UserModel
from starter_code.tests.base_test import BaseTest
import json


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post("/register", data={"username": "test", "password": "1234"})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_name("test"))

                self.assertDictEqual({"message": "User with username test created successfully"},
                                     # converts response to dictionary
                                     json.loads(response.data))

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '1234'})
                # data converted to json
                auth_response = client.post('/auth',
                                            data=json.dumps({'username': 'test', 'password': '1234'}),
                                            headers={'Content-Type': 'application/json'})
                # checking that the response contains access token
                self.assertIn('access-token', json.loads(auth_response.data).keys())

    # double registration or register duplicate below
    def test_user_exists(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '1234'})
                response = client.post("/register", data={"username": "test", "password": "1234"})
                self.assertEqual(response.status_code, 400, 'user already exists')
                self.assertDictEqual({'message': 'User with test all exists'}, json.loads(response.data))
