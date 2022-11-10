from starter_code.models.user import UserModel
from starter_code.tests.unit.unit_base_test import UnitBaseTest


class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel("test", "password")
        self.assertEqual(user.username, "test")
        self.assertEqual(user.password, "password")
        self.assertIsNotNone(user)

    def test_json(self):
        user = UserModel("test", "password")
        expected = {'username': "test", 'password': "password"}
        actual = user.json()
        self.assertDictEqual(expected, actual)


